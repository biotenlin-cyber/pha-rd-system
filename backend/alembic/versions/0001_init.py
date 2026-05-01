"""init schema

Revision ID: 0001_init
Revises:
Create Date: 2026-05-01

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001_init"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
    op.execute("CREATE EXTENSION IF NOT EXISTS citext")

    op.create_table(
        "application_domains",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("code", postgresql.CITEXT(), nullable=False),
        sa.Column("name_zh", sa.String(64), nullable=False),
        sa.Column("name_en", sa.String(64), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("icon", sa.String(64)),
        sa.Column("sort_order", sa.Integer(), server_default="0", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("code", name="uq_application_domains_code"),
    )
    op.create_index("ix_application_domains_sort_order", "application_domains", ["sort_order"])

    op.create_table(
        "application_scenarios",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("domain_id", sa.BigInteger(), sa.ForeignKey("application_domains.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("code", postgresql.CITEXT(), nullable=False),
        sa.Column("name_zh", sa.String(128), nullable=False),
        sa.Column("name_en", sa.String(128)),
        sa.Column("summary", sa.Text()),
        sa.Column("sub_scenarios", postgresql.JSONB(), server_default="[]", nullable=False),
        sa.Column("technical_requirements", postgresql.JSONB(), server_default="{}", nullable=False),
        sa.Column("typical_products", postgresql.JSONB(), server_default="[]", nullable=False),
        sa.Column("market_size_usd", sa.Numeric(18, 2)),
        sa.Column("market_year", sa.SmallInteger()),
        sa.Column("market_notes", sa.Text()),
        sa.Column("status", sa.String(16), server_default="active", nullable=False),
        sa.Column("search_vector", postgresql.TSVECTOR()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("code", name="uq_application_scenarios_code"),
        sa.CheckConstraint("status IN ('active','draft','archived')", name="ck_scenario_status"),
    )
    op.create_index("ix_scenario_domain_id", "application_scenarios", ["domain_id"])
    op.execute(
        "CREATE INDEX ix_scenario_search_vector ON application_scenarios USING GIN (search_vector)"
    )
    op.execute(
        "CREATE INDEX ix_scenario_name_trgm ON application_scenarios USING GIN (name_zh gin_trgm_ops)"
    )
    op.execute(
        "CREATE INDEX ix_scenario_summary_trgm ON application_scenarios "
        "USING GIN (summary gin_trgm_ops)"
    )
    op.execute(
        "CREATE INDEX ix_scenario_tech_req ON application_scenarios "
        "USING GIN (technical_requirements jsonb_path_ops)"
    )

    op.create_table(
        "pha_grades",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("code", postgresql.CITEXT(), nullable=False),
        sa.Column("name_zh", sa.String(128), nullable=False),
        sa.Column("full_name", sa.String(256)),
        sa.Column("polymer_family", sa.String(32)),
        sa.Column("description", sa.Text()),
        sa.Column("tm_celsius", sa.Numeric(6, 2)),
        sa.Column("tg_celsius", sa.Numeric(6, 2)),
        sa.Column("crystallinity_pct", sa.Numeric(5, 2)),
        sa.Column("elongation_at_break_pct", sa.Numeric(7, 2)),
        sa.Column("tensile_strength_mpa", sa.Numeric(7, 2)),
        sa.Column("youngs_modulus_gpa", sa.Numeric(6, 3)),
        sa.Column("biocompatibility_class", sa.String(16)),
        sa.Column("degradation_months_soil", sa.Numeric(5, 1)),
        sa.Column("degradation_months_marine", sa.Numeric(5, 1)),
        sa.Column("extra_metrics", postgresql.JSONB(), server_default="{}", nullable=False),
        sa.Column("typical_processing", postgresql.JSONB(), server_default="[]", nullable=False),
        sa.Column("status", sa.String(16), server_default="active", nullable=False),
        sa.Column("search_vector", postgresql.TSVECTOR()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("code", name="uq_pha_grades_code"),
    )
    op.execute("CREATE INDEX ix_grade_search_vector ON pha_grades USING GIN (search_vector)")
    op.execute("CREATE INDEX ix_grade_name_trgm ON pha_grades USING GIN (name_zh gin_trgm_ops)")

    op.create_table(
        "grade_scenario_matches",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("grade_id", sa.BigInteger(), sa.ForeignKey("pha_grades.id", ondelete="CASCADE"), nullable=False),
        sa.Column("scenario_id", sa.BigInteger(), sa.ForeignKey("application_scenarios.id", ondelete="CASCADE"), nullable=False),
        sa.Column("match_score", sa.SmallInteger(), nullable=False),
        sa.Column("recommendation_level", sa.String(16), nullable=False),
        sa.Column("key_metrics", postgresql.JSONB(), server_default="{}", nullable=False),
        sa.Column("rationale", sa.Text()),
        sa.Column("references", postgresql.JSONB(), server_default="[]", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("grade_id", "scenario_id", name="uq_grade_scenario"),
        sa.CheckConstraint("match_score BETWEEN 0 AND 100", name="ck_match_score_range"),
        sa.CheckConstraint(
            "recommendation_level IN ('preferred','suitable','marginal','not_recommended')",
            name="ck_recommendation_level",
        ),
    )
    op.create_index("ix_match_scenario_score", "grade_scenario_matches", ["scenario_id", sa.text("match_score DESC")])
    op.create_index("ix_match_grade_score", "grade_scenario_matches", ["grade_id", sa.text("match_score DESC")])

    op.create_table(
        "tags",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("slug", postgresql.CITEXT(), nullable=False),
        sa.Column("name_zh", sa.String(64), nullable=False),
        sa.Column("category", sa.String(32)),
        sa.Column("color", sa.String(16)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("slug", name="uq_tags_slug"),
    )

    op.create_table(
        "scenario_tags",
        sa.Column("scenario_id", sa.BigInteger(), sa.ForeignKey("application_scenarios.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("tag_id", sa.BigInteger(), sa.ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
    )
    op.create_index("ix_scenario_tags_tag_id", "scenario_tags", ["tag_id"])

    op.create_table(
        "grade_tags",
        sa.Column("grade_id", sa.BigInteger(), sa.ForeignKey("pha_grades.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("tag_id", sa.BigInteger(), sa.ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
    )
    op.create_index("ix_grade_tags_tag_id", "grade_tags", ["tag_id"])

    op.create_table(
        "scenario_external_links",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("scenario_id", sa.BigInteger(), sa.ForeignKey("application_scenarios.id", ondelete="CASCADE"), nullable=False),
        sa.Column("link_type", sa.String(16), nullable=False),
        sa.Column("external_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("label", sa.String(256)),
        sa.Column("meta", postgresql.JSONB(), server_default="{}", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("link_type IN ('patent','project')", name="ck_scenario_link_type"),
    )
    op.create_index("ix_scenario_link_lookup", "scenario_external_links", ["scenario_id", "link_type"])
    op.create_index("ix_scenario_link_ref", "scenario_external_links", ["link_type", "external_ref"])

    op.create_table(
        "grade_external_links",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("grade_id", sa.BigInteger(), sa.ForeignKey("pha_grades.id", ondelete="CASCADE"), nullable=False),
        sa.Column("link_type", sa.String(16), nullable=False),
        sa.Column("external_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("label", sa.String(256)),
        sa.Column("meta", postgresql.JSONB(), server_default="{}", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("link_type IN ('patent','project')", name="ck_grade_link_type"),
    )
    op.create_index("ix_grade_link_lookup", "grade_external_links", ["grade_id", "link_type"])
    op.create_index("ix_grade_link_ref", "grade_external_links", ["link_type", "external_ref"])


def downgrade() -> None:
    op.drop_table("grade_external_links")
    op.drop_table("scenario_external_links")
    op.drop_table("grade_tags")
    op.drop_table("scenario_tags")
    op.drop_table("tags")
    op.drop_table("grade_scenario_matches")
    op.drop_table("pha_grades")
    op.drop_table("application_scenarios")
    op.drop_table("application_domains")
