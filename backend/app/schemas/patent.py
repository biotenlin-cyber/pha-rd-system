"""Pydantic schemas for the patents module."""
from datetime import date, datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


# ── entities ──────────────────────────────────────────────────────────────
class InventorBase(BaseModel):
    name_zh: str
    name_en: str | None = None
    nationality: str | None = None
    notes: str | None = None


class Inventor(InventorBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    normalized_key: str


class ApplicantBase(BaseModel):
    name_zh: str
    name_en: str | None = None
    applicant_type: str = "company"
    country_code: str | None = None
    uscc: str | None = None
    address: str | None = None


class Applicant(ApplicantBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    normalized_key: str


# ── patent associations (read shape) ─────────────────────────────────────
class PatentInventorRead(BaseModel):
    inventor_id: int
    name_zh: str
    name_en: str | None = None
    seq: int
    contribution_pct: float | None = None
    is_corresponding: bool = False


class PatentApplicantRead(BaseModel):
    applicant_id: int
    name_zh: str
    name_en: str | None = None
    applicant_type: str
    country_code: str | None = None
    role: str
    share_pct: float | None = None


class PatentClassificationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    scheme: str
    code: str
    full_symbol: str | None = None
    section: str | None = None
    class_code: str | None = None
    subclass: str | None = None
    main_group: str | None = None
    classification_value: str = "inventive"
    rank_order: int | None = None
    is_primary: bool = False


class PatentClassificationWrite(BaseModel):
    scheme: str = "IPC"
    code: str
    is_primary: bool = False


class PatentPriorityRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    priority_type: str
    priority_no: str
    priority_date: date | None = None
    priority_country: str | None = None
    claim_status: str = "claimed"


class PatentLegalEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    event_code: str
    event_date: date
    event_desc: str | None = None
    source: str | None = None


class PatentCitationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    citing_patent_id: UUID
    cited_patent_id: UUID | None = None
    cited_docdb_key: str | None = None
    cited_npl_text: str | None = None
    citation_type: str
    by_examiner: bool = False
    citation_phase: str | None = None


# ── patents ──────────────────────────────────────────────────────────────
class PatentBase(BaseModel):
    internal_code: str
    country_code: str = "CN"
    doc_number: str | None = None
    kind_code: str | None = None
    application_no: str | None = None
    publication_no: str | None = None
    grant_no: str | None = None
    priority_no: str | None = None
    pct_no: str | None = None
    parent_application_no: str | None = None
    title_zh: str
    title_en: str | None = None
    abstract_zh: str | None = None
    abstract_en: str | None = None
    tech_field: str | None = None
    patent_type: str = "invention"
    legal_status: str = "disclosure"
    application_route: str = "direct"
    is_service_invention: bool = True
    is_divisional: bool = False
    application_date: date | None = None
    publication_date: date | None = None
    grant_date: date | None = None
    expiry_date: date | None = None
    next_annual_fee_due: date | None = None
    last_paid_annual_fee_year: int | None = None
    family_id: UUID | None = None
    confidentiality_review_required: bool = False
    confidentiality_review_status: str = "not_required"
    confidentiality_review_no: str | None = None
    first_filing_country: str | None = None
    agency_name: str | None = None
    agent_name: str | None = None
    internal_owner: str | None = None
    claim_count: int | None = None
    independent_claim_count: int | None = None
    page_count: int | None = None
    tags: list[str] = []


class PatentCreate(PatentBase):
    inventors: list[dict[str, Any]] = []
    applicants: list[dict[str, Any]] = []
    classifications: list[PatentClassificationWrite] = []
    scenario_codes: list[str] = []
    grade_codes: list[str] = []


class PatentUpdate(BaseModel):
    title_zh: str | None = None
    title_en: str | None = None
    abstract_zh: str | None = None
    abstract_en: str | None = None
    tech_field: str | None = None
    legal_status: str | None = None
    application_date: date | None = None
    publication_date: date | None = None
    grant_date: date | None = None
    expiry_date: date | None = None
    next_annual_fee_due: date | None = None
    agency_name: str | None = None
    agent_name: str | None = None
    internal_owner: str | None = None
    claim_count: int | None = None
    independent_claim_count: int | None = None
    page_count: int | None = None
    tags: list[str] | None = None
    confidentiality_review_status: str | None = None


class PatentSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    internal_code: str
    publication_no: str | None = None
    title_zh: str
    country_code: str
    patent_type: str
    legal_status: str
    application_date: date | None = None
    grant_date: date | None = None
    primary_applicant: str | None = None
    first_inventor: str | None = None
    primary_ipc: str | None = None
    tags: list[str] = []


class PatentScenarioRead(BaseModel):
    scenario_id: int
    scenario_code: str
    scenario_name_zh: str
    domain_code: str
    relevance: int = 3


class PatentGradeRead(BaseModel):
    grade_id: int
    grade_code: str
    grade_name_zh: str
    relevance: int = 3


class PatentDetail(PatentBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    docdb_key: str | None = None
    inventors: list[PatentInventorRead] = []
    applicants: list[PatentApplicantRead] = []
    classifications: list[PatentClassificationRead] = []
    priorities: list[PatentPriorityRead] = []
    legal_events: list[PatentLegalEventRead] = []
    scenarios: list[PatentScenarioRead] = []
    grades: list[PatentGradeRead] = []
    has_disclosure: bool = False
    draft_count: int = 0
    oa_count: int = 0


# ── disclosure ───────────────────────────────────────────────────────────
class DisclosureBase(BaseModel):
    submitted_by: str | None = None
    problem_statement: str | None = None
    existing_solutions: str | None = None
    proposed_solution: str | None = None
    key_points: list[Any] = []
    advantages: str | None = None
    embodiments: list[Any] = []
    attachments: list[Any] = []
    confidentiality_level: str = "internal"
    access_whitelist: list[str] = []
    status: str = "submitted"


class DisclosureCreate(DisclosureBase):
    pass


class Disclosure(DisclosureBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    patent_id: UUID


# ── draft ────────────────────────────────────────────────────────────────
class DraftBase(BaseModel):
    section: str
    content: str
    notes: str | None = None
    ai_generated: bool = False
    ai_model: str | None = None
    ai_confidence: str | None = None
    created_by: str | None = None


class DraftCreate(DraftBase):
    parent_draft_id: int | None = None
    amendment_oa_id: int | None = None


class DraftReview(BaseModel):
    review_score_clarity: int | None = Field(None, ge=1, le=5)
    review_score_essential: int | None = Field(None, ge=1, le=5)
    review_score_generalization: int | None = Field(None, ge=1, le=5)
    review_score_support: int | None = Field(None, ge=1, le=5)
    review_score_chinese: int | None = Field(None, ge=1, le=5)
    review_score_format: int | None = Field(None, ge=1, le=5)
    review_decision: str | None = None
    review_notes: str | None = None
    reviewed_by: str | None = None


class Draft(DraftBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    patent_id: UUID
    parent_draft_id: int | None = None
    amendment_oa_id: int | None = None
    version: int
    is_filed: bool = False
    filed_at: date | None = None
    reviewed_by: str | None = None
    reviewed_at: datetime | None = None
    review_score_clarity: int | None = None
    review_score_essential: int | None = None
    review_score_generalization: int | None = None
    review_score_support: int | None = None
    review_score_chinese: int | None = None
    review_score_format: int | None = None
    review_decision: str | None = None
    review_notes: str | None = None
    created_at: datetime
    updated_at: datetime


# ── office action ────────────────────────────────────────────────────────
class OfficeActionBase(BaseModel):
    action_no: str = "1"
    oa_type: str = "first_oa"
    received_date: date | None = None
    due_date: date | None = None
    extension_requested: bool = False
    extension_until: date | None = None
    examiner_name: str | None = None
    issues: list[Any] = []
    response_content: str | None = None
    responded_at: date | None = None
    status: str = "received"


class OfficeActionCreate(OfficeActionBase):
    pass


class OfficeAction(OfficeActionBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    patent_id: UUID


# ── prior art ────────────────────────────────────────────────────────────
class PriorArtBase(BaseModel):
    searched_by: str | None = None
    searched_at: date | None = None
    databases: list[str] = []
    keywords: list[str] = []
    findings: str | None = None
    novelty: str = "unknown"
    inventiveness: str = "unknown"
    cited_documents: list[Any] = []
    recommendations: str | None = None


class PriorArtCreate(PriorArtBase):
    pass


class PriorArt(PriorArtBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    patent_id: UUID


# ── AI drafting ──────────────────────────────────────────────────────────
class AIDraftRequest(BaseModel):
    scenario: str  # claims_from_disclosure / dependent_claims / spec_from_claims / oa_response
    section: str = "claims"
    extra_context: str | None = None
    target_grade_code: str | None = None
    target_scenario_code: str | None = None
    save_as_draft: bool = True
    model: str | None = None  # default chosen by service


class AIDraftJob(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    patent_id: UUID
    scenario: str
    status: str
    model: str | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    cache_read_tokens: int | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    error: str | None = None
    result_draft_id: int | None = None


# ── analytics ────────────────────────────────────────────────────────────
class FacetCount(BaseModel):
    code: str
    name_zh: str | None = None
    count: int


class AnalyticsResponse(BaseModel):
    total: int
    by_legal_status: list[FacetCount]
    by_country: list[FacetCount]
    by_year: list[FacetCount]  # code = year string
    by_top_applicant: list[FacetCount]
    by_top_inventor: list[FacetCount]
    by_subclass: list[FacetCount]
    by_grade: list[FacetCount]
    by_domain: list[FacetCount]


# ── search ───────────────────────────────────────────────────────────────
class PatentSearchHit(BaseModel):
    id: UUID
    internal_code: str
    publication_no: str | None = None
    title_zh: str
    snippet: str | None = None
    legal_status: str
    score: float


class PatentSearchResponse(BaseModel):
    meta: dict[str, Any]
    facets: dict[str, list[FacetCount]]
    data: list[PatentSearchHit]


# ── csv import ───────────────────────────────────────────────────────────
class CSVImportResult(BaseModel):
    received_rows: int
    inserted: int
    updated: int
    skipped: int
    errors: list[dict[str, Any]] = []
