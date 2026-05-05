"""CSV import for patents.

Expected columns (header row, in any order):
  internal_code (required, unique key)
  publication_no, application_no, country_code (default CN)
  title_zh (required), title_en, abstract_zh, abstract_en
  patent_type (default invention), legal_status (default disclosure)
  application_date, publication_date, grant_date  (YYYY-MM-DD)
  applicant_names    pipe-separated, e.g. "蓝晶微生物|清华大学"
  inventor_names     pipe-separated
  ipc_codes          pipe-separated, first one is primary, e.g. "C08L 67/04|C08K 5/00"
  scenario_codes     pipe-separated codes from application_scenarios
  grade_codes        pipe-separated codes from pha_grades
  tags               pipe-separated
  agency_name, internal_owner, tech_field
"""
from __future__ import annotations

import csv
import io
from datetime import date, datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.services import patent_service


def _parse_date(s: str | None) -> date | None:
    if not s or not s.strip():
        return None
    s = s.strip()
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y%m%d"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def _split_pipe(s: str | None) -> list[str]:
    if not s:
        return []
    return [p.strip() for p in s.split("|") if p.strip()]


async def import_csv(db: AsyncSession, raw: bytes) -> dict[str, Any]:
    text = raw.decode("utf-8-sig", errors="replace")
    reader = csv.DictReader(io.StringIO(text))
    received = 0
    inserted = 0
    updated = 0
    errors: list[dict[str, Any]] = []

    for line_no, row in enumerate(reader, start=2):
        received += 1
        try:
            internal_code = (row.get("internal_code") or "").strip()
            title_zh = (row.get("title_zh") or "").strip()
            if not internal_code or not title_zh:
                errors.append({"line": line_no, "error": "missing internal_code or title_zh"})
                continue

            ipc_codes = _split_pipe(row.get("ipc_codes"))
            classifications = [
                {"scheme": "IPC", "code": c, "is_primary": i == 0}
                for i, c in enumerate(ipc_codes)
            ]

            payload: dict[str, Any] = {
                "internal_code": internal_code,
                "title_zh": title_zh,
                "title_en": (row.get("title_en") or None) or None,
                "publication_no": row.get("publication_no") or None,
                "application_no": row.get("application_no") or None,
                "country_code": (row.get("country_code") or "CN").upper().strip(),
                "patent_type": (row.get("patent_type") or "invention").strip(),
                "legal_status": (row.get("legal_status") or "disclosure").strip(),
                "abstract_zh": row.get("abstract_zh") or None,
                "abstract_en": row.get("abstract_en") or None,
                "tech_field": row.get("tech_field") or None,
                "agency_name": row.get("agency_name") or None,
                "internal_owner": row.get("internal_owner") or None,
                "application_date": _parse_date(row.get("application_date")),
                "publication_date": _parse_date(row.get("publication_date")),
                "grant_date": _parse_date(row.get("grant_date")),
                "tags": _split_pipe(row.get("tags")),
                "applicant_names": _split_pipe(row.get("applicant_names")),
                "inventor_names": _split_pipe(row.get("inventor_names")),
                "classifications": classifications,
                "scenario_codes": _split_pipe(row.get("scenario_codes")),
                "grade_codes": _split_pipe(row.get("grade_codes")),
            }

            from sqlalchemy import select

            from app.models import Patent

            existing = (
                await db.execute(
                    select(Patent.id).where(Patent.internal_code == internal_code)
                )
            ).scalar_one_or_none()
            await patent_service.upsert_patent(db, payload)
            await db.commit()
            if existing is None:
                inserted += 1
            else:
                updated += 1
        except Exception as exc:  # noqa: BLE001
            await db.rollback()
            errors.append({"line": line_no, "error": str(exc)[:200]})

    return {
        "received_rows": received,
        "inserted": inserted,
        "updated": updated,
        "skipped": len(errors),
        "errors": errors,
    }
