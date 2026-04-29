"""
Transform FBI hate crime data → processed/safety/state_hate_crimes.csv
Source: fbi_hatecrimes_lgbtq_2019_2024.csv (6 years × 51+ geographies)
"""
from pathlib import Path
import polars as pl


def run() -> pl.DataFrame:
    from atlas.config import settings
    raw = settings.data_raw_dir
    proc = settings.data_processed_dir

    fips = pl.read_csv(proc / "reference" / "state_fips.csv").select(
        ["state_fips", "state_abbr"]
    )
    pop = pl.read_csv(proc / "population" / "state_population.csv").select(
        ["state_fips", "lgbtq_pop"]
    )

    hc = pl.read_csv(raw / "safety" / "fbi_hatecrimes_lgbtq_2019_2024.csv")

    # Filter to state rows only (state_abbr != "US")
    hc = hc.filter(pl.col("state_abbr") != "US")

    df = hc.join(fips, on="state_abbr", how="left")
    df = df.join(pop, on="state_fips", how="left")

    # Compute per-100k rates; lgbtq_pop is adult population
    # Use total LGBTQ+ incidents for combined SO + GI rate
    df = df.with_columns([
        pl.col("total_sexual_orientation").alias("so_incidents"),
        pl.col("total_gender_identity").alias("gi_incidents"),
        # Rate per 100k (use lgbtq_pop as denominator for LGBTQ-specific rate)
        pl.when(pl.col("lgbtq_pop").is_not_null() & (pl.col("lgbtq_pop") > 0))
          .then(
              (pl.col("total_sexual_orientation").cast(pl.Float64) / pl.col("lgbtq_pop")) * 100_000
          )
          .otherwise(None)
          .alias("so_per_100k"),
        pl.when(pl.col("lgbtq_pop").is_not_null() & (pl.col("lgbtq_pop") > 0))
          .then(
              (pl.col("total_gender_identity").cast(pl.Float64) / pl.col("lgbtq_pop")) * 100_000
          )
          .otherwise(None)
          .alias("gi_per_100k"),
        # Reporting rate: agencies reporting hate crimes / agencies reporting any data
        # Proxy: if total_all_hate_crimes > 0, assume full reporting
        pl.when(pl.col("total_all_hate_crimes") > 0)
          .then(pl.lit(1.0))
          .otherwise(pl.lit(0.5))
          .alias("reporting_rate"),
        pl.lit(0).alias("non_reporting_agency_count"),
        pl.lit(None).cast(pl.Float64).alias("adjusted_score"),
    ])

    df = df.select([
        "state_fips", "year",
        "so_incidents", "gi_incidents",
        "so_per_100k", "gi_per_100k",
        "reporting_rate", "non_reporting_agency_count", "adjusted_score",
    ])

    out = proc / "safety" / "state_hate_crimes.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.write_csv(out)
    print(f"  state_hate_crimes.csv → {len(df)} rows")
    return df


if __name__ == "__main__":
    run()
