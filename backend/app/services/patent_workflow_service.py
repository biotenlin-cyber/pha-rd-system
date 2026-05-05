"""Disclosure / draft / OA / prior-art-search workflow services."""
from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models import (
    PatentDisclosure,
    PatentDraft,
    PatentOfficeAction,
    PatentPriorArtSearch,
)


# ── disclosure ───────────────────────────────────────────────────────────
async def get_disclosure(db: AsyncSession, patent_id: uuid.UUID) -> PatentDisclosure | None:
    return (
        await db.execute(
            select(PatentDisclosure).where(PatentDisclosure.patent_id == patent_id)
        )
    ).scalar_one_or_none()


async def upsert_disclosure(
    db: AsyncSession, patent_id: uuid.UUID, payload: dict[str, Any]
) -> PatentDisclosure:
    obj = await get_disclosure(db, patent_id)
    if obj:
        for k, v in payload.items():
            setattr(obj, k, v)
    else:
        obj = PatentDisclosure(patent_id=patent_id, **payload)
        db.add(obj)
    await db.flush()
    return obj


# ── drafts ───────────────────────────────────────────────────────────────
async def list_drafts(db: AsyncSession, patent_id: uuid.UUID) -> list[PatentDraft]:
    return list(
        (
            await db.execute(
                select(PatentDraft)
                .where(PatentDraft.patent_id == patent_id)
                .order_by(
                    PatentDraft.section,
                    PatentDraft.version.desc(),
                )
            )
        ).scalars().all()
    )


async def create_draft(
    db: AsyncSession,
    patent_id: uuid.UUID,
    *,
    section: str,
    content: str,
    parent_draft_id: int | None = None,
    amendment_oa_id: int | None = None,
    ai_generated: bool = False,
    ai_model: str | None = None,
    ai_confidence: str | None = None,
    created_by: str | None = None,
    notes: str | None = None,
) -> PatentDraft:
    # auto-bump version per (patent, section)
    current = (
        await db.execute(
            select(PatentDraft.version)
            .where(
                PatentDraft.patent_id == patent_id,
                PatentDraft.section == section,
            )
            .order_by(PatentDraft.version.desc())
            .limit(1)
        )
    ).scalar_one_or_none()
    obj = PatentDraft(
        patent_id=patent_id,
        section=section,
        version=(current or 0) + 1,
        content=content,
        parent_draft_id=parent_draft_id,
        amendment_oa_id=amendment_oa_id,
        ai_generated=ai_generated,
        ai_model=ai_model,
        ai_confidence=ai_confidence,
        created_by=created_by,
        notes=notes,
    )
    db.add(obj)
    await db.flush()
    return obj


async def get_draft(db: AsyncSession, draft_id: int) -> PatentDraft:
    obj = (
        await db.execute(select(PatentDraft).where(PatentDraft.id == draft_id))
    ).scalar_one_or_none()
    if not obj:
        raise NotFoundError(f"Draft {draft_id} not found")
    return obj


async def review_draft(
    db: AsyncSession, draft_id: int, *, payload: dict[str, Any]
) -> PatentDraft:
    obj = await get_draft(db, draft_id)
    for k, v in payload.items():
        if v is None:
            continue
        setattr(obj, k, v)
    if payload.get("review_decision"):
        from datetime import datetime, timezone

        obj.reviewed_at = datetime.now(tz=timezone.utc)
    await db.flush()
    return obj


# ── office actions ───────────────────────────────────────────────────────
async def list_oas(db: AsyncSession, patent_id: uuid.UUID) -> list[PatentOfficeAction]:
    return list(
        (
            await db.execute(
                select(PatentOfficeAction)
                .where(PatentOfficeAction.patent_id == patent_id)
                .order_by(PatentOfficeAction.action_no, PatentOfficeAction.id)
            )
        ).scalars().all()
    )


async def create_oa(
    db: AsyncSession, patent_id: uuid.UUID, payload: dict[str, Any]
) -> PatentOfficeAction:
    obj = PatentOfficeAction(patent_id=patent_id, **payload)
    db.add(obj)
    await db.flush()
    return obj


# ── prior art ────────────────────────────────────────────────────────────
async def list_prior_art(
    db: AsyncSession, patent_id: uuid.UUID
) -> list[PatentPriorArtSearch]:
    return list(
        (
            await db.execute(
                select(PatentPriorArtSearch)
                .where(PatentPriorArtSearch.patent_id == patent_id)
                .order_by(PatentPriorArtSearch.searched_at.desc().nullslast())
            )
        ).scalars().all()
    )


async def create_prior_art(
    db: AsyncSession, patent_id: uuid.UUID, payload: dict[str, Any]
) -> PatentPriorArtSearch:
    obj = PatentPriorArtSearch(patent_id=patent_id, **payload)
    db.add(obj)
    await db.flush()
    return obj
