import math
import numpy as np


def score_legal(data: dict) -> float:
    """
    Base: HRC SEI numerical score (stored as map_total_score, already 0-100).
    Penalty: States with active preemption laws are hard-capped at 40.
    Bills penalty: anti-trans bills introduced (proxy for active hostility).
    """
    base = data.get("map_total_score") or 0.0
    if data.get("preemption_law"):
        base = min(base, 40.0)
    bills_penalty = min((data.get("bills_passed_against") or 0) * 1.5, 20)
    return max(0.0, min(100.0, base - bills_penalty))


def score_safety(data: dict, all_states_data: list[dict]) -> float:
    """
    Hate crime rate (per 100k LGBTQ+ adults) scored on an exponential decay curve.

    Why exponential instead of max-normalization:
    - Max normalization forces the highest-reporting state (DC, NJ) to 0.0, which
      conflates active hate crime prosecution/reporting with being "unsafe".
    - Exponential decay gives each state an absolute score based on its rate,
      so DC/NJ score low (high confirmed incidents) but not zero.

    States with 0 reported incidents are capped at 72 — zero may reflect
    underreporting rather than genuine safety (e.g. Mississippi).

    Scale constant k=28: a state with ~28 incidents/100k scores ~37 (Mixed).
    Observed range: 0 (MS) → 65 (DC).
    """
    rate = (data.get("so_per_100k") or 0.0) + (data.get("gi_per_100k") or 0.0)

    # Exponential decay: 100 at rate=0, ~37 at rate=28, ~11 at rate=65
    score = 100.0 * math.exp(-rate / 28.0)

    # States with zero LGBTQ-specific incidents are suspicious for underreporting;
    # cap them so they can't appear safer than states with moderate but honest reporting.
    total_incidents = (data.get("so_incidents") or 0) + (data.get("gi_incidents") or 0)
    if total_incidents == 0:
        score = min(score, 72.0)

    return round(max(0.0, min(100.0, score)), 1)


def score_health(data: dict) -> float:
    """
    Composite of available health indicators (all inverted — lower % = worse outcome).
    depression_pct: % considering suicide (Trevor Project)
    healthcare_avoidance_pct: % who wanted but couldn't access care
    hiv_viral_suppression_pct: % with high family support (positive direction)
    """
    indicators = []
    if (v := data.get("depression_pct")) is not None:
        # suicidality range ~10-60%; scale to 0-100 inverted
        indicators.append(100 - min(v * 2.0, 100))
    if (v := data.get("healthcare_avoidance_pct")) is not None:
        indicators.append(100 - min(v, 100))
    if (v := data.get("uninsured_pct")) is not None:
        indicators.append(100 - min(v * 5, 100))
    if (v := data.get("hiv_viral_suppression_pct")) is not None:
        indicators.append(v)
    return round(float(np.mean(indicators)), 1) if indicators else 50.0


def score_economic(data: dict) -> float:
    indicators = []
    if (v := data.get("lgbtq_poverty_pct")) is not None:
        indicators.append(100 - min(v * 4, 100))
    if (v := data.get("income_gap_pct")) is not None:
        indicators.append(100 - min(abs(v) * 2, 100))
    if (v := data.get("housing_instability_pct")) is not None:
        indicators.append(100 - min(v * 4, 100))
    return round(float(np.mean(indicators)), 1) if indicators else 50.0


def score_community(data: dict, all_states_data: list[dict] | None = None) -> float:
    """
    Hybrid community score:
      60% — percentile rank of orgs_per_100k (relative density)
      40% — percentile rank of log(absolute org count) (absolute presence)

    Pure per-100k penalises large, dense states (NJ has 95 orgs but ~26/100k
    because its LGBTQ+ population is huge). The absolute-count component
    rewards states with many organisations regardless of density.
    """
    indicators = []

    per_100k = data.get("lgbtq_orgs_per_100k")
    abs_count = data.get("lgbtq_orgs_count") or 0

    if per_100k is not None and all_states_data:
        all_per_100k = [d.get("lgbtq_orgs_per_100k") or 0 for d in all_states_data]
        pct_density = sum(1 for x in all_per_100k if x <= per_100k) / len(all_per_100k)

        all_counts = [d.get("lgbtq_orgs_count") or 0 for d in all_states_data]
        log_count = math.log1p(abs_count)
        all_log = [math.log1p(c) for c in all_counts]
        pct_abs = sum(1 for x in all_log if x <= log_count) / len(all_log)

        # Weighted blend: density 60%, absolute 40%
        blended = 0.60 * pct_density + 0.40 * pct_abs
        indicators.append(round(blended * 100, 1))

    elif per_100k is not None:
        # Fallback without cross-state data
        indicators.append(min(per_100k / 60 * 100, 100))

    if (v := data.get("pride_events_count")) is not None and v > 0:
        indicators.append(min(v * 10, 100))

    return round(float(np.mean(indicators)), 1) if indicators else 50.0


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
    return round(float(np.mean(indicators)), 1) if indicators else 50.0
