from typing import Any

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    ForeignKey,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class GradeScenarioMatch(Base, TimestampMixin):
    __tablename__ = "grade_scenario_matches"
    __table_args__ = (
        UniqueConstraint("grade_id", "scenario_id", name="uq_grade_scenario"),
        CheckConstraint("match_score BETWEEN 0 AND 100", name="ck_match_score_range"),
        CheckConstraint(
            "recommendation_level IN ('preferred','suitable','marginal','not_recommended')",
            name="ck_recommendation_level",
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    grade_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("pha_grades.id", ondelete="CASCADE"), nullable=False
    )
    scenario_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("application_scenarios.id", ondelete="CASCADE"),
        nullable=False,
    )
    match_score: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    recommendation_level: Mapped[str] = mapped_column(String(16), nullable=False)
    key_metrics: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, server_default="{}")
    rationale: Mapped[str | None] = mapped_column(Text)
    refs: Mapped[list[Any]] = mapped_column(
        "references", JSONB, default=list, server_default="[]"
    )

    grade = relationship("PhaGrade", back_populates="matches")
    scenario = relationship("ApplicationScenario", back_populates="matches")
