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

// ── patents ───────────────────────────────────────────────────────────
export interface PatentSummary {
  id: string
  internal_code: string
  publication_no: string | null
  title_zh: string
  country_code: string
  patent_type: string
  legal_status: string
  application_date: string | null
  grant_date: string | null
  primary_applicant: string | null
  first_inventor: string | null
  primary_ipc: string | null
  tags: string[]
}

export interface PatentInventor {
  inventor_id: number
  name_zh: string
  name_en: string | null
  seq: number
  contribution_pct: number | null
  is_corresponding: boolean
}

export interface PatentApplicant {
  applicant_id: number
  name_zh: string
  name_en: string | null
  applicant_type: string
  country_code: string | null
  role: string
  share_pct: number | null
}

export interface PatentClassification {
  id: number
  scheme: string
  code: string
  full_symbol: string | null
  section: string | null
  class_code: string | null
  subclass: string | null
  main_group: string | null
  classification_value: string
  is_primary: boolean
  rank_order: number | null
}

export interface PatentLegalEvent {
  id: number
  event_code: string
  event_date: string
  event_desc: string | null
  source: string | null
}

export interface PatentScenarioLink {
  scenario_id: number
  scenario_code: string
  scenario_name_zh: string
  domain_code: string
  relevance: number
}

export interface PatentGradeLink {
  grade_id: number
  grade_code: string
  grade_name_zh: string
  relevance: number
}

export interface PatentDetail {
  id: string
  internal_code: string
  docdb_key: string | null
  publication_no: string | null
  application_no: string | null
  grant_no: string | null
  title_zh: string
  title_en: string | null
  abstract_zh: string | null
  abstract_en: string | null
  tech_field: string | null
  country_code: string
  patent_type: string
  legal_status: string
  application_route: string
  is_service_invention: boolean
  application_date: string | null
  publication_date: string | null
  grant_date: string | null
  next_annual_fee_due: string | null
  agency_name: string | null
  agent_name: string | null
  internal_owner: string | null
  claim_count: number | null
  independent_claim_count: number | null
  page_count: number | null
  tags: string[]
  inventors: PatentInventor[]
  applicants: PatentApplicant[]
  classifications: PatentClassification[]
  legal_events: PatentLegalEvent[]
  scenarios: PatentScenarioLink[]
  grades: PatentGradeLink[]
  has_disclosure: boolean
  draft_count: number
  oa_count: number
}

export interface Disclosure {
  id: number
  patent_id: string
  submitted_by: string | null
  problem_statement: string | null
  existing_solutions: string | null
  proposed_solution: string | null
  key_points: unknown[]
  advantages: string | null
  embodiments: unknown[]
  attachments: unknown[]
  confidentiality_level: string
  status: string
}

export interface Draft {
  id: number
  patent_id: string
  parent_draft_id: number | null
  amendment_oa_id: number | null
  version: number
  section: string
  content: string
  ai_generated: boolean
  ai_model: string | null
  ai_confidence: string | null
  is_filed: boolean
  filed_at: string | null
  reviewed_by: string | null
  reviewed_at: string | null
  review_score_clarity: number | null
  review_score_essential: number | null
  review_score_generalization: number | null
  review_score_support: number | null
  review_score_chinese: number | null
  review_score_format: number | null
  review_decision: string | null
  review_notes: string | null
  created_at: string
  updated_at: string
}

export interface OfficeAction {
  id: number
  patent_id: string
  action_no: string
  oa_type: string
  received_date: string | null
  due_date: string | null
  examiner_name: string | null
  issues: unknown[]
  response_content: string | null
  responded_at: string | null
  status: string
}

export interface PatentAnalytics {
  total: number
  by_legal_status: SearchFacet[]
  by_country: SearchFacet[]
  by_year: SearchFacet[]
  by_top_applicant: SearchFacet[]
  by_top_inventor: SearchFacet[]
  by_subclass: SearchFacet[]
  by_grade: SearchFacet[]
  by_domain: SearchFacet[]
}

export interface PatentHeatmapCell {
  domain: string
  grade: string
  count: number
}

export interface LinkedPatent {
  id: string
  internal_code: string
  publication_no: string | null
  title_zh: string
  legal_status: string
  country_code: string
  application_date: string | null
  relevance: number
}

export interface AIDraftJob {
  id: string
  scenario: string
  status: string
  model: string | null
  input_tokens: number | null
  output_tokens: number | null
  cache_read_tokens: number | null
  started_at: string | null
  completed_at: string | null
  error: string | null
  result_draft_id: number | null
  preview: string | null
}
