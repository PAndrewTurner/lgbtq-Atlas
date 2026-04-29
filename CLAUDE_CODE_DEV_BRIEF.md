# LGBTQ+ Atlas — Claude Code Development Brief

## Project Summary

Build the **LGBTQ+ Atlas** — a full-stack, interactive web platform that provides rich, data-driven portraits of LGBTQ+ life across every U.S. state and major city. Users explore an interactive choropleth map, click into state and city profiles, and get multi-dimensional data across population, safety, legal climate, health, economics, and community infrastructure.

**The product vision:** Think NYT interactive graphics meets Williams Institute research meets the accessibility of a consumer app. Clean, beautiful, fast, and genuinely useful to LGBTQ+ people making real decisions about where to live, travel, or advocate.

---

## Tech Stack

### Backend (Python)
- **Python 3.12+**
- `httpx` + `asyncio` — async HTTP fetching
- `polars` — primary dataframe library (not pandas); reads/writes CSV and Excel natively
- `openpyxl` — Excel (.xlsx) read/write for multi-sheet processed files
- `geopandas` + `shapely` — spatial operations
- `scikit-learn` — normalization and composite scoring
- `fastapi` + `uvicorn` — REST API server; loads processed CSVs into memory at startup
- `anthropic` SDK — LLM-generated narrative summaries per state/city
- `pydantic v2` — data validation and API models
- `typer` — CLI for pipeline management
- `tenacity` — retry logic for external API calls
- `pytest` + `pytest-asyncio` — testing

### Frontend
- **React 18** + **TypeScript**
- `Vite` — build tool
- `MapLibre GL JS` — interactive vector tile map
- `D3.js` — choropleth coloring + sparkline charts
- `Recharts` — dimension charts inside profile panels
- `Tailwind CSS` — utility styling
- `Zustand` — lightweight state management
- `TanStack Query` — API data fetching and caching
- `Framer Motion` — panel animations and transitions

### Infrastructure
- `GitHub Actions` — CI/CD and annual data refresh pipeline
- `Vercel` — frontend hosting
- `Railway` — FastAPI backend hosting
- **No database.** All processed data lives as CSV/Excel files. The API loads them into memory at startup using Polars — 50 states × \~15 dimension files is well under 500MB total.

---

## Repository Structure

```
lgbtq-atlas/
├── pyproject.toml
├── .python-version                  # 3.12
├── README.md
├── .env.example
├── .gitignore
│
├── data/
│   ├── raw/                         # Gitignored — source files from Cowork pipeline
│   │   ├── population/
│   │   ├── legal/
│   │   ├── safety/
│   │   ├── health/
│   │   ├── economic/
│   │   ├── socioeconomic/
│   │   ├── community/
│   │   ├── youth/
│   │   └── geo/
│   ├── processed/                   # Gitignored — cleaned, analysis-ready flat files
│   │   ├── population/
│   │   │   ├── state_population.csv           # One row per state
│   │   │   └── city_same_sex_households.csv   # One row per city
│   │   ├── legal/
│   │   │   ├── state_policy_scores.csv
│   │   │   └── city_mei_scores.csv
│   │   ├── safety/
│   │   │   └── state_hate_crimes.csv          # With year column for trend data
│   │   ├── health/
│   │   │   └── state_health_outcomes.csv
│   │   ├── economic/
│   │   │   └── state_economic_profile.csv
│   │   ├── socioeconomic/
│   │   │   ├── state_income_education.csv     # Median income, education levels
│   │   │   ├── state_occupation_dist.xlsx     # Multi-sheet: top occupations by state
│   │   │   ├── state_marriage_households.csv  # Married/cohabiting counts and rates
│   │   │   └── state_industry_dist.csv        # Industry breakdown by state
│   │   ├── community/
│   │   │   ├── state_community.csv
│   │   │   └── city_nonprofits.csv
│   │   ├── youth/
│   │   │   └── state_youth.csv
│   │   ├── scores/
│   │   │   ├── state_scores.csv               # Composite + dimension scores, all years
│   │   │   └── city_scores.csv
│   │   └── reference/
│   │       ├── state_fips.csv                 # FIPS ↔ name ↔ abbr lookup
│   │       └── occupation_codes.csv           # SOC code → title lookup
│   └── exports/                     # Committed — static JSON/GeoJSON for frontend
│       ├── states.geojson
│       ├── states_map.json          # Slim index for map coloring
│       ├── state_profiles/          # FL.json, CA.json, etc. — full profiles
│       └── city_profiles/           # city-id.json — full city profiles
│
├── atlas/                           # Main Python package
│   ├── __init__.py
│   ├── config.py
│   │
│   ├── ingest/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── williams_institute.py
│   │   ├── map_policy.py
│   │   ├── hrc_mei.py
│   │   ├── fbi_hate_crimes.py
│   │   ├── cdc_brfss.py
│   │   ├── cdc_hiv.py
│   │   ├── census_acs.py
│   │   ├── trevor_project.py
│   │   ├── aclu_tracker.py
│   │   ├── irs_nonprofits.py
│   │   └── pride_events.py
│   │
│   ├── transform/
│   │   ├── __init__.py
│   │   ├── normalize.py
│   │   ├── geo_join.py
│   │   └── validate.py
│   │
│   ├── scoring/
│   │   ├── __init__.py
│   │   ├── dimensions.py
│   │   ├── composite.py
│   │   ├── uncertainty.py
│   │   └── corrections.py
│   │
│   ├── narrative/
│   │   ├── __init__.py
│   │   └── generator.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── routes/
│   │       ├── states.py
│   │       ├── cities.py
│   │       ├── map.py
│   │       └── search.py
│   │
│   └── export/
│       ├── __init__.py
│       └── build.py
│
├── pipeline/
│   └── cli.py                       # `atlas ingest`, `atlas build`, `atlas serve`
│
├── notebooks/
│   ├── 01_population_eda.ipynb
│   ├── 02_scoring_methodology.ipynb
│   └── 03_validation.ipynb
│
├── tests/
│   ├── test_ingest/
│   ├── test_scoring/
│   └── test_api/
│
├── frontend/
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── index.html
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── components/
│       │   ├── map/
│       │   │   ├── AtlasMap.tsx
│       │   │   ├── ChoroplethLayer.tsx
│       │   │   ├── MapControls.tsx
│       │   │   └── HoverTooltip.tsx
│       │   ├── profile/
│       │   │   ├── StateProfileDrawer.tsx
│       │   │   ├── CityProfileDrawer.tsx
│       │   │   ├── DimensionBar.tsx
│       │   │   ├── TrendSparkline.tsx
│       │   │   ├── StatCard.tsx
│       │   │   ├── PopulationPanel.tsx
│       │   │   ├── NarrativeSummary.tsx
│       │   │   ├── CityRankings.tsx
│       │   │   └── ShareCard.tsx
│       │   ├── nav/
│       │   │   ├── Header.tsx
│       │   │   ├── LayerSwitcher.tsx
│       │   │   └── SearchBar.tsx
│       │   └── ui/
│       │       ├── Badge.tsx
│       │       ├── Drawer.tsx
│       │       └── TrendArrow.tsx
│       ├── hooks/
│       │   ├── useStateProfile.ts
│       │   ├── useCityProfile.ts
│       │   ├── useMapLayer.ts
│       │   └── useComparison.ts
│       ├── store/
│       │   └── atlasStore.ts
│       ├── types/
│       │   ├── profile.ts
│       │   └── scoring.ts
│       └── utils/
│           ├── colorScales.ts
│           ├── formatters.ts
│           └── geo.ts
│
└── .github/
    └── workflows/
        ├── ci.yml
        └── data-refresh.yml
```

---

## Phase 1: Data Pipeline

### 1.1 — Project Bootstrap

```bash
# Python
uv init lgbtq-atlas && cd lgbtq-atlas
uv add polars openpyxl geopandas shapely fastapi uvicorn httpx tenacity \
        scikit-learn anthropic pydantic typer pytest pytest-asyncio

# Frontend
cd frontend
npm create vite@latest . -- --template react-ts
npm install maplibre-gl d3 recharts framer-motion zustand \
            @tanstack/react-query tailwindcss @types/d3 @types/maplibre-gl
```

### 1.2 — config.py

```python
from pathlib import Path
from pydantic_settings import BaseSettings

ROOT = Path(__file__).parent.parent

class Settings(BaseSettings):
    data_raw_dir: Path = ROOT / "data" / "raw"
    data_processed_dir: Path = ROOT / "data" / "processed"
    data_exports_dir: Path = ROOT / "data" / "exports"
    duckdb_path: Path = ROOT / "data" / "processed" / "atlas.duckdb"
    anthropic_api_key: str = ""

    # Coverage — top 100 metros by estimated LGBTQ+ population
    metro_fips: list[str] = [...]  # Populate from Census CBSA codes

    class Config:
        env_file = ".env"

settings = Settings()
```

### 1.3 — Base Ingester (atlas/ingest/base.py)

```python
from abc import ABC, abstractmethod
from pathlib import Path
import polars as pl

class BaseIngester(ABC):
    source_name: str

    @property
    def raw_dir(self) -> Path:
        from atlas.config import settings
        d = settings.data_raw_dir / self.category
        d.mkdir(parents=True, exist_ok=True)
        return d

    @abstractmethod
    async def fetch(self) -> None:
        """Download raw data files to self.raw_dir"""

    @abstractmethod
    def parse(self) -> pl.DataFrame:
        """Parse raw files into a clean Polars DataFrame"""

    def save_csv(self, df: pl.DataFrame, name: str) -> Path:
        """Write cleaned DataFrame to data/processed/ as CSV."""
        from atlas.config import settings
        out = settings.data_processed_dir / self.category / f"{name}.csv"
        out.parent.mkdir(parents=True, exist_ok=True)
        df.write_csv(out)
        return out

    def save_excel(self, sheets: dict[str, pl.DataFrame], name: str) -> Path:
        """
        Write a multi-sheet Excel file to data/processed/.
        sheets: dict of sheet_name → DataFrame
        """
        import openpyxl
        from atlas.config import settings
        out = settings.data_processed_dir / self.category / f"{name}.xlsx"
        out.parent.mkdir(parents=True, exist_ok=True)
        wb = openpyxl.Workbook()
        wb.remove(wb.active)  # remove default empty sheet
        for sheet_name, df in sheets.items():
            ws = wb.create_sheet(title=sheet_name[:31])  # Excel tab name limit
            ws.append(df.columns)
            for row in df.iter_rows(named=False):
                ws.append(list(row))
        wb.save(out)
        return out
```

### 1.4 — Processed File Schemas

No database. Each transform module writes one or more CSV or Excel files to `data/processed/`. The FastAPI app loads all of them into Polars DataFrames at startup and holds them in memory. Schemas for each file:

**`data/processed/population/state_population.csv`**
```
state_fips, state_name, state_abbr, year,
lgbtq_pop, lgbtq_pct, trans_pop, trans_pct,
bipoc_pct, urban_pct, same_sex_hh,
gen_z_pct, millennial_pct, genx_pct, boomer_pct
```

**`data/processed/legal/state_policy_scores.csv`**
```
state_fips, year,
map_total_score, non_discrimination_employment, non_discrimination_housing,
hate_crime_law, conversion_therapy_ban, adoption_rights,
trans_healthcare_protected, religious_exemption_penalty,
preemption_law, bills_passed_against
```

**`data/processed/legal/city_mei_scores.csv`**
```
city_id, city_name, state_fips, year,
mei_score, mei_grade, nd_score, services_score, le_score
```

**`data/processed/safety/state_hate_crimes.csv`**
```
state_fips, year,
so_incidents, gi_incidents, so_per_100k, gi_per_100k,
reporting_rate, non_reporting_agency_count, adjusted_score
```

**`data/processed/health/state_health_outcomes.csv`**
```
state_fips, year,
depression_pct, healthcare_avoidance_pct, uninsured_pct,
hiv_diagnosis_rate, hiv_viral_suppression_pct
```

**`data/processed/economic/state_economic_profile.csv`**
```
state_fips, year,
lgbtq_poverty_pct, income_gap_pct, housing_instability_pct
```

**`data/processed/socioeconomic/state_income_education.csv`**
```
state_fips, year,
median_individual_income_lgbtq, median_individual_income_nonlgbtq,
median_hh_income_samesex_married, median_hh_income_samesex_cohabiting,
median_hh_income_general_population,
pct_less_than_hs, pct_hs_diploma, pct_some_college,
pct_bachelors, pct_graduate,
pct_bachelors_lgbtq, pct_graduate_lgbtq,
pct_bachelors_nonlgbtq, pct_graduate_nonlgbtq
```

**`data/processed/socioeconomic/state_marriage_households.csv`**
```
state_fips, year,
same_sex_married_count, same_sex_cohabiting_count,
same_sex_marriage_rate, opposite_sex_marriage_rate,
same_sex_hh_with_children_pct, avg_hh_size_samesex
```

**`data/processed/socioeconomic/state_industry_dist.csv`**
```
state_fips, year, industry_name, naics_group,
lgbtq_pct_in_industry, general_pop_pct_in_industry
```

**`data/processed/socioeconomic/state_occupation_dist.xlsx`**
One sheet per state (tab named by state abbreviation: FL, CA, etc.).
Each sheet has columns:
```
occupation_title, soc_group, lgbtq_pct, general_pop_pct, median_wage, rank
```
Use Excel (not CSV) here because one-file-per-state would be 51 CSVs for a single dimension — a multi-sheet workbook is cleaner for this specific case.

**`data/processed/community/state_community.csv`**
```
state_fips, year,
lgbtq_orgs_count, lgbtq_orgs_per_100k,
pride_events_count, largest_pride_attendance
```

**`data/processed/youth/state_youth.csv`**
```
state_fips, year,
suicidality_pct, school_safety_score,
gsa_presence_pct, conversion_therapy_exposure_pct
```

**`data/processed/scores/state_scores.csv`**
```
state_fips, year,
legal_score, safety_score, health_score,
economic_score, community_score, youth_score,
overall_score, confidence
```

**`data/processed/reference/state_fips.csv`**
```
state_fips, state_name, state_abbr, region, division
```

**`data/processed/reference/occupation_codes.csv`**
```
pums_occp_code, soc_code, occupation_title, soc_major_group
```

---

## Phase 2: Scoring Engine

### atlas/scoring/dimensions.py

Each function accepts a dict of raw dimension values and returns a float 0–100.

```python
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def score_legal(data: dict) -> float:
    """
    Base: MAP total score (already 0-100).
    Penalty: States with active preemption laws are hard-capped at 40.
    Bonus: +5 for each proactive protection beyond baseline (max +15).
    """
    base = data.get("map_total_score", 0)
    if data.get("preemption_law"):
        base = min(base, 40.0)
    bills_penalty = min(data.get("bills_passed_against", 0) * 3, 15)
    return max(0.0, min(100.0, base - bills_penalty))


def score_safety(data: dict, all_states_data: list[dict]) -> float:
    """
    Inverted hate crime rate (per 100k), normalized across all states.
    Non-reporting agencies: penalize state score by 20 points × non-reporting rate.
    Returns 0-100 where 100 = lowest hate crime incidence.
    """
    rate = data.get("so_per_100k", 0) + data.get("gi_per_100k", 0)
    reporting_rate = data.get("reporting_rate", 1.0)
    # Penalty for non-reporting jurisdictions
    adjusted_rate = rate + (1 - reporting_rate) * 2.0
    all_rates = [
        (d.get("so_per_100k", 0) + d.get("gi_per_100k", 0))
        for d in all_states_data
    ]
    max_rate = max(all_rates) if all_rates else 1
    normalized = 1 - (adjusted_rate / max_rate)
    return round(max(0.0, min(100.0, normalized * 100)), 1)


def score_health(data: dict) -> float:
    """
    Equal-weighted composite of four sub-indicators (all inverted — lower = worse):
      - depression_pct (inverted)
      - healthcare_avoidance_pct (inverted)
      - uninsured_pct (inverted)
      - hiv_viral_suppression_pct (positive — higher is better, NOT inverted)
    """
    indicators = []
    if (v := data.get("depression_pct")) is not None:
        indicators.append(100 - min(v, 100))
    if (v := data.get("healthcare_avoidance_pct")) is not None:
        indicators.append(100 - min(v, 100))
    if (v := data.get("uninsured_pct")) is not None:
        indicators.append(100 - min(v * 5, 100))  # scale: 0-20% → 0-100
    if (v := data.get("hiv_viral_suppression_pct")) is not None:
        indicators.append(v)  # already 0-100, positive direction
    return round(np.mean(indicators), 1) if indicators else 50.0


def score_economic(data: dict) -> float:
    indicators = []
    if (v := data.get("lgbtq_poverty_pct")) is not None:
        indicators.append(100 - min(v * 4, 100))   # scale: 0-25% → 0-100
    if (v := data.get("income_gap_pct")) is not None:
        indicators.append(100 - min(abs(v) * 2, 100))
    if (v := data.get("housing_instability_pct")) is not None:
        indicators.append(100 - min(v * 4, 100))
    return round(np.mean(indicators), 1) if indicators else 50.0


def score_community(data: dict) -> float:
    indicators = []
    if (v := data.get("lgbtq_orgs_per_100k")) is not None:
        indicators.append(min(v * 20, 100))   # 5 orgs/100k = score of 100
    if (v := data.get("pride_events_count")) is not None:
        indicators.append(min(v * 10, 100))
    return round(np.mean(indicators), 1) if indicators else 50.0


def score_youth(data: dict) -> float:
    indicators = []
    if (v := data.get("suicidality_pct")) is not None:
        indicators.append(100 - min(v * 2.5, 100))
    if (v := data.get("school_safety_score")) is not None:
        indicators.append(v)
    if (v := data.get("gsa_presence_pct")) is not None:
        indicators.append(v)
    if (v := data.get("conversion_therapy_exposure_pct")) is not None:
        indicators.append(100 - min(v * 5, 100))
    return round(np.mean(indicators), 1) if indicators else 50.0
```

### atlas/scoring/composite.py

```python
WEIGHTS = {
    "legal":     0.30,
    "safety":    0.25,
    "community": 0.20,
    "health":    0.15,
    "youth":     0.10,
}

def compute_composite(dimension_scores: dict[str, float | None]) -> tuple[float, float]:
    """
    Returns (overall_score, confidence).
    Confidence is reduced when dimensions are missing.
    """
    available = {k: v for k, v in dimension_scores.items() if v is not None}
    missing = set(WEIGHTS.keys()) - set(available.keys())

    # Re-normalize weights for available dimensions
    total_weight = sum(WEIGHTS[k] for k in available)
    weighted_sum = sum(
        available[k] * (WEIGHTS[k] / total_weight)
        for k in available
    )

    # Confidence: starts at 1.0, loses 0.15 per missing high-weight dimension
    confidence = 1.0 - (len(missing) * 0.15)
    confidence = round(max(0.3, confidence), 2)

    return round(weighted_sum, 1), confidence
```

---

## Phase 3: Narrative Generator

### atlas/narrative/generator.py

```python
import anthropic
from atlas.config import settings

SYSTEM_PROMPT = """You are a data journalist writing concise, compassionate,
and accurate profiles of LGBTQ+ life in U.S. states for a public interactive atlas.
Your audience is LGBTQ+ adults considering where to live, travel, or advocate.
Tone: warm, direct, factual. Never editorialize beyond what the data shows.
Never use alarmist language. Acknowledge uncertainty when data is sparse.

Write exactly 3 paragraphs with NO headers:
1. Population and community overview (who lives here, community infrastructure)
2. Legal and safety climate (laws, hate crime context, political trend)
3. Health and economic picture (outcomes, disparities, access to care)

Each paragraph: 2-4 sentences. Output plain text only."""


def generate_state_narrative(state_name: str, profile_data: dict) -> str:
    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    user_content = f"""Write a profile for {state_name} using this data:

Population: {profile_data.get('population', {})}
Legal scores: {profile_data.get('legal', {})}
Safety data: {profile_data.get('safety', {})}
Health data: {profile_data.get('health', {})}
Economic data: {profile_data.get('economic', {})}
Community data: {profile_data.get('community', {})}
Overall score: {profile_data.get('overall_score')} / 100
Score trend: {profile_data.get('trend', [])}"""

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_content}]
    )
    return message.content[0].text.strip()
```

---

## Phase 4: FastAPI Backend

### atlas/api/models.py

```python
from pydantic import BaseModel

class DimensionScores(BaseModel):
    legal: float | None
    safety: float | None
    health: float | None
    economic: float | None
    community: float | None
    youth: float | None
    overall: float
    confidence: float

class PopulationData(BaseModel):
    lgbtq_count: int | None
    lgbtq_pct: float | None
    trans_count: int | None
    bipoc_pct: float | None
    urban_pct: float | None
    same_sex_households: int | None

class SocioeconomicData(BaseModel):
    median_individual_income_lgbtq: float | None
    median_hh_income_samesex_married: float | None
    median_hh_income_general: float | None
    income_gap_pct: float | None
    pct_bachelors_lgbtq: float | None
    pct_graduate_lgbtq: float | None
    pct_bachelors_nonlgbtq: float | None
    same_sex_married_count: int | None
    same_sex_cohabiting_count: int | None
    same_sex_marriage_rate: float | None

class TrendPoint(BaseModel):
    year: int
    overall: float

class CityPreview(BaseModel):
    city_id: str
    name: str
    mei_score: float | None
    mei_grade: str | None

class StateProfile(BaseModel):
    fips: str
    name: str
    abbr: str
    scores: DimensionScores
    population: PopulationData
    socioeconomic: SocioeconomicData
    trend: list[TrendPoint]
    narrative: str | None
    cities: list[CityPreview]
    legal_detail: dict
    safety_detail: dict
    health_detail: dict
    economic_detail: dict
    community_detail: dict
    youth_detail: dict

class StateMapItem(BaseModel):
    fips: str
    name: str
    abbr: str
    scores: DimensionScores
    year: int

class SearchResult(BaseModel):
    id: str
    name: str
    type: str   # "state" | "city"
    state_abbr: str | None
    score: float | None
```

### atlas/api/data\_store.py — In-Memory Flat File Loader

This module loads all processed CSVs/Excel files at startup and exposes them as Polars DataFrames. All routes query these in-memory frames — no I/O per request.

```python
import polars as pl
from pathlib import Path
from atlas.config import settings

class DataStore:
    """
    Loads all processed flat files at startup.
    All DataFrames are held in memory. At 50 states × 15 dimensions,
    total memory footprint is well under 100MB.
    """

    def __init__(self):
        p = settings.data_processed_dir

        # Core dimension tables
        self.population      = self._load_csv(p / "population" / "state_population.csv")
        self.policy          = self._load_csv(p / "legal" / "state_policy_scores.csv")
        self.mei             = self._load_csv(p / "legal" / "city_mei_scores.csv")
        self.hate_crimes     = self._load_csv(p / "safety" / "state_hate_crimes.csv")
        self.health          = self._load_csv(p / "health" / "state_health_outcomes.csv")
        self.economic        = self._load_csv(p / "economic" / "state_economic_profile.csv")
        self.income_edu      = self._load_csv(p / "socioeconomic" / "state_income_education.csv")
        self.marriage        = self._load_csv(p / "socioeconomic" / "state_marriage_households.csv")
        self.industry        = self._load_csv(p / "socioeconomic" / "state_industry_dist.csv")
        self.community       = self._load_csv(p / "community" / "state_community.csv")
        self.youth           = self._load_csv(p / "youth" / "state_youth.csv")
        self.scores          = self._load_csv(p / "scores" / "state_scores.csv")
        self.city_scores     = self._load_csv(p / "scores" / "city_scores.csv")
        self.fips_ref        = self._load_csv(p / "reference" / "state_fips.csv")

        # Occupation distribution is Excel (multi-sheet, one per state)
        self.occupation = self._load_occupation_excel(
            p / "socioeconomic" / "state_occupation_dist.xlsx"
        )

        # Narratives — plain text files, one per state
        self.narratives = self._load_narratives(p / "narratives")

    def _load_csv(self, path: Path) -> pl.DataFrame:
        if not path.exists():
            print(f"[DataStore] WARNING: {path} not found — returning empty DataFrame")
            return pl.DataFrame()
        return pl.read_csv(path, infer_schema_length=1000)

    def _load_occupation_excel(self, path: Path) -> dict[str, pl.DataFrame]:
        """Returns dict of state_abbr → DataFrame"""
        if not path.exists():
            return {}
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True)
        result = {}
        for sheet_name in wb.sheetnames:
            ws = wb[sheet_name]
            rows = list(ws.values)
            if len(rows) < 2:
                continue
            headers = [str(h) for h in rows[0]]
            data = [dict(zip(headers, row)) for row in rows[1:]]
            result[sheet_name] = pl.DataFrame(data)
        return result

    def _load_narratives(self, path: Path) -> dict[str, str]:
        """Returns dict of state_fips → narrative text"""
        if not path.exists():
            return {}
        return {
            f.stem: f.read_text()
            for f in path.glob("*.txt")
        }

    def state_scores_for_year(self, year: int) -> pl.DataFrame:
        return self.scores.filter(pl.col("year") == year)

    def state_profile_data(self, fips: str, year: int) -> dict:
        """Assembles all dimension data for a single state and year."""
        def row(df: pl.DataFrame) -> dict:
            if df.is_empty():
                return {}
            filtered = df.filter(
                (pl.col("state_fips") == fips) & (pl.col("year") == year)
            )
            return filtered.row(0, named=True) if len(filtered) > 0 else {}

        return {
            "population":  row(self.population),
            "policy":      row(self.policy),
            "hate_crimes": row(self.hate_crimes),
            "health":      row(self.health),
            "economic":    row(self.economic),
            "income_edu":  row(self.income_edu),
            "marriage":    row(self.marriage),
            "community":   row(self.community),
            "youth":       row(self.youth),
            "scores":      row(self.scores),
            "occupation":  self.occupation.get(
                self.fips_ref.filter(pl.col("state_fips") == fips)
                    .select("state_abbr").row(0)[0], pl.DataFrame()
            ),
            "narrative":   self.narratives.get(fips, None),
        }


# Singleton — instantiated once at app startup
store = DataStore()
```

### atlas/api/routes/states.py

```python
from fastapi import APIRouter, HTTPException
from atlas.api.models import StateProfile, StateMapItem
from atlas.api.data_store import store

router = APIRouter(prefix="/states", tags=["states"])

@router.get("/", response_model=list[StateMapItem])
async def list_states(year: int = 2024):
    scores_df = store.state_scores_for_year(year)
    fips_df = store.fips_ref

    joined = scores_df.join(fips_df, on="state_fips", how="left")
    return [_row_to_map_item(r) for r in joined.iter_rows(named=True)]

@router.get("/{fips}", response_model=StateProfile)
async def get_state(fips: str, year: int = 2024):
    data = store.state_profile_data(fips, year)
    if not data.get("scores"):
        raise HTTPException(status_code=404, detail=f"State {fips} not found")

    fips_row = store.fips_ref.filter(pl.col("state_fips") == fips)
    if fips_row.is_empty():
        raise HTTPException(status_code=404, detail=f"FIPS {fips} not in reference table")

    meta = fips_row.row(0, named=True)

    # Trend: pull all years for this state
    trend = (
        store.scores
        .filter(pl.col("state_fips") == fips)
        .select(["year", "overall_score"])
        .sort("year")
        .iter_rows(named=True)
    )

    # Top cities by MEI
    cities = (
        store.mei
        .filter((pl.col("state_fips") == fips) & (pl.col("year") == year))
        .sort("mei_score", descending=True)
        .head(5)
        .iter_rows(named=True)
    )

    return _assemble_state_profile(meta, data, list(trend), list(cities))

def _row_to_map_item(r: dict) -> StateMapItem:
    from atlas.api.models import DimensionScores
    return StateMapItem(
        fips=r["state_fips"],
        name=r["state_name"],
        abbr=r["state_abbr"],
        year=r.get("year", 2024),
        scores=DimensionScores(
            legal=r.get("legal_score"),
            safety=r.get("safety_score"),
            health=r.get("health_score"),
            economic=r.get("economic_score"),
            community=r.get("community_score"),
            youth=r.get("youth_score"),
            overall=r.get("overall_score", 0),
            confidence=r.get("confidence", 1.0),
        )
    )
```

### atlas/api/main.py

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from atlas.api.routes import states, cities, map as map_routes, search
from atlas.api.data_store import store   # triggers load at import time

app = FastAPI(
    title="LGBTQ+ Atlas API",
    description="Data API for the LGBTQ+ Atlas platform",
    version="1.0.0",
    on_startup=[lambda: print(f"DataStore loaded. States: {len(store.fips_ref)} rows.")]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://lgbtqatlas.org"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(states.router, prefix="/api")
app.include_router(cities.router, prefix="/api")
app.include_router(map_routes.router, prefix="/api")
app.include_router(search.router, prefix="/api")

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "states_loaded": len(store.fips_ref),
        "scores_rows": len(store.scores),
    }
```

---

## Phase 5: Frontend

### Design System

**Aesthetic:** Editorial cartography — dark base map, jewel-tone choropleth, serif display
font paired with humanist sans. The map is the hero; UI chrome recedes.

**Color tokens (globals.css):**
```css
:root {
  --bg:           #0F1117;
  --surface:      #1A1D27;
  --surface-alt:  #222636;
  --border:       #2A2D3A;
  --text-primary: #F2F4F8;
  --text-secondary: #9BA3B8;
  --text-muted:   #5A6070;

  /* Dimension colors */
  --legal:    #8B5CF6;
  --safety:   #EF4444;
  --health:   #10B981;
  --economic: #F59E0B;
  --community:#3B82F6;
  --youth:    #14B8A6;

  /* Score ramp */
  --score-low:     #C0392B;
  --score-mid-low: #E67E22;
  --score-mid:     #F1C40F;
  --score-high:    #27AE60;
  --score-top:     #1ABC9C;

  /* Typography */
  --font-display: 'DM Serif Display', serif;
  --font-body:    'Outfit', sans-serif;
  --font-mono:    'JetBrains Mono', monospace;
}
```

**Load fonts in index.html:**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Outfit:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

### Zustand Store (src/store/atlasStore.ts)

```typescript
import { create } from 'zustand'

type DimensionKey = 'overall' | 'legal' | 'safety' | 'health' | 'economic' | 'community' | 'youth'

interface AtlasStore {
  activeLayer: DimensionKey
  selectedStateFips: string | null
  selectedCityId: string | null
  compareMode: boolean
  compareStates: [string | null, string | null]
  hoveredFips: string | null

  setActiveLayer: (layer: DimensionKey) => void
  selectState: (fips: string | null) => void
  selectCity: (cityId: string | null) => void
  setHovered: (fips: string | null) => void
  toggleCompare: () => void
  setCompareState: (index: 0 | 1, fips: string | null) => void
}

export const useAtlasStore = create<AtlasStore>((set) => ({
  activeLayer: 'overall',
  selectedStateFips: null,
  selectedCityId: null,
  compareMode: false,
  compareStates: [null, null],
  hoveredFips: null,

  setActiveLayer: (layer) => set({ activeLayer: layer }),
  selectState: (fips) => set({ selectedStateFips: fips, selectedCityId: null }),
  selectCity: (cityId) => set({ selectedCityId: cityId }),
  setHovered: (fips) => set({ hoveredFips: fips }),
  toggleCompare: () => set((s) => ({ compareMode: !s.compareMode })),
  setCompareState: (index, fips) =>
    set((s) => {
      const next = [...s.compareStates] as [string | null, string | null]
      next[index] = fips
      return { compareStates: next }
    }),
}))
```

### Score Color Utility (src/utils/colorScales.ts)

```typescript
import * as d3 from 'd3'

export const scoreColor = d3.scaleThreshold<number, string>()
  .domain([30, 50, 70, 85])
  .range(['#C0392B', '#E67E22', '#F1C40F', '#27AE60', '#1ABC9C'])

export const scoreLabel = (score: number): string => {
  if (score >= 85) return 'Excellent'
  if (score >= 70) return 'Good'
  if (score >= 50) return 'Fair'
  if (score >= 30) return 'Poor'
  return 'Critical'
}

export const DIMENSION_META = {
  overall:   { label: 'Overall',   color: '#F2F4F8', weight: null },
  legal:     { label: 'Legal',     color: '#8B5CF6', weight: '30%' },
  safety:    { label: 'Safety',    color: '#EF4444', weight: '25%' },
  community: { label: 'Community', color: '#3B82F6', weight: '20%' },
  health:    { label: 'Health',    color: '#10B981', weight: '15%' },
  youth:     { label: 'Youth',     color: '#14B8A6', weight: '10%' },
} as const
```

### AtlasMap.tsx

```tsx
import { useEffect, useRef } from 'react'
import maplibregl from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'
import { useAtlasStore } from '@/store/atlasStore'
import { scoreColor } from '@/utils/colorScales'
import { useQuery } from '@tanstack/react-query'
import { fetchMapData } from '@/api/atlas'

export default function AtlasMap() {
  const mapRef = useRef<maplibregl.Map | null>(null)
  const containerRef = useRef<HTMLDivElement>(null)
  const { activeLayer, selectState, setHovered } = useAtlasStore()

  const { data: mapData } = useQuery({
    queryKey: ['map', activeLayer],
    queryFn: () => fetchMapData(activeLayer),
  })

  useEffect(() => {
    if (!containerRef.current) return
    mapRef.current = new maplibregl.Map({
      container: containerRef.current,
      style: 'https://tiles.stadiamaps.com/styles/alidade_smooth_dark.json',
      center: [-96, 38],
      zoom: 3.8,
      minZoom: 2,
      maxZoom: 10,
    })

    const map = mapRef.current
    map.on('load', () => {
      map.addSource('states', {
        type: 'geojson',
        data: '/data/exports/states.geojson',
      })
      map.addLayer({
        id: 'states-fill',
        type: 'fill',
        source: 'states',
        paint: {
          'fill-color': '#1A1D27',
          'fill-opacity': 0.9,
        },
      })
      map.addLayer({
        id: 'states-border',
        type: 'line',
        source: 'states',
        paint: {
          'line-color': '#2A2D3A',
          'line-width': 1,
        },
      })
      map.on('mousemove', 'states-fill', (e) => {
        const fips = e.features?.[0]?.properties?.fips
        if (fips) setHovered(fips)
        map.getCanvas().style.cursor = 'pointer'
      })
      map.on('mouseleave', 'states-fill', () => {
        setHovered(null)
        map.getCanvas().style.cursor = ''
      })
      map.on('click', 'states-fill', (e) => {
        const fips = e.features?.[0]?.properties?.fips
        if (fips) selectState(fips)
      })
    })
    return () => map.remove()
  }, [])

  // Update fill colors when layer or data changes
  useEffect(() => {
    if (!mapRef.current || !mapData) return
    const map = mapRef.current
    if (!map.getLayer('states-fill')) return

    const colorExpression: maplibregl.ExpressionSpecification = [
      'match',
      ['get', 'fips'],
      ...mapData.flatMap((s: any) => [s.fips, scoreColor(s.scores[activeLayer] ?? 0)]),
      '#1A1D27',
    ]
    map.setPaintProperty('states-fill', 'fill-color', colorExpression)
  }, [activeLayer, mapData])

  return <div ref={containerRef} className="w-full h-full" />
}
```

### StateProfileDrawer.tsx

```tsx
import { motion, AnimatePresence } from 'framer-motion'
import { useAtlasStore } from '@/store/atlasStore'
import { useStateProfile } from '@/hooks/useStateProfile'
import DimensionBar from './DimensionBar'
import TrendSparkline from './TrendSparkline'
import PopulationPanel from './PopulationPanel'
import NarrativeSummary from './NarrativeSummary'
import CityRankings from './CityRankings'
import { scoreColor, scoreLabel, DIMENSION_META } from '@/utils/colorScales'
import { X } from 'lucide-react'

export default function StateProfileDrawer() {
  const { selectedStateFips, selectState } = useAtlasStore()
  const { data: profile, isLoading } = useStateProfile(selectedStateFips)

  return (
    <AnimatePresence>
      {selectedStateFips && (
        <motion.aside
          initial={{ x: '100%', opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          exit={{ x: '100%', opacity: 0 }}
          transition={{ type: 'spring', damping: 30, stiffness: 300 }}
          className="absolute right-0 top-0 h-full w-[440px] bg-surface border-l border-border
                     overflow-y-auto z-10 shadow-2xl"
        >
          {isLoading ? (
            <DrawerSkeleton />
          ) : profile ? (
            <div className="p-6 space-y-6">
              {/* Header */}
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-xs text-text-muted uppercase tracking-widest mb-1">
                    LGBTQ+ Atlas
                  </p>
                  <h1 className="font-display text-3xl text-text-primary">
                    {profile.name}
                  </h1>
                  <div className="flex items-center gap-2 mt-2">
                    <span
                      className="text-2xl font-mono font-bold"
                      style={{ color: scoreColor(profile.scores.overall) }}
                    >
                      {profile.scores.overall}
                    </span>
                    <span className="text-sm text-text-secondary">
                      {scoreLabel(profile.scores.overall)}
                    </span>
                    <span className="text-xs text-text-muted">
                      ({Math.round(profile.scores.confidence * 100)}% confidence)
                    </span>
                  </div>
                </div>
                <button
                  onClick={() => selectState(null)}
                  className="text-text-muted hover:text-text-primary transition-colors p-1"
                >
                  <X size={20} />
                </button>
              </div>

              {/* Narrative */}
              {profile.narrative && (
                <NarrativeSummary text={profile.narrative} />
              )}

              {/* Dimension Bars */}
              <section>
                <h2 className="text-xs uppercase tracking-widest text-text-muted mb-3">
                  Dimensions
                </h2>
                <div className="space-y-2">
                  {(Object.keys(DIMENSION_META) as Array<keyof typeof DIMENSION_META>)
                    .filter(k => k !== 'overall')
                    .map(dim => (
                      <DimensionBar
                        key={dim}
                        label={DIMENSION_META[dim].label}
                        score={profile.scores[dim] ?? null}
                        color={DIMENSION_META[dim].color}
                        weight={DIMENSION_META[dim].weight}
                      />
                    ))
                  }
                </div>
              </section>

              {/* Population */}
              <PopulationPanel data={profile.population} />

              {/* Trend */}
              <section>
                <h2 className="text-xs uppercase tracking-widest text-text-muted mb-3">
                  Score Trend
                </h2>
                <TrendSparkline data={profile.trend} />
              </section>

              {/* Cities */}
              {profile.cities.length > 0 && (
                <CityRankings cities={profile.cities} stateName={profile.name} />
              )}

              {/* Footer */}
              <div className="pt-4 border-t border-border">
                <p className="text-xs text-text-muted">
                  Data from Williams Institute, MAP, HRC, FBI, CDC, Trevor Project.{' '}
                  <a href="/methodology" className="underline hover:text-text-secondary">
                    Full methodology
                  </a>
                </p>
              </div>
            </div>
          ) : null}
        </motion.aside>
      )}
    </AnimatePresence>
  )
}
```

### DimensionBar.tsx

```tsx
import { scoreColor } from '@/utils/colorScales'

interface Props {
  label: string
  score: number | null
  color: string
  weight: string | null
}

export default function DimensionBar({ label, score, color, weight }: Props) {
  return (
    <div className="flex items-center gap-3 group">
      <div className="w-1.5 h-1.5 rounded-full flex-shrink-0" style={{ background: color }} />
      <span className="text-sm text-text-secondary w-24 flex-shrink-0">{label}</span>
      <div className="flex-1 bg-[#0F1117] rounded-full h-1.5 overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-700 ease-out"
          style={{
            width: score !== null ? `${score}%` : '0%',
            background: score !== null ? scoreColor(score) : '#2A2D3A'
          }}
        />
      </div>
      <span className="text-sm font-mono w-8 text-right text-text-primary">
        {score !== null ? Math.round(score) : '—'}
      </span>
      {weight && (
        <span className="text-xs text-text-muted w-8 opacity-0 group-hover:opacity-100 transition-opacity">
          {weight}
        </span>
      )}
    </div>
  )
}
```

### LayerSwitcher.tsx

```tsx
import { useAtlasStore } from '@/store/atlasStore'
import { DIMENSION_META } from '@/utils/colorScales'

export default function LayerSwitcher() {
  const { activeLayer, setActiveLayer } = useAtlasStore()

  return (
    <div className="absolute top-4 left-4 z-10 bg-surface border border-border
                    rounded-lg overflow-hidden shadow-xl">
      <div className="px-3 py-2 border-b border-border">
        <p className="text-xs text-text-muted uppercase tracking-widest">Map Layer</p>
      </div>
      {(Object.entries(DIMENSION_META) as [string, any][]).map(([key, meta]) => (
        <button
          key={key}
          onClick={() => setActiveLayer(key as any)}
          className={`w-full flex items-center gap-3 px-4 py-2.5 text-sm transition-colors
                      hover:bg-surface-alt text-left
                      ${activeLayer === key ? 'bg-surface-alt' : ''}`}
        >
          <div
            className="w-0.5 h-4 rounded-full flex-shrink-0 transition-opacity"
            style={{
              background: meta.color,
              opacity: activeLayer === key ? 1 : 0.3
            }}
          />
          <span className={activeLayer === key ? 'text-text-primary' : 'text-text-secondary'}>
            {meta.label}
          </span>
          {meta.weight && (
            <span className="ml-auto text-xs text-text-muted">{meta.weight}</span>
          )}
        </button>
      ))}
    </div>
  )
}
```

### App.tsx

```tsx
import AtlasMap from '@/components/map/AtlasMap'
import StateProfileDrawer from '@/components/profile/StateProfileDrawer'
import LayerSwitcher from '@/components/nav/LayerSwitcher'
import Header from '@/components/nav/Header'
import SearchBar from '@/components/nav/SearchBar'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

const queryClient = new QueryClient()

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="w-screen h-screen bg-bg relative overflow-hidden"
           style={{ fontFamily: 'var(--font-body)' }}>
        <Header />
        <div className="absolute inset-0">
          <AtlasMap />
        </div>
        <LayerSwitcher />
        <SearchBar />
        <StateProfileDrawer />
      </div>
    </QueryClientProvider>
  )
}
```

---

## Phase 6: Static Export Pipeline

For performance and cost, pre-generate all state and city JSON files at build time.

### atlas/export/build.py

```python
import json
import duckdb
from pathlib import Path
from atlas.config import settings
from atlas.api.models import StateProfile
from atlas.narrative.generator import generate_state_narrative

def build_exports(year: int = 2024) -> None:
    """
    Pre-generate all static JSON exports for the frontend.
    Runs as part of the annual data refresh pipeline.
    """
    exports_dir = settings.data_exports_dir
    exports_dir.mkdir(parents=True, exist_ok=True)
    (exports_dir / "state_profiles").mkdir(exist_ok=True)
    (exports_dir / "city_profiles").mkdir(exist_ok=True)

    con = duckdb.connect(str(settings.duckdb_path), read_only=True)

    states = con.execute("SELECT state_fips, state_name FROM ref_states ORDER BY state_name").fetchall()

    all_map_data = []

    for fips, name in states:
        print(f"Exporting {name}...")
        profile = _build_state_profile(con, fips, name, year)

        # Write per-state file
        out_path = exports_dir / "state_profiles" / f"{fips}.json"
        out_path.write_text(json.dumps(profile, indent=2))

        # Append to map index (stripped-down)
        all_map_data.append({
            "fips": fips,
            "name": name,
            "abbr": profile["abbr"],
            "scores": profile["scores"],
            "year": year,
        })

    # Write map index
    (exports_dir / "states_map.json").write_text(json.dumps(all_map_data, indent=2))
    print("Export complete.")
```

---

## Phase 7: CLI Pipeline Runner

### pipeline/cli.py

```python
import typer
import asyncio

app = typer.Typer(help="LGBTQ+ Atlas data pipeline")

@app.command()
def ingest(source: str = typer.Argument("all", help="Source name or 'all'")):
    """Fetch and parse raw data from all sources"""
    asyncio.run(_run_ingest(source))

@app.command()
def transform():
    """Clean, normalize, and load data into DuckDB"""
    from atlas.transform.normalize import run_all_transforms
    run_all_transforms()

@app.command()
def score(year: int = 2024):
    """Compute composite scores for all states"""
    from atlas.scoring.composite import score_all_states
    score_all_states(year)

@app.command()
def narratives(year: int = 2024):
    """Generate LLM narratives for all states via Claude API"""
    from atlas.narrative.generator import generate_all_narratives
    generate_all_narratives(year)

@app.command()
def build(year: int = 2024):
    """Export all static JSON files for the frontend"""
    from atlas.export.build import build_exports
    build_exports(year)

@app.command()
def serve(port: int = 8000, reload: bool = True):
    """Start the FastAPI development server"""
    import uvicorn
    uvicorn.run("atlas.api.main:app", host="0.0.0.0", port=port, reload=reload)

@app.command()
def pipeline(year: int = 2024):
    """Run the full pipeline end-to-end: ingest → transform → score → narratives → build"""
    ingest("all")
    transform()
    score(year)
    narratives(year)
    build(year)

if __name__ == "__main__":
    app()
```

---

## GitHub Actions: Annual Refresh

### .github/workflows/data-refresh.yml

```yaml
name: Annual Data Refresh

on:
  schedule:
    - cron: '0 9 1 2 *'   # February 1st annually (after most sources publish)
  workflow_dispatch:        # Allow manual trigger

jobs:
  refresh:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv sync
      - run: uv run atlas pipeline
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
      - name: Commit updated exports
        run: |
          git config user.name "atlas-bot"
          git config user.email "atlas@lgbtqatlas.org"
          git add data/exports/
          git commit -m "chore: annual data refresh $(date +%Y)"
          git push
```

---

## Environment Variables (.env.example)

```bash
# Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# Optional API keys for live data fetching
FBI_API_KEY=                # FBI Crime Data Explorer API key
CENSUS_API_KEY=             # Census Bureau API key

# Frontend
VITE_API_BASE_URL=http://localhost:8000

# Deployment
RAILWAY_PROJECT_ID=
VERCEL_PROJECT_ID=
```

---

## Build Order Summary

Execute phases in this exact order:

1. `uv init` + `npm create vite` — scaffold both projects
2. Implement `config.py`, `base.py`, DuckDB schema
3. Implement ingestion modules (start with `williams_institute.py` and `map_policy.py`)
4. Build transform layer — normalize each source into DuckDB tables
5. Implement scoring engine — dimensions first, then composite
6. Implement narrative generator — test with one state before running all 50
7. Build FastAPI routes — start with `GET /api/states` and `GET /api/states/{fips}`
8. Implement static export pipeline
9. Build frontend: `App.tsx` → `AtlasMap.tsx` → `LayerSwitcher.tsx` → `StateProfileDrawer.tsx`
10. Wire up `useStateProfile` hook + TanStack Query
11. Polish: animations, mobile responsiveness, share card generation
12. Set up GitHub Actions workflow

---

## Data Directory Note

The `data/raw/` directory is pre-populated by the Claude Cowork data gathering pipeline. The `data/processed/` directory is produced by running `atlas transform`. Assume the following processed files exist when building routes and the export pipeline:

```
data/processed/
├── population/state_population.csv
├── legal/state_policy_scores.csv
├── legal/city_mei_scores.csv
├── safety/state_hate_crimes.csv
├── health/state_health_outcomes.csv
├── economic/state_economic_profile.csv
├── socioeconomic/state_income_education.csv
├── socioeconomic/state_marriage_households.csv
├── socioeconomic/state_industry_dist.csv
├── socioeconomic/state_occupation_dist.xlsx  ← multi-sheet Excel, one tab per state abbr
├── community/state_community.csv
├── youth/state_youth.csv
├── scores/state_scores.csv
├── scores/city_scores.csv
├── narratives/[fips].txt                     ← one text file per state
└── reference/
    ├── state_fips.csv
    └── occupation_codes.csv
```

If any file is missing, `DataStore._load_csv()` returns an empty DataFrame and logs a warning. The scoring engine handles missing dimensions via the confidence penalty — the API will still return results, just with lower confidence values and null dimension scores.
