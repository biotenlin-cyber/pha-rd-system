from fastapi import APIRouter

from app.api.v1 import domains, grades, matches, patents, scenarios, search, tags

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(domains.router, prefix="/domains", tags=["domains"])
api_router.include_router(scenarios.router, prefix="/scenarios", tags=["scenarios"])
api_router.include_router(grades.router, prefix="/grades", tags=["grades"])
api_router.include_router(matches.router, prefix="/matches", tags=["matches"])
api_router.include_router(tags.router, prefix="/tags", tags=["tags"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(patents.router, prefix="/patents", tags=["patents"])
