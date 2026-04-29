import { useRef, useCallback, useState } from 'react'
import Map, { Source, Layer, type MapRef, type MapLayerMouseEvent } from 'react-map-gl/maplibre'
import type { ExpressionSpecification } from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'
import { useAtlasStore, type SelectedCity } from '../../store/atlasStore'
import { useMapLayer } from '../../hooks/useMapLayer'
import { scoreToColor } from '../../utils/colorScales'
import { HoverTooltip } from './HoverTooltip'
import { MapControls } from './MapControls'
import { CityLayer } from './CityLayer'
import type { StateSummary } from '../../types/profile'

const GEOJSON_URL = '/exports/states.geojson'

const INITIAL_VIEW = {
  longitude: -98.5795,
  latitude: 39.8283,
  zoom: 3.5,
}

export function AtlasMap() {
  const mapRef = useRef<MapRef>(null)
  const { states, activeLayer, selectedFips, hoveredFips, setSelectedFips, setHoveredFips, setSelectedCity } = useAtlasStore()
  const { isLoading } = useMapLayer()

  const [tooltip, setTooltip] = useState<{ state: StateSummary; x: number; y: number } | null>(null)
  const [cityTooltip, setCityTooltip] = useState<{ name: string; score: number; x: number; y: number } | null>(null)

  const stateByFips = Object.fromEntries(states.map((s) => [s.fips, s]))
  const selectedAbbr = selectedFips ? stateByFips[selectedFips]?.abbr : null

  const colorExpression: ExpressionSpecification = (() => {
    const pairs: Array<[string, string]> = []
    for (const s of states) {
      const fips = s?.fips
      if (!fips || typeof fips !== 'string') continue
      const rawScore = activeLayer === 'composite' ? s.composite_score : s.dimensions[activeLayer]
      const score = typeof rawScore === 'number' && isFinite(rawScore) ? rawScore : 0
      const color = scoreToColor(score)
      if (color && typeof color === 'string' && color.length > 0) pairs.push([fips, color])
    }
    if (!pairs.length) return '#444455' as unknown as ExpressionSpecification
    const expr: unknown[] = ['match', ['get', 'fips']]
    for (const [fips, color] of pairs) expr.push(fips, color)
    expr.push('#444455')
    return expr as unknown as ExpressionSpecification
  })()

  const fipsFromFeature = (props: Record<string, unknown> | null): string | null => {
    const raw = props?.fips
    if (raw == null) return null
    return String(raw).padStart(2, '0')
  }

  const onMouseMove = useCallback(
    (e: MapLayerMouseEvent) => {
      const feature = e.features?.[0]
      if (!feature) { setHoveredFips(null); setTooltip(null); setCityTooltip(null); return }

      if (feature.layer.id === 'cities-zoom' || feature.layer.id === 'cities-selected') {
        setHoveredFips(null)
        setTooltip(null)
        const p = feature.properties ?? {}
        setCityTooltip({
          name: `${p.city}, ${p.state}`,
          score: p.mei_score as number,
          x: e.originalEvent.clientX,
          y: e.originalEvent.clientY,
        })
        return
      }

      setCityTooltip(null)
      const fips = fipsFromFeature(feature.properties)
      if (!fips) return
      setHoveredFips(fips)
      const s = stateByFips[fips]
      if (s) setTooltip({ state: s, x: e.originalEvent.clientX, y: e.originalEvent.clientY })
    },
    [stateByFips, setHoveredFips],
  )

  const onMouseLeave = useCallback(() => {
    setHoveredFips(null)
    setTooltip(null)
    setCityTooltip(null)
  }, [setHoveredFips])

  const onClick = useCallback(
    (e: MapLayerMouseEvent) => {
      const feature = e.features?.[0]
      if (feature?.layer.id === 'cities-zoom' || feature?.layer.id === 'cities-selected') {
        const p = feature.properties ?? {}
        setSelectedCity({
          city:      String(p.city ?? ''),
          state:     String(p.state ?? ''),
          mei_score: Number(p.mei_score ?? 0),
          slug:      String(p.slug ?? ''),
        } as SelectedCity)
        return
      }
      const fips = fipsFromFeature(feature?.properties ?? null)
      setSelectedFips(fips === selectedFips ? null : fips)
    },
    [selectedFips, setSelectedFips, setSelectedCity],
  )

  return (
    <div className="relative w-full h-full">
      <Map
        ref={mapRef}
        initialViewState={INITIAL_VIEW}
        style={{ width: '100%', height: '100%' }}
        mapStyle="https://basemaps.cartocdn.com/gl/dark-matter-nolabels-gl-style/style.json"
        interactiveLayerIds={['states-fill', 'cities-zoom', 'cities-selected']}
        onMouseMove={onMouseMove}
        onMouseLeave={onMouseLeave}
        onClick={onClick}
        cursor={hoveredFips || cityTooltip ? 'pointer' : 'grab'}
      >
        <Source id="states" type="geojson" data={GEOJSON_URL}>
          <Layer
            id="states-fill"
            type="fill"
            paint={{
              'fill-color': colorExpression,
              'fill-opacity': [
                'case',
                ['==', ['get', 'fips'], hoveredFips ?? ''],
                0.9,
                0.75,
              ] as ExpressionSpecification,
            }}
          />
          <Layer
            id="states-outline"
            type="line"
            paint={{
              'line-color': [
                'case',
                ['==', ['get', 'fips'], selectedFips ?? ''],
                '#ffffff',
                ['==', ['get', 'fips'], hoveredFips ?? ''],
                '#aaaaaa',
                '#333344',
              ] as ExpressionSpecification,
              'line-width': [
                'case',
                ['==', ['get', 'fips'], selectedFips ?? ''],
                2.5,
                0.8,
              ] as ExpressionSpecification,
            }}
          />
        </Source>

        <CityLayer selectedStateAbbr={selectedAbbr} />

        <MapControls mapRef={mapRef} />
      </Map>

      {tooltip && <HoverTooltip {...tooltip} />}

      {cityTooltip && (
        <div
          className="fixed z-50 pointer-events-none bg-[var(--surface)] border border-[var(--border)] rounded-lg shadow-xl px-3 py-2"
          style={{ left: cityTooltip.x + 12, top: cityTooltip.y - 8, transform: 'translateY(-50%)' }}
        >
          <div className="text-sm font-medium text-[var(--text-primary)]">{cityTooltip.name}</div>
          <div className="text-xs text-[var(--text-muted)]">MEI Score: <span className="font-mono text-[var(--community)]">{cityTooltip.score}</span></div>
        </div>
      )}

      {isLoading && (
        <div className="absolute inset-0 flex items-center justify-center bg-[var(--bg)]/60">
          <div className="text-[var(--text-muted)] text-sm">Loading map data…</div>
        </div>
      )}
    </div>
  )
}
