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
