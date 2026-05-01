from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Pagination(BaseModel):
    page: int = 1
    page_size: int = 20
    total: int = 0


class Page(BaseModel, Generic[T]):
    data: list[T]
    meta: Pagination


class IdName(BaseModel):
    id: int
    code: str
    name_zh: str
