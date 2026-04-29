"""
Build cities GeoJSON with MEI scores + coordinates from Census Places Gazetteer.
Downloads Gazetteer on first run; subsequent runs use cached copy.
"""
import io
import zipfile
from pathlib import Path

import httpx
import polars as pl


GAZETTEER_URL = "https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2023_Gazetteer/2023_Gaz_place_national.zip"
GAZETTEER_CACHE = Path(__file__).parent.parent.parent / "data" / "raw" / "geo" / "2023_Gaz_place_national.txt"


def _fetch_gazetteer() -> pl.DataFrame:
    if not GAZETTEER_CACHE.exists():
        print("  Downloading Census Gazetteer (places)…")
        GAZETTEER_CACHE.parent.mkdir(parents=True, exist_ok=True)
        r = httpx.get(GAZETTEER_URL, follow_redirects=True, timeout=60)
        r.raise_for_status()
        with zipfile.ZipFile(io.BytesIO(r.content)) as z:
            name = z.namelist()[0]
            GAZETTEER_CACHE.write_bytes(z.read(name))

    df = pl.read_csv(
        GAZETTEER_CACHE,
        separator="\t",
        infer_schema_length=500,
        ignore_errors=True,
    )
    # Strip trailing whitespace from column names (Gazetteer pads last column)
    df = df.rename({c: c.strip() for c in df.columns})

    # Actual Census 2023 Gazetteer columns: USPS, NAME, INTPTLAT, INTPTLONG
    df = df.rename({"USPS": "state_abbr", "NAME": "place_name",
                    "INTPTLAT": "lat", "INTPTLONG": "lng"})

    return df.select(["place_name", "state_abbr", "lat", "lng"]).with_columns([
        pl.col("place_name").str.strip_chars(),
        pl.col("state_abbr").str.strip_chars(),
        pl.col("lat").cast(pl.Float64, strict=False),
        pl.col("lng").str.strip_chars().cast(pl.Float64, strict=False),
    ]).drop_nulls(subset=["lat", "lng"])


def _normalize(name: str) -> str:
    """Strip common suffixes used in Gazetteer but not in HRC names."""
    for suffix in (" city", " town", " village", " borough", " CDP", " municipality"):
        if name.lower().endswith(suffix):
            return name[: -len(suffix)].strip()
    return name.strip()


def run() -> pl.DataFrame:
    from atlas.config import settings

    raw = settings.data_raw_dir
    exports = settings.data_exports_dir
    exports.mkdir(parents=True, exist_ok=True)

    mei = pl.read_csv(raw / "legal" / "hrc_mei_city_scores_2025.csv").with_columns([
        pl.col("city").str.strip_chars(),
        pl.col("state").str.strip_chars(),
        pl.col("mei_score").cast(pl.Int32),
    ])

    gaz = _fetch_gazetteer()

    # Add normalised name column for matching
    gaz = gaz.with_columns(
        pl.col("place_name").map_elements(_normalize, return_dtype=pl.Utf8).alias("name_norm")
    )
    mei = mei.with_columns(
        pl.col("city").map_elements(_normalize, return_dtype=pl.Utf8).alias("name_norm")
    )

    joined = mei.join(
        gaz.rename({"state_abbr": "state"}),
        on=["name_norm", "state"],
        how="left",
    )

    matched = joined.drop_nulls(subset=["lat", "lng"])
    missed = len(joined) - len(matched)
    print(f"  Cities matched: {len(matched)}/{len(joined)}  (unmatched: {missed})")

    # Build GeoJSON
    features = []
    for row in matched.iter_rows(named=True):
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [row["lng"], row["lat"]]},
            "properties": {
                "city": row["city"],
                "state": row["state"],
                "mei_score": row["mei_score"],
                "slug": row.get("hrc_slug", ""),
            },
        })

    geojson = {"type": "FeatureCollection", "features": features}

    import json
    out = exports / "cities.geojson"
    out.write_text(json.dumps(geojson))
    print(f"  cities.geojson → {len(features)} city points")
    return matched
