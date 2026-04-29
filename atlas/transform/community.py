"""
Transform community infrastructure data → processed/community/state_community.csv
Source: IRS LGBTQ+ nonprofits (NCCS BMF), ~4,981 orgs
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

    nonprofits = pl.read_csv(
        raw / "community" / "irs_lgbtq_nonprofits_2026.csv",
        infer_schema_length=2000,
    )

    # Count orgs per state
    org_counts = (
        nonprofits
        .filter(pl.col("org_addr_state").is_not_null())
        .group_by("org_addr_state")
        .agg(pl.len().alias("lgbtq_orgs_count"))
        .rename({"org_addr_state": "state_abbr"})
    )

    df = fips.join(org_counts, on="state_abbr", how="left")
    df = df.join(pop, on="state_fips", how="left")

    df = df.with_columns([
        pl.lit(2024).alias("year"),
        pl.col("lgbtq_orgs_count").fill_null(0),
        # Orgs per 100k LGBTQ+ adults
        pl.when(pl.col("lgbtq_pop").is_not_null() & (pl.col("lgbtq_pop") > 0))
          .then(
              pl.col("lgbtq_orgs_count").cast(pl.Float64) / pl.col("lgbtq_pop") * 100_000
          )
          .otherwise(None)
          .alias("lgbtq_orgs_per_100k"),
        # Pride events not yet collected — placeholder
        pl.lit(0).alias("pride_events_count"),
        pl.lit(None).cast(pl.Int64).alias("largest_pride_attendance"),
    ]).select([
        "state_fips", "year",
        "lgbtq_orgs_count", "lgbtq_orgs_per_100k",
        "pride_events_count", "largest_pride_attendance",
    ])

    out = proc / "community" / "state_community.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.write_csv(out)
    print(f"  state_community.csv → {len(df)} rows")
    return df


if __name__ == "__main__":
    run()
