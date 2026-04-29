"""
Transform youth data → processed/youth/state_youth.csv
Sources: Trevor Project 2024 extracted CSV (primary), CDC YRBSS (2015-17, supplementary)
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

    df = fips.join(
        trevor.select([
            "state_abbr",
            "pct_considered_suicide",
            "pct_felt_safe_school",
            "pct_conversion_therapy_exposed",
        ]),
        on="state_abbr", how="left"
    )

    df = df.with_columns([
        pl.lit(2024).alias("year"),
        # suicidality_pct = % who seriously considered suicide
        pl.col("pct_considered_suicide").alias("suicidality_pct"),
        # school_safety_score = % who felt school was LGBTQ+-affirming (0-100)
        pl.col("pct_felt_safe_school").alias("school_safety_score"),
        # GSA presence: not directly measured in Trevor data — use school safety as proxy
        pl.col("pct_felt_safe_school").alias("gsa_presence_pct"),
        # conversion therapy exposure
        pl.col("pct_conversion_therapy_exposed").alias("conversion_therapy_exposure_pct"),
    ]).select([
        "state_fips", "year",
        "suicidality_pct", "school_safety_score",
        "gsa_presence_pct", "conversion_therapy_exposure_pct",
    ])

    out = proc / "youth" / "state_youth.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.write_csv(out)
    print(f"  state_youth.csv → {len(df)} rows")
    return df


if __name__ == "__main__":
    run()
