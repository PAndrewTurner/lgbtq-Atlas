import type { MapRef } from 'react-map-gl/maplibre'
import { Plus, Minus, Compass } from 'lucide-react'

interface MapControlsProps {
  mapRef: React.RefObject<MapRef>
}

export function MapControls({ mapRef }: MapControlsProps) {
  const map = mapRef.current?.getMap()

  return (
    <div className="absolute bottom-6 right-4 flex flex-col gap-1 z-10">
      <button
        onClick={() => map?.zoomIn()}
        className="w-8 h-8 flex items-center justify-center bg-[var(--surface)] border border-[var(--border)] rounded text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--surface-alt)] transition-colors"
        aria-label="Zoom in"
      >
        <Plus size={14} />
      </button>
      <button
        onClick={() => map?.zoomOut()}
        className="w-8 h-8 flex items-center justify-center bg-[var(--surface)] border border-[var(--border)] rounded text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--surface-alt)] transition-colors"
        aria-label="Zoom out"
      >
        <Minus size={14} />
      </button>
      <button
        onClick={() => map?.resetNorth()}
        className="w-8 h-8 flex items-center justify-center bg-[var(--surface)] border border-[var(--border)] rounded text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--surface-alt)] transition-colors"
        aria-label="Reset north"
      >
        <Compass size={14} />
      </button>
    </div>
  )
}
