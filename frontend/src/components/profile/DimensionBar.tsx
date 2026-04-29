import { DIMENSION_META } from '../../utils/colorScales'
import type { Dimension } from '../../types/profile'

interface DimensionBarProps {
  dimension: Dimension
  score: number
  showLabel?: boolean
}

export function DimensionBar({ dimension, score, showLabel = true }: DimensionBarProps) {
  const meta = DIMENSION_META[dimension]
  const pct = Math.min(100, Math.max(0, score))

  return (
    <div className="space-y-1">
      {showLabel && (
        <div className="flex justify-between items-center">
          <span className="text-xs text-[var(--text-secondary)]">{meta.label}</span>
          <span className="text-xs font-mono font-medium" style={{ color: meta.color }}>
            {score.toFixed(1)}
          </span>
        </div>
      )}
      <div className="h-1.5 rounded-full bg-[var(--surface-alt)] overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-500"
          style={{ width: `${pct}%`, backgroundColor: meta.color }}
        />
      </div>
    </div>
  )
}
