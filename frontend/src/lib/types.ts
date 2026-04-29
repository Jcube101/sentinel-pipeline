export interface NaturalEvent {
  id: string
  external_id: string
  source: string
  category: 'fire' | 'flood' | 'cyclone' | 'earthquake'
  title: string
  description: string | null
  severity: string | null
  severity_value: number | null
  severity_unit: string | null
  status: 'open' | 'closed'
  started_at: string
  closed_at: string | null
  latitude: number
  longitude: number
  place_name: string | null
  source_url: string | null
}

export interface AqiReading {
  id: number
  location_id: string
  location_name: string
  city: string | null
  latitude: number
  longitude: number
  parameter: string
  value: number
  unit: string
  recorded_at: string
}

export interface EventFilters {
  categories: Array<'fire' | 'flood' | 'cyclone' | 'earthquake'>
  status: 'open' | 'closed' | 'all'
  days: 7 | 30 | 90
}

export const CATEGORY_COLORS = {
  fire: '#ef4444',
  flood: '#3b82f6',
  cyclone: '#8b5cf6',
  earthquake: '#f59e0b',
} as const

export const CATEGORY_EMOJIS = {
  fire: '🔥',
  flood: '🌊',
  cyclone: '🌀',
  earthquake: '🌍',
} as const
