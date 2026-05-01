from typing import Any

from sqlalchemy import BigInteger, Numeric, String, Text
from sqlalchemy.dialects.postgresql import CITEXT, JSONB, TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class PhaGrade(Base, TimestampMixin):
    __tablename__ = "pha_grades"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    code: Mapped[str] = mapped_column(CITEXT, unique=True, nullable=False)
    name_zh: Mapped[str] = mapped_column(String(128), nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(256))
    polymer_family: Mapped[str | None] = mapped_column(String(32))
    description: Mapped[str | None] = mapped_column(Text)

    tm_celsius: Mapped[float | None] = mapped_column(Numeric(6, 2))
    tg_celsius: Mapped[float | None] = mapped_column(Numeric(6, 2))
    crystallinity_pct: Mapped[float | None] = mapped_column(Numeric(5, 2))
    elongation_at_break_pct: Mapped[float | None] = mapped_column(Numeric(7, 2))
    tensile_strength_mpa: Mapped[float | None] = mapped_column(Numeric(7, 2))
    youngs_modulus_gpa: Mapped[float | None] = mapped_column(Numeric(6, 3))
    biocompatibility_class: Mapped[str | None] = mapped_column(String(16))
    degradation_months_soil: Mapped[float | None] = mapped_column(Numeric(5, 1))
    degradation_months_marine: Mapped[float | None] = mapped_column(Numeric(5, 1))

    extra_metrics: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, server_default="{}")
    typical_processing: Mapped[list[Any]] = mapped_column(JSONB, default=list, server_default="[]")
    status: Mapped[str] = mapped_column(String(16), default="active", server_default="active")
    search_vector: Mapped[Any | None] = mapped_column(TSVECTOR)

    matches = relationship(
        "GradeScenarioMatch", back_populates="grade", cascade="all, delete-orphan"
    )
    tag_links = relationship(
        "GradeTag", back_populates="grade", cascade="all, delete-orphan"
    )
    external_links = relationship(
        "GradeExternalLink", back_populates="grade", cascade="all, delete-orphan"
    )
