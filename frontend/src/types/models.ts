export interface Pagination {
  page: number
  page_size: number
  total: number
}

export interface Page<T> {
  data: T[]
  meta: Pagination
}

export interface Tag {
  id: number
  slug: string
  name_zh: string
  category: string | null
  color: string | null
}

export interface Domain {
  id: number
  code: string
  name_zh: string
  name_en: string
  description: string | null
  icon: string | null
  sort_order: number
  scenario_count: number
}

export interface ScenarioSummary {
  id: number
  code: string
  name_zh: string
  domain_code: string
  summary: string | null
  tags: Tag[]
  top_match_grade: string | null
}

export interface ScenarioMatchSummary {
  grade_id: number
  grade_code: string
  grade_name_zh: string
  match_score: number
  recommendation_level: string
  key_metrics: Record<string, unknown>
  rationale: string | null
}

export interface ExternalLink {
  id: number
  link_type: string
  external_ref: string
  label: string | null
  meta: Record<string, unknown>
}

export interface ScenarioDetail {
  id: number
  domain_id: number
  domain_code: string
  code: string
  name_zh: string
  name_en: string | null
  summary: string | null
  sub_scenarios: unknown[]
  technical_requirements: Record<string, unknown>
  typical_products: unknown[]
  market_size_usd: number | null
  market_year: number | null
  market_notes: string | null
  status: string
  tags: Tag[]
  matches: ScenarioMatchSummary[]
  external_links: ExternalLink[]
}

export interface Grade {
  id: number
  code: string
  name_zh: string
  full_name: string | null
  polymer_family: string | null
  description: string | null
  tm_celsius: number | null
  tg_celsius: number | null
  crystallinity_pct: number | null
  elongation_at_break_pct: number | null
  tensile_strength_mpa: number | null
  youngs_modulus_gpa: number | null
  biocompatibility_class: string | null
  degradation_months_soil: number | null
  degradation_months_marine: number | null
  extra_metrics: Record<string, unknown>
  typical_processing: unknown[]
  status: string
}

export interface GradeMatchSummary {
  scenario_id: number
  scenario_code: string
  scenario_name_zh: string
  domain_code: string
  match_score: number
  recommendation_level: string
  key_metrics: Record<string, unknown>
  rationale: string | null
}

export interface GradeDetail extends Grade {
  matches: GradeMatchSummary[]
}

export interface SearchHit {
  type: 'scenario' | 'grade'
  id: number
  code: string
  name_zh: string
  snippet: string | null
  score: number
  domain_code: string | null
}

export interface SearchFacet {
  code: string
  count: number
}

export interface SearchResponse {
  meta: { total: number; page: number; page_size: number; took_ms: number }
  facets: { domain: SearchFacet[]; tag: SearchFacet[]; type: SearchFacet[] }
  data: SearchHit[]
}
