"""
Composite scoring engine.
Reads all processed dimension files, computes dimension scores, writes:
  processed/scores/state_scores.csv
"""
from pathlib import Path
import polars as pl

WEIGHTS = {
    "legal":     0.30,
    "safety":    0.20,
    "community": 0.15,
    "health":    0.15,
    "economic":  0.10,
    "youth":     0.10,
}


def compute_composite(dimension_scores: dict[str, float | None]) -> tuple[float, float]:
    available = {k: v for k, v in dimension_scores.items() if v is not None}
    missing = set(WEIGHTS.keys()) - set(available.keys())
    total_weight = sum(WEIGHTS[k] for k in available)
    weighted_sum = sum(
        available[k] * (WEIGHTS[k] / total_weight)
        for k in available
    ) if total_weight > 0 else 50.0
    confidence = max(0.3, round(1.0 - len(missing) * 0.15, 2))
    return round(weighted_sum, 1), confidence


def score_all_states(year: int = 2024) -> pl.DataFrame:
    from atlas.config import settings
    from atlas.scoring.dimensions import (
        score_legal, score_safety, score_health,
        score_economic, score_community, score_youth,
    )

    proc = settings.data_processed_dir

    def load(path: str) -> pl.DataFrame:
        p = proc / path
        if not p.exists():
            return pl.DataFrame()
        df = pl.read_csv(p)
        if "year" in df.columns:
            df = df.filter(pl.col("year") == year)
        return df

    fips = pl.read_csv(proc / "reference" / "state_fips.csv")
    legal_df  = load("legal/state_policy_scores.csv")
    safety_df = load("safety/state_hate_crimes.csv")
    health_df = load("health/state_health_outcomes.csv")
    econ_df   = load("economic/state_economic_profile.csv")
    comm_df   = load("community/state_community.csv")
    youth_df  = load("youth/state_youth.csv")

    def row(df: pl.DataFrame, fips_code: str) -> dict:
        if df.is_empty() or "state_fips" not in df.columns:
            return {}
        f = df.filter(pl.col("state_fips") == fips_code)
        return f.row(0, named=True) if len(f) > 0 else {}

    # Pre-build all-states lists for cross-state normalization
    all_fips = fips["state_fips"].to_list()
    all_safety = [row(safety_df, f) for f in all_fips]
    all_community = [row(comm_df, f) for f in all_fips]

    records = []
    for fips_code in all_fips:
        l = row(legal_df, fips_code)
        s = row(safety_df, fips_code)
        h = row(health_df, fips_code)
        e = row(econ_df, fips_code)
        c = row(comm_df, fips_code)
        y = row(youth_df, fips_code)

        legal_score   = score_legal(l) if l else None
        safety_score  = score_safety(s, all_safety) if s else None
        health_score  = score_health(h) if h else None
        econ_score    = score_economic(e) if e else None
        comm_score    = score_community(c, all_community) if c else None
        youth_score   = score_youth(y) if y else None

        overall, confidence = compute_composite({
            "legal": legal_score, "safety": safety_score,
            "health": health_score, "economic": econ_score,
            "community": comm_score, "youth": youth_score,
        })

        records.append({
            "state_fips": fips_code,
            "year": year,
            "legal_score":     legal_score,
            "safety_score":    safety_score,
            "health_score":    health_score,
            "economic_score":  econ_score,
            "community_score": comm_score,
            "youth_score":     youth_score,
            "overall_score":   overall,
            "confidence":      confidence,
        })

    df = pl.DataFrame(records)
    out = proc / "scores" / "state_scores.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.write_csv(out)
    print(f"  state_scores.csv → {len(df)} rows")
    return df


if __name__ == "__main__":
    score_all_states()
