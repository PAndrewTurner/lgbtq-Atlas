"""
Extract key mental health metrics from Trevor Project 2024 state PDFs.
50 state PDFs → one CSV: data/raw/health/trevorproject_survey_2024_extracted.csv
"""
import re
from pathlib import Path
import pdfplumber
import polars as pl

STATE_ABBR = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
    "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN",
    "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE",
    "Nevada": "NV", "NewHampshire": "NH", "NewJersey": "NJ", "NewMexico": "NM",
    "NewYork": "NY", "NorthCarolina": "NC", "NorthDakota": "ND", "Ohio": "OH",
    "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "RhodeIsland": "RI",
    "SouthCarolina": "SC", "SouthDakota": "SD", "Tennessee": "TN", "Texas": "TX",
    "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
    "WestVirginia": "WV", "Wisconsin": "WI", "Wyoming": "WY",
}

# CamelCase filename → display name
DISPLAY_NAME = {k: re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', k) for k in STATE_ABBR}


def _get_pages(pdf_path: Path) -> list[str]:
    with pdfplumber.open(pdf_path) as pdf:
        return [p.extract_text() or "" for p in pdf.pages]


def _extract_float(pattern: str, text: str, flags: int = 0) -> float | None:
    m = re.search(pattern, text, flags)
    return float(m.group(1)) if m else None


def extract_state(pdf_path: Path, state_key: str) -> dict:
    pages = _get_pages(pdf_path)
    full = "\n".join(pages)
    p4 = pages[3] if len(pages) > 3 else ""
    p5 = pages[4] if len(pages) > 4 else ""
    p7 = pages[6] if len(pages) > 6 else ""
    p9 = pages[8] if len(pages) > 8 else ""

    # Considered suicide: "35 in California seriously 11" or "39 Massachusetts seriously 11"
    considered, attempted = None, None
    m = re.search(r'(\d+)\s+(?:(?:people\s+)?in\s+)?[\w][\w ]{1,30}\bseriously\b\s+(\d+)', full)
    if m:
        considered = float(m.group(1))
        attempted = float(m.group(2))

    # No mental health access: "52% Wanted but did not receive care"
    no_care = _extract_float(r'(\d+)%\s+Wanted but did', p5)

    # Conversion therapy exposure: "5% Subjected to conversion therapy"
    ct = _extract_float(r'(\d+)%\s+Subjected to conversion therapy', p7)

    # School as affirming space (line after the phrase)
    school = _extract_float(
        r'identified school as an LGBTQ\+-affirming space\s*\n(\d+)%', p9
    )

    # High family support: "73% LGBTQ+ 27%" → take second number
    fam = _extract_float(r'\d+%\s+LGBTQ\+\s+(\d+)%', p9)

    return {
        "state": DISPLAY_NAME[state_key],
        "state_abbr": STATE_ABBR[state_key],
        "pct_considered_suicide": considered,
        "pct_attempted_suicide": attempted,
        "pct_no_mental_health_access": no_care,
        "pct_conversion_therapy_exposed": ct,
        "pct_felt_safe_school": school,
        "pct_high_family_support": fam,
        "year": 2024,
        "source": "Trevor Project",
    }


def run(raw_dir: Path | None = None) -> pl.DataFrame:
    from atlas.config import settings
    raw_dir = raw_dir or settings.data_raw_dir / "health"

    rows = []
    missing = []
    for state_key, abbr in STATE_ABBR.items():
        pdf_path = raw_dir / f"trevorproject_survey_2024_{state_key}.pdf"
        if not pdf_path.exists():
            missing.append(state_key)
            continue
        try:
            rows.append(extract_state(pdf_path, state_key))
        except Exception as e:
            print(f"  ERROR {state_key}: {e}")
            missing.append(state_key)

    if missing:
        print(f"  Missing/failed: {missing}")

    df = pl.DataFrame(rows)
    out = raw_dir / "trevorproject_survey_2024_extracted.csv"
    df.write_csv(out)
    print(f"  Saved {len(df)} rows → {out}")
    return df


if __name__ == "__main__":
    run()
