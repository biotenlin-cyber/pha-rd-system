import { api } from './client'
import type { Grade, GradeDetail, GradeMatchSummary } from '@/types/models'

export const listGrades = async (params: {
  family?: string
  q?: string
} = {}): Promise<Grade[]> => {
  const { data } = await api.get<Grade[]>('/grades', { params })
  return data
}

export const fetchGrade = async (code: string): Promise<GradeDetail> => {
  const { data } = await api.get<GradeDetail>(`/grades/${code}`)
  return data
}

export const fetchGradeRecommendedScenarios = async (
  code: string,
  top = 5,
): Promise<GradeMatchSummary[]> => {
  const { data } = await api.get<GradeMatchSummary[]>(
    `/grades/${code}/recommended-scenarios`,
    { params: { top } },
  )
  return data
}
