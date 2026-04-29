import { Source, Layer } from 'react-map-gl/maplibre'
import type { ExpressionSpecification } from 'maplibre-gl'
import { scoreToColor } from '../../utils/colorScales'

const CITIES_URL = '/exports/cities.geojson'

// Build a step expression mapping MEI score ranges to colors
const MEI_COLOR: ExpressionSpecification = [
  'step',
  ['get', 'mei_score'],
  '#C0392B',   // < 30  hostile
  30,  '#E67E22',  // 30–59
  60,  '#F1C40F',  // 60–79
  80,  '#27AE60',  // 80–99
  100, '#1ABC9C',  // 100
] as unknown as ExpressionSpecification

interface CityLayerProps {
  selectedStateAbbr?: string | null
}

export function CityLayer({ selectedStateAbbr }: CityLayerProps) {
  const stateFilter: ExpressionSpecification | undefined = selectedStateAbbr
    ? ['==', ['get', 'state'], selectedStateAbbr] as ExpressionSpecification
    : undefined

  return (
    <Source id="cities" type="geojson" data={CITIES_URL}>
      {/* Show all cities when zoomed in */}
      <Layer
        id="cities-zoom"
        type="circle"
        minzoom={6}
        paint={{
          'circle-radius': [
            'interpolate', ['linear'], ['zoom'],
            6, 3,
            10, 7,
          ] as ExpressionSpecification,
          'circle-color': MEI_COLOR,
          'circle-stroke-width': 1,
          'circle-stroke-color': 'rgba(0,0,0,0.4)',
          'circle-opacity': 0.85,
        }}
      />
      {/* Show selected state's cities at any zoom */}
      {selectedStateAbbr && (
        <Layer
          id="cities-selected"
          type="circle"
          filter={stateFilter}
          paint={{
            'circle-radius': 6,
            'circle-color': MEI_COLOR,
            'circle-stroke-width': 1.5,
            'circle-stroke-color': 'rgba(255,255,255,0.6)',
            'circle-opacity': 0.9,
          }}
        />
      )}
    </Source>
  )
}
