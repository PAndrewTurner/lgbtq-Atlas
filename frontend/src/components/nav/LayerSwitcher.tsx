import { useAtlasStore } from '../../store/atlasStore'
import { DIMENSION_META } from '../../utils/colorScales'
import type { Dimension } from '../../types/profile'

const LAYERS: Array<{ key: Dimension | 'composite'; label: string; color?: string }> = [
  { key: 'composite', label: 'Overall' },
  ...Object.entries(DIMENSION_META).map(([key, meta]) => ({
    key: key as Dimension,
    label: meta.label.split(' ')[0],
    color: meta.color,
  })),
]

export function LayerSwitcher() {
  const { activeLayer, setActiveLayer } = useAtlasStore()

  return (
    <div className="flex gap-1 flex-wrap">
      {LAYERS.map(({ key, label, color }) => {
        const active = activeLayer === key
        return (
          <button
            key={key}
            onClick={() => setActiveLayer(key)}
            className={`px-2.5 py-1 rounded text-xs font-medium transition-all ${
              active
                ? 'text-white'
                : 'text-[var(--text-muted)] hover:text-[var(--text-secondary)] bg-[var(--surface-alt)] hover:bg-[var(--border)]'
            }`}
            style={active ? { backgroundColor: color ?? '#6366f1' } : undefined}
          >
            {label}
          </button>
        )
      })}
    </div>
  )
}
