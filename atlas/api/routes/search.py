import polars as pl
from fastapi import APIRouter
from atlas.api.models import SearchResult
from atlas.api.data_store import store

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/", response_model=list[SearchResult])
async def search(q: str, limit: int = 10):
    q_lower = q.lower()
    results: list[SearchResult] = []

    # Search states
    if not store.fips_ref.is_empty():
        for row in store.fips_ref.iter_rows(named=True):
            name = row.get("state_name") or ""
            abbr = row.get("state_abbr") or ""
            if q_lower in name.lower() or q_lower == abbr.lower():
                fips = str(int(row["state_fips"])).zfill(2)
                score_row = store.scores.filter(
                    pl.col("state_fips").cast(pl.Utf8).str.zfill(2) == fips
                )
                score = float(score_row["overall_score"][0]) if len(score_row) > 0 else None
                results.append(SearchResult(
                    id=fips, name=name, type="state",
                    state_abbr=abbr, score=score,
                ))

    # Search cities
    if not store.mei.is_empty():
        city_matches = store.mei.filter(
            pl.col("city_name").str.to_lowercase().str.contains(q_lower)
        ).head(limit)
        fips_lookup = {
            str(int(r["state_fips"])): r["state_abbr"]
            for r in store.fips_ref.iter_rows(named=True)
        }
        for row in city_matches.iter_rows(named=True):
            sfips = str(int(row.get("state_fips") or 0))
            results.append(SearchResult(
                id=row.get("city_id") or "",
                name=row.get("city_name") or "",
                type="city",
                state_abbr=fips_lookup.get(sfips),
                score=row.get("mei_score"),
            ))

    return results[:limit]
