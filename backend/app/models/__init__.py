from app.models.associations import GradeExternalLink, ScenarioExternalLink
from app.models.domain import ApplicationDomain
from app.models.grade import PhaGrade
from app.models.match import GradeScenarioMatch
from app.models.patent import (
    Applicant,
    Inventor,
    Patent,
    PatentApplicant,
    PatentCitation,
    PatentClassification,
    PatentDisclosure,
    PatentDraft,
    PatentDraftJob,
    PatentFeeEvent,
    PatentGrade,
    PatentInventor,
    PatentLegalEvent,
    PatentOfficeAction,
    PatentPriority,
    PatentPriorArtSearch,
    PatentScenario,
)
from app.models.scenario import ApplicationScenario
from app.models.tag import GradeTag, ScenarioTag, Tag


def register_all() -> None:
    """No-op anchor so Alembic env can import all models in one place."""


__all__ = [
    "ApplicationDomain",
    "ApplicationScenario",
    "PhaGrade",
    "GradeScenarioMatch",
    "Tag",
    "ScenarioTag",
    "GradeTag",
    "ScenarioExternalLink",
    "GradeExternalLink",
    "Inventor",
    "Applicant",
    "Patent",
    "PatentClassification",
    "PatentPriority",
    "PatentInventor",
    "PatentApplicant",
    "PatentLegalEvent",
    "PatentCitation",
    "PatentDisclosure",
    "PatentDraft",
    "PatentOfficeAction",
    "PatentPriorArtSearch",
    "PatentFeeEvent",
    "PatentDraftJob",
    "PatentScenario",
    "PatentGrade",
    "register_all",
]
