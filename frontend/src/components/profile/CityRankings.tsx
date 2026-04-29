import type { CityScore } from '../../types/profile'
import { scoreToColor } from '../../utils/colorScales'

interface CityRankingsProps {
  cities: CityScore[]
}

export function CityRankings({ cities }: CityRankingsProps) {
  if (!cities?.length) return null

  return (
    <div>
      <div className="text-xs font-medium text-[var(--text-muted)] uppercase tracking-wider mb-2">
        Top Cities (HRC MEI)
      </div>
      <div className="space-y-1.5">
        {cities.slice(0, 5).map((c, i) => (
          <div key={c.city} className="flex items-center gap-2">
            <span className="text-xs text-[var(--text-muted)] w-4 text-right">{i + 1}</span>
            <div className="flex-1 flex items-center justify-between bg-[var(--surface-alt)] rounded px-2.5 py-1.5">
              <span className="text-sm text-[var(--text-primary)]">{c.city}</span>
              <span
                className="text-xs font-mono font-medium"
                style={{ color: scoreToColor(c.mei_score) }}
              >
                {c.mei_score}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
