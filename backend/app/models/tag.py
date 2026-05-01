from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.dialects.postgresql import CITEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class Tag(Base, TimestampMixin):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    slug: Mapped[str] = mapped_column(CITEXT, unique=True, nullable=False)
    name_zh: Mapped[str] = mapped_column(String(64), nullable=False)
    category: Mapped[str | None] = mapped_column(String(32))
    color: Mapped[str | None] = mapped_column(String(16))


class ScenarioTag(Base):
    __tablename__ = "scenario_tags"

    scenario_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("application_scenarios.id", ondelete="CASCADE"),
        primary_key=True,
    )
    tag_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True
    )

    scenario = relationship("ApplicationScenario", back_populates="tag_links")
    tag = relationship("Tag")


class GradeTag(Base):
    __tablename__ = "grade_tags"

    grade_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("pha_grades.id", ondelete="CASCADE"), primary_key=True
    )
    tag_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True
    )

    grade = relationship("PhaGrade", back_populates="tag_links")
    tag = relationship("Tag")
