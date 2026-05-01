from pydantic import BaseModel


class SearchHit(BaseModel):
    type: str  # 'scenario' | 'grade'
    id: int
    code: str
    name_zh: str
    snippet: str | None = None
    score: float
    domain_code: str | None = None


class SearchFacet(BaseModel):
    code: str
    count: int


class SearchFacets(BaseModel):
    domain: list[SearchFacet] = []
    tag: list[SearchFacet] = []
    type: list[SearchFacet] = []


class SearchMeta(BaseModel):
    total: int
    page: int
    page_size: int
    took_ms: int


class SearchResponse(BaseModel):
    meta: SearchMeta
    facets: SearchFacets
    data: list[SearchHit]
