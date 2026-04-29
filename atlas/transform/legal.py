"""
Transform legal/policy data → processed/legal/state_policy_scores.csv
Sources: HRC SEI 2024 extracted + Trans Legislation Tracker 2025
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

    sei = pl.read_csv(raw / "legal" / "hrc_sei_2024_extracted.csv").select([
        "state_abbr", "hrc_sei_numerical_score", "sei_overall_climate",
        "conversion_therapy_ban", "hate_crime_law", "preemption_law",
        "bills_introduced_against",
    ])

    df = fips.join(sei, on="state_abbr", how="left")
    df = df.with_columns(pl.lit(2024).alias("year"))

    # Schema alignment with brief
    df = df.rename({
        "hrc_sei_numerical_score": "map_total_score",  # used as base in scoring engine
        "sei_overall_climate": "overall_climate",
        "bills_introduced_against": "bills_passed_against",
    }).select([
        "state_fips", "year",
        "map_total_score", "overall_climate",
        "conversion_therapy_ban", "hate_crime_law",
        "preemption_law", "bills_passed_against",
    ])

    out = proc / "legal" / "state_policy_scores.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.write_csv(out)
    print(f"  state_policy_scores.csv → {len(df)} rows")
    return df


if __name__ == "__main__":
    run()
