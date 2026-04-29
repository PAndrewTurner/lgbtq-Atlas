"""
Transform socioeconomic data → processed/socioeconomic/
Sources: Census ACS B12001 (marriage), B15002 (education), S1101, S1501
"""
from pathlib import Path
import polars as pl


def _load_census(path: Path) -> pl.DataFrame:
    return pl.read_csv(path, infer_schema_length=1000)


def build_income_education(raw: Path, proc: Path) -> pl.DataFrame:
    fips = pl.read_csv(proc / "reference" / "state_fips.csv").select(
        ["state_fips", "state_abbr"]
    )

    # B15002 — educational attainment (25+)
    b15002 = _load_census(raw / "socioeconomic" / "census_acs_B15002_state_2024.csv")

    # S1501 — education summary (has % bachelor's+)
    s1501 = _load_census(raw / "socioeconomic" / "census_acs_S1501_state_2024.csv")

    df = fips.join(
        b15002.select(["state_fips", "total_population_25plus",
                       "males_bachelors_degree", "males_masters_degree",
                       "females_bachelors_degree"]),
        on="state_fips", how="left"
    ).join(
        s1501.select(["state_fips",
                      "pct_bachelors_or_higher_female",
                      "pct_bachelors_or_higher_male"]),
        on="state_fips", how="left"
    )

    df = df.with_columns([
        pl.lit(2024).alias("year"),
        # General pop bachelor's rate (average of M/F)
        ((pl.col("pct_bachelors_or_higher_female") + pl.col("pct_bachelors_or_higher_male")) / 2)
        .alias("pct_bachelors"),
        # LGBT-specific income/education not in Census ACS aggregate tables
        pl.lit(None).cast(pl.Float64).alias("median_individual_income_lgbtq"),
        pl.lit(None).cast(pl.Float64).alias("median_individual_income_nonlgbtq"),
        pl.lit(None).cast(pl.Float64).alias("median_hh_income_samesex_married"),
        pl.lit(None).cast(pl.Float64).alias("median_hh_income_samesex_cohabiting"),
        pl.lit(None).cast(pl.Float64).alias("median_hh_income_general_population"),
        pl.lit(None).cast(pl.Float64).alias("pct_bachelors_lgbtq"),
        pl.lit(None).cast(pl.Float64).alias("pct_graduate_lgbtq"),
        pl.lit(None).cast(pl.Float64).alias("pct_graduate"),
        pl.lit(None).cast(pl.Float64).alias("pct_bachelors_nonlgbtq"),
        pl.lit(None).cast(pl.Float64).alias("pct_graduate_nonlgbtq"),
        pl.lit(None).cast(pl.Float64).alias("pct_less_than_hs"),
        pl.lit(None).cast(pl.Float64).alias("pct_hs_diploma"),
        pl.lit(None).cast(pl.Float64).alias("pct_some_college"),
    ]).select([
        "state_fips", "year",
        "median_individual_income_lgbtq", "median_individual_income_nonlgbtq",
        "median_hh_income_samesex_married", "median_hh_income_samesex_cohabiting",
        "median_hh_income_general_population",
        "pct_less_than_hs", "pct_hs_diploma", "pct_some_college",
        "pct_bachelors", "pct_graduate",
        "pct_bachelors_lgbtq", "pct_graduate_lgbtq",
        "pct_bachelors_nonlgbtq", "pct_graduate_nonlgbtq",
    ])

    out = proc / "socioeconomic" / "state_income_education.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.write_csv(out)
    print(f"  state_income_education.csv → {len(df)} rows")
    return df


def build_marriage_households(raw: Path, proc: Path) -> pl.DataFrame:
    fips = pl.read_csv(proc / "reference" / "state_fips.csv").select(
        ["state_fips", "state_abbr"]
    )

    b11009 = _load_census(raw / "population" / "census_acs_B11009_state_2024.csv")
    b12001 = _load_census(raw / "socioeconomic" / "census_acs_B12001_state_2024.csv")
    s1101 = _load_census(raw / "socioeconomic" / "census_acs_S1101_state_2024.csv")

    df = fips.join(
        b11009.select(["state_fips",
                       "same_sex_married_households", "same_sex_cohabiting_households",
                       "total_households", "married_couple_households"]),
        on="state_fips", how="left"
    ).join(
        b12001.select(["state_fips", "males_now_married", "females_now_married"]),
        on="state_fips", how="left"
    ).join(
        s1101.select(["state_fips", "avg_household_size"]),
        on="state_fips", how="left"
    )

    df = df.with_columns([
        pl.lit(2024).alias("year"),
        # Same-sex marriage rate as share of all married couple households
        pl.when(pl.col("married_couple_households") > 0)
          .then(pl.col("same_sex_married_households").cast(pl.Float64)
                / pl.col("married_couple_households") * 100)
          .otherwise(None)
          .alias("same_sex_marriage_rate"),
        # Opposite-sex marriage rate as share of all households
        pl.when(pl.col("total_households") > 0)
          .then(pl.col("married_couple_households").cast(pl.Float64)
                / pl.col("total_households") * 100)
          .otherwise(None)
          .alias("opposite_sex_marriage_rate"),
        pl.lit(None).cast(pl.Float64).alias("same_sex_hh_with_children_pct"),
        pl.col("avg_household_size").alias("avg_hh_size_samesex"),
    ]).select([
        "state_fips", "year",
        "same_sex_married_households",
        pl.col("same_sex_cohabiting_households").alias("same_sex_cohabiting_count"),
        "same_sex_marriage_rate", "opposite_sex_marriage_rate",
        "same_sex_hh_with_children_pct", "avg_hh_size_samesex",
    ]).rename({"same_sex_married_households": "same_sex_married_count"})

    out = proc / "socioeconomic" / "state_marriage_households.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.write_csv(out)
    print(f"  state_marriage_households.csv → {len(df)} rows")
    return df


def run() -> None:
    from atlas.config import settings
    raw = settings.data_raw_dir
    proc = settings.data_processed_dir
    build_income_education(raw, proc)
    build_marriage_households(raw, proc)


if __name__ == "__main__":
    run()
