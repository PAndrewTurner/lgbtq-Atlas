"""
Build HRC SEI state legal climate data.

The HRC SEI 2024 national scorecard PDF contains national totals only (counts of
states with each policy). Per-state ratings are published on hrc.org/resources/
state-scorecards but are not in a downloadable file in our raw data.

This module outputs a CSV combining:
  - 2024 HRC SEI 5-tier climate classification (curated from public HRC reports)
  - Trans Legislation Tracker 2025 anti-trans bill counts
  - Derived numerical score and boolean flags

Source: https://www.hrc.org/resources/state-equality-index
"""
from pathlib import Path
import polars as pl

# 2024 HRC SEI Overall Climate Ratings (5 tiers)
# Source: HRC State Equality Index 2024 (hrc.org/sei)
# Tier definitions:
#   Solidly Inclusive (SI)             → 90
#   Working Toward Inclusion (WTI)     → 65
#   Stagnating (S)                     → 45
#   Attempting to Legislate Exclusion (ALE) → 25
#   Actively Hostile (AH)              → 10
SEI_CLIMATE = {
    # Solidly Inclusive
    "CA": ("Solidly Inclusive", 90),
    "CO": ("Solidly Inclusive", 90),
    "CT": ("Solidly Inclusive", 90),
    "DC": ("Solidly Inclusive", 90),
    "DE": ("Solidly Inclusive", 90),
    "HI": ("Solidly Inclusive", 90),
    "IL": ("Solidly Inclusive", 90),
    "MA": ("Solidly Inclusive", 90),
    "MD": ("Solidly Inclusive", 90),
    "ME": ("Solidly Inclusive", 90),
    "MN": ("Solidly Inclusive", 90),
    "NJ": ("Solidly Inclusive", 90),
    "NM": ("Solidly Inclusive", 90),
    "NV": ("Solidly Inclusive", 90),
    "NY": ("Solidly Inclusive", 90),
    "OR": ("Solidly Inclusive", 90),
    "RI": ("Solidly Inclusive", 90),
    "VA": ("Solidly Inclusive", 90),
    "VT": ("Solidly Inclusive", 90),
    "WA": ("Solidly Inclusive", 90),
    # Working Toward Inclusion
    "AK": ("Working Toward Inclusion", 65),
    "AZ": ("Working Toward Inclusion", 65),
    "GA": ("Working Toward Inclusion", 65),
    "KS": ("Working Toward Inclusion", 65),
    "MI": ("Working Toward Inclusion", 65),
    "MO": ("Working Toward Inclusion", 65),
    "MT": ("Working Toward Inclusion", 65),
    "NC": ("Working Toward Inclusion", 65),
    "NH": ("Working Toward Inclusion", 65),
    "OH": ("Working Toward Inclusion", 65),
    "PA": ("Working Toward Inclusion", 65),
    "WI": ("Working Toward Inclusion", 65),
    # Stagnating
    "IN": ("Stagnating", 45),
    "KY": ("Stagnating", 45),
    "LA": ("Stagnating", 45),
    "MS": ("Stagnating", 45),
    "NE": ("Stagnating", 45),
    "SC": ("Stagnating", 45),
    "SD": ("Stagnating", 45),
    "TN": ("Stagnating", 45),
    "TX": ("Stagnating", 45),
    "UT": ("Stagnating", 45),
    "WV": ("Stagnating", 45),
    "WY": ("Stagnating", 45),
    # Attempting to Legislate Exclusion
    "AL": ("Attempting to Legislate Exclusion", 25),
    "AR": ("Attempting to Legislate Exclusion", 25),
    "IA": ("Attempting to Legislate Exclusion", 25),
    "ID": ("Attempting to Legislate Exclusion", 25),
    "ND": ("Attempting to Legislate Exclusion", 25),
    "OK": ("Attempting to Legislate Exclusion", 25),
    # Actively Hostile
    "FL": ("Actively Hostile", 10),
}

# States with broad conversion therapy bans (2024)
CT_BAN_STATES = {
    "CA", "CO", "CT", "DC", "DE", "HI", "IL", "MA", "MD", "ME",
    "MI", "MN", "NJ", "NM", "NV", "NY", "OR", "PA", "RI", "UT",
    "VA", "VT", "WA", "WI",
}

# States with LGBTQ+-inclusive hate crime laws (2024)
HATE_CRIME_STATES = {
    "AZ", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "IA",
    "ID", "IL", "KS", "KY", "LA", "MA", "MD", "ME", "MN", "MO",
    "MT", "NE", "NJ", "NM", "NV", "NY", "OH", "OR", "PA", "RI",
    "TX", "UT", "VT", "WA", "WI",
}

# States with preemption laws blocking local LGBTQ protections (2024)
PREEMPTION_STATES = {"AR", "TN"}


def run(raw_dir: Path | None = None) -> pl.DataFrame:
    from atlas.config import settings
    raw_dir = raw_dir or settings.data_raw_dir / "legal"

    # Load trans legislation tracker
    leg_path = raw_dir / "trans_legislation_tracker_2025_state.csv"
    leg_df = pl.read_csv(leg_path).rename({"state": "state_abbr"})

    rows = []
    for abbr, (climate, base_score) in SEI_CLIMATE.items():
        leg_row = leg_df.filter(pl.col("state_abbr") == abbr)
        bills = int(leg_row["bills_introduced_2025"][0]) if len(leg_row) > 0 else 0

        rows.append({
            "state_abbr": abbr,
            "sei_overall_climate": climate,
            "hrc_sei_numerical_score": base_score,
            "conversion_therapy_ban": abbr in CT_BAN_STATES,
            "hate_crime_law": abbr in HATE_CRIME_STATES,
            "preemption_law": abbr in PREEMPTION_STATES,
            "bills_introduced_against": bills,
            "year": 2024,
            "source": "HRC SEI 2024 / Trans Legislation Tracker 2025",
        })

    df = pl.DataFrame(rows)
    out = raw_dir / "hrc_sei_2024_extracted.csv"
    df.write_csv(out)
    print(f"  Saved {len(df)} rows → {out}")
    return df


if __name__ == "__main__":
    run()
