import { api } from './client'
import type { Domain } from '@/types/models'

export const fetchDomains = async (): Promise<Domain[]> => {
  const { data } = await api.get<Domain[]>('/domains')
  return data
}

export const fetchDomain = async (code: string): Promise<Domain> => {
  const { data } = await api.get<Domain>(`/domains/${code}`)
  return data
}
