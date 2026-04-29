"""
Transform geographic reference files.
Outputs:
  processed/reference/state_fips.csv   — FIPS ↔ name ↔ abbr lookup (51 rows: 50 + DC)
  data/exports/states.geojson          — state boundary polygons for MapLibre
"""
from pathlib import Path
import polars as pl


REGIONS = {
    "AL": ("South", "East South Central"), "AK": ("West", "Pacific"),
    "AZ": ("West", "Mountain"), "AR": ("South", "West South Central"),
    "CA": ("West", "Pacific"), "CO": ("West", "Mountain"),
    "CT": ("Northeast", "New England"), "DC": ("South", "South Atlantic"),
    "DE": ("South", "South Atlantic"), "FL": ("South", "South Atlantic"),
    "GA": ("South", "South Atlantic"), "HI": ("West", "Pacific"),
    "ID": ("West", "Mountain"), "IL": ("Midwest", "East North Central"),
    "IN": ("Midwest", "East North Central"), "IA": ("Midwest", "West North Central"),
    "KS": ("Midwest", "West North Central"), "KY": ("South", "East South Central"),
    "LA": ("South", "West South Central"), "ME": ("Northeast", "New England"),
    "MD": ("South", "South Atlantic"), "MA": ("Northeast", "New England"),
    "MI": ("Midwest", "East North Central"), "MN": ("Midwest", "West North Central"),
    "MS": ("South", "East South Central"), "MO": ("Midwest", "West North Central"),
    "MT": ("West", "Mountain"), "NE": ("Midwest", "West North Central"),
    "NV": ("West", "Mountain"), "NH": ("Northeast", "New England"),
    "NJ": ("Northeast", "Middle Atlantic"), "NM": ("West", "Mountain"),
    "NY": ("Northeast", "Middle Atlantic"), "NC": ("South", "South Atlantic"),
    "ND": ("Midwest", "West North Central"), "OH": ("Midwest", "East North Central"),
    "OK": ("South", "West South Central"), "OR": ("West", "Pacific"),
    "PA": ("Northeast", "Middle Atlantic"), "RI": ("Northeast", "New England"),
    "SC": ("South", "South Atlantic"), "SD": ("Midwest", "West North Central"),
    "TN": ("South", "East South Central"), "TX": ("South", "West South Central"),
    "UT": ("West", "Mountain"), "VT": ("Northeast", "New England"),
    "VA": ("South", "South Atlantic"), "WA": ("West", "Pacific"),
    "WV": ("South", "South Atlantic"), "WI": ("Midwest", "East North Central"),
    "WY": ("West", "Mountain"),
}


def build_state_fips(raw_dir: Path, out_dir: Path) -> pl.DataFrame:
    fips_path = raw_dir / "geo" / "census_fips_state.txt"
    df = pl.read_csv(fips_path, separator="|").rename({
        "STATE": "state_abbr",
        "STATEFP": "state_fips",
        "STATE_NAME": "state_name",
    }).select(["state_fips", "state_name", "state_abbr"])

    # Zero-pad FIPS to 2 chars
    df = df.with_columns(
        pl.col("state_fips").cast(pl.Utf8).str.zfill(2)
    )

    # Filter to 50 states + DC (exclude territories)
    df = df.filter(pl.col("state_fips").cast(pl.Int32) <= 56)

    df = df.with_columns([
        pl.col("state_abbr").map_elements(
            lambda a: REGIONS.get(a, ("Unknown", "Unknown"))[0], return_dtype=pl.Utf8
        ).alias("region"),
        pl.col("state_abbr").map_elements(
            lambda a: REGIONS.get(a, ("Unknown", "Unknown"))[1], return_dtype=pl.Utf8
        ).alias("division"),
    ])

    out = out_dir / "reference" / "state_fips.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.write_csv(out)
    print(f"  state_fips.csv → {len(df)} rows")
    return df


def build_states_geojson(raw_dir: Path, exports_dir: Path) -> None:
    import zipfile, tempfile, subprocess, shutil
    zip_path = raw_dir / "geo" / "census_state_boundaries_500k.zip"
    if not zip_path.exists():
        print(f"  WARNING: {zip_path} not found — skipping GeoJSON")
        return

    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(tmp)
        shp_files = list(Path(tmp).rglob("*.shp"))
        if not shp_files:
            print("  WARNING: No .shp found in zip")
            return
        shp = shp_files[0]
        out_path = exports_dir / "states.geojson"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            import geopandas as gpd
            gdf = gpd.read_file(shp)
            # Keep only 50 states + DC; rename STATEFP → fips
            gdf = gdf[gdf["STATEFP"].astype(int) <= 56].copy()
            gdf = gdf.rename(columns={"STATEFP": "fips", "NAME": "name", "STUSPS": "abbr"})
            gdf = gdf[["fips", "name", "abbr", "geometry"]]
            gdf.to_file(out_path, driver="GeoJSON")
            print(f"  states.geojson → {len(gdf)} features")
        except Exception as e:
            print(f"  WARNING: GeoJSON build failed: {e}")


def run() -> None:
    from atlas.config import settings
    build_state_fips(settings.data_raw_dir, settings.data_processed_dir)
    build_states_geojson(settings.data_raw_dir, settings.data_exports_dir)


if __name__ == "__main__":
    run()
