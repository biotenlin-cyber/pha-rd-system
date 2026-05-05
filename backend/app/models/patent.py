"""Patents module — designed per Chinese patent practice & informatics review.

Highlights vs naive design:
  * inventors / applicants normalized into entity + link tables (collaboration & aggregation)
  * IPC/CPC classifications keep section/subclass/main_group columns for tech-map
  * patent_citations as graph edges (forward/backward citation analysis)
  * patent_legal_events as time-series (state replay & CNIPA sync ready)
  * docdb_key generated column for cross-source dedup
  * search_vector maintained by trigger (handled in 0002 migration)
"""
from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Any

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    Computed,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import CITEXT, JSONB, TSVECTOR, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

LEGAL_STATUSES = (
    "disclosure",
    "drafting",
    "filed",
    "pre_examination_pending",
    "pre_examination_passed",
    "published_no_substantive_request",
    "substantive_pending",
    "oa_pending",
    "oa_responded",
    "pre_grant_notice",
    "granted",
    "annual_fee_due",
    "lapsed_unpaid",
    "terminated_no_fee",
    "reexamination",
    "invalidation",
    "rejected_final",
    "withdrawn",
    "abandoned",
    "expired",
)
LEGAL_STATUS_CHECK = (
    "legal_status IN ("
    + ", ".join(f"'{s}'" for s in LEGAL_STATUSES)
    + ")"
)


class Patent(Base, TimestampMixin):
    __tablename__ = "patents"
    __table_args__ = (
        CheckConstraint(
            "patent_type IN ('invention','utility_model','design')",
            name="ck_patent_type",
        ),
        CheckConstraint(LEGAL_STATUS_CHECK, name="ck_patent_legal_status"),
        CheckConstraint(
            "application_route IN ('direct','paris','pct_national_phase','pct_international')",
            name="ck_patent_app_route",
        ),
        CheckConstraint(
            "confidentiality_review_status IN ('not_required','pending','passed','restricted')",
            name="ck_patent_confidentiality_review",
        ),
        UniqueConstraint("country_code", "application_no", name="uq_patent_country_appno"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    internal_code: Mapped[str] = mapped_column(CITEXT, unique=True, nullable=False)

    country_code: Mapped[str] = mapped_column(
        String(2), default="CN", server_default="CN", nullable=False
    )
    doc_number: Mapped[str | None] = mapped_column(String(20))
    kind_code: Mapped[str | None] = mapped_column(String(4))
    # docdb_key is a STORED generated column; SQLAlchemy must not write it.
    docdb_key: Mapped[str | None] = mapped_column(
        String(32),
        Computed(
            "country_code || COALESCE(doc_number,'') || COALESCE(kind_code,'')",
            persisted=True,
        ),
    )

    application_no: Mapped[str | None] = mapped_column(String(64))
    publication_no: Mapped[str | None] = mapped_column(String(64))
    grant_no: Mapped[str | None] = mapped_column(String(64))
    priority_no: Mapped[str | None] = mapped_column(String(64))
    pct_no: Mapped[str | None] = mapped_column(String(32))
    parent_application_no: Mapped[str | None] = mapped_column(String(64))

    title_zh: Mapped[str] = mapped_column(String(512), nullable=False)
    title_en: Mapped[str | None] = mapped_column(String(512))
    abstract_zh: Mapped[str | None] = mapped_column(Text)
    abstract_en: Mapped[str | None] = mapped_column(Text)
    tech_field: Mapped[str | None] = mapped_column(Text)

    patent_type: Mapped[str] = mapped_column(
        String(16), default="invention", server_default="invention", nullable=False
    )
    legal_status: Mapped[str] = mapped_column(
        String(32), default="disclosure", server_default="disclosure", nullable=False
    )
    application_route: Mapped[str] = mapped_column(
        String(24), default="direct", server_default="direct", nullable=False
    )
    is_service_invention: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default="true", nullable=False
    )
    is_divisional: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false", nullable=False
    )

    application_date: Mapped[date | None] = mapped_column(Date)
    publication_date: Mapped[date | None] = mapped_column(Date)
    grant_date: Mapped[date | None] = mapped_column(Date)
    expiry_date: Mapped[date | None] = mapped_column(Date)
    next_annual_fee_due: Mapped[date | None] = mapped_column(Date)
    last_paid_annual_fee_year: Mapped[int | None] = mapped_column(SmallInteger)

    family_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))

    confidentiality_review_required: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false", nullable=False
    )
    confidentiality_review_status: Mapped[str] = mapped_column(
        String(16),
        default="not_required",
        server_default="not_required",
        nullable=False,
    )
    confidentiality_review_no: Mapped[str | None] = mapped_column(String(32))
    first_filing_country: Mapped[str | None] = mapped_column(String(2))

    agency_name: Mapped[str | None] = mapped_column(String(256))
    agent_name: Mapped[str | None] = mapped_column(String(128))
    internal_owner: Mapped[str | None] = mapped_column(String(128))

    claim_count: Mapped[int | None] = mapped_column(Integer)
    independent_claim_count: Mapped[int | None] = mapped_column(Integer)
    page_count: Mapped[int | None] = mapped_column(Integer)

    tags: Mapped[list[str]] = mapped_column(JSONB, default=list, server_default="[]")
    extras: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, server_default="{}")
    search_vector: Mapped[Any | None] = mapped_column(TSVECTOR)

    classifications = relationship(
        "PatentClassification", back_populates="patent", cascade="all, delete-orphan"
    )
    priorities = relationship(
        "PatentPriority", back_populates="patent", cascade="all, delete-orphan"
    )
    inventor_links = relationship(
        "PatentInventor", back_populates="patent", cascade="all, delete-orphan"
    )
    applicant_links = relationship(
        "PatentApplicant", back_populates="patent", cascade="all, delete-orphan"
    )
    legal_events = relationship(
        "PatentLegalEvent", back_populates="patent", cascade="all, delete-orphan"
    )
    citations = relationship(
        "PatentCitation",
        back_populates="citing_patent",
        foreign_keys="PatentCitation.citing_patent_id",
        cascade="all, delete-orphan",
    )
    disclosure = relationship(
        "PatentDisclosure",
        back_populates="patent",
        cascade="all, delete-orphan",
        uselist=False,
    )
    drafts = relationship(
        "PatentDraft", back_populates="patent", cascade="all, delete-orphan"
    )
    office_actions = relationship(
        "PatentOfficeAction", back_populates="patent", cascade="all, delete-orphan"
    )
    prior_art_searches = relationship(
        "PatentPriorArtSearch",
        back_populates="patent",
        cascade="all, delete-orphan",
    )
    fee_events = relationship(
        "PatentFeeEvent", back_populates="patent", cascade="all, delete-orphan"
    )
    draft_jobs = relationship(
        "PatentDraftJob", back_populates="patent", cascade="all, delete-orphan"
    )
    scenario_links = relationship(
        "PatentScenario", back_populates="patent", cascade="all, delete-orphan"
    )
    grade_links = relationship(
        "PatentGrade", back_populates="patent", cascade="all, delete-orphan"
    )


class Inventor(Base, TimestampMixin):
    __tablename__ = "inventors"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name_zh: Mapped[str] = mapped_column(String(128), nullable=False)
    name_en: Mapped[str | None] = mapped_column(String(128))
    normalized_key: Mapped[str] = mapped_column(String(160), unique=True, nullable=False)
    nationality: Mapped[str | None] = mapped_column(String(2))
    notes: Mapped[str | None] = mapped_column(Text)


class Applicant(Base, TimestampMixin):
    __tablename__ = "applicants"
    __table_args__ = (
        CheckConstraint(
            "applicant_type IN ('individual','company','university','research_institute','government','other')",
            name="ck_applicant_type",
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name_zh: Mapped[str] = mapped_column(String(256), nullable=False)
    name_en: Mapped[str | None] = mapped_column(String(256))
    normalized_key: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)
    applicant_type: Mapped[str] = mapped_column(
        String(24), default="company", server_default="company", nullable=False
    )
    country_code: Mapped[str | None] = mapped_column(String(2))
    uscc: Mapped[str | None] = mapped_column(String(32))
    address: Mapped[str | None] = mapped_column(Text)


class PatentInventor(Base):
    __tablename__ = "patent_inventors"

    patent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("patents.id", ondelete="CASCADE"), primary_key=True
    )
    inventor_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("inventors.id", ondelete="CASCADE"), primary_key=True
    )
    seq: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    contribution_pct: Mapped[float | None] = mapped_column(Numeric(5, 2))
    is_corresponding: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false", nullable=False
    )
    notes: Mapped[str | None] = mapped_column(Text)

    patent = relationship("Patent", back_populates="inventor_links")
    inventor = relationship("Inventor")


class PatentApplicant(Base):
    __tablename__ = "patent_applicants"
    __table_args__ = (
        CheckConstraint(
            "role IN ('primary','co','assignee')", name="ck_patent_applicant_role"
        ),
    )

    patent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("patents.id", ondelete="CASCADE"), primary_key=True
    )
    applicant_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("applicants.id", ondelete="CASCADE"), primary_key=True
    )
    role: Mapped[str] = mapped_column(
        String(16), default="primary", server_default="primary", nullable=False
    )
    share_pct: Mapped[float | None] = mapped_column(Numeric(5, 2))
    notes: Mapped[str | None] = mapped_column(Text)

    patent = relationship("Patent", back_populates="applicant_links")
    applicant = relationship("Applicant")


class PatentClassification(Base):
    __tablename__ = "patent_classifications"
    __table_args__ = (
        CheckConstraint("scheme IN ('IPC','CPC')", name="ck_patent_classif_scheme"),
        CheckConstraint(
            "classification_value IN ('inventive','additional','further')",
            name="ck_patent_classif_value",
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    patent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("patents.id", ondelete="CASCADE"), nullable=False
    )
    scheme: Mapped[str] = mapped_column(String(8), nullable=False)
    code: Mapped[str] = mapped_column(String(32), nullable=False)
    full_symbol: Mapped[str | None] = mapped_column(String(32))
    section: Mapped[str | None] = mapped_column(String(1))
    class_code: Mapped[str | None] = mapped_column(String(3))
    subclass: Mapped[str | None] = mapped_column(String(4))
    main_group: Mapped[str | None] = mapped_column(String(8))
    classification_value: Mapped[str] = mapped_column(
        String(16),
        default="inventive",
        server_default="inventive",
        nullable=False,
    )
    rank_order: Mapped[int | None] = mapped_column(SmallInteger)
    is_primary: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false", nullable=False
    )

    patent = relationship("Patent", back_populates="classifications")


class PatentPriority(Base):
    __tablename__ = "patent_priorities"
    __table_args__ = (
        CheckConstraint(
            "priority_type IN ('paris','domestic','pct')",
            name="ck_patent_priority_type",
        ),
        CheckConstraint(
            "claim_status IN ('claimed','restored','withdrawn')",
            name="ck_patent_priority_status",
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    patent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("patents.id", ondelete="CASCADE"), nullable=False
    )
    priority_type: Mapped[str] = mapped_column(String(16), nullable=False)
    priority_no: Mapped[str] = mapped_column(String(64), nullable=False)
    priority_date: Mapped[date | None] = mapped_column(Date)
    priority_country: Mapped[str | None] = mapped_column(String(2))
    claim_status: Mapped[str] = mapped_column(
        String(16), default="claimed", server_default="claimed", nullable=False
    )

    patent = relationship("Patent", back_populates="priorities")


class PatentLegalEvent(Base):
    __tablename__ = "patent_legal_events"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    patent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("patents.id", ondelete="CASCADE"), nullable=False
    )
    event_code: Mapped[str] = mapped_column(String(16), nullable=False)
    event_date: Mapped[date] = mapped_column(Date, nullable=False)
    event_desc: Mapped[str | None] = mapped_column(Text)
    source: Mapped[str | None] = mapped_column(String(32))
    evidence_url: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=__import__("sqlalchemy").func.now(), nullable=False
    )

    patent = relationship("Patent", back_populates="legal_events")


class PatentCitation(Base):
    __tablename__ = "patent_citations"
    __table_args__ = (
        CheckConstraint(
            "citation_type IN ('X','Y','A','D','E','I','O','P','T')",
            name="ck_patent_citation_type",
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    citing_patent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("patents.id", ondelete="CASCADE"), nullable=False
    )
    cited_patent_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("patents.id", ondelete="SET NULL")
    )
    cited_docdb_key: Mapped[str | None] = mapped_column(String(32))
    cited_npl_text: Mapped[str | None] = mapped_column(Text)
    citation_type: Mapped[str] = mapped_column(
        String(2), default="A", server_default="A", nullable=False
    )
    by_examiner: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false", nullable=False
    )
    citation_phase: Mapped[str | None] = mapped_column(String(16))
    notes: Mapped[str | None] = mapped_column(Text)

    citing_patent = relationship(
        "Patent", back_populates="citations", foreign_keys=[citing_patent_id]
    )
    cited_patent = relationship("Patent", foreign_keys=[cited_patent_id])


class PatentDisclosure(Base, TimestampMixin):
    __tablename__ = "patent_disclosures"
    __table_args__ = (
        CheckConstraint(
            "status IN ('submitted','reviewing','approved','rejected')",
            name="ck_disclosure_status",
        ),
        CheckConstraint(
            "confidentiality_level IN ('public','internal','secret','top_secret')",
            name="ck_disclosure_confidentiality",
        ),
        UniqueConstraint("patent_id", name="uq_disclosure_patent"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    patent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("patents.id", ondelete="CASCADE"), nullable=False
    )
    submitted_by: Mapped[str | None] = mapped_column(String(128))
    problem_statement: Mapped[str | None] = mapped_column(Text)
    existing_solutions: Mapped[str | None] = mapped_column(Text)
    proposed_solution: Mapped[str | None] = mapped_column(Text)
    key_points: Mapped[list[Any]] = mapped_column(JSONB, default=list, server_default="[]")
    advantages: Mapped[str | None] = mapped_column(Text)
    embodiments: Mapped[list[Any]] = mapped_column(JSONB, default=list, server_default="[]")
    attachments: Mapped[list[Any]] = mapped_column(JSONB, default=list, server_default="[]")
    confidentiality_level: Mapped[str] = mapped_column(
        String(16),
        default="internal",
        server_default="internal",
        nullable=False,
    )
    access_whitelist: Mapped[list[str]] = mapped_column(
        JSONB, default=list, server_default="[]"
    )
    status: Mapped[str] = mapped_column(
        String(16), default="submitted", server_default="submitted", nullable=False
    )

    patent = relationship("Patent", back_populates="disclosure")


DRAFT_SECTIONS = (
    "title",
    "claims",
    "abstract",
    "description",
    "background",
    "summary",
    "embodiments",
    "technical_effect",
    "figures_caption",
    "reference_signs",
    "sequence_listing",
    "abstract_figure",
)


class PatentDraft(Base, TimestampMixin):
    __tablename__ = "patent_drafts"
    __table_args__ = (
        CheckConstraint(
            "section IN (" + ", ".join(f"'{s}'" for s in DRAFT_SECTIONS) + ")",
            name="ck_draft_section",
        ),
        CheckConstraint(
            "review_decision IS NULL OR review_decision IN "
            "('accept','minor_edit','major_rewrite','reject')",
            name="ck_draft_review_decision",
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    patent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("patents.id", ondelete="CASCADE"), nullable=False
    )
    parent_draft_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("patent_drafts.id", ondelete="SET NULL")
    )
    amendment_oa_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("patent_office_actions.id", ondelete="SET NULL")
    )
    version: Mapped[int] = mapped_column(Integer, default=1, server_default="1", nullable=False)
    section: Mapped[str] = mapped_column(String(24), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    ai_generated: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false", nullable=False
    )
    ai_model: Mapped[str | None] = mapped_column(String(64))
    ai_confidence: Mapped[str | None] = mapped_column(String(16))
    created_by: Mapped[str | None] = mapped_column(String(128))
    is_filed: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false", nullable=False
    )
    filed_at: Mapped[date | None] = mapped_column(Date)
    reviewed_by: Mapped[str | None] = mapped_column(String(128))
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    review_score_clarity: Mapped[int | None] = mapped_column(SmallInteger)
    review_score_essential: Mapped[int | None] = mapped_column(SmallInteger)
    review_score_generalization: Mapped[int | None] = mapped_column(SmallInteger)
    review_score_support: Mapped[int | None] = mapped_column(SmallInteger)
    review_score_chinese: Mapped[int | None] = mapped_column(SmallInteger)
    review_score_format: Mapped[int | None] = mapped_column(SmallInteger)
    review_decision: Mapped[str | None] = mapped_column(String(16))
    review_notes: Mapped[str | None] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text)

    patent = relationship("Patent", back_populates="drafts")


class PatentOfficeAction(Base, TimestampMixin):
    __tablename__ = "patent_office_actions"
    __table_args__ = (
        CheckConstraint(
            "status IN ('received','responding','responded','closed')",
            name="ck_oa_status",
        ),
        CheckConstraint(
            "oa_type IN ('notice_to_make_correction','first_oa','second_oa',"
            "'nth_oa','pre_grant_notice','divisional_notice','reexamination','invalidation')",
            name="ck_oa_type",
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    patent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("patents.id", ondelete="CASCADE"), nullable=False
    )
    action_no: Mapped[str] = mapped_column(String(16), default="1", server_default="1")
    oa_type: Mapped[str] = mapped_column(
        String(32), default="first_oa", server_default="first_oa", nullable=False
    )
    received_date: Mapped[date | None] = mapped_column(Date)
    due_date: Mapped[date | None] = mapped_column(Date)
    extension_requested: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false", nullable=False
    )
    extension_until: Mapped[date | None] = mapped_column(Date)
    examiner_name: Mapped[str | None] = mapped_column(String(128))
    issues: Mapped[list[Any]] = mapped_column(JSONB, default=list, server_default="[]")
    response_content: Mapped[str | None] = mapped_column(Text)
    responded_at: Mapped[date | None] = mapped_column(Date)
    status: Mapped[str] = mapped_column(
        String(16), default="received", server_default="received", nullable=False
    )

    patent = relationship("Patent", back_populates="office_actions")


class PatentPriorArtSearch(Base, TimestampMixin):
    __tablename__ = "patent_prior_art_searches"
    __table_args__ = (
        CheckConstraint(
            "novelty IN ('high','medium','low','unknown')", name="ck_prior_art_novelty"
        ),
        CheckConstraint(
            "inventiveness IN ('high','medium','low','unknown')",
            name="ck_prior_art_inventiveness",
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    patent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("patents.id", ondelete="CASCADE"), nullable=False
    )
    searched_by: Mapped[str | None] = mapped_column(String(128))
    searched_at: Mapped[date | None] = mapped_column(Date)
    databases: Mapped[list[str]] = mapped_column(JSONB, default=list, server_default="[]")
    keywords: Mapped[list[str]] = mapped_column(JSONB, default=list, server_default="[]")
    findings: Mapped[str | None] = mapped_column(Text)
    novelty: Mapped[str] = mapped_column(
        String(16), default="unknown", server_default="unknown", nullable=False
    )
    inventiveness: Mapped[str] = mapped_column(
        String(16), default="unknown", server_default="unknown", nullable=False
    )
    cited_documents: Mapped[list[Any]] = mapped_column(
        JSONB, default=list, server_default="[]"
    )
    recommendations: Mapped[str | None] = mapped_column(Text)

    patent = relationship("Patent", back_populates="prior_art_searches")


class PatentFeeEvent(Base, TimestampMixin):
    __tablename__ = "patent_fee_events"
    __table_args__ = (
        CheckConstraint(
            "fee_type IN ('application','publication','substantive_exam','grant','annual',"
            "'reexamination','invalidation','other')",
            name="ck_fee_type",
        ),
        CheckConstraint(
            "status IN ('pending','paid','overdue','waived','reduced')", name="ck_fee_status"
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    patent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("patents.id", ondelete="CASCADE"), nullable=False
    )
    fee_type: Mapped[str] = mapped_column(String(24), nullable=False)
    year_no: Mapped[int | None] = mapped_column(SmallInteger)
    amount: Mapped[float | None] = mapped_column(Numeric(12, 2))
    due_date: Mapped[date | None] = mapped_column(Date)
    paid_date: Mapped[date | None] = mapped_column(Date)
    status: Mapped[str] = mapped_column(
        String(16), default="pending", server_default="pending", nullable=False
    )
    notes: Mapped[str | None] = mapped_column(Text)

    patent = relationship("Patent", back_populates="fee_events")


class PatentDraftJob(Base, TimestampMixin):
    __tablename__ = "patent_draft_jobs"
    __table_args__ = (
        CheckConstraint(
            "status IN ('pending','streaming','done','cancelled','failed')",
            name="ck_draft_job_status",
        ),
        CheckConstraint(
            "scenario IN ('claims_from_disclosure','dependent_claims','spec_from_claims','oa_response')",
            name="ck_draft_job_scenario",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    patent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("patents.id", ondelete="CASCADE"), nullable=False
    )
    scenario: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(
        String(16), default="pending", server_default="pending", nullable=False
    )
    model: Mapped[str | None] = mapped_column(String(64))
    input_tokens: Mapped[int | None] = mapped_column(Integer)
    output_tokens: Mapped[int | None] = mapped_column(Integer)
    cache_read_tokens: Mapped[int | None] = mapped_column(Integer)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    error: Mapped[str | None] = mapped_column(Text)
    result_draft_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("patent_drafts.id", ondelete="SET NULL")
    )
    request_payload: Mapped[dict[str, Any]] = mapped_column(
        JSONB, default=dict, server_default="{}"
    )
    result_payload: Mapped[dict[str, Any]] = mapped_column(
        JSONB, default=dict, server_default="{}"
    )

    patent = relationship("Patent", back_populates="draft_jobs")


class PatentScenario(Base):
    __tablename__ = "patent_scenarios"

    patent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("patents.id", ondelete="CASCADE"),
        primary_key=True,
    )
    scenario_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("application_scenarios.id", ondelete="CASCADE"),
        primary_key=True,
    )
    relevance: Mapped[int] = mapped_column(SmallInteger, default=3, server_default="3")
    notes: Mapped[str | None] = mapped_column(Text)

    patent = relationship("Patent", back_populates="scenario_links")
    scenario = relationship("ApplicationScenario")


class PatentGrade(Base):
    __tablename__ = "patent_grades"

    patent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("patents.id", ondelete="CASCADE"),
        primary_key=True,
    )
    grade_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("pha_grades.id", ondelete="CASCADE"),
        primary_key=True,
    )
    relevance: Mapped[int] = mapped_column(SmallInteger, default=3, server_default="3")
    notes: Mapped[str | None] = mapped_column(Text)

    patent = relationship("Patent", back_populates="grade_links")
    grade = relationship("PhaGrade")
