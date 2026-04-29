import polars as pl
from fastapi import APIRouter, HTTPException
from atlas.api.data_store import store

router = APIRouter(prefix="/cities", tags=["cities"])


@router.get("/")
async def list_cities(state_fips: str | None = None, year: int = 2025, limit: int = 50):
    if store.mei.is_empty():
        return []
    df = store.mei.filter(pl.col("year") == year)
    if state_fips:
        df = df.filter(pl.col("state_fips") == int(state_fips))
    df = df.sort("mei_score", descending=True).head(limit)
    return df.to_dicts()


@router.get("/{city_id}")
async def get_city(city_id: str):
    if store.mei.is_empty():
        raise HTTPException(status_code=404, detail="City data not loaded")
    row = store.mei.filter(pl.col("city_id") == city_id)
    if row.is_empty():
        raise HTTPException(status_code=404, detail=f"City {city_id} not found")
    return row.row(0, named=True)
