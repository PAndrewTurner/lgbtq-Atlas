from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from atlas.api.routes import states, cities, map as map_routes, search
from atlas.api.data_store import store   # triggers load at import time

app = FastAPI(
    title="LGBTQ+ Atlas API",
    description="Data API for the LGBTQ+ Atlas platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:4173",
        "https://lgbtqatlas.org",
    ],
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(states.router, prefix="/api")
app.include_router(cities.router, prefix="/api")
app.include_router(map_routes.router, prefix="/api")
app.include_router(search.router, prefix="/api")

# Serve static data exports (GeoJSON, state JSON files)
exports_dir = Path(__file__).parent.parent.parent / "data" / "exports"
if exports_dir.exists():
    app.mount("/data/exports", StaticFiles(directory=str(exports_dir)), name="exports")


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "states_loaded": len(store.fips_ref),
        "scores_rows": len(store.scores),
        "cities_loaded": len(store.mei),
    }
