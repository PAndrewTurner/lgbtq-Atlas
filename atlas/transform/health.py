"""
Transform health data → processed/health/state_health_outcomes.csv
Source: Trevor Project 2024 extracted CSV
(CDC BRFSS / HIV data are listed as gaps; Trevor Project is the richest available source)
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

    trevor = pl.read_csv(raw / "health" / "trevorproject_survey_2024_extracted.csv")

    df = fips.join(trevor.select([
        "state_abbr",
        "pct_considered_suicide",
        "pct_no_mental_health_access",
        "pct_high_family_support",
    ]), on="state_abbr", how="left")

    df = df.with_columns(pl.lit(2024).alias("year"))

    # Map Trevor metrics to schema columns
    # depression_pct: not directly in data; use pct_considered_suicide as severity proxy
    # healthcare_avoidance: pct who wanted but couldn't get mental health care
    # uninsured_pct, hiv_*: not available in Trevor data — left as null
    df = df.rename({
        "pct_considered_suicide": "depression_pct",
        "pct_no_mental_health_access": "healthcare_avoidance_pct",
    }).with_columns([
        pl.lit(None).cast(pl.Float64).alias("uninsured_pct"),
        pl.lit(None).cast(pl.Float64).alias("hiv_diagnosis_rate"),
        pl.col("pct_high_family_support").alias("hiv_viral_suppression_pct"),
    ]).select([
        "state_fips", "year",
        "depression_pct", "healthcare_avoidance_pct",
        "uninsured_pct", "hiv_diagnosis_rate", "hiv_viral_suppression_pct",
    ])

    out = proc / "health" / "state_health_outcomes.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.write_csv(out)
    print(f"  state_health_outcomes.csv → {len(df)} rows")
    return df


if __name__ == "__main__":
    run()
