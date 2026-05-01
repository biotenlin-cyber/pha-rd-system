from pydantic import BaseModel, ConfigDict


class DomainBase(BaseModel):
    code: str
    name_zh: str
    name_en: str
    description: str | None = None
    icon: str | None = None
    sort_order: int = 0


class DomainCreate(DomainBase):
    pass


class DomainUpdate(BaseModel):
    name_zh: str | None = None
    name_en: str | None = None
    description: str | None = None
    icon: str | None = None
    sort_order: int | None = None


class Domain(DomainBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    scenario_count: int = 0
