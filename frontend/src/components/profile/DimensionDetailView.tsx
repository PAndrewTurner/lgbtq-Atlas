/**
 * Dimension-specific detail panels shown when a layer tab is active.
 * Each dimension surfaces the most relevant data for that category.
 */
import { DimensionBar } from './DimensionBar'
import { CityRankings } from './CityRankings'
import { CommunityPanel } from './CommunityPanel'
import { scoreToColor, DIMENSION_META } from '../../utils/colorScales'
import type { StateProfile, Dimension } from '../../types/profile'

// ── helpers ──────────────────────────────────────────────────────────────────

function StatRow({
  label,
  value,
  unit = '',
  good,
}: {
  label: string
  value: number | null | undefined
  unit?: string
  good?: boolean
}) {
  if (value == null) return null
  const formatted = Number.isInteger(value) ? value.toLocaleString() : value.toFixed(1)
  return (
    <div className="flex justify-between items-center text-sm py-1 border-b border-[var(--border)] last:border-0">
      <span className="text-[var(--text-secondary)]">{label}</span>
      <span
        className="font-mono font-medium"
        style={{ color: good === true ? 'var(--health)' : good === false ? 'var(--safety)' : 'var(--text-primary)' }}
      >
        {formatted}{unit}
      </span>
    </div>
  )
}

function ScoreHero({ score, dimension }: { score: number; dimension: Dimension }) {
  const meta = DIMENSION_META[dimension]
  return (
    <div className="flex items-center gap-3 py-2">
      <div className="text-3xl">{meta.icon}</div>
      <div>
        <div className="text-2xl font-display leading-none" style={{ color: scoreToColor(score) }}>
          {score.toFixed(1)}
        </div>
        <div className="text-xs text-[var(--text-muted)] mt-0.5">{meta.label} Score</div>
      </div>
    </div>
  )
}

// ── dimension panels ──────────────────────────────────────────────────────────

function LegalView({ profile }: { profile: StateProfile }) {
  const { legal } = profile
  return (
    <div className="space-y-4">
      <ScoreHero score={profile.dimensions.legal} dimension="legal" />
      <div className="bg-[var(--surface-alt)] rounded-lg p-3 space-y-1">
        <StatRow label="HRC Climate Rating" value={null} />
        <div className="flex justify-between items-center text-sm py-1 border-b border-[var(--border)]">
          <span className="text-[var(--text-secondary)]">HRC Climate</span>
          <span className="text-[var(--text-primary)] font-medium">{legal.hrc_climate || '—'}</span>
        </div>
        <div className="flex justify-between items-center text-sm py-1 border-b border-[var(--border)]">
          <span className="text-[var(--text-secondary)]">Conversion Therapy Ban</span>
          <span style={{ color: legal.conversion_therapy_ban ? 'var(--health)' : 'var(--safety)' }}>
            {legal.conversion_therapy_ban ? '✓ Yes' : '✗ No'}
          </span>
        </div>
        <div className="flex justify-between items-center text-sm py-1 border-b border-[var(--border)]">
          <span className="text-[var(--text-secondary)]">Hate Crime Law</span>
          <span style={{ color: legal.hate_crime_law ? 'var(--health)' : 'var(--safety)' }}>
            {legal.hate_crime_law ? '✓ Yes' : '✗ No'}
          </span>
        </div>
        <div className="flex justify-between items-center text-sm py-1">
          <span className="text-[var(--text-secondary)]">Anti-LGBTQ+ Bills Passed</span>
          <span style={{ color: legal.bills_passed_against > 0 ? 'var(--safety)' : 'var(--health)' }}>
            {legal.bills_passed_against > 0 ? legal.bills_passed_against : '0 ✓'}
          </span>
        </div>
      </div>
    </div>
  )
}

function SafetyView({ profile }: { profile: StateProfile }) {
  const { safety } = profile
  const totalIncidents = (safety.so_incidents ?? 0) + (safety.gi_incidents ?? 0)
  const totalPer100k = (safety.so_per_100k ?? 0) + (safety.gi_per_100k ?? 0)
  const reportingPct = ((safety.reporting_rate ?? 1) * 100)
  return (
    <div className="space-y-4">
      <ScoreHero score={profile.dimensions.safety} dimension="safety" />
      <div className="bg-[var(--surface-alt)] rounded-lg p-3 space-y-0">
        <StatRow label="Total Hate Crime Incidents" value={totalIncidents} />
        <StatRow label="SO-Based Incidents" value={safety.so_incidents} />
        <StatRow label="GI-Based Incidents" value={safety.gi_incidents} />
        <StatRow label="Rate per 100k LGBTQ+" value={totalPer100k} unit=" incidents" />
        <StatRow label="Agency Reporting Rate" value={reportingPct} unit="%" good={reportingPct > 80} />
      </div>
      <p className="text-xs text-[var(--text-muted)] leading-relaxed">
        SO = sexual orientation bias · GI = gender identity bias. Higher score = lower hate crime incidence relative to other states.
      </p>
    </div>
  )
}

function HealthView({ profile }: { profile: StateProfile }) {
  const { health } = profile
  return (
    <div className="space-y-4">
      <ScoreHero score={profile.dimensions.health} dimension="health" />
      <div className="text-xs font-medium text-[var(--text-muted)] uppercase tracking-wider">Mental Health</div>
      <div className="bg-[var(--surface-alt)] rounded-lg p-3 space-y-0">
        <StatRow label="Considered Suicide (past yr)" value={health.pct_considered_suicide} unit="%" good={false} />
        <StatRow label="Attempted Suicide" value={health.pct_attempted_suicide > 0 ? health.pct_attempted_suicide : null} unit="%" good={false} />
        <StatRow label="Could Not Access Care" value={health.pct_no_mental_health_access} unit="%" good={false} />
        <StatRow label="Exposed to Conversion Therapy" value={health.pct_conversion_therapy_exposed > 0 ? health.pct_conversion_therapy_exposed : null} unit="%" good={false} />
      </div>
      <div className="text-xs font-medium text-[var(--text-muted)] uppercase tracking-wider">Physical Health</div>
      <div className="bg-[var(--surface-alt)] rounded-lg p-3 space-y-0">
        <StatRow label="Uninsured Rate" value={health.uninsured_pct} unit="%" good={false} />
        <StatRow label="HIV Viral Suppression" value={health.hiv_viral_suppression_pct} unit="%" good={true} />
      </div>
      <p className="text-xs text-[var(--text-muted)] leading-relaxed">
        Source: Trevor Project Youth Survey 2024. Mental health data reflects LGBTQ+ youth (13-24).
      </p>
    </div>
  )
}

function EconomicView({ profile }: { profile: StateProfile }) {
  const { economic } = profile
  const gapDir = economic.income_gap_pct != null
    ? economic.income_gap_pct < 0 ? '▼ below median' : '▲ above median'
    : null
  return (
    <div className="space-y-4">
      <ScoreHero score={profile.dimensions.economic} dimension="economic" />
      <div className="bg-[var(--surface-alt)] rounded-lg p-3 space-y-0">
        <StatRow label="LGBTQ+ Poverty Rate" value={economic.lgbtq_poverty_pct} unit="%" good={false} />
        <StatRow label="Housing Instability" value={economic.housing_instability_pct} unit="%" good={false} />
        {economic.income_gap_pct != null && (
          <div className="flex justify-between items-center text-sm py-1">
            <span className="text-[var(--text-secondary)]">Income vs. Non-LGBTQ+</span>
            <span style={{ color: (economic.income_gap_pct ?? 0) < 0 ? 'var(--safety)' : 'var(--health)' }}>
              {Math.abs(economic.income_gap_pct ?? 0).toFixed(1)}% {gapDir}
            </span>
          </div>
        )}
      </div>
      <p className="text-xs text-[var(--text-muted)] leading-relaxed">
        Economic indicators reflect LGBTQ+ adults relative to the general population. Higher score = greater economic equity.
      </p>
    </div>
  )
}

function CommunityView({ profile }: { profile: StateProfile }) {
  const { community } = profile
  return (
    <div className="space-y-4">
      <ScoreHero score={profile.dimensions.community} dimension="community" />
      <div className="bg-[var(--surface-alt)] rounded-lg p-3 space-y-0">
        <StatRow label="LGBTQ+ Orgs (IRS)" value={community.lgbtq_orgs_count} />
        <StatRow label="Orgs per 100k LGBTQ+" value={community.lgbtq_orgs_per_100k} />
        <StatRow label="Pride Events" value={community.pride_events_count > 0 ? community.pride_events_count : null} />
      </div>
      <CityRankings cities={profile.top_cities} />
      <CommunityPanel organizations={profile.organizations} />
    </div>
  )
}

function YouthView({ profile }: { profile: StateProfile }) {
  const { youth } = profile
  return (
    <div className="space-y-4">
      <ScoreHero score={profile.dimensions.youth} dimension="youth" />
      <div className="bg-[var(--surface-alt)] rounded-lg p-3 space-y-0">
        <StatRow label="Youth Suicidality Rate" value={youth.suicidality_pct} unit="%" good={false} />
        <StatRow label="School Safety Score" value={youth.school_safety_score} unit="/100" good={true} />
        <StatRow label="Schools with GSA" value={youth.gsa_presence_pct} unit="%" good={true} />
        <StatRow label="Exposed to Conversion Therapy" value={youth.conversion_therapy_exposure_pct} unit="%" good={false} />
      </div>
      <p className="text-xs text-[var(--text-muted)] leading-relaxed">
        Source: Trevor Project 2024, CDC YRBSS. GSA = Gender & Sexuality Alliance school clubs.
      </p>
    </div>
  )
}

// ── overall view (all dimensions summary) ────────────────────────────────────

function OverallView({ profile }: { profile: StateProfile }) {
  const dimensions = Object.keys(DIMENSION_META) as Dimension[]
  return (
    <div className="space-y-3">
      {dimensions.map((dim) => (
        <DimensionBar key={dim} dimension={dim} score={profile.dimensions[dim]} />
      ))}
    </div>
  )
}

// ── main export ───────────────────────────────────────────────────────────────

interface Props {
  profile: StateProfile
  activeLayer: Dimension | 'composite'
}

export function DimensionDetailView({ profile, activeLayer }: Props) {
  switch (activeLayer) {
    case 'legal':     return <LegalView profile={profile} />
    case 'safety':    return <SafetyView profile={profile} />
    case 'health':    return <HealthView profile={profile} />
    case 'economic':  return <EconomicView profile={profile} />
    case 'community': return <CommunityView profile={profile} />
    case 'youth':     return <YouthView profile={profile} />
    default:          return <OverallView profile={profile} />
  }
}
