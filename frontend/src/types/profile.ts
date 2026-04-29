export interface DimensionScores {
  legal: number
  safety: number
  health: number
  economic: number
  community: number
  youth: number
}

export interface StateSummary {
  fips: string
  name: string
  abbr: string
  composite_score: number
  dimensions: DimensionScores
  year: number
}

export interface TrendPoint {
  year: number
  composite_score: number
}

export interface CityScore {
  city: string
  state_abbr: string
  mei_score: number
  rank?: number
}

export interface Organization {
  org_name_display: string
  org_addr_city: string
  ntee_code_definition: string
  revenue_amount: number
}

export interface StateProfile extends StateSummary {
  population: {
    lgbtq_adult_count: number
    lgbtq_pct_of_adults: number
    transgender_count: number
    transgender_pct: number
  }
  legal: {
    hrc_climate: string
    conversion_therapy_ban: boolean
    hate_crime_law: boolean
    bills_passed_against: number
  }
  health: {
    pct_considered_suicide: number
    pct_attempted_suicide: number
    pct_no_mental_health_access: number
    pct_conversion_therapy_exposed: number
    pct_felt_safe_school: number
    pct_accepting_adult: number
    hiv_viral_suppression_pct: number | null
    uninsured_pct: number | null
  }
  safety: {
    so_incidents: number
    gi_incidents: number
    so_per_100k: number
    gi_per_100k: number
    reporting_rate: number
  }
  community: {
    lgbtq_orgs_count: number
    lgbtq_orgs_per_100k: number
    pride_events_count: number
  }
  economic: {
    lgbtq_poverty_pct: number | null
    income_gap_pct: number | null
    housing_instability_pct: number | null
  }
  youth: {
    suicidality_pct: number | null
    school_safety_score: number | null
    gsa_presence_pct: number | null
    conversion_therapy_exposure_pct: number | null
  }
  narrative?: string
  top_cities: CityScore[]
  trend: TrendPoint[]
  organizations: Organization[]
}

export type Dimension = keyof DimensionScores
