import { api } from './client'
import type {
  ExternalLink,
  Page,
  ScenarioDetail,
  ScenarioMatchSummary,
  ScenarioSummary,
} from '@/types/models'

export interface ListScenarioParams {
  domain?: string
  q?: string
  tags?: string[]
  page?: number
  page_size?: number
}

export const listScenarios = async (
  params: ListScenarioParams = {},
): Promise<Page<ScenarioSummary>> => {
  const { data } = await api.get<Page<ScenarioSummary>>('/scenarios', { params })
  return data
}

export const fetchScenario = async (code: string): Promise<ScenarioDetail> => {
  const { data } = await api.get<ScenarioDetail>(`/scenarios/${code}`)
  return data
}

export const fetchScenarioMatches = async (
  code: string,
): Promise<ScenarioMatchSummary[]> => {
  const { data } = await api.get<ScenarioMatchSummary[]>(`/scenarios/${code}/matches`)
  return data
}

export const fetchScenarioExternalLinks = async (
  code: string,
  type?: string,
): Promise<ExternalLink[]> => {
  const { data } = await api.get<ExternalLink[]>(`/scenarios/${code}/external-links`, {
    params: type ? { type } : {},
  })
  return data
}
