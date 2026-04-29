import { scoreToColor, scoreToLabel } from '../../utils/colorScales'
import type { StateSummary } from '../../types/profile'

interface HoverTooltipProps {
  state: StateSummary
  x: number
  y: number
}

export function HoverTooltip({ state, x, y }: HoverTooltipProps) {
  const color = scoreToColor(state.composite_score)

  return (
    <div
      className="fixed z-50 pointer-events-none bg-[var(--surface)] border border-[var(--border)] rounded-lg shadow-xl px-3 py-2 min-w-[160px]"
      style={{ left: x + 12, top: y - 8, transform: 'translateY(-50%)' }}
    >
      <div className="font-medium text-sm text-[var(--text-primary)]">{state.name}</div>
      <div className="flex items-center gap-2 mt-1">
        <span className="text-xl font-display" style={{ color }}>
          {state.composite_score.toFixed(1)}
        </span>
        <span className="text-xs text-[var(--text-muted)]">{scoreToLabel(state.composite_score)}</span>
      </div>
    </div>
  )
}
