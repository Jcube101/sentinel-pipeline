import { useQuery } from '@tanstack/react-query'
import { supabase } from '@/lib/supabase'
import type { NaturalEvent, EventFilters } from '@/lib/types'

export function useNaturalEvents(filters: EventFilters) {
  return useQuery({
    queryKey: ['sentinel-events', filters],
    queryFn: async () => {
      if (!supabase) return []
      const since = new Date()
      since.setDate(since.getDate() - filters.days)

      let query = supabase
        .from('events')
        .select(
          'id, external_id, source, category, title, description, severity, severity_value, severity_unit, status, started_at, closed_at, latitude, longitude, place_name, source_url'
        )
        .gte('started_at', since.toISOString())
        .order('started_at', { ascending: false })
        .range(0, 4999)

      if (filters.categories.length > 0) {
        query = query.in('category', filters.categories)
      }
      if (filters.status !== 'all') {
        query = query.eq('status', filters.status)
      }

      const { data, error } = await query
      if (error) throw error
      return (data ?? []) as unknown as NaturalEvent[]
    },
    staleTime: 1000 * 60 * 15,
    enabled: !!supabase,
  })
}
