from typing import Any

from pydantic import BaseModel, ConfigDict


class GradeBase(BaseModel):
    code: str
    name_zh: str
    full_name: str | None = None
    polymer_family: str | None = None
    description: str | None = None
    tm_celsius: float | None = None
    tg_celsius: float | None = None
    crystallinity_pct: float | None = None
    elongation_at_break_pct: float | None = None
    tensile_strength_mpa: float | None = None
    youngs_modulus_gpa: float | None = None
    biocompatibility_class: str | None = None
    degradation_months_soil: float | None = None
    degradation_months_marine: float | None = None
    extra_metrics: dict[str, Any] = {}
    typical_processing: list[Any] = []
    status: str = "active"


class GradeCreate(GradeBase):
    pass


class GradeUpdate(BaseModel):
    name_zh: str | None = None
    full_name: str | None = None
    polymer_family: str | None = None
    description: str | None = None
    tm_celsius: float | None = None
    tg_celsius: float | None = None
    crystallinity_pct: float | None = None
    elongation_at_break_pct: float | None = None
    tensile_strength_mpa: float | None = None
    youngs_modulus_gpa: float | None = None
    biocompatibility_class: str | None = None
    degradation_months_soil: float | None = None
    degradation_months_marine: float | None = None
    extra_metrics: dict[str, Any] | None = None
    typical_processing: list[Any] | None = None
    status: str | None = None


class Grade(GradeBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class GradeMatchSummary(BaseModel):
    scenario_id: int
    scenario_code: str
    scenario_name_zh: str
    domain_code: str
    match_score: int
    recommendation_level: str
    key_metrics: dict[str, Any] = {}
    rationale: str | None = None


class GradeDetail(Grade):
    matches: list[GradeMatchSummary] = []
