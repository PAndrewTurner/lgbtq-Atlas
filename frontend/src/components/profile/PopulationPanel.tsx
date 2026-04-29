import type { StateProfile } from '../../types/profile'

interface PopulationPanelProps {
  profile: StateProfile
}

function fmt(n: number): string {
  return n >= 1_000_000
    ? `${(n / 1_000_000).toFixed(2)}M`
    : n >= 1_000
    ? `${(n / 1_000).toFixed(1)}K`
    : String(n)
}

export function PopulationPanel({ profile }: PopulationPanelProps) {
  const { population } = profile

  return (
    <div className="grid grid-cols-2 gap-3">
      <div className="bg-[var(--surface-alt)] rounded-lg p-3">
        <div className="text-xs text-[var(--text-muted)] mb-1">LGBTQ+ Adults</div>
        <div className="text-xl font-display text-[var(--text-primary)]">
          {fmt(population.lgbtq_adult_count)}
        </div>
        <div className="text-xs text-[var(--text-secondary)]">
          {population.lgbtq_pct_of_adults.toFixed(1)}% of adults
        </div>
      </div>
      <div className="bg-[var(--surface-alt)] rounded-lg p-3">
        <div className="text-xs text-[var(--text-muted)] mb-1">Transgender</div>
        <div className="text-xl font-display text-[var(--text-primary)]">
          {fmt(population.transgender_count)}
        </div>
        <div className="text-xs text-[var(--text-secondary)]">
          {population.transgender_pct.toFixed(2)}% of adults
        </div>
      </div>
    </div>
  )
}
