"""
Extract LGBT population estimates from Williams Institute 2023 PDF.
Output: data/raw/population/williams_population_estimates_extracted_2023.csv
"""
import re
from pathlib import Path
import pdfplumber
import polars as pl

STATE_ABBR = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT",
    "Delaware": "DE", "District of Columbia": "DC", "D.C.": "DC",
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
    "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN",
    "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE",
    "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC",
    "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR",
    "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
    "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
    "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY",
}

SKIP_NAMES = {
    "", "United States", "Northeast", "Midwest", "South", "West", "Total",
    "RANK", "STATE", "Total adults",
}


def run(raw_dir: Path | None = None) -> pl.DataFrame:
    from atlas.config import settings
    raw_dir = raw_dir or settings.data_raw_dir / "population"
    pdf_path = raw_dir / "williams_population_estimates_2023.pdf"

    seen: set[str] = set()
    rows = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables():
                for row in table:
                    if not row or not row[0]:
                        continue
                    name = str(row[0]).strip().rstrip("*")
                    if name in SKIP_NAMES or "PERCENT" in name or "NUMBER" in name:
                        continue
                    # Only rows with a percentage in column 1
                    if len(row) < 2 or not row[1] or "%" not in str(row[1]):
                        continue
                    abbr = STATE_ABBR.get(name)
                    if not abbr or abbr in seen:
                        continue
                    seen.add(abbr)
                    pct = float(re.sub(r"[^0-9.]", "", str(row[1])))
                    count_str = re.sub(r"[^0-9]", "", str(row[2])) if len(row) > 2 and row[2] else ""
                    count = int(count_str) if count_str else None
                    rows.append({
                        "state": name if name != "D.C." else "District of Columbia",
                        "state_abbr": abbr,
                        "lgbtq_pct_of_adults": pct,
                        "lgbtq_adult_count": count,
                        "source": "Williams Institute",
                        "vintage": 2023,
                    })

    df = pl.DataFrame(rows).sort("state_abbr")
    out = raw_dir / "williams_population_estimates_extracted_2023.csv"
    df.write_csv(out)
    print(f"  Saved {len(df)} rows → {out}")
    return df


if __name__ == "__main__":
    run()
