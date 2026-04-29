import { useQuery } from '@tanstack/react-query'
import { atlasApi } from '../api/atlas'

export function useCityProfile(stateAbbr?: string) {
  return useQuery({
    queryKey: ['cities', stateAbbr],
    queryFn: () => atlasApi.getCities({ state: stateAbbr, limit: 20 }),
    staleTime: 10 * 60 * 1000,
  })
}
