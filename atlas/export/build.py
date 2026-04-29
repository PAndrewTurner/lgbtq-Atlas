"""
Pre-generate all static JSON exports for the frontend.
Uses the DataStore singleton (same as the API) — no separate DB connection.
"""
import json
from pathlib import Path
from atlas.config import settings


def build_exports(year: int = 2024) -> None:
    import polars as pl
    from atlas.api.data_store import store

    exports_dir = settings.data_exports_dir
    # Load nonprofits once for all states
    nonprofits_path = settings.data_raw_dir / "community" / "irs_lgbtq_nonprofits_2026.csv"
    if nonprofits_path.exists():
        nonprofits_df = pl.read_csv(nonprofits_path, infer_schema_length=2000)
    else:
        nonprofits_df = pl.DataFrame()
    exports_dir.mkdir(parents=True, exist_ok=True)
    (exports_dir / "state_profiles").mkdir(exist_ok=True)

    all_map_data = []

    for row in store.fips_ref.iter_rows(named=True):
        fips = str(int(row["state_fips"])).zfill(2)
        name = row.get("state_name") or ""
        abbr = row.get("state_abbr") or ""
        print(f"  Exporting {name}…")

        data = store.state_profile_data(fips, year)
        scores = data.get("scores") or {}

        profile = {
            "fips":  fips,
            "name":  name,
            "abbr":  abbr,
            "year":  year,
            "scores": {
                "legal":     scores.get("legal_score"),
                "safety":    scores.get("safety_score"),
                "health":    scores.get("health_score"),
                "economic":  scores.get("economic_score"),
                "community": scores.get("community_score"),
                "youth":     scores.get("youth_score"),
                "overall":   scores.get("overall_score") or 0.0,
                "confidence":scores.get("confidence") or 1.0,
            },
            "population":   data.get("population") or {},
            "legal_detail": data.get("policy") or {},
            "safety_detail":data.get("hate_crimes") or {},
            "health_detail":data.get("health") or {},
            "economic_detail": data.get("economic") or {},
            "community_detail":data.get("community") or {},
            "youth_detail": data.get("youth") or {},
            "narrative":    data.get("narrative"),
        }

        # Trend data
        if not store.scores.is_empty():
            trend_df = (
                store.scores
                .filter(pl.col("state_fips").cast(pl.Utf8).str.zfill(2) == fips)
                .select(["year", "overall_score"])
                .sort("year")
            )
            profile["trend"] = [
                {"year": r["year"], "overall": r["overall_score"]}
                for r in trend_df.iter_rows(named=True)
            ]
        else:
            profile["trend"] = []

        # Top cities by MEI
        if not store.mei.is_empty():
            mei_rows = (
                store.mei
                .filter(pl.col("state_fips") == int(fips))
                .sort("mei_score", descending=True)
                .head(5)
            )
            profile["cities"] = mei_rows.to_dicts()
        else:
            profile["cities"] = []

        # Top nonprofits/orgs for this state (up to 20, sorted by revenue)
        if not nonprofits_df.is_empty() and "org_addr_state" in nonprofits_df.columns:
            orgs = (
                nonprofits_df
                .filter(pl.col("org_addr_state") == abbr)
                .with_columns(
                    pl.col("revenue_amount").cast(pl.Int64, strict=False).fill_null(0)
                )
                .sort("revenue_amount", descending=True)
                .head(20)
                .select(["org_name_display", "org_addr_city", "ntee_code_definition", "revenue_amount"])
            )
            profile["organizations"] = orgs.to_dicts()
        else:
            profile["organizations"] = []

        out_path = exports_dir / "state_profiles" / f"{fips}.json"
        out_path.write_text(json.dumps(profile, indent=2, default=str))

        all_map_data.append({
            "fips":   fips,
            "name":   name,
            "abbr":   abbr,
            "scores": profile["scores"],
            "year":   year,
        })

    (exports_dir / "states_map.json").write_text(
        json.dumps(all_map_data, indent=2)
    )
    print(f"Export complete — {len(all_map_data)} states → {exports_dir}")


if __name__ == "__main__":
    build_exports()
