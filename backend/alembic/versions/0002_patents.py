"""patents module — designed per CN-patent practice & informatics review

Tables:
  inventors / applicants (entity tables)
  patents (main, with GENERATED docdb_key)
  patent_inventors / patent_applicants (M:N with role/seq/contribution)
  patent_classifications (IPC/CPC with section/subclass/main_group)
  patent_priorities / patent_legal_events / patent_citations
  patent_disclosures / patent_drafts / patent_office_actions
  patent_prior_art_searches / patent_fee_events
  patent_draft_jobs (AI streaming jobs)
  patent_scenarios / patent_grades (M:N to existing module)

Plus: patents.search_vector maintained by trigger (weighted A/B/C).

Revision ID: 0002_patents
Revises: 0001_init
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0002_patents"
down_revision: str | None = "0001_init"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


_LEGAL_STATUSES = (
    "disclosure", "drafting", "filed",
    "pre_examination_pending", "pre_examination_passed",
    "published_no_substantive_request", "substantive_pending",
    "oa_pending", "oa_responded", "pre_grant_notice",
    "granted", "annual_fee_due", "lapsed_unpaid", "terminated_no_fee",
    "reexamination", "invalidation", "rejected_final",
    "withdrawn", "abandoned", "expired",
)
_LEGAL_STATUS_CHECK = "legal_status IN (" + ", ".join(f"'{s}'" for s in _LEGAL_STATUSES) + ")"

_DRAFT_SECTIONS = (
    "title", "claims", "abstract", "description",
    "background", "summary", "embodiments", "technical_effect",
    "figures_caption", "reference_signs", "sequence_listing", "abstract_figure",
)
_DRAFT_SECTION_CHECK = (
    "section IN (" + ", ".join(f"'{s}'" for s in _DRAFT_SECTIONS) + ")"
)


def upgrade() -> None:
    # ── entity tables ────────────────────────────────────────────────────
    op.create_table(
        "inventors",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("name_zh", sa.String(128), nullable=False),
        sa.Column("name_en", sa.String(128)),
        sa.Column("normalized_key", sa.String(160), nullable=False),
        sa.Column("nationality", sa.String(2)),
        sa.Column("notes", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("normalized_key", name="uq_inventors_normalized_key"),
    )

    op.create_table(
        "applicants",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("name_zh", sa.String(256), nullable=False),
        sa.Column("name_en", sa.String(256)),
        sa.Column("normalized_key", sa.String(320), nullable=False),
        sa.Column("applicant_type", sa.String(24), server_default="company", nullable=False),
        sa.Column("country_code", sa.String(2)),
        sa.Column("uscc", sa.String(32)),
        sa.Column("address", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("normalized_key", name="uq_applicants_normalized_key"),
        sa.CheckConstraint(
            "applicant_type IN ('individual','company','university','research_institute',"
            "'government','other')",
            name="ck_applicant_type",
        ),
    )

    # ── patents main ─────────────────────────────────────────────────────
    op.create_table(
        "patents",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("internal_code", postgresql.CITEXT(), nullable=False),
        sa.Column("country_code", sa.String(2), server_default="CN", nullable=False),
        sa.Column("doc_number", sa.String(20)),
        sa.Column("kind_code", sa.String(4)),
        # docdb_key as STORED generated column — added via raw SQL after create_table
        sa.Column("application_no", sa.String(64)),
        sa.Column("publication_no", sa.String(64)),
        sa.Column("grant_no", sa.String(64)),
        sa.Column("priority_no", sa.String(64)),
        sa.Column("pct_no", sa.String(32)),
        sa.Column("parent_application_no", sa.String(64)),
        sa.Column("title_zh", sa.String(512), nullable=False),
        sa.Column("title_en", sa.String(512)),
        sa.Column("abstract_zh", sa.Text()),
        sa.Column("abstract_en", sa.Text()),
        sa.Column("tech_field", sa.Text()),
        sa.Column("patent_type", sa.String(16), server_default="invention", nullable=False),
        sa.Column("legal_status", sa.String(32), server_default="disclosure", nullable=False),
        sa.Column("application_route", sa.String(24), server_default="direct", nullable=False),
        sa.Column("is_service_invention", sa.Boolean(), server_default="true", nullable=False),
        sa.Column("is_divisional", sa.Boolean(), server_default="false", nullable=False),
        sa.Column("application_date", sa.Date()),
        sa.Column("publication_date", sa.Date()),
        sa.Column("grant_date", sa.Date()),
        sa.Column("expiry_date", sa.Date()),
        sa.Column("next_annual_fee_due", sa.Date()),
        sa.Column("last_paid_annual_fee_year", sa.SmallInteger()),
        sa.Column("family_id", postgresql.UUID(as_uuid=True)),
        sa.Column("confidentiality_review_required", sa.Boolean(), server_default="false", nullable=False),
        sa.Column("confidentiality_review_status", sa.String(16), server_default="not_required", nullable=False),
        sa.Column("confidentiality_review_no", sa.String(32)),
        sa.Column("first_filing_country", sa.String(2)),
        sa.Column("agency_name", sa.String(256)),
        sa.Column("agent_name", sa.String(128)),
        sa.Column("internal_owner", sa.String(128)),
        sa.Column("claim_count", sa.Integer()),
        sa.Column("independent_claim_count", sa.Integer()),
        sa.Column("page_count", sa.Integer()),
        sa.Column("tags", postgresql.JSONB(), server_default="[]", nullable=False),
        sa.Column("extras", postgresql.JSONB(), server_default="{}", nullable=False),
        sa.Column("search_vector", postgresql.TSVECTOR()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("internal_code", name="uq_patents_internal_code"),
        sa.UniqueConstraint("country_code", "application_no", name="uq_patent_country_appno"),
        sa.CheckConstraint(
            "patent_type IN ('invention','utility_model','design')", name="ck_patent_type"
        ),
        sa.CheckConstraint(_LEGAL_STATUS_CHECK, name="ck_patent_legal_status"),
        sa.CheckConstraint(
            "application_route IN ('direct','paris','pct_national_phase','pct_international')",
            name="ck_patent_app_route",
        ),
        sa.CheckConstraint(
            "confidentiality_review_status IN ('not_required','pending','passed','restricted')",
            name="ck_patent_confidentiality_review",
        ),
    )
    # GENERATED docdb_key
    op.execute(
        """
        ALTER TABLE patents
        ADD COLUMN docdb_key VARCHAR(32)
        GENERATED ALWAYS AS (
            country_code || COALESCE(doc_number,'') || COALESCE(kind_code,'')
        ) STORED
        """
    )
    op.execute(
        "CREATE UNIQUE INDEX uq_patents_docdb ON patents(docdb_key) "
        "WHERE doc_number IS NOT NULL"
    )
    op.create_index("ix_patents_status", "patents", ["legal_status"])
    op.create_index("ix_patents_country", "patents", ["country_code"])
    op.create_index("ix_patents_app_date", "patents", ["application_date"])
    op.create_index("ix_patents_family", "patents", ["family_id"])
    op.execute("CREATE INDEX ix_patents_search_vector ON patents USING GIN (search_vector)")
    op.execute("CREATE INDEX ix_patents_title_trgm ON patents USING GIN (title_zh gin_trgm_ops)")
    op.execute(
        "CREATE INDEX ix_patents_abstract_trgm ON patents USING GIN (abstract_zh gin_trgm_ops)"
    )
    op.execute("CREATE INDEX ix_patents_tags_gin ON patents USING GIN (tags jsonb_path_ops)")

    # search_vector trigger (weighted)
    op.execute(
        """
        CREATE OR REPLACE FUNCTION patents_tsv_update() RETURNS trigger AS $$
        BEGIN
            NEW.search_vector :=
                setweight(to_tsvector('simple',
                    coalesce(NEW.title_zh,'') || ' ' || coalesce(NEW.title_en,'')
                ), 'A')
              || setweight(to_tsvector('simple', coalesce(NEW.tech_field,'')), 'B')
              || setweight(to_tsvector('simple',
                    coalesce(NEW.abstract_zh,'') || ' ' || coalesce(NEW.abstract_en,'')
                ), 'C')
              || setweight(to_tsvector('simple',
                    coalesce(NEW.internal_code,'') || ' ' ||
                    coalesce(NEW.publication_no,'') || ' ' ||
                    coalesce(NEW.application_no,'')
                ), 'D');
            RETURN NEW;
        END $$ LANGUAGE plpgsql;
        """
    )
    op.execute(
        "CREATE TRIGGER trg_patents_tsv "
        "BEFORE INSERT OR UPDATE ON patents "
        "FOR EACH ROW EXECUTE FUNCTION patents_tsv_update()"
    )

    # ── relation tables ──────────────────────────────────────────────────
    op.create_table(
        "patent_inventors",
        sa.Column("patent_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("patents.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("inventor_id", sa.BigInteger(),
                  sa.ForeignKey("inventors.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("seq", sa.SmallInteger(), nullable=False),
        sa.Column("contribution_pct", sa.Numeric(5, 2)),
        sa.Column("is_corresponding", sa.Boolean(), server_default="false", nullable=False),
        sa.Column("notes", sa.Text()),
    )
    op.create_index("ix_patent_inventors_inventor", "patent_inventors", ["inventor_id"])
    op.create_index("ix_patent_inventors_patent_seq", "patent_inventors", ["patent_id", "seq"])

    op.create_table(
        "patent_applicants",
        sa.Column("patent_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("patents.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("applicant_id", sa.BigInteger(),
                  sa.ForeignKey("applicants.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("role", sa.String(16), server_default="primary", nullable=False),
        sa.Column("share_pct", sa.Numeric(5, 2)),
        sa.Column("notes", sa.Text()),
        sa.CheckConstraint("role IN ('primary','co','assignee')", name="ck_patent_applicant_role"),
    )
    op.create_index("ix_patent_applicants_applicant", "patent_applicants", ["applicant_id"])

    op.create_table(
        "patent_classifications",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("patent_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("patents.id", ondelete="CASCADE"), nullable=False),
        sa.Column("scheme", sa.String(8), nullable=False),
        sa.Column("code", sa.String(32), nullable=False),
        sa.Column("full_symbol", sa.String(32)),
        sa.Column("section", sa.String(1)),
        sa.Column("class_code", sa.String(3)),
        sa.Column("subclass", sa.String(4)),
        sa.Column("main_group", sa.String(8)),
        sa.Column("classification_value", sa.String(16),
                  server_default="inventive", nullable=False),
        sa.Column("rank_order", sa.SmallInteger()),
        sa.Column("is_primary", sa.Boolean(), server_default="false", nullable=False),
        sa.CheckConstraint("scheme IN ('IPC','CPC')", name="ck_patent_classif_scheme"),
        sa.CheckConstraint(
            "classification_value IN ('inventive','additional','further')",
            name="ck_patent_classif_value",
        ),
    )
    op.create_index("ix_patent_classif_patent", "patent_classifications", ["patent_id"])
    op.create_index(
        "ix_patent_classif_subclass", "patent_classifications", ["scheme", "subclass"]
    )
    op.create_index(
        "ix_patent_classif_maingroup", "patent_classifications", ["scheme", "main_group"]
    )

    op.create_table(
        "patent_priorities",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("patent_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("patents.id", ondelete="CASCADE"), nullable=False),
        sa.Column("priority_type", sa.String(16), nullable=False),
        sa.Column("priority_no", sa.String(64), nullable=False),
        sa.Column("priority_date", sa.Date()),
        sa.Column("priority_country", sa.String(2)),
        sa.Column("claim_status", sa.String(16),
                  server_default="claimed", nullable=False),
        sa.CheckConstraint(
            "priority_type IN ('paris','domestic','pct')", name="ck_patent_priority_type"
        ),
        sa.CheckConstraint(
            "claim_status IN ('claimed','restored','withdrawn')",
            name="ck_patent_priority_status",
        ),
    )
    op.create_index("ix_patent_priorities_patent", "patent_priorities", ["patent_id"])

    op.create_table(
        "patent_legal_events",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("patent_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("patents.id", ondelete="CASCADE"), nullable=False),
        sa.Column("event_code", sa.String(16), nullable=False),
        sa.Column("event_date", sa.Date(), nullable=False),
        sa.Column("event_desc", sa.Text()),
        sa.Column("source", sa.String(32)),
        sa.Column("evidence_url", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=False),
    )
    op.create_index(
        "ix_legal_events_patent_date",
        "patent_legal_events",
        ["patent_id", sa.text("event_date DESC")],
    )

    op.create_table(
        "patent_citations",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("citing_patent_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("patents.id", ondelete="CASCADE"), nullable=False),
        sa.Column("cited_patent_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("patents.id", ondelete="SET NULL")),
        sa.Column("cited_docdb_key", sa.String(32)),
        sa.Column("cited_npl_text", sa.Text()),
        sa.Column("citation_type", sa.String(2), server_default="A", nullable=False),
        sa.Column("by_examiner", sa.Boolean(), server_default="false", nullable=False),
        sa.Column("citation_phase", sa.String(16)),
        sa.Column("notes", sa.Text()),
        sa.CheckConstraint(
            "citation_type IN ('X','Y','A','D','E','I','O','P','T')",
            name="ck_patent_citation_type",
        ),
    )
    op.create_index("ix_cit_citing", "patent_citations", ["citing_patent_id"])
    op.create_index("ix_cit_cited", "patent_citations", ["cited_patent_id"])
    op.create_index("ix_cit_docdb", "patent_citations", ["cited_docdb_key"])

    op.create_table(
        "patent_disclosures",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("patent_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("patents.id", ondelete="CASCADE"), nullable=False),
        sa.Column("submitted_by", sa.String(128)),
        sa.Column("problem_statement", sa.Text()),
        sa.Column("existing_solutions", sa.Text()),
        sa.Column("proposed_solution", sa.Text()),
        sa.Column("key_points", postgresql.JSONB(), server_default="[]", nullable=False),
        sa.Column("advantages", sa.Text()),
        sa.Column("embodiments", postgresql.JSONB(), server_default="[]", nullable=False),
        sa.Column("attachments", postgresql.JSONB(), server_default="[]", nullable=False),
        sa.Column("confidentiality_level", sa.String(16),
                  server_default="internal", nullable=False),
        sa.Column("access_whitelist", postgresql.JSONB(),
                  server_default="[]", nullable=False),
        sa.Column("status", sa.String(16), server_default="submitted", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("patent_id", name="uq_disclosure_patent"),
        sa.CheckConstraint(
            "status IN ('submitted','reviewing','approved','rejected')",
            name="ck_disclosure_status",
        ),
        sa.CheckConstraint(
            "confidentiality_level IN ('public','internal','secret','top_secret')",
            name="ck_disclosure_confidentiality",
        ),
    )

    op.create_table(
        "patent_office_actions",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("patent_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("patents.id", ondelete="CASCADE"), nullable=False),
        sa.Column("action_no", sa.String(16), server_default="1", nullable=False),
        sa.Column("oa_type", sa.String(32), server_default="first_oa", nullable=False),
        sa.Column("received_date", sa.Date()),
        sa.Column("due_date", sa.Date()),
        sa.Column("extension_requested", sa.Boolean(), server_default="false", nullable=False),
        sa.Column("extension_until", sa.Date()),
        sa.Column("examiner_name", sa.String(128)),
        sa.Column("issues", postgresql.JSONB(), server_default="[]", nullable=False),
        sa.Column("response_content", sa.Text()),
        sa.Column("responded_at", sa.Date()),
        sa.Column("status", sa.String(16), server_default="received", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint(
            "status IN ('received','responding','responded','closed')", name="ck_oa_status"
        ),
        sa.CheckConstraint(
            "oa_type IN ('notice_to_make_correction','first_oa','second_oa',"
            "'nth_oa','pre_grant_notice','divisional_notice','reexamination','invalidation')",
            name="ck_oa_type",
        ),
    )
    op.create_index("ix_oa_patent_action", "patent_office_actions", ["patent_id", "action_no"])

    op.create_table(
        "patent_drafts",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("patent_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("patents.id", ondelete="CASCADE"), nullable=False),
        sa.Column("parent_draft_id", sa.BigInteger(),
                  sa.ForeignKey("patent_drafts.id", ondelete="SET NULL")),
        sa.Column("amendment_oa_id", sa.BigInteger(),
                  sa.ForeignKey("patent_office_actions.id", ondelete="SET NULL")),
        sa.Column("version", sa.Integer(), server_default="1", nullable=False),
        sa.Column("section", sa.String(24), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("ai_generated", sa.Boolean(), server_default="false", nullable=False),
        sa.Column("ai_model", sa.String(64)),
        sa.Column("ai_confidence", sa.String(16)),
        sa.Column("created_by", sa.String(128)),
        sa.Column("is_filed", sa.Boolean(), server_default="false", nullable=False),
        sa.Column("filed_at", sa.Date()),
        sa.Column("reviewed_by", sa.String(128)),
        sa.Column("reviewed_at", sa.DateTime(timezone=True)),
        sa.Column("review_score_clarity", sa.SmallInteger()),
        sa.Column("review_score_essential", sa.SmallInteger()),
        sa.Column("review_score_generalization", sa.SmallInteger()),
        sa.Column("review_score_support", sa.SmallInteger()),
        sa.Column("review_score_chinese", sa.SmallInteger()),
        sa.Column("review_score_format", sa.SmallInteger()),
        sa.Column("review_decision", sa.String(16)),
        sa.Column("review_notes", sa.Text()),
        sa.Column("notes", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint(_DRAFT_SECTION_CHECK, name="ck_draft_section"),
        sa.CheckConstraint(
            "review_decision IS NULL OR review_decision IN "
            "('accept','minor_edit','major_rewrite','reject')",
            name="ck_draft_review_decision",
        ),
    )
    op.create_index(
        "ix_drafts_patent_section_version",
        "patent_drafts",
        ["patent_id", "section", sa.text("version DESC")],
    )

    op.create_table(
        "patent_prior_art_searches",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("patent_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("patents.id", ondelete="CASCADE"), nullable=False),
        sa.Column("searched_by", sa.String(128)),
        sa.Column("searched_at", sa.Date()),
        sa.Column("databases", postgresql.JSONB(), server_default="[]", nullable=False),
        sa.Column("keywords", postgresql.JSONB(), server_default="[]", nullable=False),
        sa.Column("findings", sa.Text()),
        sa.Column("novelty", sa.String(16), server_default="unknown", nullable=False),
        sa.Column("inventiveness", sa.String(16), server_default="unknown", nullable=False),
        sa.Column("cited_documents", postgresql.JSONB(), server_default="[]", nullable=False),
        sa.Column("recommendations", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("novelty IN ('high','medium','low','unknown')",
                           name="ck_prior_art_novelty"),
        sa.CheckConstraint("inventiveness IN ('high','medium','low','unknown')",
                           name="ck_prior_art_inventiveness"),
    )
    op.create_index("ix_prior_art_patent", "patent_prior_art_searches", ["patent_id"])

    op.create_table(
        "patent_fee_events",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("patent_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("patents.id", ondelete="CASCADE"), nullable=False),
        sa.Column("fee_type", sa.String(24), nullable=False),
        sa.Column("year_no", sa.SmallInteger()),
        sa.Column("amount", sa.Numeric(12, 2)),
        sa.Column("due_date", sa.Date()),
        sa.Column("paid_date", sa.Date()),
        sa.Column("status", sa.String(16), server_default="pending", nullable=False),
        sa.Column("notes", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint(
            "fee_type IN ('application','publication','substantive_exam','grant','annual',"
            "'reexamination','invalidation','other')",
            name="ck_fee_type",
        ),
        sa.CheckConstraint(
            "status IN ('pending','paid','overdue','waived','reduced')",
            name="ck_fee_status",
        ),
    )
    op.create_index(
        "ix_fee_due", "patent_fee_events", ["status", "due_date"]
    )

    op.create_table(
        "patent_draft_jobs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("patent_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("patents.id", ondelete="CASCADE"), nullable=False),
        sa.Column("scenario", sa.String(32), nullable=False),
        sa.Column("status", sa.String(16), server_default="pending", nullable=False),
        sa.Column("model", sa.String(64)),
        sa.Column("input_tokens", sa.Integer()),
        sa.Column("output_tokens", sa.Integer()),
        sa.Column("cache_read_tokens", sa.Integer()),
        sa.Column("started_at", sa.DateTime(timezone=True)),
        sa.Column("completed_at", sa.DateTime(timezone=True)),
        sa.Column("error", sa.Text()),
        sa.Column("result_draft_id", sa.BigInteger(),
                  sa.ForeignKey("patent_drafts.id", ondelete="SET NULL")),
        sa.Column("request_payload", postgresql.JSONB(), server_default="{}", nullable=False),
        sa.Column("result_payload", postgresql.JSONB(), server_default="{}", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint(
            "status IN ('pending','streaming','done','cancelled','failed')",
            name="ck_draft_job_status",
        ),
        sa.CheckConstraint(
            "scenario IN ('claims_from_disclosure','dependent_claims',"
            "'spec_from_claims','oa_response')",
            name="ck_draft_job_scenario",
        ),
    )
    op.create_index("ix_draft_jobs_patent", "patent_draft_jobs", ["patent_id"])

    op.create_table(
        "patent_scenarios",
        sa.Column("patent_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("patents.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("scenario_id", sa.BigInteger(),
                  sa.ForeignKey("application_scenarios.id", ondelete="CASCADE"),
                  primary_key=True),
        sa.Column("relevance", sa.SmallInteger(), server_default="3", nullable=False),
        sa.Column("notes", sa.Text()),
    )
    op.create_index("ix_patent_scenarios_scenario", "patent_scenarios", ["scenario_id"])

    op.create_table(
        "patent_grades",
        sa.Column("patent_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("patents.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("grade_id", sa.BigInteger(),
                  sa.ForeignKey("pha_grades.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("relevance", sa.SmallInteger(), server_default="3", nullable=False),
        sa.Column("notes", sa.Text()),
    )
    op.create_index("ix_patent_grades_grade", "patent_grades", ["grade_id"])


def downgrade() -> None:
    op.drop_table("patent_grades")
    op.drop_table("patent_scenarios")
    op.drop_table("patent_draft_jobs")
    op.drop_table("patent_fee_events")
    op.drop_table("patent_prior_art_searches")
    op.drop_table("patent_drafts")
    op.drop_table("patent_office_actions")
    op.drop_table("patent_disclosures")
    op.drop_table("patent_citations")
    op.drop_table("patent_legal_events")
    op.drop_table("patent_priorities")
    op.drop_table("patent_classifications")
    op.drop_table("patent_applicants")
    op.drop_table("patent_inventors")
    op.execute("DROP TRIGGER IF EXISTS trg_patents_tsv ON patents")
    op.execute("DROP FUNCTION IF EXISTS patents_tsv_update()")
    op.drop_table("patents")
    op.drop_table("applicants")
    op.drop_table("inventors")
