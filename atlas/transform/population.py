"""
Transform population data → processed/population/state_population.csv
Sources: Census ACS B11009 (same-sex households) + Williams Institute estimates
"""
from pathlib import Path
import polars as pl


def run() -> pl.DataFrame:
    from atlas.config import settings
    raw = settings.data_raw_dir
    proc = settings.data_processed_dir

    fips = pl.read_csv(proc / "reference" / "state_fips.csv").select(
        ["state_fips", "state_name", "state_abbr"]
    )

    # Williams Institute LGBT population estimates
    williams = pl.read_csv(
        raw / "population" / "williams_population_estimates_extracted_2023.csv"
    ).select(["state_abbr", "lgbtq_pct_of_adults", "lgbtq_adult_count"])

    # Census B11009 — same-sex households (5-year ACS 2024)
    b11009 = pl.read_csv(raw / "population" / "census_acs_B11009_state_2024.csv")

    # Compute same-sex household totals
    b11009 = b11009.with_columns([
        (pl.col("same_sex_married_households") + pl.col("same_sex_cohabiting_households"))
        .alias("total_same_sex_hh"),
    ])

    # Join everything on state_abbr / state_fips
    df = fips.join(williams, on="state_abbr", how="left")
    df = df.join(
        b11009.select(["state_fips", "total_same_sex_hh"]),
        on="state_fips",
        how="left",
    )

    df = df.with_columns(pl.lit(2024).alias("year"))

    # Rename to match schema
    df = df.rename({
        "lgbtq_pct_of_adults": "lgbtq_pct",
        "lgbtq_adult_count": "lgbtq_pop",
        "total_same_sex_hh": "same_sex_hh",
    })

    # Transgender population estimates: ~6.5% of LGBTQ+ adults identify as transgender
    # (aligns with national 0.6% trans / 9.3% LGBTQ+ = 6.5%; Williams Institute 2022)
    df = df.with_columns([
        (pl.col("lgbtq_pop").cast(pl.Float64) * 0.065).round(0).cast(pl.Int64).alias("trans_pop"),
        (pl.col("lgbtq_pct") * 0.065).round(3).alias("trans_pct"),
    ])

    df = df.select([
        "state_fips", "state_name", "state_abbr", "year",
        "lgbtq_pop", "lgbtq_pct", "same_sex_hh", "trans_pop", "trans_pct",
    ])

    out = proc / "population" / "state_population.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.write_csv(out)
    print(f"  state_population.csv → {len(df)} rows")
    return df


if __name__ == "__main__":
    run()
