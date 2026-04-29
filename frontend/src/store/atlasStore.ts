import { create } from 'zustand'
import type { StateSummary, Dimension } from '../types/profile'

export interface SelectedCity {
  city: string
  state: string  // abbr
  mei_score: number
  slug: string
}

interface AtlasState {
  selectedFips: string | null
  selectedCity: SelectedCity | null
  hoveredFips: string | null
  activeLayer: Dimension | 'composite'
  year: number
  states: StateSummary[]
  isLoading: boolean

  setSelectedFips: (fips: string | null) => void
  setSelectedCity: (city: SelectedCity | null) => void
  setHoveredFips: (fips: string | null) => void
  setActiveLayer: (layer: Dimension | 'composite') => void
  setYear: (year: number) => void
  setStates: (states: StateSummary[]) => void
  setLoading: (loading: boolean) => void
}

export const useAtlasStore = create<AtlasState>((set) => ({
  selectedFips: null,
  selectedCity: null,
  hoveredFips: null,
  activeLayer: 'composite',
  year: 2024,
  states: [],
  isLoading: false,

  setSelectedFips: (fips) => set({ selectedFips: fips, selectedCity: null }),
  setSelectedCity: (city) => set({ selectedCity: city }),
  setHoveredFips: (fips) => set({ hoveredFips: fips }),
  setActiveLayer: (layer) => set({ activeLayer: layer }),
  setYear: (year) => set({ year }),
  setStates: (states) => set({ states }),
  setLoading: (isLoading) => set({ isLoading }),
}))
