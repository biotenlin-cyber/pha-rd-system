"""Seed loader: idempotent upsert from YAML files into the knowledge base.

Usage:
    python -m scripts.seed [--reset] [--only domains|scenarios|grades|matches|tags]
"""
import argparse
import asyncio
from pathlib import Path

import yaml
from sqlalchemy import delete, func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.models import (
    ApplicationDomain,
    ApplicationScenario,
    GradeScenarioMatch,
    GradeTag,
    Patent,
    PatentDisclosure,
    PatentLegalEvent,
    PhaGrade,
    ScenarioTag,
    Tag,
)
from app.services import patent_service

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "seed"


def _load(name: str) -> list[dict]:
    path = DATA_DIR / f"{name}.yaml"
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or []


async def _upsert_domains(db: AsyncSession) -> dict[str, int]:
    rows = _load("domains")
    code_to_id: dict[str, int] = {}
    for i, row in enumerate(rows):
        existing = (
            await db.execute(select(ApplicationDomain).where(ApplicationDomain.code == row["code"]))
        ).scalar_one_or_none()
        if existing:
            existing.name_zh = row["name_zh"]
            existing.name_en = row["name_en"]
            existing.description = row.get("description")
            existing.icon = row.get("icon")
            existing.sort_order = row.get("sort_order", i)
            code_to_id[row["code"]] = existing.id
        else:
            obj = ApplicationDomain(
                code=row["code"],
                name_zh=row["name_zh"],
                name_en=row["name_en"],
                description=row.get("description"),
                icon=row.get("icon"),
                sort_order=row.get("sort_order", i),
            )
            db.add(obj)
            await db.flush()
            code_to_id[row["code"]] = obj.id
    await db.commit()
    return code_to_id


async def _upsert_tags(db: AsyncSession) -> dict[str, int]:
    rows = _load("tags")
    slug_to_id: dict[str, int] = {}
    for row in rows:
        existing = (
            await db.execute(select(Tag).where(Tag.slug == row["slug"]))
        ).scalar_one_or_none()
        if existing:
            existing.name_zh = row["name_zh"]
            existing.category = row.get("category")
            existing.color = row.get("color")
            slug_to_id[row["slug"]] = existing.id
        else:
            obj = Tag(
                slug=row["slug"],
                name_zh=row["name_zh"],
                category=row.get("category"),
                color=row.get("color"),
            )
            db.add(obj)
            await db.flush()
            slug_to_id[row["slug"]] = obj.id
    await db.commit()
    return slug_to_id


async def _upsert_scenarios(
    db: AsyncSession, domain_codes: dict[str, int], tag_slugs: dict[str, int]
) -> dict[str, int]:
    rows = _load("scenarios")
    code_to_id: dict[str, int] = {}
    for row in rows:
        domain_id = domain_codes[row["domain"]]
        existing = (
            await db.execute(
                select(ApplicationScenario).where(ApplicationScenario.code == row["code"])
            )
        ).scalar_one_or_none()
        data = {
            "domain_id": domain_id,
            "name_zh": row["name_zh"],
            "name_en": row.get("name_en"),
            "summary": row.get("summary"),
            "sub_scenarios": row.get("sub_scenarios", []),
            "technical_requirements": row.get("technical_requirements", {}),
            "typical_products": row.get("typical_products", []),
            "market_size_usd": row.get("market_size_usd"),
            "market_year": row.get("market_year"),
            "market_notes": row.get("market_notes"),
            "status": row.get("status", "active"),
        }
        if existing:
            for k, v in data.items():
                setattr(existing, k, v)
            scenario_id = existing.id
        else:
            obj = ApplicationScenario(code=row["code"], **data)
            db.add(obj)
            await db.flush()
            scenario_id = obj.id
        code_to_id[row["code"]] = scenario_id

        await db.execute(delete(ScenarioTag).where(ScenarioTag.scenario_id == scenario_id))
        for slug in row.get("tags", []) or []:
            if slug in tag_slugs:
                db.add(ScenarioTag(scenario_id=scenario_id, tag_id=tag_slugs[slug]))

        await _set_scenario_search_vector(db, scenario_id)
    await db.commit()
    return code_to_id


async def _set_scenario_search_vector(db: AsyncSession, scenario_id: int) -> None:
    await db.execute(
        text(
            """
            UPDATE application_scenarios
            SET search_vector = to_tsvector('simple',
                coalesce(name_zh,'') || ' ' ||
                coalesce(name_en,'') || ' ' ||
                coalesce(summary,'') || ' ' ||
                coalesce(code,''))
            WHERE id = :sid
            """
        ),
        {"sid": scenario_id},
    )


async def _upsert_grades(
    db: AsyncSession, tag_slugs: dict[str, int]
) -> dict[str, int]:
    rows = _load("grades")
    code_to_id: dict[str, int] = {}
    for row in rows:
        existing = (
            await db.execute(select(PhaGrade).where(PhaGrade.code == row["code"]))
        ).scalar_one_or_none()
        data = {
            "name_zh": row["name_zh"],
            "full_name": row.get("full_name"),
            "polymer_family": row.get("polymer_family"),
            "description": row.get("description"),
            "tm_celsius": row.get("tm_celsius"),
            "tg_celsius": row.get("tg_celsius"),
            "crystallinity_pct": row.get("crystallinity_pct"),
            "elongation_at_break_pct": row.get("elongation_at_break_pct"),
            "tensile_strength_mpa": row.get("tensile_strength_mpa"),
            "youngs_modulus_gpa": row.get("youngs_modulus_gpa"),
            "biocompatibility_class": row.get("biocompatibility_class"),
            "degradation_months_soil": row.get("degradation_months_soil"),
            "degradation_months_marine": row.get("degradation_months_marine"),
            "extra_metrics": row.get("extra_metrics", {}),
            "typical_processing": row.get("typical_processing", []),
            "status": row.get("status", "active"),
        }
        if existing:
            for k, v in data.items():
                setattr(existing, k, v)
            grade_id = existing.id
        else:
            obj = PhaGrade(code=row["code"], **data)
            db.add(obj)
            await db.flush()
            grade_id = obj.id
        code_to_id[row["code"]] = grade_id

        await db.execute(delete(GradeTag).where(GradeTag.grade_id == grade_id))
        for slug in row.get("tags", []) or []:
            if slug in tag_slugs:
                db.add(GradeTag(grade_id=grade_id, tag_id=tag_slugs[slug]))

        await db.execute(
            text(
                """
                UPDATE pha_grades
                SET search_vector = to_tsvector('simple',
                    coalesce(name_zh,'') || ' ' ||
                    coalesce(code,'') || ' ' ||
                    coalesce(full_name,'') || ' ' ||
                    coalesce(description,''))
                WHERE id = :gid
                """
            ),
            {"gid": grade_id},
        )
    await db.commit()
    return code_to_id


async def _upsert_matches(
    db: AsyncSession, grades: dict[str, int], scenarios: dict[str, int]
) -> int:
    rows = _load("matches")
    count = 0
    for row in rows:
        grade_id = grades.get(row["grade"])
        scenario_id = scenarios.get(row["scenario"])
        if not grade_id or not scenario_id:
            continue
        existing = (
            await db.execute(
                select(GradeScenarioMatch).where(
                    GradeScenarioMatch.grade_id == grade_id,
                    GradeScenarioMatch.scenario_id == scenario_id,
                )
            )
        ).scalar_one_or_none()
        data = {
            "match_score": row["match_score"],
            "recommendation_level": row["recommendation_level"],
            "key_metrics": row.get("key_metrics", {}),
            "rationale": row.get("rationale"),
            "refs": row.get("references", []),
        }
        if existing:
            for k, v in data.items():
                setattr(existing, k, v)
        else:
            db.add(
                GradeScenarioMatch(grade_id=grade_id, scenario_id=scenario_id, **data)
            )
        count += 1
    await db.commit()
    return count


async def _reset(db: AsyncSession) -> None:
    # Truncate in dependency order (CASCADE cleans children automatically)
    for tbl in (
        "patent_draft_jobs",
        "patent_drafts",
        "patent_office_actions",
        "patent_disclosures",
        "patent_prior_art_searches",
        "patent_fee_events",
        "patent_legal_events",
        "patent_citations",
        "patent_priorities",
        "patent_classifications",
        "patent_inventors",
        "patent_applicants",
        "patent_scenarios",
        "patent_grades",
        "patents",
        "applicants",
        "inventors",
        "grade_scenario_matches",
        "scenario_tags",
        "grade_tags",
        "scenario_external_links",
        "grade_external_links",
        "application_scenarios",
        "pha_grades",
        "tags",
        "application_domains",
    ):
        await db.execute(text(f"TRUNCATE {tbl} RESTART IDENTITY CASCADE"))
    await db.commit()


async def _upsert_patents(db: AsyncSession) -> int:
    rows = _load("patents")
    n = 0
    for row in rows:
        # Map YAML row → patent_service payload
        payload = {
            **row,
            "applicant_names": row.get("applicant_names") or [],
            "inventor_names": row.get("inventor_names") or [],
        }
        patent = await patent_service.upsert_patent(db, dict(payload))
        # Add a couple of representative legal events so the UI can show timeline
        if patent.application_date:
            await patent_service.add_legal_event(
                db,
                patent.id,
                event_code="filed",
                event_date=patent.application_date,
                event_desc="申请",
                source="seed",
            )
        if patent.publication_date:
            await patent_service.add_legal_event(
                db,
                patent.id,
                event_code="published",
                event_date=patent.publication_date,
                event_desc="公开",
                source="seed",
            )
        if patent.grant_date:
            await patent_service.add_legal_event(
                db,
                patent.id,
                event_code="granted",
                event_date=patent.grant_date,
                event_desc="授权",
                source="seed",
            )
        # Disclosure for the disclosure/drafting status patents (PHA-2024-007, 008)
        if patent.legal_status in ("disclosure", "drafting"):
            existing = await db.execute(
                text("SELECT id FROM patent_disclosures WHERE patent_id = :pid"),
                {"pid": patent.id},
            )
            if existing.scalar_one_or_none() is None:
                tags_l = patent.tags or []
                db.add(
                    PatentDisclosure(
                        patent_id=patent.id,
                        submitted_by=patent.internal_owner or "研发组",
                        problem_statement="现有 PHA 在该应用场景下存在加工窗口窄、力学指标不足或降解周期不可控的问题。",
                        existing_solutions="检索到的现有技术多采用单一 PHA 牌号或 PLA 共混，难以兼顾上述指标。",
                        proposed_solution="采用多元共混 + 成核/扩链协同改性，并通过精确的工艺参数窗口控制实现性能目标。",
                        key_points=[
                            "共混体系中各组分配比的关键区间",
                            "成核 / 扩链剂用量与协同机理",
                            "关键工艺温度窗口与停留时间",
                        ],
                        advantages="性能指标较单一牌号显著提升，加工窗口拓宽，降解周期可控。",
                        embodiments=[
                            {"id": 1, "title": "实施例 1", "content": "按主权利要求最优配比制备样品，性能指标达标。"},
                        ],
                        confidentiality_level="internal",
                        status="approved" if patent.legal_status == "drafting" else "submitted",
                    )
                )
        n += 1
    await db.commit()
    return n


async def main(reset: bool, only: str | None) -> None:
    async with AsyncSessionLocal() as db:
        if reset:
            print("[seed] reset → truncating tables")
            await _reset(db)

        domains = await _upsert_domains(db)
        print(f"[seed] domains: {len(domains)}")

        tags = await _upsert_tags(db)
        print(f"[seed] tags: {len(tags)}")

        scenarios = await _upsert_scenarios(db, domains, tags)
        print(f"[seed] scenarios: {len(scenarios)}")

        grades = await _upsert_grades(db, tags)
        print(f"[seed] grades: {len(grades)}")

        n = await _upsert_matches(db, grades, scenarios)
        print(f"[seed] matches: {n}")

        np = await _upsert_patents(db)
        print(f"[seed] patents: {np}")

        total_scenarios = (
            await db.execute(select(func.count()).select_from(ApplicationScenario))
        ).scalar_one()
        total_grades = (
            await db.execute(select(func.count()).select_from(PhaGrade))
        ).scalar_one()
        total_matches = (
            await db.execute(select(func.count()).select_from(GradeScenarioMatch))
        ).scalar_one()
        print(
            f"[seed] done. scenarios={total_scenarios} grades={total_grades} "
            f"matches={total_matches}"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true")
    parser.add_argument("--only", default=None)
    args = parser.parse_args()
    asyncio.run(main(args.reset, args.only))
