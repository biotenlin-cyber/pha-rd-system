"""Patents REST API — list/detail/CRUD/workflow/AI-draft/CSV-import/analytics."""
from __future__ import annotations

import json
import uuid
from typing import Any

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.schemas.common import Page, Pagination
from app.schemas.patent import (
    AIDraftRequest,
    AnalyticsResponse,
    CSVImportResult,
    Disclosure,
    DisclosureCreate,
    Draft,
    DraftCreate,
    DraftReview,
    OfficeAction,
    OfficeActionCreate,
    PatentCreate,
    PatentDetail,
    PatentSummary,
    PatentUpdate,
    PriorArt,
    PriorArtCreate,
)
from app.services import (
    patent_ai_service,
    patent_analytics_service,
    patent_csv_service,
    patent_service,
    patent_workflow_service,
)

router = APIRouter()


# ── list / detail / create / update ──────────────────────────────────────
@router.get("", response_model=Page[PatentSummary])
async def list_patents(
    q: str | None = None,
    legal_status: str | None = None,
    country: str | None = None,
    grade: str | None = None,
    domain: str | None = None,
    scenario: str | None = None,
    applicant: str | None = None,
    tag: str | None = None,
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db),
):
    data, total = await patent_service.list_patents(
        db,
        q=q,
        legal_status=legal_status,
        country=country,
        grade=grade,
        domain=domain,
        scenario=scenario,
        applicant=applicant,
        tag=tag,
        page=page,
        page_size=page_size,
    )
    return {"data": data, "meta": Pagination(page=page, page_size=page_size, total=total)}


@router.get("/analytics", response_model=AnalyticsResponse)
async def analytics(db: AsyncSession = Depends(get_db)):
    return await patent_analytics_service.overview(db)


@router.get("/analytics/heatmap")
async def domain_grade_heatmap(db: AsyncSession = Depends(get_db)):
    return await patent_analytics_service.domain_grade_heatmap(db)


@router.post("/import-csv", response_model=CSVImportResult)
async def import_csv(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    raw = await file.read()
    return await patent_csv_service.import_csv(db, raw)


@router.post("", response_model=PatentDetail, status_code=status.HTTP_201_CREATED)
async def create_patent(payload: PatentCreate, db: AsyncSession = Depends(get_db)):
    body = payload.model_dump()
    patent = await patent_service.upsert_patent(db, body)
    await db.commit()
    return await patent_service.get_patent_detail(db, str(patent.id))


@router.get("/{key}", response_model=PatentDetail)
async def get_patent(key: str, db: AsyncSession = Depends(get_db)):
    return await patent_service.get_patent_detail(db, key)


@router.patch("/{key}", response_model=PatentDetail)
async def update_patent(
    key: str, payload: PatentUpdate, db: AsyncSession = Depends(get_db)
):
    detail = await patent_service.get_patent_detail(db, key)
    pid = detail["id"]
    from app.models import Patent

    obj = await db.get(Patent, pid)
    if not obj:
        raise HTTPException(404, "patent missing after lookup")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    await db.commit()
    return await patent_service.get_patent_detail(db, key)


# ── disclosure ───────────────────────────────────────────────────────────
@router.get("/{key}/disclosure", response_model=Disclosure | None)
async def get_disclosure(key: str, db: AsyncSession = Depends(get_db)):
    detail = await patent_service.get_patent_detail(db, key)
    obj = await patent_workflow_service.get_disclosure(db, detail["id"])
    return obj


@router.put("/{key}/disclosure", response_model=Disclosure)
async def upsert_disclosure(
    key: str, payload: DisclosureCreate, db: AsyncSession = Depends(get_db)
):
    detail = await patent_service.get_patent_detail(db, key)
    obj = await patent_workflow_service.upsert_disclosure(
        db, detail["id"], payload.model_dump()
    )
    await db.commit()
    return obj


# ── drafts ───────────────────────────────────────────────────────────────
@router.get("/{key}/drafts", response_model=list[Draft])
async def list_drafts(key: str, db: AsyncSession = Depends(get_db)):
    detail = await patent_service.get_patent_detail(db, key)
    return await patent_workflow_service.list_drafts(db, detail["id"])


@router.post("/{key}/drafts", response_model=Draft, status_code=status.HTTP_201_CREATED)
async def create_draft(
    key: str, payload: DraftCreate, db: AsyncSession = Depends(get_db)
):
    detail = await patent_service.get_patent_detail(db, key)
    obj = await patent_workflow_service.create_draft(
        db, detail["id"], **payload.model_dump()
    )
    await db.commit()
    return obj


@router.post("/drafts/{draft_id}/review", response_model=Draft)
async def review_draft(
    draft_id: int, payload: DraftReview, db: AsyncSession = Depends(get_db)
):
    obj = await patent_workflow_service.review_draft(
        db, draft_id, payload=payload.model_dump(exclude_unset=True)
    )
    await db.commit()
    return obj


# ── office actions ───────────────────────────────────────────────────────
@router.get("/{key}/office-actions", response_model=list[OfficeAction])
async def list_oas(key: str, db: AsyncSession = Depends(get_db)):
    detail = await patent_service.get_patent_detail(db, key)
    return await patent_workflow_service.list_oas(db, detail["id"])


@router.post(
    "/{key}/office-actions", response_model=OfficeAction, status_code=status.HTTP_201_CREATED
)
async def create_oa(
    key: str, payload: OfficeActionCreate, db: AsyncSession = Depends(get_db)
):
    detail = await patent_service.get_patent_detail(db, key)
    obj = await patent_workflow_service.create_oa(db, detail["id"], payload.model_dump())
    await db.commit()
    return obj


# ── prior art ────────────────────────────────────────────────────────────
@router.get("/{key}/prior-art", response_model=list[PriorArt])
async def list_prior_art(key: str, db: AsyncSession = Depends(get_db)):
    detail = await patent_service.get_patent_detail(db, key)
    return await patent_workflow_service.list_prior_art(db, detail["id"])


@router.post(
    "/{key}/prior-art", response_model=PriorArt, status_code=status.HTTP_201_CREATED
)
async def create_prior_art(
    key: str, payload: PriorArtCreate, db: AsyncSession = Depends(get_db)
):
    detail = await patent_service.get_patent_detail(db, key)
    obj = await patent_workflow_service.create_prior_art(
        db, detail["id"], payload.model_dump()
    )
    await db.commit()
    return obj


# ── AI drafting (SSE) ────────────────────────────────────────────────────
@router.post("/{key}/ai/draft")
async def ai_draft(
    key: str,
    payload: AIDraftRequest,
    db: AsyncSession = Depends(get_db),
):
    detail = await patent_service.get_patent_detail(db, key)
    pid = detail["id"]

    async def gen():
        try:
            async for evt in patent_ai_service.stream_draft(
                db,
                pid,
                scenario=payload.scenario,
                extra_context=payload.extra_context,
                save_as_draft=payload.save_as_draft,
                section=payload.section,
                model_override=payload.model,
            ):
                line = f"event: {evt['event']}\ndata: {json.dumps(evt['data'], ensure_ascii=False)}\n\n"
                yield line
        except HTTPException:
            raise
        except Exception as exc:  # noqa: BLE001
            yield (
                "event: error\n"
                f"data: {json.dumps({'message': str(exc)[:300]})}\n\n"
            )

    return StreamingResponse(
        gen(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.get("/{key}/ai/jobs")
async def list_ai_jobs(
    key: str,
    db: AsyncSession = Depends(get_db),
    limit: int = Query(20, le=100),
):
    detail = await patent_service.get_patent_detail(db, key)
    from sqlalchemy import select

    from app.models import PatentDraftJob

    rows = (
        await db.execute(
            select(PatentDraftJob)
            .where(PatentDraftJob.patent_id == detail["id"])
            .order_by(PatentDraftJob.created_at.desc())
            .limit(limit)
        )
    ).scalars().all()
    return [
        {
            "id": str(r.id),
            "scenario": r.scenario,
            "status": r.status,
            "model": r.model,
            "input_tokens": r.input_tokens,
            "output_tokens": r.output_tokens,
            "cache_read_tokens": r.cache_read_tokens,
            "started_at": r.started_at,
            "completed_at": r.completed_at,
            "error": r.error,
            "result_draft_id": r.result_draft_id,
            "preview": (r.result_payload or {}).get("preview"),
        }
        for r in rows
    ]
