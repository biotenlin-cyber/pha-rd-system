import uuid
from typing import Any

from sqlalchemy import BigInteger, CheckConstraint, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class ScenarioExternalLink(Base, TimestampMixin):
    __tablename__ = "scenario_external_links"
    __table_args__ = (
        CheckConstraint("link_type IN ('patent','project')", name="ck_scenario_link_type"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    scenario_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("application_scenarios.id", ondelete="CASCADE"),
        nullable=False,
    )
    link_type: Mapped[str] = mapped_column(String(16), nullable=False)
    external_ref: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    label: Mapped[str | None] = mapped_column(String(256))
    meta: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, server_default="{}")

    scenario = relationship("ApplicationScenario", back_populates="external_links")


class GradeExternalLink(Base, TimestampMixin):
    __tablename__ = "grade_external_links"
    __table_args__ = (
        CheckConstraint("link_type IN ('patent','project')", name="ck_grade_link_type"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    grade_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("pha_grades.id", ondelete="CASCADE"), nullable=False
    )
    link_type: Mapped[str] = mapped_column(String(16), nullable=False)
    external_ref: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    label: Mapped[str | None] = mapped_column(String(256))
    meta: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, server_default="{}")

    grade = relationship("PhaGrade", back_populates="external_links")
