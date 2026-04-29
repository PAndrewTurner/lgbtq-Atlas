"""
Transform HRC MEI city scores → processed/legal/city_mei_scores.csv
Source: hrc_mei_city_scores_2025.csv (506 cities)
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

    mei = pl.read_csv(raw / "legal" / "hrc_mei_city_scores_2025.csv")

    # Derive city_id from state abbr + hrc_slug
    mei = mei.with_columns([
        (pl.col("state") + "-" + pl.col("hrc_slug")).alias("city_id"),
        pl.lit(2025).alias("year"),
        pl.lit(None).cast(pl.Utf8).alias("mei_grade"),
        pl.lit(None).cast(pl.Float64).alias("nd_score"),
        pl.lit(None).cast(pl.Float64).alias("services_score"),
        pl.lit(None).cast(pl.Float64).alias("le_score"),
    ])

    df = mei.join(fips, left_on="state", right_on="state_abbr", how="left")

    df = df.rename({
        "city": "city_name",
        "state": "state_abbr_orig",
        "mei_score": "mei_score",
    }).select([
        "city_id", "city_name", "state_fips", "year",
        "mei_score", "mei_grade", "nd_score", "services_score", "le_score",
    ])

    out = proc / "legal" / "city_mei_scores.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.write_csv(out)
    print(f"  city_mei_scores.csv → {len(df)} rows")
    return df


if __name__ == "__main__":
    run()
