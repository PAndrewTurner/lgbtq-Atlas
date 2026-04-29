import { useQuery } from '@tanstack/react-query'
import { atlasApi } from '../api/atlas'

export function useStateProfile(fips: string | null, year = 2024) {
  return useQuery({
    queryKey: ['state', fips, year],
    queryFn: () => atlasApi.getState(fips!, year),
    enabled: !!fips,
    staleTime: 5 * 60 * 1000,
  })
}
