/**
 * National overview panel — shown when no state is selected.
 * Aggregates all loaded state data and responds to the active layer tab.
 */
import { useMemo } from 'react'
import { useAtlasStore } from '../../store/atlasStore'
import { scoreToColor, DIMENSION_META } from '../../utils/colorScales'
import type { Dimension, StateSummary } from '../../types/profile'

// ── helpers ──────────────────────────────────────────────────────────────────

const TIERS = [
  { label: 'Thriving',    min: 75,  color: '#1ABC9C' },
  { label: 'Supportive',  min: 60,  color: '#27AE60' },
  { label: 'Mixed',       min: 45,  color: '#F1C40F' },
  { label: 'Challenging', min: 30,  color: '#E67E22' },
  { label: 'Hostile',     min: 0,   color: '#C0392B' },
]

function tierFor(score: number) {
  return TIERS.find((t) => score >= t.min) ?? TIERS[TIERS.length - 1]
}

function getScore(s: StateSummary, layer: Dimension | 'composite'): number {
  return layer === 'composite' ? s.composite_score : (s.dimensions[layer] ?? 0)
}

function avg(nums: number[]) {
  return nums.length ? nums.reduce((a, b) => a + b, 0) / nums.length : 0
}

// ── sub-components ────────────────────────────────────────────────────────────

function TierBar({ states, layer }: { states: StateSummary[]; layer: Dimension | 'composite' }) {
  const total = states.length
  if (!total) return null

  const counts = TIERS.map((t, i) => {
    const nextMin = i > 0 ? TIERS[i - 1].min : 101
    return {
      ...t,
      count: states.filter((s) => {
        const score = getScore(s, layer)
        return score >= t.min && score < nextMin
      }).length,
    }
  })

  return (
    <div className="space-y-2">
      <div className="flex h-3 rounded-full overflow-hidden gap-px">
        {counts.map((t) =>
          t.count > 0 ? (
            <div
              key={t.label}
              style={{ width: `${(t.count / total) * 100}%`, backgroundColor: t.color }}
              title={`${t.label}: ${t.count}`}
            />
          ) : null
        )}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-1">
        {counts
          .filter((t) => t.count > 0)
          .map((t) => (
            <div key={t.label} className="flex items-center gap-1 text-xs text-[var(--text-muted)]">
              <span className="w-2 h-2 rounded-full inline-block" style={{ backgroundColor: t.color }} />
              {t.count} {t.label}
            </div>
          ))}
      </div>
    </div>
  )
}

function StateRankRow({
  rank,
  state,
  score,
  onClick,
}: {
  rank: number
  state: StateSummary
  score: number
  onClick: () => void
}) {
  return (
    <button
      onClick={onClick}
      className="w-full flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-[var(--surface-alt)] transition-colors text-left"
    >
      <span className="text-xs text-[var(--text-muted)] w-5 text-right shrink-0">{rank}</span>
      <span className="flex-1 text-sm text-[var(--text-primary)]">{state.name}</span>
      <span className="text-sm font-mono font-medium shrink-0" style={{ color: scoreToColor(score) }}>
        {score.toFixed(1)}
      </span>
    </button>
  )
}

// ── main component ────────────────────────────────────────────────────────────

export function NationalOverviewPanel() {
  const { states, activeLayer, setSelectedFips } = useAtlasStore()

  const sorted = useMemo(
    () => [...states].sort((a, b) => getScore(b, activeLayer) - getScore(a, activeLayer)),
    [states, activeLayer],
  )

  const scores = useMemo(() => states.map((s) => getScore(s, activeLayer)), [states, activeLayer])
  const national = useMemo(() => avg(scores), [scores])

  if (!states.length) {
    return (
      <div className="flex items-center justify-center h-32 text-[var(--text-muted)] text-sm">
        Loading data…
      </div>
    )
  }

  const meta = activeLayer !== 'composite' ? DIMENSION_META[activeLayer] : null
  const label = meta ? meta.label : 'Overall'
  const icon = meta ? meta.icon : '🗺️'
  const tier = tierFor(national)
  const top5 = sorted.slice(0, 5)
  const bottom5 = sorted.slice(-5).reverse()

  return (
    <div className="px-5 py-4 space-y-6">
      {/* Hero */}
      <div className="space-y-1">
        <div className="text-xs text-[var(--text-muted)] uppercase tracking-wider">
          National Average · {label}
        </div>
        <div className="flex items-end gap-3">
          <div className="text-5xl font-display leading-none" style={{ color: scoreToColor(national) }}>
            {national.toFixed(1)}
          </div>
          <div className="mb-1">
            <span
              className="text-xs font-medium px-2 py-0.5 rounded-full"
              style={{ backgroundColor: tier.color + '33', color: tier.color }}
            >
              {tier.label}
            </span>
          </div>
          <div className="ml-auto text-2xl">{icon}</div>
        </div>
        <div className="text-xs text-[var(--text-muted)]">51 states + DC · 2024</div>
      </div>

      {/* Distribution bar */}
      <div className="space-y-2">
        <div className="text-xs font-medium text-[var(--text-muted)] uppercase tracking-wider">
          Distribution
        </div>
        <TierBar states={states} layer={activeLayer} />
      </div>

      {/* Dimension summary (composite only) */}
      {activeLayer === 'composite' && (
        <div className="space-y-2">
          <div className="text-xs font-medium text-[var(--text-muted)] uppercase tracking-wider">
            Average by Dimension
          </div>
          <div className="space-y-2">
            {(Object.keys(DIMENSION_META) as Dimension[]).map((dim) => {
              const dimAvg = avg(states.map((s) => s.dimensions[dim] ?? 0))
              const pct = Math.round(dimAvg)
              return (
                <div key={dim} className="space-y-0.5">
                  <div className="flex justify-between text-xs">
                    <span className="text-[var(--text-secondary)]">
                      {DIMENSION_META[dim].icon} {DIMENSION_META[dim].label}
                    </span>
                    <span className="font-mono" style={{ color: scoreToColor(dimAvg) }}>
                      {dimAvg.toFixed(1)}
                    </span>
                  </div>
                  <div className="h-1.5 rounded-full bg-[var(--border)] overflow-hidden">
                    <div
                      className="h-full rounded-full transition-all"
                      style={{ width: `${pct}%`, backgroundColor: scoreToColor(dimAvg) }}
                    />
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      )}

      {/* Top 5 */}
      <div className="space-y-1">
        <div className="text-xs font-medium text-[var(--text-muted)] uppercase tracking-wider mb-1">
          Highest Ranked
        </div>
        {top5.map((s, i) => (
          <StateRankRow
            key={s.fips}
            rank={i + 1}
            state={s}
            score={getScore(s, activeLayer)}
            onClick={() => setSelectedFips(s.fips)}
          />
        ))}
      </div>

      {/* Bottom 5 */}
      <div className="space-y-1">
        <div className="text-xs font-medium text-[var(--text-muted)] uppercase tracking-wider mb-1">
          Lowest Ranked
        </div>
        {bottom5.map((s, i) => (
          <StateRankRow
            key={s.fips}
            rank={states.length - 4 + i}
            state={s}
            score={getScore(s, activeLayer)}
            onClick={() => setSelectedFips(s.fips)}
          />
        ))}
      </div>

      <p className="text-xs text-[var(--text-muted)] text-center pb-2">
        Click any state to see details, or click on the map.
      </p>
    </div>
  )
}
