import { api } from './client'
import type { SearchResponse } from '@/types/models'

export interface SearchParams {
  q?: string
  domain?: string
  grade?: string
  tags?: string[]
  types?: string[]
  page?: number
  page_size?: number
}

export const search = async (params: SearchParams): Promise<SearchResponse> => {
  const { data } = await api.get<SearchResponse>('/search', { params })
  return data
}
