"""Core CRUD + composite read for patents.

Handles the patents main table together with normalized inventors/applicants
and IPC classifications. Splits the IPC code into section/class/subclass/main_group
on write so the analytics layer can do efficient GROUP BY.
"""
from __future__ import annotations

import re
import unicodedata
import uuid
from typing import Any

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import NotFoundError
from app.models import (
    ApplicationDomain,
    ApplicationScenario,
    Applicant,
    GradeScenarioMatch,  # noqa: F401  (registered)
    Inventor,
    Patent,
    PatentApplicant,
    PatentClassification,
    PatentDisclosure,
    PatentDraft,
    PatentGrade,
    PatentInventor,
    PatentLegalEvent,
    PatentOfficeAction,
    PatentScenario,
    PhaGrade,
)


# ── helpers ──────────────────────────────────────────────────────────────
def normalize_name(name: str) -> str:
    s = unicodedata.normalize("NFKC", (name or "").strip().lower())
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[（）()【】\[\],，.。\-—_/]+", " ", s)
    return s.strip()[:300]


_IPC_RE = re.compile(
    r"^([A-H])"            # section
    r"(\d{2})"             # class digits
    r"([A-Z])"             # subclass
    r"\s*"                 # space
    r"(\d{1,4})"           # main group
    r"\s*/\s*"
    r"(\d{1,6})"           # subgroup
    r"$"
)


def parse_ipc(code: str) -> dict[str, str | None]:
    cleaned = (code or "").strip().upper().replace("  ", " ")
    m = _IPC_RE.match(cleaned)
    if not m:
        return {
            "full_symbol": cleaned,
            "section": cleaned[:1] if cleaned else None,
            "class_code": cleaned[:3] if len(cleaned) >= 3 else None,
            "subclass": cleaned[:4] if len(cleaned) >= 4 else None,
            "main_group": None,
        }
    section, cls, subc, mg, _sg = m.groups()
    return {
        "full_symbol": f"{section}{cls}{subc} {mg}/{_sg}",
        "section": section,
        "class_code": f"{section}{cls}",
        "subclass": f"{section}{cls}{subc}",
        "main_group": f"{section}{cls}{subc}{mg}",
    }


# ── upsert helpers ───────────────────────────────────────────────────────
async def get_or_create_inventor(db: AsyncSession, name_zh: str, *, name_en: str | None = None) -> Inventor:
    key = normalize_name(name_zh)
    obj = (
        await db.execute(select(Inventor).where(Inventor.normalized_key == key))
    ).scalar_one_or_none()
    if obj:
        return obj
    obj = Inventor(name_zh=name_zh, name_en=name_en, normalized_key=key)
    db.add(obj)
    await db.flush()
    return obj


async def get_or_create_applicant(
    db: AsyncSession,
    name_zh: str,
    *,
    name_en: str | None = None,
    applicant_type: str = "company",
    country_code: str | None = None,
) -> Applicant:
    key = normalize_name(name_zh)
    obj = (
        await db.execute(select(Applicant).where(Applicant.normalized_key == key))
    ).scalar_one_or_none()
    if obj:
        return obj
    obj = Applicant(
        name_zh=name_zh,
        name_en=name_en,
        normalized_key=key,
        applicant_type=applicant_type,
        country_code=country_code,
    )
    db.add(obj)
    await db.flush()
    return obj


# ── core ops ─────────────────────────────────────────────────────────────
async def list_patents(
    db: AsyncSession,
    *,
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
) -> tuple[list[dict[str, Any]], int]:
    base = select(Patent.id).where(Patent.legal_status != "withdrawn")
    if q:
        like = f"%{q}%"
        base = base.where(
            (Patent.title_zh.ilike(like))
            | (Patent.abstract_zh.ilike(like))
            | (Patent.internal_code.ilike(like))
            | (Patent.publication_no.ilike(like))
        )
    if legal_status:
        base = base.where(Patent.legal_status == legal_status)
    if country:
        base = base.where(Patent.country_code == country)
    if grade:
        base = base.where(
            Patent.id.in_(
                select(PatentGrade.patent_id)
                .join(PhaGrade, PhaGrade.id == PatentGrade.grade_id)
                .where(PhaGrade.code == grade)
            )
        )
    if scenario or domain:
        scenario_filter = (
            select(PatentScenario.patent_id)
            .join(ApplicationScenario, ApplicationScenario.id == PatentScenario.scenario_id)
            .join(ApplicationDomain, ApplicationDomain.id == ApplicationScenario.domain_id)
        )
        if scenario:
            scenario_filter = scenario_filter.where(ApplicationScenario.code == scenario)
        if domain:
            scenario_filter = scenario_filter.where(ApplicationDomain.code == domain)
        base = base.where(Patent.id.in_(scenario_filter))
    if applicant:
        base = base.where(
            Patent.id.in_(
                select(PatentApplicant.patent_id)
                .join(Applicant, Applicant.id == PatentApplicant.applicant_id)
                .where(Applicant.name_zh.ilike(f"%{applicant}%"))
            )
        )
    if tag:
        base = base.where(Patent.tags.contains([tag]))

    total = (
        await db.execute(select(func.count()).select_from(base.subquery()))
    ).scalar_one()

    paged_ids = list(
        (
            await db.execute(
                base.order_by(Patent.application_date.desc().nullslast(), Patent.id)
                .offset((page - 1) * page_size)
                .limit(page_size)
            )
        ).scalars().all()
    )
    if not paged_ids:
        return [], int(total)

    summaries = await _fetch_patent_summaries(db, paged_ids)
    return summaries, int(total)


async def _fetch_patent_summaries(
    db: AsyncSession, patent_ids: list[uuid.UUID]
) -> list[dict[str, Any]]:
    rows = (
        await db.execute(
            select(Patent)
            .options(
                selectinload(Patent.inventor_links).selectinload(PatentInventor.inventor),
                selectinload(Patent.applicant_links).selectinload(PatentApplicant.applicant),
                selectinload(Patent.classifications),
            )
            .where(Patent.id.in_(patent_ids))
        )
    ).scalars().all()
    by_id = {r.id: r for r in rows}
    out: list[dict[str, Any]] = []
    for pid in patent_ids:
        p = by_id.get(pid)
        if not p:
            continue
        primary_appl = next(
            (l for l in p.applicant_links if l.role == "primary"), p.applicant_links[0] if p.applicant_links else None
        )
        first_inv = next(
            (l for l in sorted(p.inventor_links, key=lambda x: x.seq)),
            None,
        )
        primary_ipc = next(
            (c.full_symbol or c.code for c in p.classifications if c.is_primary),
            (p.classifications[0].full_symbol or p.classifications[0].code) if p.classifications else None,
        )
        out.append(
            {
                "id": p.id,
                "internal_code": p.internal_code,
                "publication_no": p.publication_no,
                "title_zh": p.title_zh,
                "country_code": p.country_code,
                "patent_type": p.patent_type,
                "legal_status": p.legal_status,
                "application_date": p.application_date,
                "grant_date": p.grant_date,
                "primary_applicant": primary_appl.applicant.name_zh if primary_appl else None,
                "first_inventor": first_inv.inventor.name_zh if first_inv else None,
                "primary_ipc": primary_ipc,
                "tags": p.tags or [],
            }
        )
    return out


async def get_patent_detail(db: AsyncSession, key: str) -> dict[str, Any]:
    stmt = (
        select(Patent)
        .options(
            selectinload(Patent.inventor_links).selectinload(PatentInventor.inventor),
            selectinload(Patent.applicant_links).selectinload(PatentApplicant.applicant),
            selectinload(Patent.classifications),
            selectinload(Patent.priorities),
            selectinload(Patent.legal_events),
            selectinload(Patent.scenario_links)
            .selectinload(PatentScenario.scenario)
            .selectinload(ApplicationScenario.domain),
            selectinload(Patent.grade_links).selectinload(PatentGrade.grade),
        )
    )
    if _is_uuid(key):
        stmt = stmt.where(Patent.id == uuid.UUID(key))
    else:
        stmt = stmt.where(Patent.internal_code == key)
    p = (await db.execute(stmt)).scalar_one_or_none()
    if not p:
        raise NotFoundError(f"Patent '{key}' not found")

    has_disclosure = (
        await db.execute(
            select(func.count()).select_from(PatentDisclosure).where(PatentDisclosure.patent_id == p.id)
        )
    ).scalar_one() > 0
    draft_count = (
        await db.execute(
            select(func.count()).select_from(PatentDraft).where(PatentDraft.patent_id == p.id)
        )
    ).scalar_one()
    oa_count = (
        await db.execute(
            select(func.count()).select_from(PatentOfficeAction).where(PatentOfficeAction.patent_id == p.id)
        )
    ).scalar_one()

    return {
        **{c.name: getattr(p, c.name) for c in p.__table__.columns},
        "inventors": [
            {
                "inventor_id": l.inventor_id,
                "name_zh": l.inventor.name_zh,
                "name_en": l.inventor.name_en,
                "seq": l.seq,
                "contribution_pct": float(l.contribution_pct) if l.contribution_pct else None,
                "is_corresponding": l.is_corresponding,
            }
            for l in sorted(p.inventor_links, key=lambda x: x.seq)
        ],
        "applicants": [
            {
                "applicant_id": l.applicant_id,
                "name_zh": l.applicant.name_zh,
                "name_en": l.applicant.name_en,
                "applicant_type": l.applicant.applicant_type,
                "country_code": l.applicant.country_code,
                "role": l.role,
                "share_pct": float(l.share_pct) if l.share_pct else None,
            }
            for l in p.applicant_links
        ],
        "classifications": p.classifications,
        "priorities": p.priorities,
        "legal_events": sorted(p.legal_events, key=lambda x: x.event_date, reverse=True),
        "scenarios": [
            {
                "scenario_id": l.scenario_id,
                "scenario_code": l.scenario.code,
                "scenario_name_zh": l.scenario.name_zh,
                "domain_code": l.scenario.domain.code,
                "relevance": l.relevance,
            }
            for l in p.scenario_links
        ],
        "grades": [
            {
                "grade_id": l.grade_id,
                "grade_code": l.grade.code,
                "grade_name_zh": l.grade.name_zh,
                "relevance": l.relevance,
            }
            for l in p.grade_links
        ],
        "has_disclosure": has_disclosure,
        "draft_count": int(draft_count),
        "oa_count": int(oa_count),
    }


def _is_uuid(s: str) -> bool:
    try:
        uuid.UUID(s)
        return True
    except (ValueError, TypeError):
        return False


async def upsert_patent(db: AsyncSession, payload: dict[str, Any]) -> Patent:
    """Insert or update a patent by internal_code, plus all relations.

    Used by both /patents POST endpoint and the seed loader.
    """
    inventor_payload = payload.pop("inventors", []) or []
    applicant_payload = payload.pop("applicants", []) or []
    classifications = payload.pop("classifications", []) or []
    scenario_codes = payload.pop("scenario_codes", []) or []
    grade_codes = payload.pop("grade_codes", []) or []
    inventor_names = payload.pop("inventor_names", None)
    applicant_names = payload.pop("applicant_names", None)
    payload.pop("key_points", None)  # ignore: not part of patents table

    existing = (
        await db.execute(
            select(Patent).where(Patent.internal_code == payload["internal_code"])
        )
    ).scalar_one_or_none()

    if existing:
        for k, v in payload.items():
            if hasattr(existing, k):
                setattr(existing, k, v)
        patent = existing
    else:
        patent = Patent(**payload)
        db.add(patent)
    await db.flush()

    # Inventors: accept either structured dicts or simple name list
    await _set_inventors(db, patent, inventor_payload, fallback_names=inventor_names or [])
    await _set_applicants(db, patent, applicant_payload, fallback_names=applicant_names or [])
    await _set_classifications(db, patent, classifications)
    await _set_scenarios(db, patent, scenario_codes)
    await _set_grades(db, patent, grade_codes)

    return patent


async def _set_inventors(
    db: AsyncSession,
    patent: Patent,
    structured: list[dict[str, Any]],
    *,
    fallback_names: list[str] = (),
) -> None:
    items = list(structured) or [{"name_zh": n} for n in fallback_names]
    await db.execute(delete(PatentInventor).where(PatentInventor.patent_id == patent.id))
    await db.flush()
    for idx, item in enumerate(items, start=1):
        if not item.get("name_zh"):
            continue
        inv = await get_or_create_inventor(
            db, item["name_zh"], name_en=item.get("name_en")
        )
        db.add(
            PatentInventor(
                patent_id=patent.id,
                inventor_id=inv.id,
                seq=item.get("seq", idx),
                contribution_pct=item.get("contribution_pct"),
                is_corresponding=bool(item.get("is_corresponding", False)),
            )
        )
    await db.flush()


async def _set_applicants(
    db: AsyncSession,
    patent: Patent,
    structured: list[dict[str, Any]],
    *,
    fallback_names: list[str] = (),
) -> None:
    items = list(structured) or [
        {"name_zh": n, "role": "primary" if i == 0 else "co"}
        for i, n in enumerate(fallback_names)
    ]
    await db.execute(delete(PatentApplicant).where(PatentApplicant.patent_id == patent.id))
    await db.flush()
    for idx, item in enumerate(items):
        if not item.get("name_zh"):
            continue
        appl = await get_or_create_applicant(
            db,
            item["name_zh"],
            name_en=item.get("name_en"),
            applicant_type=item.get("applicant_type", "company"),
            country_code=item.get("country_code"),
        )
        role = item.get("role") or ("primary" if idx == 0 else "co")
        db.add(
            PatentApplicant(
                patent_id=patent.id,
                applicant_id=appl.id,
                role=role,
                share_pct=item.get("share_pct"),
            )
        )
    await db.flush()


async def _set_classifications(
    db: AsyncSession, patent: Patent, items: list[dict[str, Any]]
) -> None:
    await db.execute(
        delete(PatentClassification).where(PatentClassification.patent_id == patent.id)
    )
    await db.flush()
    for idx, item in enumerate(items):
        scheme = item.get("scheme", "IPC")
        code = item.get("code")
        if not code:
            continue
        parsed = parse_ipc(code) if scheme == "IPC" else {"full_symbol": code}
        db.add(
            PatentClassification(
                patent_id=patent.id,
                scheme=scheme,
                code=code,
                full_symbol=parsed.get("full_symbol"),
                section=parsed.get("section"),
                class_code=parsed.get("class_code"),
                subclass=parsed.get("subclass"),
                main_group=parsed.get("main_group"),
                classification_value=item.get("classification_value", "inventive"),
                rank_order=item.get("rank_order", idx),
                is_primary=bool(item.get("is_primary", False)),
            )
        )
    await db.flush()


async def _set_scenarios(
    db: AsyncSession, patent: Patent, codes: list[str]
) -> None:
    await db.execute(delete(PatentScenario).where(PatentScenario.patent_id == patent.id))
    await db.flush()
    if not codes:
        return
    rows = (
        await db.execute(
            select(ApplicationScenario.id, ApplicationScenario.code).where(
                ApplicationScenario.code.in_(codes)
            )
        )
    ).all()
    for sid, _code in rows:
        db.add(PatentScenario(patent_id=patent.id, scenario_id=sid, relevance=3))
    await db.flush()


async def _set_grades(
    db: AsyncSession, patent: Patent, codes: list[str]
) -> None:
    await db.execute(delete(PatentGrade).where(PatentGrade.patent_id == patent.id))
    await db.flush()
    if not codes:
        return
    rows = (
        await db.execute(
            select(PhaGrade.id, PhaGrade.code).where(PhaGrade.code.in_(codes))
        )
    ).all()
    for gid, _code in rows:
        db.add(PatentGrade(patent_id=patent.id, grade_id=gid, relevance=3))
    await db.flush()


async def add_legal_event(
    db: AsyncSession,
    patent_id: uuid.UUID,
    *,
    event_code: str,
    event_date,
    event_desc: str | None = None,
    source: str | None = "manual",
) -> PatentLegalEvent:
    ev = PatentLegalEvent(
        patent_id=patent_id,
        event_code=event_code,
        event_date=event_date,
        event_desc=event_desc,
        source=source,
    )
    db.add(ev)
    await db.flush()
    return ev


async def list_patents_for_scenario(
    db: AsyncSession, scenario_id: int
) -> list[dict[str, Any]]:
    stmt = (
        select(Patent, PatentScenario.relevance)
        .join(PatentScenario, PatentScenario.patent_id == Patent.id)
        .where(PatentScenario.scenario_id == scenario_id)
        .order_by(Patent.application_date.desc().nullslast())
    )
    rows = (await db.execute(stmt)).all()
    return [
        {
            "id": p.id,
            "internal_code": p.internal_code,
            "publication_no": p.publication_no,
            "title_zh": p.title_zh,
            "legal_status": p.legal_status,
            "country_code": p.country_code,
            "application_date": p.application_date,
            "relevance": rel,
        }
        for p, rel in rows
    ]


async def list_patents_for_grade(
    db: AsyncSession, grade_id: int
) -> list[dict[str, Any]]:
    stmt = (
        select(Patent, PatentGrade.relevance)
        .join(PatentGrade, PatentGrade.patent_id == Patent.id)
        .where(PatentGrade.grade_id == grade_id)
        .order_by(Patent.application_date.desc().nullslast())
    )
    rows = (await db.execute(stmt)).all()
    return [
        {
            "id": p.id,
            "internal_code": p.internal_code,
            "publication_no": p.publication_no,
            "title_zh": p.title_zh,
            "legal_status": p.legal_status,
            "country_code": p.country_code,
            "application_date": p.application_date,
            "relevance": rel,
        }
        for p, rel in rows
    ]
