import { useQuery } from '@tanstack/react-query'
import { supabase } from '@/lib/supabase'
import type { AqiReading } from '@/lib/types'

export function useAqiReadings() {
  return useQuery({
    queryKey: ['sentinel-aqi'],
    queryFn: async () => {
      if (!supabase) return []
      const since = new Date()
      since.setDate(since.getDate() - 1)

      const { data, error } = await supabase
        .from('aqi_readings')
        .select('*')
        .gte('recorded_at', since.toISOString())
        .order('recorded_at', { ascending: false })

      if (error) throw error
      return (data ?? []) as unknown as AqiReading[]
    },
    staleTime: 0,
    refetchOnWindowFocus: true,
    enabled: !!supabase,
  })
}
