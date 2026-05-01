from typing import Any

from sqlalchemy import BigInteger, CheckConstraint, ForeignKey, Numeric, SmallInteger, String, Text
from sqlalchemy.dialects.postgresql import CITEXT, JSONB, TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class ApplicationScenario(Base, TimestampMixin):
    __tablename__ = "application_scenarios"
    __table_args__ = (
        CheckConstraint(
            "status IN ('active','draft','archived')", name="ck_scenario_status"
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    domain_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("application_domains.id", ondelete="RESTRICT"), nullable=False
    )
    code: Mapped[str] = mapped_column(CITEXT, unique=True, nullable=False)
    name_zh: Mapped[str] = mapped_column(String(128), nullable=False)
    name_en: Mapped[str | None] = mapped_column(String(128))
    summary: Mapped[str | None] = mapped_column(Text)
    sub_scenarios: Mapped[list[Any]] = mapped_column(JSONB, default=list, server_default="[]")
    technical_requirements: Mapped[dict[str, Any]] = mapped_column(
        JSONB, default=dict, server_default="{}"
    )
    typical_products: Mapped[list[Any]] = mapped_column(JSONB, default=list, server_default="[]")
    market_size_usd: Mapped[float | None] = mapped_column(Numeric(18, 2))
    market_year: Mapped[int | None] = mapped_column(SmallInteger)
    market_notes: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(16), default="active", server_default="active")
    search_vector: Mapped[Any | None] = mapped_column(TSVECTOR)

    domain = relationship("ApplicationDomain", back_populates="scenarios")
    matches = relationship(
        "GradeScenarioMatch", back_populates="scenario", cascade="all, delete-orphan"
    )
    tag_links = relationship(
        "ScenarioTag", back_populates="scenario", cascade="all, delete-orphan"
    )
    external_links = relationship(
        "ScenarioExternalLink", back_populates="scenario", cascade="all, delete-orphan"
    )
