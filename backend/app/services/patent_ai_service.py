"""AI-assisted patent drafting via Anthropic Claude API.

Designed per the AI-drafting expert review:
  * professional Chinese-patent-attorney system prompt with hard constraints
  * 4-block prompt caching (rules / CNIPA-guideline excerpt / glossary / output schema)
  * 4 scenarios: claims_from_disclosure / dependent_claims / spec_from_claims / oa_response
  * streaming via SSE for long outputs
  * model selection: Sonnet for drafting, Opus for OA, Haiku for self-critique
  * persists every job in patent_draft_jobs and saves drafts when scenario=='claims_from_disclosure'

Env: ANTHROPIC_API_KEY required; when missing, raise so endpoint returns 503.
"""
from __future__ import annotations

import json
import logging
import os
import uuid
from collections.abc import AsyncIterator
from datetime import datetime, timezone
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import NotFoundError
from app.models import Patent, PatentDraftJob
from app.services import patent_service, patent_workflow_service

logger = logging.getLogger(__name__)


SYSTEM_ROLE_AND_RULES = """# 角色
你是一位资深中国专利代理师（专代师），具备 10 年以上化工 / PHA（聚羟基脂肪酸酯）领域专利代理经验，深度熟悉《中华人民共和国专利法》《专利法实施细则》《专利审查指南（2023）》第二部分（实质审查）。你的输出将由人工专代师复核后递交国家知识产权局（CNIPA）。

# 撰写硬约束
1. 权利要求采用"前序部分+特征部分"两段式（独权）。从权按引用关系层层展开，禁止多项引用多项。
2. 独权追求最大合理保护范围（必要技术特征最少集合）；从权依次添加优选范围、具体参数、Markush 通式成员、实施例特征，构成防御梯度。
3. 化合物用 Markush 通式（R1/R2/X/n 等占位符必须定义清楚）；工艺参数用闭区间，并在说明书给出端点+中点共 ≥3 实施例支持。
4. 中文专利文体：禁用"应该 / 可能 / 比较 / 大约 / 差不多 / 较好 / 良好"等弱化词；允许"优选 / 进一步优选 / 特别地 / 在一些实施方式中"。
5. 术语一致性：全文同一概念用同一术语；首次出现的英文缩写须给中文全称。
6. 说明书五段：技术领域 / 背景技术 / 发明内容（含技术问题/技术方案/有益效果） / 附图说明 / 具体实施方式。
7. 实施例必须包含原料、配比、操作步骤、表征数据。

# 安全护栏
- **禁止编造**：仅可基于用户提供的"技术交底书"内容撰写；缺失要素一律输出到 missing_inputs 字段。
- **禁止抄袭**：不得复制现有技术综述中的连续 ≥20 字原文。
- **不确定性透传**：推断性内容用 confidence:"low" 标记并在 ai_generated_segments.notes 解释。
- **拒绝越权**：不得就专利可专利性 / 新颖性 / 创造性给出法律结论。

# 输出格式（严格 JSON，不要 Markdown 代码块包裹）
{
  "claims": [{"number": 1, "type": "independent|dependent", "depends_on": null|int, "text": "..."}],
  "abstract": "200 字以内",
  "description": {
    "technical_field": "...",
    "background_art": "...",
    "summary_of_invention": {"problem":"...", "solution":"...", "effects":"..."},
    "detailed_description": "...",
    "embodiments": [{"id": 1, "title":"...", "content":"..."}]
  },
  "missing_inputs": ["..."],
  "ai_generated_segments": [{"path":"claims[0]", "confidence":"high|medium|low", "notes":"..."}]
}
"""

CNIPA_GUIDELINES_EXCERPT = """# 《专利审查指南（2023）》第二部分核心节选

## 第二章 说明书和权利要求书
3.1.1 独立权利要求应当从整体上反映发明或者实用新型的技术方案，记载解决其技术问题的必要技术特征。
3.2.2 引用两项以上权利要求的多项从属权利要求，只能以择一方式引用在前的权利要求，并不得作为另一项多项从属权利要求的基础。
3.3 权利要求的撰写：
  - 一项发明或实用新型应当只有一个独立权利要求；
  - 独立权利要求应当包括前序部分和特征部分；
  - 前序部分应当写明发明或实用新型要求保护的主题名称和与现有技术共有的必要技术特征；
  - 特征部分应当用"其特征在于"或类似用语写明使发明或实用新型区别于现有技术的技术特征。

## 第三章 新颖性
2.1 新颖性指：在申请日以前没有同样的发明或者实用新型在国内外出版物上公开发表过、在国内公开使用过或者以其他方式为公众所知，也没有同样的发明或者实用新型由他人向国务院专利行政部门提出过申请。

## 第四章 创造性
2.2 创造性的判断方法 — 三步法：
  (1) 确定最接近的现有技术；
  (2) 确定发明的区别特征和发明实际解决的技术问题；
  (3) 判断要求保护的发明对本领域的技术人员来说是否显而易见。

## 第七章 充分公开
2.1 说明书应当对发明或者实用新型作出清楚、完整的说明，以所属技术领域的技术人员能够实现为准。
"""

PHA_GLOSSARY = """# PHA 领域术语表（撰写时优先使用）

## 高分子家族
- 聚羟基脂肪酸酯（PHA）：polyhydroxyalkanoate；微生物合成的可降解聚酯总称。
- 聚 3-羟基丁酸酯（PHB）：poly(3-hydroxybutyrate)，scl-PHA 代表牌号。
- 聚 3-羟基丁酸酯-co-3-羟基戊酸酯（PHBV）：HV 含量影响结晶度与韧性。
- 聚 3-羟基丁酸酯-co-3-羟基己酸酯（PHBHHx）：HHx 单体显著提升断裂伸长率与生物相容性。
- 聚 3-羟基丁酸酯-co-4-羟基丁酸酯（P34HB）：4HB 含量从 0~99% 连续可调，性能从硬塑料到弹性体。
- 中链 mcl-PHA：medium-chain-length PHA，C6–C14 单体单元，呈热塑性弹性体特征。

## 工艺与表征
- 双螺杆熔融共混挤出造粒；流化床喷涂；熔融纺丝；FDM 长丝；选区激光烧结（SLS）；静电纺丝。
- 拉伸强度 / 断裂伸长率 / 冲击强度 / 撕裂强度 / 结节强度。
- 熔点 Tm / 玻璃化温度 Tg / 结晶度 / 熔体流动指数 MFR。
- 体外 / 体内降解周期；ISO 10993 系列生物相容性评价；EN13432 / ASTM D6400 工业堆肥认证。

## CNIPA 实务
- "本发明涉及…技术领域，特别涉及…"；"现有技术中存在…的问题"；
  "为解决上述技术问题，本发明提供…"；"在一些实施方式中…"；"实施例 1:";
- 数值范围两端值视为可选优选点："5%~15%，优选 8%~12%，更优选 10%"。
"""

OUTPUT_SCHEMA_HINT = """# 输出 schema 提示
仅输出一个合法 JSON 对象，不带 markdown 围栏 ```json 标签。
所有字符串使用 UTF-8 中文字符，权利要求每条以中文标点 "。" 结尾。
"""


def _build_system_prompt() -> list[dict[str, Any]]:
    """4-block cache_control system prompt (per AI expert review)."""
    return [
        {"type": "text", "text": SYSTEM_ROLE_AND_RULES},
        {
            "type": "text",
            "text": CNIPA_GUIDELINES_EXCERPT,
            "cache_control": {"type": "ephemeral"},
        },
        {
            "type": "text",
            "text": PHA_GLOSSARY,
            "cache_control": {"type": "ephemeral"},
        },
        {
            "type": "text",
            "text": OUTPUT_SCHEMA_HINT,
            "cache_control": {"type": "ephemeral"},
        },
    ]


def _build_user_prompt(
    scenario: str,
    *,
    patent: Patent,
    disclosure: Any | None = None,
    extra_context: str | None = None,
) -> str:
    grade_codes = ", ".join(g.grade.code for g in (patent.grade_links or []))
    scenario_codes = ", ".join(s.scenario.code for s in (patent.scenario_links or []))
    base = (
        f"[案件] {patent.internal_code} {patent.title_zh}\n"
        f"[关联牌号] {grade_codes or '未指定'}\n"
        f"[关联应用场景] {scenario_codes or '未指定'}\n"
    )

    if scenario == "claims_from_disclosure":
        if not disclosure:
            return base + "\n[错误] 缺少技术交底书，无法起草。"
        return (
            base
            + f"\n[技术问题] {disclosure.problem_statement or '未提供'}\n"
            + f"[现有技术] {disclosure.existing_solutions or '未提供'}\n"
            + f"[技术方案] {disclosure.proposed_solution or '未提供'}\n"
            + f"[发明点] {json.dumps(disclosure.key_points or [], ensure_ascii=False)}\n"
            + f"[有益效果] {disclosure.advantages or '未提供'}\n"
            + f"[实施例] {json.dumps(disclosure.embodiments or [], ensure_ascii=False)}\n"
            + (f"[补充上下文] {extra_context}\n" if extra_context else "")
            + "\n[任务] 撰写权 1 独权（≤7 个必要技术特征）+ 8~12 项从权，"
            + "并输出摘要、说明书五段、≥3 个实施例。严格按 system 中的 JSON schema 输出。"
        )

    if scenario == "dependent_claims":
        return (
            base
            + f"\n[补充上下文 / 已有权利要求 1] {extra_context or '未提供'}\n"
            + "\n[任务] 在已有权 1 基础上撰写 8~12 项从权，覆盖参数优选 / 子结构 Markush / 工艺步骤 / 应用场景。"
        )

    if scenario == "spec_from_claims":
        return (
            base
            + f"\n[已有权利要求] {extra_context or '未提供'}\n"
            + "\n[任务] 撰写说明书技术领域 / 背景技术 / 发明内容 / 附图说明 / 具体实施方式（≥3 实施例）。"
        )

    if scenario == "oa_response":
        return (
            base
            + f"\n[OA 通知书与对比文件] {extra_context or '未提供'}\n"
            + "\n[任务] 输出权利要求修改建议（标 add/del）+ 答辩意见（逐条针对审查意见，区分新颖性/创造性/A26.3/A26.4）。"
        )

    raise ValueError(f"Unknown scenario: {scenario}")


def _select_model(scenario: str, override: str | None) -> str:
    if override:
        return override
    if scenario == "oa_response":
        return settings.anthropic_oa_model
    return settings.anthropic_default_model


async def stream_draft(
    db: AsyncSession,
    patent_id: uuid.UUID,
    *,
    scenario: str,
    extra_context: str | None = None,
    save_as_draft: bool = True,
    section: str = "claims",
    model_override: str | None = None,
) -> AsyncIterator[dict[str, Any]]:
    """Stream a patent drafting job. Yields SSE-shaped events.

    Event shapes:
      {"event":"job_created","data":{"job_id":"..."}}
      {"event":"delta","data":"<text-chunk>"}
      {"event":"done","data":{"tokens":..., "draft_id":...}}
      {"event":"error","data":{"code":"...","message":"..."}}
    """
    api_key = settings.anthropic_api_key or os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        yield {
            "event": "error",
            "data": {
                "code": "no_api_key",
                "message": "ANTHROPIC_API_KEY 未配置；请在 backend/.env 中设置后重启。",
            },
        }
        return

    patent = await db.get(Patent, patent_id)
    if not patent:
        raise NotFoundError(f"Patent {patent_id} not found")

    # Eagerly load workflow context so the prompt builder doesn't hit lazy-load
    # during streaming (which would surface as a different async error).
    await db.refresh(patent, attribute_names=["grade_links", "scenario_links"])
    disclosure = await patent_workflow_service.get_disclosure(db, patent_id)

    model = _select_model(scenario, model_override)

    job = PatentDraftJob(
        patent_id=patent_id,
        scenario=scenario,
        status="streaming",
        model=model,
        started_at=datetime.now(tz=timezone.utc),
        request_payload={"section": section, "extra_context": extra_context or ""},
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)
    job_id = job.id

    yield {"event": "job_created", "data": {"job_id": str(job_id), "model": model}}

    system = _build_system_prompt()
    user_prompt = _build_user_prompt(
        scenario, patent=patent, disclosure=disclosure, extra_context=extra_context
    )

    accumulated: list[str] = []
    final_usage: dict[str, Any] = {}

    try:
        # Lazy-import so test envs without anthropic still load the module
        import anthropic  # type: ignore

        client = anthropic.AsyncAnthropic(api_key=api_key, timeout=540.0, max_retries=2)
        async with client.messages.stream(
            model=model,
            max_tokens=12000,
            system=system,
            messages=[{"role": "user", "content": user_prompt}],
        ) as stream:
            async for text in stream.text_stream:
                accumulated.append(text)
                yield {"event": "delta", "data": text}
            final_message = await stream.get_final_message()
            usage = getattr(final_message, "usage", None)
            if usage is not None:
                in_tok = getattr(usage, "input_tokens", 0) or 0
                out_tok = getattr(usage, "output_tokens", 0) or 0
                cache_tok = getattr(usage, "cache_read_input_tokens", 0) or 0
                final_usage = {
                    "input_tokens": int(in_tok),
                    "output_tokens": int(out_tok),
                    "cache_read_input_tokens": int(cache_tok),
                }
    except Exception as exc:  # noqa: BLE001
        logger.exception("AI streaming failed for job %s", job_id)
        job.status = "failed"
        job.error = str(exc)[:1000]
        job.completed_at = datetime.now(tz=timezone.utc)
        await db.commit()
        yield {
            "event": "error",
            "data": {"code": "api_error", "message": str(exc)[:500]},
        }
        return

    full_text = "".join(accumulated)
    draft_id: int | None = None
    if save_as_draft and full_text.strip():
        draft = await patent_workflow_service.create_draft(
            db,
            patent_id,
            section=section,
            content=full_text,
            ai_generated=True,
            ai_model=model,
            ai_confidence="medium",
            created_by="ai",
        )
        draft_id = draft.id

    job.status = "done"
    job.input_tokens = final_usage.get("input_tokens")
    job.output_tokens = final_usage.get("output_tokens")
    job.cache_read_tokens = final_usage.get("cache_read_input_tokens")
    job.completed_at = datetime.now(tz=timezone.utc)
    job.result_draft_id = draft_id
    job.result_payload = {"length": len(full_text), "preview": full_text[:200]}
    await db.commit()

    yield {
        "event": "done",
        "data": {
            "job_id": str(job_id),
            "draft_id": draft_id,
            "tokens": final_usage,
            "model": model,
        },
    }
