from app.models.associations import GradeExternalLink, ScenarioExternalLink
from app.models.domain import ApplicationDomain
from app.models.grade import PhaGrade
from app.models.match import GradeScenarioMatch
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
    "register_all",
]
