from pydantic import BaseModel, ConfigDict


class TagBase(BaseModel):
    slug: str
    name_zh: str
    category: str | None = None
    color: str | None = None


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
