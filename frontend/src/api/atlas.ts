import type { StateSummary, StateProfile, CityScore } from '../types/profile'

const API_BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api'

async function getApi<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`)
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`)
  return res.json()
}

async function getStatic<T>(path: string): Promise<T> {
  const res = await fetch(path)
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`)
  return res.json()
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function adaptSummary(raw: any): StateSummary {
  return {
    fips: String(raw.fips).padStart(2, '0'),
    name: raw.name,
    abbr: raw.abbr,
    year: raw.year,
    composite_score: raw.scores?.overall ?? raw.composite_score ?? 0,
    dimensions: {
      legal:     raw.scores?.legal     ?? raw.dimensions?.legal     ?? 0,
      safety:    raw.scores?.safety    ?? raw.dimensions?.safety    ?? 0,
      health:    raw.scores?.health    ?? raw.dimensions?.health    ?? 0,
      economic:  raw.scores?.economic  ?? raw.dimensions?.economic  ?? 0,
      community: raw.scores?.community ?? raw.dimensions?.community ?? 0,
      youth:     raw.scores?.youth     ?? raw.dimensions?.youth     ?? 0,
    },
  }
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function adaptProfile(raw: any): StateProfile {
  const base = adaptSummary(raw)
  const pop = raw.population ?? {}
  const legal = raw.legal_detail ?? raw.legal ?? {}
  const health = raw.health_detail ?? raw.health ?? {}
  const safety = raw.safety_detail ?? raw.safety ?? {}
  const community = raw.community_detail ?? raw.community ?? {}
  const economic = raw.economic_detail ?? raw.economic ?? {}
  const youth = raw.youth_detail ?? raw.youth ?? {}

  return {
    ...base,
    population: {
      lgbtq_adult_count:   pop.lgbtq_pop  ?? pop.lgbtq_adult_count  ?? 0,
      lgbtq_pct_of_adults: pop.lgbtq_pct  ?? pop.lgbtq_pct_of_adults ?? 0,
      transgender_count:   pop.trans_pop  ?? pop.transgender_count   ?? 0,
      transgender_pct:     pop.trans_pct  ?? pop.transgender_pct     ?? 0,
    },
    legal: {
      hrc_climate:            legal.overall_climate        ?? legal.hrc_climate ?? '',
      conversion_therapy_ban: legal.conversion_therapy_ban ?? false,
      hate_crime_law:         legal.hate_crime_law         ?? false,
      bills_passed_against:   legal.bills_passed_against   ?? 0,
    },
    health: {
      pct_considered_suicide:         health.pct_considered_suicide         ?? health.depression_pct           ?? 0,
      pct_attempted_suicide:          health.pct_attempted_suicide          ?? 0,
      pct_no_mental_health_access:    health.pct_no_mental_health_access    ?? health.healthcare_avoidance_pct ?? 0,
      pct_conversion_therapy_exposed: health.pct_conversion_therapy_exposed ?? 0,
      pct_felt_safe_school:           health.pct_felt_safe_school           ?? 0,
      pct_accepting_adult:            health.pct_accepting_adult            ?? 0,
      hiv_viral_suppression_pct:      health.hiv_viral_suppression_pct      ?? null,
      uninsured_pct:                  health.uninsured_pct                  ?? null,
    },
    safety: {
      so_incidents:   safety.so_incidents  ?? 0,
      gi_incidents:   safety.gi_incidents  ?? 0,
      so_per_100k:    safety.so_per_100k   ?? 0,
      gi_per_100k:    safety.gi_per_100k   ?? 0,
      reporting_rate: safety.reporting_rate ?? 1,
    },
    community: {
      lgbtq_orgs_count:    community.lgbtq_orgs_count    ?? 0,
      lgbtq_orgs_per_100k: community.lgbtq_orgs_per_100k ?? 0,
      pride_events_count:  community.pride_events_count  ?? 0,
    },
    economic: {
      lgbtq_poverty_pct:        economic.lgbtq_poverty_pct        ?? null,
      income_gap_pct:           economic.income_gap_pct           ?? null,
      housing_instability_pct:  economic.housing_instability_pct  ?? null,
    },
    youth: {
      suicidality_pct:                 youth.suicidality_pct                 ?? null,
      school_safety_score:             youth.school_safety_score             ?? null,
      gsa_presence_pct:                youth.gsa_presence_pct                ?? null,
      conversion_therapy_exposure_pct: youth.conversion_therapy_exposure_pct ?? null,
    },
    narrative:  raw.narrative,
    organizations: (raw.organizations ?? []).map((o: Record<string, unknown>) => ({
      org_name_display:    String(o.org_name_display ?? ''),
      org_addr_city:       String(o.org_addr_city ?? ''),
      ntee_code_definition: String(o.ntee_code_definition ?? ''),
      revenue_amount:      Number(o.revenue_amount ?? 0),
    })),
    top_cities: (raw.cities ?? raw.top_cities ?? []).map((c: Record<string, unknown>) => ({
      city:      (c.city_name ?? c.city ?? '') as string,
      state_abbr:(c.state_abbr ?? c.state ?? '') as string,
      mei_score: Number(c.mei_score ?? 0),
    })),
    trend: (raw.trend ?? []).map((t: Record<string, unknown>) => ({
      year:            Number(t.year),
      composite_score: Number(t.overall ?? t.composite_score ?? 0),
    })),
  }
}

export const atlasApi = {
  getStates: async (year = 2024): Promise<StateSummary[]> => {
    try {
      return await getApi(`/states?year=${year}`)
    } catch {
      const data = await getStatic<unknown[]>(`${import.meta.env.BASE_URL}exports/states_map.json`)
      return data.map(adaptSummary)
    }
  },

  getState: async (fips: string, year = 2024): Promise<StateProfile> => {
    const paddedFips = fips.padStart(2, '0')
    try {
      return await getApi(`/states/${paddedFips}?year=${year}`)
    } catch {
      const raw = await getStatic<unknown>(`${import.meta.env.BASE_URL}exports/state_profiles/${paddedFips}.json`)
      return adaptProfile(raw)
    }
  },

  getCities: (params?: { state?: string; limit?: number }): Promise<CityScore[]> => {
    const qs = new URLSearchParams()
    if (params?.state) qs.set('state', params.state)
    if (params?.limit) qs.set('limit', String(params.limit))
    return getApi(`/cities?${qs}`)
  },

  search: (q: string): Promise<Array<{ type: 'state' | 'city'; label: string; fips?: string; state_abbr?: string }>> =>
    getApi(`/search?q=${encodeURIComponent(q)}`),
}
