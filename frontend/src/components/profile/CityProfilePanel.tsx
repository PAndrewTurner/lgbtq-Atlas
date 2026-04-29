/**
 * City detail panel — shown when a city dot is clicked on the map.
 * Displays HRC Municipal Equality Index (MEI) data for that city.
 */
import { useAtlasStore, type SelectedCity } from '../../store/atlasStore'
import { scoreToColor, scoreToLabel } from '../../utils/colorScales'

const MEI_CATEGORIES = [
  { label: 'Non-Discrimination Laws',    icon: '⚖️', desc: 'City & county protections for LGBTQ+ residents, employees, and visitors' },
  { label: 'Municipality as Employer',   icon: '🏛️', desc: 'Equal benefits, gender marker policies, and trans-inclusive healthcare for city employees' },
  { label: 'Municipal Services',         icon: '🤝', desc: 'LGBTQ+-inclusive housing, homeless services, and health programs' },
  { label: 'Law Enforcement',            icon: '🛡️', desc: 'Hate crime reporting, bias training, and police department anti-discrimination policies' },
  { label: 'Leadership on Equality',     icon: '🌈', desc: 'Visible municipal support for LGBTQ+ equality and community engagement' },
]

function ScoreTier({ score }: { score: number }) {
  const color = scoreToColor(score)
  const label = scoreToLabel(score)
  const pct = score

  return (
    <div className="space-y-2">
      <div className="flex items-end gap-3">
        <div className="text-5xl font-display leading-none" style={{ color }}>
          {score}
        </div>
        <div className="mb-1 space-y-1">
          <span
            className="text-xs font-medium px-2 py-0.5 rounded-full"
            style={{ backgroundColor: color + '33', color }}
          >
            {label}
          </span>
          <div className="text-xs text-[var(--text-muted)]">out of 100</div>
        </div>
      </div>
      <div className="h-2 rounded-full bg-[var(--border)] overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-500"
          style={{ width: `${pct}%`, backgroundColor: color }}
        />
      </div>
    </div>
  )
}

interface Props {
  city: SelectedCity
}

export function CityProfilePanel({ city }: Props) {
  const { states, setSelectedFips, setSelectedCity } = useAtlasStore()

  // Find the state FIPS so clicking the state name drills into it
  const stateSummary = states.find((s) => s.abbr === city.state)

  // Rank this city among all cities in the same state from top_cities — we
  // don't have per-city sub-scores from the raw CSV, so we show national
  // ranking context by comparing against the states list
  const hrcUrl = city.slug
    ? `https://www.hrc.org/resources/municipalities/${city.slug}`
    : null

  function openState() {
    if (stateSummary) {
      setSelectedCity(null)
      setSelectedFips(stateSummary.fips)
    }
  }

  return (
    <div className="px-5 py-4 space-y-6">
      {/* Header */}
      <div className="space-y-1">
        <div className="text-xs text-[var(--text-muted)] uppercase tracking-wider">
          HRC Municipal Equality Index
        </div>
        <ScoreTier score={city.mei_score} />
        <div className="text-xs text-[var(--text-muted)] pt-1">
          {city.city}, {city.state}
          {stateSummary && (
            <button
              onClick={openState}
              className="ml-2 text-[var(--legal)] hover:underline"
            >
              ↗ View {stateSummary.name}
            </button>
          )}
        </div>
      </div>

      {/* What MEI measures */}
      <div className="space-y-2">
        <div className="text-xs font-medium text-[var(--text-muted)] uppercase tracking-wider">
          What MEI Measures
        </div>
        <div className="space-y-2">
          {MEI_CATEGORIES.map((cat) => (
            <div
              key={cat.label}
              className="bg-[var(--surface-alt)] rounded-lg px-3 py-2.5"
            >
              <div className="flex items-center gap-2 text-sm font-medium text-[var(--text-primary)]">
                <span>{cat.icon}</span>
                <span>{cat.label}</span>
              </div>
              <p className="text-xs text-[var(--text-muted)] mt-0.5 leading-relaxed">
                {cat.desc}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Score interpretation */}
      <div className="bg-[var(--surface-alt)] rounded-lg p-3 space-y-1.5">
        <div className="text-xs font-medium text-[var(--text-muted)] uppercase tracking-wider mb-2">
          Score Guide
        </div>
        {[
          { range: '80–100', label: 'High Equality',     color: '#1ABC9C' },
          { range: '60–79',  label: 'Supportive',        color: '#27AE60' },
          { range: '45–59',  label: 'Some Protections',  color: '#F1C40F' },
          { range: '30–44',  label: 'Limited',           color: '#E67E22' },
          { range: '0–29',   label: 'Hostile',           color: '#C0392B' },
        ].map((tier) => (
          <div key={tier.range} className="flex justify-between text-xs">
            <span className="font-mono text-[var(--text-muted)]">{tier.range}</span>
            <span style={{ color: tier.color }}>{tier.label}</span>
          </div>
        ))}
      </div>

      {/* External link */}
      {hrcUrl && (
        <a
          href={hrcUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center justify-center gap-2 w-full py-2.5 rounded-lg border border-[var(--border)] text-sm text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:border-[var(--text-muted)] transition-colors"
        >
          <span>View full HRC scorecard</span>
          <span className="text-xs">↗</span>
        </a>
      )}

      <p className="text-xs text-[var(--text-muted)] text-center pb-1">
        Source: HRC Municipal Equality Index 2025
      </p>
    </div>
  )
}
