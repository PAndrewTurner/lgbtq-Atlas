import polars as pl
from fastapi import APIRouter, HTTPException
from atlas.api.models import StateProfile, StateMapItem, DimensionScores, PopulationData, SocioeconomicData, TrendPoint, CityPreview
from atlas.api.data_store import store

router = APIRouter(prefix="/states", tags=["states"])


def _fips_str(fips) -> str:
    return str(int(fips)).zfill(2)


def _scores_from_row(r: dict) -> DimensionScores:
    return DimensionScores(
        legal=r.get("legal_score"),
        safety=r.get("safety_score"),
        health=r.get("health_score"),
        economic=r.get("economic_score"),
        community=r.get("community_score"),
        youth=r.get("youth_score"),
        overall=r.get("overall_score") or 0.0,
        confidence=r.get("confidence") or 1.0,
    )


@router.get("/", response_model=list[StateMapItem])
async def list_states(year: int = 2024):
    scores_df = store.state_scores_for_year(year)
    if scores_df.is_empty():
        return []
    joined = scores_df.join(store.fips_ref, on="state_fips", how="left")
    return [
        StateMapItem(
            fips=_fips_str(r["state_fips"]),
            name=r.get("state_name") or "",
            abbr=r.get("state_abbr") or "",
            year=r.get("year") or year,
            scores=_scores_from_row(r),
        )
        for r in joined.iter_rows(named=True)
    ]


@router.get("/{fips}", response_model=StateProfile)
async def get_state(fips: str, year: int = 2024):
    fips_padded = fips.zfill(2)

    fips_row = store.fips_ref.filter(
        pl.col("state_fips").cast(pl.Utf8).str.zfill(2) == fips_padded
    )
    if fips_row.is_empty():
        raise HTTPException(status_code=404, detail=f"FIPS {fips} not found")

    meta = fips_row.row(0, named=True)
    data = store.state_profile_data(fips_padded, year)

    if not data.get("scores"):
        raise HTTPException(status_code=404, detail=f"No scores for state {fips}")

    # Trend across all years
    trend = []
    if not store.scores.is_empty():
        trend_df = (
            store.scores
            .filter(pl.col("state_fips").cast(pl.Utf8).str.zfill(2) == fips_padded)
            .select(["year", "overall_score"])
            .sort("year")
        )
        trend = [
            TrendPoint(year=r["year"], overall=r["overall_score"])
            for r in trend_df.iter_rows(named=True)
        ]

    # Top 5 cities by MEI score
    cities = []
    if not store.mei.is_empty():
        state_fips_int = int(fips_padded)
        mei_rows = (
            store.mei
            .filter(pl.col("state_fips") == state_fips_int)
            .sort("mei_score", descending=True)
            .head(5)
        )
        cities = [
            CityPreview(
                city_id=r.get("city_id") or "",
                name=r.get("city_name") or "",
                mei_score=r.get("mei_score"),
                mei_grade=r.get("mei_grade"),
            )
            for r in mei_rows.iter_rows(named=True)
        ]

    scores_row = data.get("scores") or {}
    pop = data.get("population") or {}
    soc = data.get("marriage") or {}
    edu = data.get("income_edu") or {}
    econ = data.get("economic") or {}

    return StateProfile(
        fips=fips_padded,
        name=meta.get("state_name") or "",
        abbr=meta.get("state_abbr") or "",
        scores=_scores_from_row(scores_row),
        population=PopulationData(
            lgbtq_count=pop.get("lgbtq_pop"),
            lgbtq_pct=pop.get("lgbtq_pct"),
            trans_count=None,
            bipoc_pct=None,
            urban_pct=None,
            same_sex_households=pop.get("same_sex_hh"),
        ),
        socioeconomic=SocioeconomicData(
            median_individual_income_lgbtq=edu.get("median_individual_income_lgbtq"),
            median_hh_income_samesex_married=edu.get("median_hh_income_samesex_married"),
            median_hh_income_general=edu.get("median_hh_income_general_population"),
            income_gap_pct=econ.get("income_gap_pct"),
            pct_bachelors_lgbtq=edu.get("pct_bachelors_lgbtq"),
            pct_graduate_lgbtq=edu.get("pct_graduate_lgbtq"),
            pct_bachelors_nonlgbtq=edu.get("pct_bachelors_nonlgbtq"),
            same_sex_married_count=soc.get("same_sex_married_count"),
            same_sex_cohabiting_count=soc.get("same_sex_cohabiting_count"),
            same_sex_marriage_rate=soc.get("same_sex_marriage_rate"),
        ),
        trend=trend,
        narrative=data.get("narrative"),
        cities=cities,
        legal_detail=data.get("policy") or {},
        safety_detail=data.get("hate_crimes") or {},
        health_detail=data.get("health") or {},
        economic_detail=econ,
        community_detail=data.get("community") or {},
        youth_detail=data.get("youth") or {},
    )
