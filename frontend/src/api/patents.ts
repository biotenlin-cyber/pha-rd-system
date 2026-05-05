import { api } from './client'
import type {
  AIDraftJob,
  Disclosure,
  Draft,
  LinkedPatent,
  OfficeAction,
  Page,
  PatentAnalytics,
  PatentDetail,
  PatentHeatmapCell,
  PatentSummary,
} from '@/types/models'

export interface ListPatentParams {
  q?: string
  legal_status?: string
  country?: string
  grade?: string
  domain?: string
  scenario?: string
  applicant?: string
  tag?: string
  page?: number
  page_size?: number
}

export const listPatents = async (
  params: ListPatentParams = {},
): Promise<Page<PatentSummary>> => {
  const { data } = await api.get<Page<PatentSummary>>('/patents', { params })
  return data
}

export const fetchPatent = async (key: string): Promise<PatentDetail> => {
  const { data } = await api.get<PatentDetail>(`/patents/${encodeURIComponent(key)}`)
  return data
}

export const fetchAnalytics = async (): Promise<PatentAnalytics> => {
  const { data } = await api.get<PatentAnalytics>('/patents/analytics')
  return data
}

export const fetchHeatmap = async (): Promise<PatentHeatmapCell[]> => {
  const { data } = await api.get<PatentHeatmapCell[]>('/patents/analytics/heatmap')
  return data
}

export const fetchDisclosure = async (key: string): Promise<Disclosure | null> => {
  const { data } = await api.get<Disclosure | null>(
    `/patents/${encodeURIComponent(key)}/disclosure`,
  )
  return data
}

export const upsertDisclosure = async (
  key: string,
  payload: Partial<Disclosure>,
): Promise<Disclosure> => {
  const { data } = await api.put<Disclosure>(
    `/patents/${encodeURIComponent(key)}/disclosure`,
    payload,
  )
  return data
}

export const listDrafts = async (key: string): Promise<Draft[]> => {
  const { data } = await api.get<Draft[]>(`/patents/${encodeURIComponent(key)}/drafts`)
  return data
}

export const createDraft = async (
  key: string,
  payload: { section: string; content: string; notes?: string; created_by?: string },
): Promise<Draft> => {
  const { data } = await api.post<Draft>(
    `/patents/${encodeURIComponent(key)}/drafts`,
    payload,
  )
  return data
}

export const reviewDraft = async (
  draftId: number,
  payload: Record<string, unknown>,
): Promise<Draft> => {
  const { data } = await api.post<Draft>(`/patents/drafts/${draftId}/review`, payload)
  return data
}

export const listOAs = async (key: string): Promise<OfficeAction[]> => {
  const { data } = await api.get<OfficeAction[]>(
    `/patents/${encodeURIComponent(key)}/office-actions`,
  )
  return data
}

export const createOA = async (
  key: string,
  payload: Partial<OfficeAction>,
): Promise<OfficeAction> => {
  const { data } = await api.post<OfficeAction>(
    `/patents/${encodeURIComponent(key)}/office-actions`,
    payload,
  )
  return data
}

export const listAIJobs = async (key: string): Promise<AIDraftJob[]> => {
  const { data } = await api.get<AIDraftJob[]>(
    `/patents/${encodeURIComponent(key)}/ai/jobs`,
  )
  return data
}

export const importCSV = async (file: File): Promise<{
  received_rows: number
  inserted: number
  updated: number
  skipped: number
  errors: { line: number; error: string }[]
}> => {
  const fd = new FormData()
  fd.append('file', file)
  const { data } = await api.post('/patents/import-csv', fd)
  return data
}

export const fetchScenarioPatents = async (
  scenarioCode: string,
): Promise<LinkedPatent[]> => {
  const { data } = await api.get<LinkedPatent[]>(
    `/scenarios/${encodeURIComponent(scenarioCode)}/patents`,
  )
  return data
}

export const fetchGradePatents = async (
  gradeCode: string,
): Promise<LinkedPatent[]> => {
  const { data } = await api.get<LinkedPatent[]>(
    `/grades/${encodeURIComponent(gradeCode)}/patents`,
  )
  return data
}

/**
 * Stream AI patent drafting via SSE. Calls onEvent(eventName, data) for each event.
 * Returns an AbortController so caller can cancel.
 */
export const streamAIDraft = (
  key: string,
  payload: {
    scenario: string
    section?: string
    extra_context?: string
    save_as_draft?: boolean
    model?: string
  },
  onEvent: (eventName: string, data: unknown) => void,
): AbortController => {
  const ctrl = new AbortController()
  const baseURL = (api.defaults.baseURL || '/api/v1').replace(/\/$/, '')
  const url = `${baseURL}/patents/${encodeURIComponent(key)}/ai/draft`

  ;(async () => {
    try {
      const resp = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'text/event-stream' },
        body: JSON.stringify(payload),
        signal: ctrl.signal,
      })
      if (!resp.ok || !resp.body) {
        const text = await resp.text().catch(() => '')
        onEvent('error', { message: text || `HTTP ${resp.status}` })
        return
      }
      const reader = resp.body.getReader()
      const decoder = new TextDecoder('utf-8')
      let buffer = ''
      while (true) {
        const { value, done } = await reader.read()
        if (done) break
        buffer += decoder.decode(value, { stream: true })
        let nl
        while ((nl = buffer.indexOf('\n\n')) !== -1) {
          const chunk = buffer.slice(0, nl)
          buffer = buffer.slice(nl + 2)
          const ev: { event: string; data: string } = { event: 'message', data: '' }
          for (const line of chunk.split('\n')) {
            if (line.startsWith('event: ')) ev.event = line.slice(7).trim()
            else if (line.startsWith('data: ')) ev.data += (ev.data ? '\n' : '') + line.slice(6)
          }
          let parsed: unknown = ev.data
          try {
            parsed = JSON.parse(ev.data)
          } catch {
            /* keep as string */
          }
          onEvent(ev.event, parsed)
        }
      }
    } catch (err: unknown) {
      if ((err as Error).name !== 'AbortError') {
        onEvent('error', { message: (err as Error).message })
      }
    }
  })()

  return ctrl
}
