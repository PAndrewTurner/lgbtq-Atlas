import { useAtlasStore } from '../../store/atlasStore'
import { useStateProfile } from '../../hooks/useStateProfile'
import { Drawer } from '../ui/Drawer'
import { TrendSparkline } from './TrendSparkline'
import { PopulationPanel } from './PopulationPanel'
import { NarrativeSummary } from './NarrativeSummary'
import { DimensionDetailView } from './DimensionDetailView'
import { NationalOverviewPanel } from './NationalOverviewPanel'
import { CityProfilePanel } from './CityProfilePanel'
import { Badge } from '../ui/Badge'
import { scoreToColor, scoreToLabel, DIMENSION_META } from '../../utils/colorScales'
import type { Dimension } from '../../types/profile'

export function StateProfileDrawer() {
  const { selectedFips, selectedCity, year, activeLayer, setSelectedFips, setSelectedCity } = useAtlasStore()
  const { data: profile, isLoading } = useStateProfile(selectedFips, year)

  const heroScore = profile
    ? activeLayer === 'composite'
      ? profile.composite_score
      : profile.dimensions[activeLayer as Dimension]
    : 0

  const heroColor = scoreToColor(heroScore)
  const activeMeta = activeLayer !== 'composite' ? DIMENSION_META[activeLayer] : null

  // Determine title and close action based on what's selected
  const drawerTitle = selectedCity
    ? `${selectedCity.city}, ${selectedCity.state}`
    : selectedFips
      ? profile
        ? activeMeta ? `${profile.name} — ${activeMeta.label}` : profile.name
        : '…'
      : activeMeta
        ? `United States — ${activeMeta.label}`
        : 'United States — Overview'

  const drawerClose = selectedCity
    ? () => setSelectedCity(null)
    : selectedFips
      ? () => setSelectedFips(null)
      : undefined

  return (
    <Drawer onClose={drawerClose} title={drawerTitle}>
      {/* City profile — highest priority */}
      {selectedCity && <CityProfilePanel city={selectedCity} />}

      {/* National overview when nothing selected */}
      {!selectedCity && !selectedFips && <NationalOverviewPanel />}

      {/* State profile */}
      {!selectedCity && selectedFips && isLoading && (
        <div className="flex items-center justify-center h-32 text-[var(--text-muted)] text-sm">
          Loading…
        </div>
      )}

      {!selectedCity && selectedFips && profile && (
        <div className="px-5 py-4 space-y-6">
          {/* Score hero */}
          <div className="flex items-end gap-3">
            <div className="text-5xl font-display leading-none" style={{ color: heroColor }}>
              {heroScore.toFixed(1)}
            </div>
            <div className="mb-1 space-y-0.5">
              <Badge color={heroColor}>{scoreToLabel(heroScore)}</Badge>
              <div className="text-xs text-[var(--text-muted)]">
                {profile.abbr} · {year}
                {activeMeta ? ` · ${activeMeta.label}` : ' · Overall'}
              </div>
            </div>
            <div className="ml-auto w-24">
              <TrendSparkline data={profile.trend} color={heroColor} />
            </div>
          </div>

          {/* Dimension-specific content */}
          <DimensionDetailView profile={profile} activeLayer={activeLayer} />

          {/* Narrative always at bottom */}
          <NarrativeSummary narrative={profile.narrative} />

          {/* Population only on Overall */}
          {activeLayer === 'composite' && (
            <div>
              <div className="text-xs font-medium text-[var(--text-muted)] uppercase tracking-wider mb-2">
                Population
              </div>
              <PopulationPanel profile={profile} />
            </div>
          )}
        </div>
      )}
    </Drawer>
  )
}
