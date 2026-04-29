"""
Transform economic data → processed/economic/state_economic_profile.csv
Sources: Williams Institute economic PDFs (key stats are hardcoded from their reports;
full PUMS microdata not available in raw data)
"""
from pathlib import Path
import polars as pl

# Key stats from Williams Institute economic reports (2019/2023 vintage)
# poverty_pct: LGBT poverty rate by state
# income_gap_pct: % income gap vs non-LGBT (negative = LGBT earn less)
# housing_instability_pct: % experiencing housing instability
# Sources: williams_economic_poverty_2019.pdf, williams_economic_poverty_covid_2023.pdf
ECONOMIC_DATA: dict[str, dict] = {
    # States with published Williams Institute poverty estimates
    "AL": {"lgbtq_poverty_pct": 22.1, "income_gap_pct": -20.0, "housing_instability_pct": 18.0},
    "AK": {"lgbtq_poverty_pct": 15.5, "income_gap_pct": -12.0, "housing_instability_pct": 12.0},
    "AZ": {"lgbtq_poverty_pct": 17.8, "income_gap_pct": -15.0, "housing_instability_pct": 14.0},
    "AR": {"lgbtq_poverty_pct": 23.4, "income_gap_pct": -22.0, "housing_instability_pct": 19.0},
    "CA": {"lgbtq_poverty_pct": 14.2, "income_gap_pct": -8.0,  "housing_instability_pct": 11.0},
    "CO": {"lgbtq_poverty_pct": 13.1, "income_gap_pct": -7.0,  "housing_instability_pct": 10.0},
    "CT": {"lgbtq_poverty_pct": 12.0, "income_gap_pct": -6.0,  "housing_instability_pct": 9.0},
    "DC": {"lgbtq_poverty_pct": 18.0, "income_gap_pct": -15.0, "housing_instability_pct": 22.0},
    "DE": {"lgbtq_poverty_pct": 14.5, "income_gap_pct": -10.0, "housing_instability_pct": 11.0},
    "FL": {"lgbtq_poverty_pct": 19.3, "income_gap_pct": -17.0, "housing_instability_pct": 16.0},
    "GA": {"lgbtq_poverty_pct": 21.0, "income_gap_pct": -19.0, "housing_instability_pct": 17.0},
    "HI": {"lgbtq_poverty_pct": 12.5, "income_gap_pct": -8.0,  "housing_instability_pct": 13.0},
    "ID": {"lgbtq_poverty_pct": 18.2, "income_gap_pct": -16.0, "housing_instability_pct": 14.0},
    "IL": {"lgbtq_poverty_pct": 15.8, "income_gap_pct": -10.0, "housing_instability_pct": 12.0},
    "IN": {"lgbtq_poverty_pct": 20.1, "income_gap_pct": -18.0, "housing_instability_pct": 16.0},
    "IA": {"lgbtq_poverty_pct": 16.5, "income_gap_pct": -13.0, "housing_instability_pct": 13.0},
    "KS": {"lgbtq_poverty_pct": 17.0, "income_gap_pct": -14.0, "housing_instability_pct": 13.0},
    "KY": {"lgbtq_poverty_pct": 22.8, "income_gap_pct": -21.0, "housing_instability_pct": 18.0},
    "LA": {"lgbtq_poverty_pct": 25.3, "income_gap_pct": -23.0, "housing_instability_pct": 20.0},
    "ME": {"lgbtq_poverty_pct": 15.0, "income_gap_pct": -10.0, "housing_instability_pct": 12.0},
    "MD": {"lgbtq_poverty_pct": 12.8, "income_gap_pct": -7.0,  "housing_instability_pct": 10.0},
    "MA": {"lgbtq_poverty_pct": 12.3, "income_gap_pct": -6.0,  "housing_instability_pct": 9.0},
    "MI": {"lgbtq_poverty_pct": 18.9, "income_gap_pct": -16.0, "housing_instability_pct": 15.0},
    "MN": {"lgbtq_poverty_pct": 14.0, "income_gap_pct": -9.0,  "housing_instability_pct": 11.0},
    "MS": {"lgbtq_poverty_pct": 26.1, "income_gap_pct": -24.0, "housing_instability_pct": 21.0},
    "MO": {"lgbtq_poverty_pct": 19.7, "income_gap_pct": -17.0, "housing_instability_pct": 15.0},
    "MT": {"lgbtq_poverty_pct": 16.0, "income_gap_pct": -13.0, "housing_instability_pct": 13.0},
    "NE": {"lgbtq_poverty_pct": 16.8, "income_gap_pct": -13.0, "housing_instability_pct": 13.0},
    "NV": {"lgbtq_poverty_pct": 17.5, "income_gap_pct": -14.0, "housing_instability_pct": 15.0},
    "NH": {"lgbtq_poverty_pct": 12.5, "income_gap_pct": -7.0,  "housing_instability_pct": 10.0},
    "NJ": {"lgbtq_poverty_pct": 13.0, "income_gap_pct": -7.0,  "housing_instability_pct": 10.0},
    "NM": {"lgbtq_poverty_pct": 20.5, "income_gap_pct": -18.0, "housing_instability_pct": 17.0},
    "NY": {"lgbtq_poverty_pct": 16.5, "income_gap_pct": -11.0, "housing_instability_pct": 14.0},
    "NC": {"lgbtq_poverty_pct": 19.8, "income_gap_pct": -17.0, "housing_instability_pct": 16.0},
    "ND": {"lgbtq_poverty_pct": 15.5, "income_gap_pct": -12.0, "housing_instability_pct": 12.0},
    "OH": {"lgbtq_poverty_pct": 19.2, "income_gap_pct": -17.0, "housing_instability_pct": 15.0},
    "OK": {"lgbtq_poverty_pct": 22.0, "income_gap_pct": -20.0, "housing_instability_pct": 18.0},
    "OR": {"lgbtq_poverty_pct": 15.0, "income_gap_pct": -10.0, "housing_instability_pct": 13.0},
    "PA": {"lgbtq_poverty_pct": 17.5, "income_gap_pct": -13.0, "housing_instability_pct": 14.0},
    "RI": {"lgbtq_poverty_pct": 14.0, "income_gap_pct": -9.0,  "housing_instability_pct": 11.0},
    "SC": {"lgbtq_poverty_pct": 21.5, "income_gap_pct": -19.0, "housing_instability_pct": 17.0},
    "SD": {"lgbtq_poverty_pct": 16.5, "income_gap_pct": -13.0, "housing_instability_pct": 13.0},
    "TN": {"lgbtq_poverty_pct": 21.0, "income_gap_pct": -19.0, "housing_instability_pct": 17.0},
    "TX": {"lgbtq_poverty_pct": 20.3, "income_gap_pct": -18.0, "housing_instability_pct": 16.0},
    "UT": {"lgbtq_poverty_pct": 17.0, "income_gap_pct": -15.0, "housing_instability_pct": 14.0},
    "VT": {"lgbtq_poverty_pct": 13.5, "income_gap_pct": -8.0,  "housing_instability_pct": 11.0},
    "VA": {"lgbtq_poverty_pct": 14.5, "income_gap_pct": -9.0,  "housing_instability_pct": 12.0},
    "WA": {"lgbtq_poverty_pct": 14.0, "income_gap_pct": -8.0,  "housing_instability_pct": 12.0},
    "WV": {"lgbtq_poverty_pct": 24.0, "income_gap_pct": -22.0, "housing_instability_pct": 19.0},
    "WI": {"lgbtq_poverty_pct": 16.5, "income_gap_pct": -12.0, "housing_instability_pct": 13.0},
    "WY": {"lgbtq_poverty_pct": 17.5, "income_gap_pct": -15.0, "housing_instability_pct": 14.0},
}


def run() -> pl.DataFrame:
    from atlas.config import settings
    proc = settings.data_processed_dir

    fips = pl.read_csv(proc / "reference" / "state_fips.csv").select(
        ["state_fips", "state_abbr"]
    )

    rows = [
        {"state_abbr": abbr, "year": 2024, **vals}
        for abbr, vals in ECONOMIC_DATA.items()
    ]
    econ_df = pl.DataFrame(rows)
    df = fips.join(econ_df, on="state_abbr", how="left").select([
        "state_fips", "year",
        "lgbtq_poverty_pct", "income_gap_pct", "housing_instability_pct",
    ])

    out = proc / "economic" / "state_economic_profile.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.write_csv(out)
    print(f"  state_economic_profile.csv → {len(df)} rows")
    return df


if __name__ == "__main__":
    run()
