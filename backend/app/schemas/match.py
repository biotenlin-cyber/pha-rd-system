from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class MatchBase(BaseModel):
    grade_id: int
    scenario_id: int
    match_score: int = Field(ge=0, le=100)
    recommendation_level: str
    key_metrics: dict[str, Any] = {}
    rationale: str | None = None
    refs: list[Any] = []


class MatchCreate(MatchBase):
    pass


class MatchUpdate(BaseModel):
    match_score: int | None = None
    recommendation_level: str | None = None
    key_metrics: dict[str, Any] | None = None
    rationale: str | None = None
    refs: list[Any] | None = None


class Match(MatchBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
