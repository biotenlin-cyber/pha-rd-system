from typing import Any

from pydantic import BaseModel, ConfigDict

from app.schemas.tag import Tag


class ScenarioBase(BaseModel):
    code: str
    name_zh: str
    name_en: str | None = None
    summary: str | None = None
    sub_scenarios: list[Any] = []
    technical_requirements: dict[str, Any] = {}
    typical_products: list[Any] = []
    market_size_usd: float | None = None
    market_year: int | None = None
    market_notes: str | None = None
    status: str = "active"


class ScenarioCreate(ScenarioBase):
    domain_code: str
    tag_slugs: list[str] = []


class ScenarioUpdate(BaseModel):
    name_zh: str | None = None
    name_en: str | None = None
    summary: str | None = None
    sub_scenarios: list[Any] | None = None
    technical_requirements: dict[str, Any] | None = None
    typical_products: list[Any] | None = None
    market_size_usd: float | None = None
    market_year: int | None = None
    market_notes: str | None = None
    status: str | None = None
    tag_slugs: list[str] | None = None


class ScenarioSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    code: str
    name_zh: str
    domain_code: str
    summary: str | None = None
    tags: list[Tag] = []
    top_match_grade: str | None = None


class Scenario(ScenarioBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    domain_id: int
    domain_code: str
    tags: list[Tag] = []


class ExternalLink(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    link_type: str
    external_ref: str
    label: str | None = None
    meta: dict[str, Any] = {}


class ScenarioMatchSummary(BaseModel):
    grade_id: int
    grade_code: str
    grade_name_zh: str
    match_score: int
    recommendation_level: str
    key_metrics: dict[str, Any] = {}
    rationale: str | None = None


class ScenarioDetail(Scenario):
    matches: list[ScenarioMatchSummary] = []
    external_links: list[ExternalLink] = []
