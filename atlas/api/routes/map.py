import polars as pl
from fastapi import APIRouter
from atlas.api.data_store import store

router = APIRouter(prefix="/map", tags=["map"])


@router.get("/states")
async def map_states(layer: str = "overall", year: int = 2024):
    """Slim endpoint for choropleth coloring — returns fips + requested score only."""
    scores_df = store.state_scores_for_year(year)
    if scores_df.is_empty():
        return []

    col_map = {
        "overall":   "overall_score",
        "legal":     "legal_score",
        "safety":    "safety_score",
        "health":    "health_score",
        "economic":  "economic_score",
        "community": "community_score",
        "youth":     "youth_score",
    }
    score_col = col_map.get(layer, "overall_score")
    joined = scores_df.join(store.fips_ref, on="state_fips", how="left")

    return [
        {
            "fips": str(int(r["state_fips"])).zfill(2),
            "name": r.get("state_name") or "",
            "abbr": r.get("state_abbr") or "",
            "score": r.get(score_col),
        }
        for r in joined.iter_rows(named=True)
    ]
