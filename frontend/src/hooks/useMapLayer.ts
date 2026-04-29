import { useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'
import { atlasApi } from '../api/atlas'
import { useAtlasStore } from '../store/atlasStore'

export function useMapLayer() {
  const { year, activeLayer, setStates, setLoading } = useAtlasStore()

  const query = useQuery({
    queryKey: ['states', year],
    queryFn: () => atlasApi.getStates(year),
    staleTime: 10 * 60 * 1000,
  })

  useEffect(() => {
    if (query.data) {
      setStates(query.data)
      setLoading(false)
    }
  }, [query.data, setStates, setLoading])

  useEffect(() => {
    if (query.isError) setLoading(false)
  }, [query.isError, setLoading])

  return { ...query, activeLayer }
}
