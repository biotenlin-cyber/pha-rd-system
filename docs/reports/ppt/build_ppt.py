# -*- coding: utf-8 -*-
"""Generate the EUBP Seedling 2025 deep-dive PPT.

The deck targets a 16:9 widescreen layout and uses WenQuanYi Zen Hei,
which is the only Chinese-capable font available in this environment.
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

CN_FONT = "WenQuanYi Zen Hei"
EN_FONT = "WenQuanYi Zen Hei"

# Color palette — clean / professional green theme matching the Seedling motif
C_PRIMARY = RGBColor(0x1F, 0x6B, 0x4C)     # deep green
C_ACCENT  = RGBColor(0x2E, 0xA0, 0x6B)     # lively green
C_LIGHT   = RGBColor(0xE6, 0xF3, 0xEC)     # soft tint
C_DARK    = RGBColor(0x1F, 0x29, 0x37)     # near-black
C_GREY    = RGBColor(0x55, 0x5F, 0x6D)
C_WARN    = RGBColor(0xC0, 0x39, 0x2B)
C_INFO    = RGBColor(0x1B, 0x5E, 0xA8)
C_BG      = RGBColor(0xFF, 0xFF, 0xFF)


prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height


def _set_run(run, text, *, size=18, bold=False, color=C_DARK, font=CN_FONT):
    run.text = text
    run.font.name = font
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    # Make sure CJK font is also explicitly set
    rPr = run._r.get_or_add_rPr()
    from pptx.oxml.ns import qn
    eastAsia = rPr.find(qn('a:ea'))
    if eastAsia is None:
        from lxml import etree
        eastAsia = etree.SubElement(rPr, qn('a:ea'))
    eastAsia.set('typeface', CN_FONT)


def add_textbox(slide, left, top, width, height, text, *,
                size=18, bold=False, color=C_DARK, align=PP_ALIGN.LEFT,
                anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = Emu(0)
    tf.margin_right = Emu(0)
    tf.margin_top = Emu(0)
    tf.margin_bottom = Emu(0)
    p = tf.paragraphs[0]
    p.alignment = align
    if isinstance(text, list):
        for i, line in enumerate(text):
            if i == 0:
                run = p.add_run()
                _set_run(run, line, size=size, bold=bold, color=color)
            else:
                np = tf.add_paragraph()
                np.alignment = align
                run = np.add_run()
                _set_run(run, line, size=size, bold=bold, color=color)
    else:
        run = p.add_run()
        _set_run(run, text, size=size, bold=bold, color=color)
    return tb


def add_bullets(slide, left, top, width, height, items, *,
                size=14, color=C_DARK, line_spacing=1.25, bullet_color=None):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = Emu(0)
    tf.margin_right = Emu(0)
    tf.margin_top = Emu(0)
    tf.margin_bottom = Emu(0)
    bc = bullet_color or C_ACCENT
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.line_spacing = line_spacing
        # Bullet marker
        r1 = p.add_run()
        _set_run(r1, "▎ ", size=size, bold=True, color=bc)
        # Body
        r2 = p.add_run()
        _set_run(r2, item, size=size, bold=False, color=color)
    return tb


def add_rect(slide, left, top, width, height, fill_color, *,
             line_color=None, shape=MSO_SHAPE.RECTANGLE):
    sh = slide.shapes.add_shape(shape, left, top, width, height)
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill_color
    if line_color is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line_color
    sh.shadow.inherit = False
    sh.text_frame.text = ""
    return sh


def add_card(slide, left, top, width, height, title, body, *,
             title_color=C_PRIMARY, body_color=C_DARK, fill=C_LIGHT,
             title_size=16, body_size=12):
    add_rect(slide, left, top, width, height, fill)
    # Left accent bar
    add_rect(slide, left, top, Inches(0.08), height, C_PRIMARY)
    add_textbox(slide, left + Inches(0.20), top + Inches(0.15),
                width - Inches(0.30), Inches(0.45),
                title, size=title_size, bold=True, color=title_color)
    if isinstance(body, list):
        body_lines = body
    else:
        body_lines = [body]
    add_textbox(slide, left + Inches(0.20), top + Inches(0.65),
                width - Inches(0.30), height - Inches(0.75),
                body_lines, size=body_size, color=body_color)


def add_header(slide, page_no, total, section, title):
    # Top color band
    add_rect(slide, 0, 0, SW, Inches(0.55), C_PRIMARY)
    # Section tag (left)
    add_textbox(slide, Inches(0.5), Inches(0.10), Inches(5.5), Inches(0.35),
                section, size=12, bold=True, color=C_BG)
    # Page no (right)
    add_textbox(slide, SW - Inches(2.0), Inches(0.10), Inches(1.5), Inches(0.35),
                f"{page_no} / {total}",
                size=11, color=C_BG, align=PP_ALIGN.RIGHT)
    # Page title
    add_textbox(slide, Inches(0.5), Inches(0.75), SW - Inches(1.0), Inches(0.7),
                title, size=26, bold=True, color=C_DARK)
    # Underline accent
    add_rect(slide, Inches(0.5), Inches(1.45), Inches(0.6), Inches(0.05), C_ACCENT)


def add_footer(slide, page_no, total):
    add_rect(slide, 0, SH - Inches(0.30), SW, Inches(0.30), C_LIGHT)
    add_textbox(slide, Inches(0.5), SH - Inches(0.28),
                Inches(8), Inches(0.25),
                "EUBP Seedling 2025 工业可堆肥认证方案 · 深度解读",
                size=10, color=C_GREY)
    add_textbox(slide, SW - Inches(2.5), SH - Inches(0.28),
                Inches(2.0), Inches(0.25),
                f"{page_no} / {total}",
                size=10, color=C_GREY, align=PP_ALIGN.RIGHT)


def new_slide(layout_idx=6):
    return prs.slides.add_slide(prs.slide_layouts[layout_idx])  # blank


# Total slide count for footer numbering — set after build
PAGES = []


def page(builder):
    """Decorator-style: collect slide builders, executed in order."""
    PAGES.append(builder)
    return builder


# ==============================================================================
# SLIDE 1 — Cover
# ==============================================================================
@page
def slide_cover(no, total):
    s = new_slide()
    # Background
    add_rect(s, 0, 0, SW, SH, C_BG)
    # Big left color block
    add_rect(s, 0, 0, Inches(4.5), SH, C_PRIMARY)
    # Decorative seedling-ish circle
    add_rect(s, Inches(3.2), Inches(2.6), Inches(2.5), Inches(2.5), C_ACCENT,
             shape=MSO_SHAPE.OVAL)
    add_rect(s, Inches(3.6), Inches(3.0), Inches(1.7), Inches(1.7), C_LIGHT,
             shape=MSO_SHAPE.OVAL)
    # Small tag
    add_textbox(s, Inches(0.6), Inches(0.7), Inches(3.5), Inches(0.4),
                "EUBP · Seedling Certification Scheme",
                size=12, color=C_LIGHT, bold=True)
    add_textbox(s, Inches(0.6), Inches(1.2), Inches(3.5), Inches(0.4),
                "Revision 2025 (October)",
                size=12, color=C_LIGHT)
    # Title (right)
    add_textbox(s, Inches(5.0), Inches(2.0), Inches(8.0), Inches(1.2),
                "工业可堆肥认证方案",
                size=44, bold=True, color=C_DARK)
    add_textbox(s, Inches(5.0), Inches(3.0), Inches(8.0), Inches(0.8),
                "2025年10月版深度解读",
                size=28, bold=True, color=C_PRIMARY)
    # Divider
    add_rect(s, Inches(5.0), Inches(3.95), Inches(1.0), Inches(0.06), C_ACCENT)
    add_textbox(s, Inches(5.0), Inches(4.15), Inches(8.0), Inches(0.4),
                "原文真实性核实 · 阈值体系深解 · 行业影响 · 应对路线图",
                size=15, color=C_GREY)
    add_textbox(s, Inches(5.0), Inches(5.5), Inches(8.0), Inches(0.4),
                "PHA 材料研发与产品开发团队",
                size=14, bold=True, color=C_DARK)
    add_textbox(s, Inches(5.0), Inches(5.95), Inches(8.0), Inches(0.4),
                "2026-05-05  |  内部决策参考",
                size=12, color=C_GREY)


# ==============================================================================
# SLIDE 2 — Agenda
# ==============================================================================
@page
def slide_agenda(no, total):
    s = new_slide()
    add_header(s, no, total, "目录 AGENDA", "本报告将回答的 6 个核心问题")
    items = [
        ("01", "这篇文章是真的吗?",      "原文论点逐条核实"),
        ("02", "Seedling 认证是什么?",   "体系架构与标准底座"),
        ("03", "新版到底改了哪些?",      "六大核心变更"),
        ("04", "1% / 3% / 15% 究竟管什么?", "阈值体系深度解读"),
        ("05", "对我们行业有何影响?",    "PHA / PLA / 纸塑分行业拆解"),
        ("06", "现在该怎么做?",          "0–18 月企业应对路线图"),
    ]
    top = Inches(2.0)
    cw, ch = Inches(6.0), Inches(0.75)
    gap = Inches(0.15)
    for i, (num, q, sub) in enumerate(items):
        col = i % 2
        row = i // 2
        left = Inches(0.6) + col * (cw + Inches(0.5))
        topp = top + row * (ch + gap)
        add_rect(s, left, topp, cw, ch, C_LIGHT)
        # Number badge
        add_rect(s, left, topp, Inches(0.85), ch, C_PRIMARY)
        add_textbox(s, left, topp, Inches(0.85), ch,
                    num, size=22, bold=True, color=C_BG,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        add_textbox(s, left + Inches(1.0), topp + Inches(0.08),
                    cw - Inches(1.1), Inches(0.35),
                    q, size=15, bold=True, color=C_DARK)
        add_textbox(s, left + Inches(1.0), topp + Inches(0.42),
                    cw - Inches(1.1), Inches(0.32),
                    sub, size=11, color=C_GREY)
    add_footer(s, no, total)


# ==============================================================================
# SLIDE 3 — Executive Summary
# ==============================================================================
@page
def slide_exec_summary(no, total):
    s = new_slide()
    add_header(s, no, total, "执行摘要 EXECUTIVE SUMMARY",
               "修订主旋律:全 · 严 · 细 · 透")
    # Four pillars
    titles = ["全面", "严格", "精细", "透明"]
    descs = [
        "1%–15% 区间组分逐项独立测试;0.1% 微量成分纳入生态毒性",
        "<1% 豁免总额从 5% 收紧至 3%(下调 40%)",
        "湿巾 / 无纺布新增专项崩解协议;化学回收单体单列条款",
        "Logo 必须标注 industrially compostable,杜绝家庭堆肥误读",
    ]
    cw, ch = Inches(2.95), Inches(2.6)
    top = Inches(2.0)
    for i in range(4):
        left = Inches(0.6) + i * (cw + Inches(0.15))
        add_rect(s, left, top, cw, ch, C_LIGHT)
        add_rect(s, left, top, cw, Inches(0.55), C_PRIMARY)
        add_textbox(s, left, top, cw, Inches(0.55),
                    titles[i], size=18, bold=True, color=C_BG,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        add_textbox(s, left + Inches(0.20), top + Inches(0.75),
                    cw - Inches(0.40), ch - Inches(0.85),
                    descs[i], size=12, color=C_DARK)
    # Bottom warning bar
    bottom_top = Inches(5.1)
    add_rect(s, Inches(0.6), bottom_top, SW - Inches(1.2), Inches(1.5),
             RGBColor(0xFD, 0xF4, 0xEC))
    add_rect(s, Inches(0.6), bottom_top, Inches(0.08), Inches(1.5), C_WARN)
    add_textbox(s, Inches(0.85), bottom_top + Inches(0.10),
                SW - Inches(1.5), Inches(0.35),
                "⚠ 关键提醒:生效日期实际为「新申请立即生效 + 续证时强制」,",
                size=14, bold=True, color=C_WARN)
    add_textbox(s, Inches(0.85), bottom_top + Inches(0.55),
                SW - Inches(1.5), Inches(0.85),
                ["「2026 年 1 月」是中文媒体对过渡期的概括,并非官方一刀切日期。",
                 "出口企业:配方表必须重新审视,尤其 1%–15% 区间助剂将面临逐项送检压力。"],
                size=12, color=C_DARK)
    add_footer(s, no, total)


# ==============================================================================
# SLIDE 4 — Authenticity verification matrix
# ==============================================================================
@page
def slide_authenticity(no, total):
    s = new_slide()
    add_header(s, no, total, "01 · 文章真实性核实",
               "7 项论点逐条比对官方信源")
    # Table-like rows
    headers = ["#", "论点", "结论", "证据来源"]
    widths = [Inches(0.5), Inches(5.2), Inches(1.6), Inches(5.2)]
    rows = [
        ("1", "新版认证方案存在",            "✅ 属实",  "EUBP 官网正式页面 + PDF 存档"),
        ("2", "发布主体为 EUBP",             "✅ 属实",  "DIN CERTCO / TÜV Austria 联合维护"),
        ("3", "Seedling 标志",               "✅ 属实",  "EUBP 注册商标,沿用至今"),
        ("4", "1%–15% 独立生物降解测试",     "✅ 属实",  "Annex B.2 + 多家认证机构通告"),
        ("5", "碳酸钙等无机物豁免",          "✅ 属实",  "EN 13432 一贯做法,新规未变"),
        ("6", "5%→3% 总额上限收紧",         "⚠ 方向属实", "多渠道间接确认,以官方 PDF 为准"),
        ("7", "2026 年 1 月生效",            "⚠ 简化表述", "官方为「新申请即时 + 续证强制」"),
    ]
    top = Inches(1.85)
    rh = Inches(0.50)
    # Header row
    left = Inches(0.5)
    for i, h in enumerate(headers):
        add_rect(s, left, top, widths[i], Inches(0.45), C_PRIMARY)
        add_textbox(s, left, top, widths[i], Inches(0.45),
                    h, size=13, bold=True, color=C_BG,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        left += widths[i]
    # Body rows
    for ri, row in enumerate(rows):
        rtop = top + Inches(0.45) + ri * rh
        bg = C_LIGHT if ri % 2 == 0 else C_BG
        left = Inches(0.5)
        for ci, val in enumerate(row):
            add_rect(s, left, rtop, widths[ci], rh, bg)
            color = C_DARK
            bold = False
            if ci == 2:
                if "✅" in val:
                    color = C_ACCENT
                    bold = True
                elif "⚠" in val:
                    color = C_WARN
                    bold = True
            align = PP_ALIGN.CENTER if ci in (0, 2) else PP_ALIGN.LEFT
            pad = Inches(0.10) if ci not in (0, 2) else Inches(0)
            add_textbox(s, left + pad, rtop, widths[ci] - pad * 2, rh,
                        val, size=11, bold=bold, color=color,
                        align=align, anchor=MSO_ANCHOR.MIDDLE)
            left += widths[ci]
    # Bottom takeaway
    add_textbox(s, Inches(0.5), Inches(6.55), SW - Inches(1.0), Inches(0.5),
                "▎ 总判断:文章主体真实、方向正确,但生效日期表述简化、信息不全(漏报 5 项同等重要变更)",
                size=13, bold=True, color=C_PRIMARY)
    add_footer(s, no, total)


# ==============================================================================
# SLIDE 5 — Architecture
# ==============================================================================
@page
def slide_architecture(no, total):
    s = new_slide()
    add_header(s, no, total, "02 · Seedling 认证体系基础架构",
               "标准制定者 → 认证机构 → 申请企业的三级链条")
    # Top: EUBP
    cx = SW / 2
    box_w, box_h = Inches(4.5), Inches(0.85)
    add_rect(s, cx - box_w / 2, Inches(2.0), box_w, box_h, C_PRIMARY)
    add_textbox(s, cx - box_w / 2, Inches(2.0), box_w, box_h,
                "European Bioplastics e.V. (EUBP)",
                size=18, bold=True, color=C_BG,
                align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_textbox(s, cx - box_w / 2, Inches(2.92), box_w, Inches(0.3),
                "标准制定 + Seedling 商标持有",
                size=11, color=C_GREY,
                align=PP_ALIGN.CENTER)
    # Connector
    add_rect(s, cx - Inches(0.02), Inches(3.30), Inches(0.04), Inches(0.40), C_GREY)
    # Two certification bodies
    body_w, body_h = Inches(3.6), Inches(0.85)
    add_rect(s, Inches(2.5), Inches(3.75), body_w, body_h, C_ACCENT)
    add_textbox(s, Inches(2.5), Inches(3.75), body_w, body_h,
                "DIN CERTCO (德国)",
                size=15, bold=True, color=C_BG,
                align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_rect(s, Inches(7.2), Inches(3.75), body_w, body_h, C_ACCENT)
    add_textbox(s, Inches(7.2), Inches(3.75), body_w, body_h,
                "TÜV AUSTRIA Belgium",
                size=15, bold=True, color=C_BG,
                align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_textbox(s, Inches(2.5), Inches(4.65), Inches(8.3), Inches(0.3),
                "↑ 两家执行机构,企业可任选其一",
                size=11, color=C_GREY,
                align=PP_ALIGN.CENTER)
    # Bottom: applicants
    add_rect(s, Inches(1.5), Inches(5.30), Inches(10.3), Inches(0.85), C_LIGHT)
    add_textbox(s, Inches(1.5), Inches(5.30), Inches(10.3), Inches(0.85),
                "申请企业:材料商  |  中间品商  |  终端产品商",
                size=15, bold=True, color=C_DARK,
                align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    # Standard pillars at top
    add_textbox(s, Inches(0.5), Inches(1.6), SW - Inches(1.0), Inches(0.35),
                "底层标准:EN 13432 · EN 14995 · ISO 17088 · ISO 18606 · ASTM D6400",
                size=12, color=C_INFO, bold=True, align=PP_ALIGN.CENTER)
    add_footer(s, no, total)


# ==============================================================================
# SLIDE 6 — Four-gate certification flow
# ==============================================================================
@page
def slide_four_gates(no, total):
    s = new_slide()
    add_header(s, no, total, "02 · Seedling 通过的「四关」",
               "EN 13432 框架下的硬性考核流程")
    gates = [
        ("①", "化学特性",       "Chemical Characterisation",
         ["重金属 12 项限值", "氟含量 ≤ 100 mg/kg(防 PFAS)", "挥发性固体 ≥ 50%"]),
        ("②", "生物降解性",     "Biodegradability",
         ["6 个月内 ≥ 90% 矿化为 CO₂", "依据 ISO 14855", "水浴 / 静态条件"]),
        ("③", "崩解性",         "Disintegration",
         ["12 周内 ≥ 90% 通过 2mm 筛", "工业堆肥模拟", "按产品形态分组"]),
        ("④", "生态毒性",       "Ecotoxicity",
         ["OECD 208 植物生长试验", "发芽率/生物量 ≥ 空白 90%", "新规扩至 0.1% 成分"]),
    ]
    cw, ch = Inches(3.0), Inches(4.4)
    top = Inches(1.85)
    for i, (num, title_cn, title_en, bullets) in enumerate(gates):
        left = Inches(0.45) + i * (cw + Inches(0.15))
        add_rect(s, left, top, cw, ch, C_LIGHT)
        # Number circle
        add_rect(s, left + cw / 2 - Inches(0.45), top + Inches(0.20),
                 Inches(0.9), Inches(0.9), C_PRIMARY,
                 shape=MSO_SHAPE.OVAL)
        add_textbox(s, left + cw / 2 - Inches(0.45), top + Inches(0.20),
                    Inches(0.9), Inches(0.9),
                    num, size=24, bold=True, color=C_BG,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # Titles
        add_textbox(s, left, top + Inches(1.25), cw, Inches(0.4),
                    title_cn, size=18, bold=True, color=C_PRIMARY,
                    align=PP_ALIGN.CENTER)
        add_textbox(s, left, top + Inches(1.65), cw, Inches(0.3),
                    title_en, size=10, color=C_GREY,
                    align=PP_ALIGN.CENTER)
        # Divider
        add_rect(s, left + Inches(0.6), top + Inches(2.05),
                 cw - Inches(1.2), Inches(0.03), C_ACCENT)
        # Bullets
        add_bullets(s, left + Inches(0.25), top + Inches(2.25),
                    cw - Inches(0.5), Inches(2.0),
                    bullets, size=11, color=C_DARK, line_spacing=1.3)
    # Footer note
    add_textbox(s, Inches(0.5), Inches(6.50), SW - Inches(1.0), Inches(0.5),
                "▎ 任一关失败 → 不予颁发 Seedling 标志",
                size=13, bold=True, color=C_WARN)
    add_footer(s, no, total)


# ==============================================================================
# SLIDE 7 — Six core changes
# ==============================================================================
@page
def slide_six_changes(no, total):
    s = new_slide()
    add_header(s, no, total, "03 · 2025 年 10 月版六大核心变更",
               "由「防漏洞」到「全透明」的全方位升级")
    changes = [
        ("01", "1%–15% 独立测试", "每种有机组分必须独立送检\n堵住「打包送检」漏洞", C_PRIMARY),
        ("02", "5% → 3% 信封",    "<1% 豁免总额收紧 40%\n微量助剂空间压缩",   C_ACCENT),
        ("03", "0.1% 生态毒性",  "微量成分纳入生态毒性\n对应 PFAS 严控趋势",   C_INFO),
        ("04", "Logo 改字",       "明确加入 industrially\ncompostable 字样",  C_PRIMARY),
        ("05", "湿巾 / 无纺布",   "新增专项崩解协议\n应对欧盟一次性立法",     C_ACCENT),
        ("06", "化学回收单体",   "已认证 PLA 可使用化学回收\n单体,无需重新认证", C_INFO),
    ]
    cw, ch = Inches(4.10), Inches(2.30)
    top = Inches(1.95)
    for i, (num, title, body, color) in enumerate(changes):
        col = i % 3
        row = i // 3
        left = Inches(0.45) + col * (cw + Inches(0.20))
        topp = top + row * (ch + Inches(0.20))
        add_rect(s, left, topp, cw, ch, C_LIGHT)
        # Big number on left
        add_rect(s, left, topp, Inches(0.95), ch, color)
        add_textbox(s, left, topp, Inches(0.95), ch,
                    num, size=32, bold=True, color=C_BG,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        add_textbox(s, left + Inches(1.10), topp + Inches(0.20),
                    cw - Inches(1.20), Inches(0.5),
                    title, size=16, bold=True, color=C_DARK)
        add_textbox(s, left + Inches(1.10), topp + Inches(0.85),
                    cw - Inches(1.20), Inches(1.30),
                    body.split("\n"), size=11, color=C_GREY)
    add_footer(s, no, total)


# ==============================================================================
# SLIDE 8 — Threshold logic (THE key slide)
# ==============================================================================
@page
def slide_threshold_logic(no, total):
    s = new_slide()
    add_header(s, no, total, "04 · 阈值体系 · 必读核心",
               "1% / 3% / 15% 究竟管什么?")
    # Title bar
    add_rect(s, Inches(0.5), Inches(1.85), SW - Inches(1.0), Inches(0.5), C_PRIMARY)
    add_textbox(s, Inches(0.5), Inches(1.85), SW - Inches(1.0), Inches(0.5),
                "产品中所有「有机成分」按单一组分质量分数划分(无机填料、水分不计入)",
                size=14, bold=True, color=C_BG,
                align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    # Three buckets
    bucket_w, bucket_h = Inches(4.0), Inches(3.7)
    bucket_top = Inches(2.55)
    buckets = [
        ("< 1%", "单项可豁免",
         ["每种有机成分 < 1%",
          "可不送独立生物降解测试",
          "—— 但是 ——",
          "所有此类成分总和 ≤ 3%(新规)",
          "(旧规 ≤ 5%,本次收紧 40%)"],
         C_INFO),
        ("1% — 15%", "必须独立送检",
         ["每种有机成分独立送检",
          "出具独立 ISO 14855 证书",
          "不允许「打包送检」",
          "≥ 90% 矿化为 CO₂(180天)",
          "本轮修订最关键的新增条款"],
         C_PRIMARY),
        ("≥ 15%", "绝对必测",
         ["所有主组分必测",
          "出具独立生物降解证书",
          "+ 完整生态毒性试验",
          "+ 重金属 / 氟含量限值",
          "(本来就如此,新规未变)"],
         C_ACCENT),
    ]
    for i, (band, tag, items, color) in enumerate(buckets):
        left = Inches(0.5) + i * (bucket_w + Inches(0.20))
        add_rect(s, left, bucket_top, bucket_w, bucket_h, C_LIGHT)
        # Top color stripe
        add_rect(s, left, bucket_top, bucket_w, Inches(0.85), color)
        add_textbox(s, left, bucket_top + Inches(0.05),
                    bucket_w, Inches(0.45),
                    band, size=24, bold=True, color=C_BG,
                    align=PP_ALIGN.CENTER)
        add_textbox(s, left, bucket_top + Inches(0.50),
                    bucket_w, Inches(0.32),
                    tag, size=13, color=C_BG,
                    align=PP_ALIGN.CENTER)
        # Items
        add_bullets(s, left + Inches(0.25), bucket_top + Inches(1.05),
                    bucket_w - Inches(0.50), bucket_h - Inches(1.15),
                    items, size=11, color=C_DARK, line_spacing=1.4,
                    bullet_color=color)
    # Bottom note
    add_textbox(s, Inches(0.5), Inches(6.55), SW - Inches(1.0), Inches(0.5),
                "▎ 提醒:无机物(碳酸钙、滑石、TiO₂)不进入此分母,但仍受「挥发性固体 ≥ 50%」约束",
                size=12, bold=True, color=C_WARN)
    add_footer(s, no, total)


# ==============================================================================
# SLIDE 9 — Common misconceptions
# ==============================================================================
@page
def slide_misconceptions(no, total):
    s = new_slide()
    add_header(s, no, total, "04 · 五大常见误解澄清",
               "用错误理解 vs 正确解读对照表")
    rows = [
        ("PE 涂层 < 3% 就可以拿 Seedling",
         "PE 是石化非降解物,即使 0.5% 也违反「非降解残留」限制。3% 信封只给可豁免单测的助剂",),
        ("几个成分各 0.9%,就可以无限叠加",
         "单项可豁免,但总和必须 ≤ 3%。4 种 × 0.9% = 3.6% 已超标",),
        ("≥ 15% 就不用测了",
         "完全相反。≥ 15% 是绝对主成分,永远必须通过独立测试(本来就如此)",),
        ("1%–15% 区间是新发明的概念",
         "≥ 1% 必测原则一直存在,本次新增的是「逐项独立」要求,堵混合送检漏洞",),
        ("碳酸钙不限量,加多少都行",
         "CaCO₃ 不参与有机成分阈值计算,但仍受「VS ≥ 50%」总要求约束",),
    ]
    top = Inches(1.85)
    rh = Inches(0.95)
    for i, (wrong, right) in enumerate(rows):
        rtop = top + i * (rh + Inches(0.05))
        # Wrong cell
        add_rect(s, Inches(0.5), rtop, Inches(5.8), rh, RGBColor(0xFC, 0xEE, 0xEC))
        add_rect(s, Inches(0.5), rtop, Inches(0.08), rh, C_WARN)
        add_textbox(s, Inches(0.7), rtop + Inches(0.10),
                    Inches(0.4), Inches(0.35),
                    "✗", size=22, bold=True, color=C_WARN)
        add_textbox(s, Inches(1.05), rtop + Inches(0.18),
                    Inches(5.2), rh - Inches(0.25),
                    wrong, size=12, color=C_DARK,
                    anchor=MSO_ANCHOR.MIDDLE)
        # Arrow
        add_textbox(s, Inches(6.35), rtop + Inches(0.20),
                    Inches(0.4), Inches(0.5),
                    "→", size=20, bold=True, color=C_GREY,
                    align=PP_ALIGN.CENTER)
        # Right cell
        add_rect(s, Inches(6.85), rtop, Inches(6.0), rh,
                 RGBColor(0xEC, 0xF6, 0xEF))
        add_rect(s, Inches(6.85), rtop, Inches(0.08), rh, C_ACCENT)
        add_textbox(s, Inches(7.05), rtop + Inches(0.10),
                    Inches(0.4), Inches(0.35),
                    "✓", size=22, bold=True, color=C_ACCENT)
        add_textbox(s, Inches(7.40), rtop + Inches(0.10),
                    Inches(5.4), rh - Inches(0.15),
                    right, size=11, color=C_DARK,
                    anchor=MSO_ANCHOR.MIDDLE)
    add_footer(s, no, total)


# ==============================================================================
# SLIDE 10 — Paper cup case study (the user's question)
# ==============================================================================
@page
def slide_paper_cup(no, total):
    s = new_slide()
    add_header(s, no, total, "05 · 典型案例 · 纸杯 / 纸碗",
               "能否拿 Seedling 取决于涂层化学性质,不取决于 3% 阈值")
    # Top message
    add_rect(s, Inches(0.5), Inches(1.85), SW - Inches(1.0), Inches(0.6),
             RGBColor(0xFD, 0xF4, 0xEC))
    add_rect(s, Inches(0.5), Inches(1.85), Inches(0.08), Inches(0.6), C_WARN)
    add_textbox(s, Inches(0.75), Inches(1.85), SW - Inches(1.5), Inches(0.6),
                "结论:涂层能不能拿 Seedling 看「材料是否可降解」,与 3% 信封无关",
                size=14, bold=True, color=C_WARN, anchor=MSO_ANCHOR.MIDDLE)
    # Table
    headers = ["涂层类型", "占比典型值", "是否能拿 Seedling", "受 3% 阈值影响"]
    rows = [
        ("PE 聚乙烯涂层",        "5% – 15%",  "❌ 完全不可能",      "与 3% 无关 · PE 不可降解"),
        ("EAA / EMAA 增粘层",   "0.5% – 2%", "❌ 完全不可能",      "即便 < 1% 也属非降解残留"),
        ("PLA 涂层",             "5% – 18%",  "✅ 可,需 PLA 已认证", "≥ 15% 时绝对必测"),
        ("PBS / PBAT 涂层",      "5% – 15%",  "✅ 可",              "1%–15% 区间需独立报告"),
        ("PHA 水性涂层(新兴)", "1% – 10%",  "✅ 可",              "1%–15% 区间需独立报告"),
        ("水基生物聚合物涂层",   "1% – 8%",   "✅ 可",              "同上"),
    ]
    widths = [Inches(3.0), Inches(2.0), Inches(3.5), Inches(3.8)]
    top = Inches(2.65)
    rh = Inches(0.50)
    left0 = Inches(0.5)
    # Header
    left = left0
    for i, h in enumerate(headers):
        add_rect(s, left, top, widths[i], Inches(0.45), C_PRIMARY)
        add_textbox(s, left, top, widths[i], Inches(0.45),
                    h, size=12, bold=True, color=C_BG,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        left += widths[i]
    # Body
    for ri, row in enumerate(rows):
        rtop = top + Inches(0.45) + ri * rh
        bg = C_LIGHT if ri % 2 == 0 else C_BG
        left = left0
        for ci, val in enumerate(row):
            add_rect(s, left, rtop, widths[ci], rh, bg)
            color = C_DARK
            bold = False
            if "❌" in val:
                color = C_WARN
                bold = True
            elif "✅" in val:
                color = C_ACCENT
                bold = True
            align = PP_ALIGN.LEFT if ci == 0 else PP_ALIGN.CENTER
            pad = Inches(0.15) if ci == 0 else Inches(0)
            add_textbox(s, left + pad, rtop, widths[ci] - pad * 2, rh,
                        val, size=11, bold=bold, color=color,
                        align=align, anchor=MSO_ANCHOR.MIDDLE)
            left += widths[ci]
    # Bottom takeaway
    add_textbox(s, Inches(0.5), Inches(6.40), SW - Inches(1.0), Inches(0.5),
                "▎ 关键判断 · 先确认涂层是可降解材料,再考虑助剂层面的 3% 阈值",
                size=13, bold=True, color=C_PRIMARY)
    add_footer(s, no, total)


# ==============================================================================
# SLIDE 11 — Industry impact
# ==============================================================================
@page
def slide_industry_impact(no, total):
    s = new_slide()
    add_header(s, no, total, "05 · 分行业影响评估",
               "PHA / PLA / 纸塑 / 助剂 / 中国出口五维拆解")
    rows = [
        ("PHA 行业(本系统主体)", "✅ 总体利好", C_ACCENT,
         "本身可全场景降解 · 共混伙伴需独立认证 · 助剂总和注意 ≤ 3%"),
        ("PLA / PBAT 共混料商",   "⚠ 测试压力大", C_WARN,
         "1%–15% 改性组分必须独立送检 · 单项 ISO 14855 ≈ €15K–25K · 6 个月周期"),
        ("纸塑复合(纸杯/纸碗)", "✅ 取决于涂层", C_ACCENT,
         "PE/EAA 直接出局 · 选用 PLA/PBS/PHA 涂层即可 · 关注油墨/施胶剂的 3% 信封"),
        ("色母粒 / 助剂供应商",  "⚠ 高风险区", C_WARN,
         "载体树脂往往 1%–3% 正踩双重门槛 · 含 F/Br/Cd 助剂直接淘汰"),
        ("中国出口企业",          "⚠ 合规雷区", C_WARN,
         "GB/T 19277 数据不能直接跨用 · 需在 EUBP 认可实验室重新送检 · 防止四类雷区"),
    ]
    top = Inches(1.95)
    rh = Inches(0.95)
    for i, (industry, verdict, vcolor, detail) in enumerate(rows):
        rtop = top + i * (rh + Inches(0.05))
        add_rect(s, Inches(0.5), rtop, SW - Inches(1.0), rh, C_LIGHT)
        # Industry name
        add_rect(s, Inches(0.5), rtop, Inches(3.5), rh, C_PRIMARY)
        add_textbox(s, Inches(0.65), rtop, Inches(3.3), rh,
                    industry, size=14, bold=True, color=C_BG,
                    anchor=MSO_ANCHOR.MIDDLE)
        # Verdict
        add_textbox(s, Inches(4.1), rtop + Inches(0.10),
                    Inches(2.3), Inches(0.40),
                    verdict, size=14, bold=True, color=vcolor,
                    anchor=MSO_ANCHOR.MIDDLE)
        # Detail
        add_textbox(s, Inches(4.1), rtop + Inches(0.45),
                    SW - Inches(4.7), Inches(0.45),
                    detail, size=11, color=C_DARK,
                    anchor=MSO_ANCHOR.MIDDLE)
    add_footer(s, no, total)


# ==============================================================================
# SLIDE 12 — Roadmap
# ==============================================================================
@page
def slide_roadmap(no, total):
    s = new_slide()
    add_header(s, no, total, "06 · 企业应对路线图",
               "0 – 18 个月分阶段行动清单")
    phases = [
        ("0 – 6 个月", "短期 · 盘点与准备", C_INFO,
         ["配方表全面盘点,标注各成分质量分数",
          "校核 < 1% 有机成分总和是否 ≤ 3%",
          "联系 DIN CERTCO / TÜV 确认过渡安排",
          "向供应商索取助剂的子认证证书"]),
        ("6 – 18 个月", "中期 · 测试与切换", C_ACCENT,
         ["1%–15% 组分启动 ISO 14855 独立送检",
          "<0.1% 微量成分补充 OECD 208 等生态毒性测试",
          "包装 Logo 同步增加 industrially compostable",
          "在 PLM/ERP 中建立合规 BOM 字段"]),
        ("18 个月以上", "长期 · 战略布局", C_PRIMARY,
         ["跟踪 EN 13432 新版征求意见(2026–2027)",
          "布局 PHA / 化学回收闭环路径",
          "拓展 OK Compost HOME / Soil / Marine 多认证矩阵",
          "建立合规日历 · 提前 6 月启动续证"]),
    ]
    cw, ch = Inches(4.10), Inches(4.5)
    top = Inches(1.85)
    for i, (period, title, color, items) in enumerate(phases):
        left = Inches(0.45) + i * (cw + Inches(0.20))
        add_rect(s, left, top, cw, ch, C_LIGHT)
        # Top color band with period
        add_rect(s, left, top, cw, Inches(0.75), color)
        add_textbox(s, left, top + Inches(0.05),
                    cw, Inches(0.35),
                    period, size=16, bold=True, color=C_BG,
                    align=PP_ALIGN.CENTER)
        add_textbox(s, left, top + Inches(0.40),
                    cw, Inches(0.32),
                    title, size=12, color=C_BG,
                    align=PP_ALIGN.CENTER)
        # Items
        add_bullets(s, left + Inches(0.25), top + Inches(0.95),
                    cw - Inches(0.50), ch - Inches(1.05),
                    items, size=12, color=C_DARK, line_spacing=1.5,
                    bullet_color=color)
    add_footer(s, no, total)


# ==============================================================================
# SLIDE 13 — Risk & uncertainty
# ==============================================================================
@page
def slide_risks(no, total):
    s = new_slide()
    add_header(s, no, total, "风险提示 RISK NOTICE",
               "重大决策前需企业自行二次核实的不确定项")
    risks = [
        ("01", "5% → 3% 具体数字",
         "来自二次行业解读,作者团队尚未直读 EUBP PDF 中相应条款的精确段落",
         "建议:由企业法务/合规部门直接索取 EUBP 原始文件确认"),
        ("02", "生效日期非一刀切",
         "各认证机构(DIN CERTCO / TÜV)可能分别公告不同的过渡安排",
         "建议:跨认证机构客户分别确认续证窗口"),
        ("03", "PFAS 限值收紧趋势",
         "EN 13432 总氟 100 mg/kg,但 REACH 对 PFAS 更严限值正在制定",
         "建议:Seedling 后续可能进一步收紧,提前布局无氟配方"),
        ("04", "海外互认不确定",
         "美国 BPI、澳洲 ABA 是否同步收紧尚未明确",
         "建议:多国出口需分别评估,不可只盯欧盟"),
    ]
    top = Inches(1.85)
    rh = Inches(1.10)
    for i, (num, title, body, advice) in enumerate(risks):
        rtop = top + i * (rh + Inches(0.05))
        add_rect(s, Inches(0.5), rtop, SW - Inches(1.0), rh,
                 RGBColor(0xFD, 0xF4, 0xEC))
        # Number
        add_rect(s, Inches(0.5), rtop, Inches(1.0), rh, C_WARN)
        add_textbox(s, Inches(0.5), rtop, Inches(1.0), rh,
                    num, size=22, bold=True, color=C_BG,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # Title
        add_textbox(s, Inches(1.65), rtop + Inches(0.08),
                    Inches(4.0), Inches(0.35),
                    title, size=14, bold=True, color=C_DARK)
        # Body
        add_textbox(s, Inches(1.65), rtop + Inches(0.45),
                    Inches(4.0), Inches(0.6),
                    body, size=10, color=C_GREY)
        # Advice
        add_textbox(s, Inches(5.85), rtop + Inches(0.10),
                    SW - Inches(6.4), Inches(0.40),
                    "建议", size=12, bold=True, color=C_PRIMARY)
        add_textbox(s, Inches(5.85), rtop + Inches(0.45),
                    SW - Inches(6.4), rh - Inches(0.55),
                    advice, size=11, color=C_DARK)
    add_footer(s, no, total)


# ==============================================================================
# SLIDE 14 — Sources
# ==============================================================================
@page
def slide_sources(no, total):
    s = new_slide()
    add_header(s, no, total, "信息源 SOURCES",
               "三级信源结构 · 一级官方为最终依据")
    sections = [
        ("一级 · EUBP / 认证机构官方", C_PRIMARY, [
            "EUBP 官方公告页:european-bioplastics.org/seedling-certification-scheme-october2025",
            "官方 PDF 全文:Seedling_FINAL_CertificationScheme_Revision_2025.pdf",
            "EUBP 标准与标识事实表 (2025)",
            "DIN CERTCO 公告页:dincertco.de/din-certco/en/news/certification-scheme.html",
        ]),
        ("二级 · 法规联动", C_ACCENT, [
            "PPWR (Regulation EU 2025/40) 全文 — 欧盟环境总司",
            "EEA 可堆肥塑料标准对照页",
            "Green Claims Directive(欧盟绿色声明指令)",
        ]),
        ("三级 · 历史版本与第三方解读(交叉验证)", C_INFO, [
            "Seedling Certification Scheme 2023 / 2020 历史版本(对比研究)",
            "Power Adhesives:Understanding the 1% rule under PPWR (2025-10)",
            "Vincotte:Requirements of the EN 13432 standard",
            "Measurlabs:Biodegradability and Compostability Testing Standards",
        ]),
    ]
    top = Inches(1.85)
    block_h = Inches(1.65)
    for i, (title, color, items) in enumerate(sections):
        ttop = top + i * (block_h + Inches(0.10))
        add_rect(s, Inches(0.5), ttop, SW - Inches(1.0), Inches(0.45), color)
        add_textbox(s, Inches(0.7), ttop, SW - Inches(1.4), Inches(0.45),
                    title, size=14, bold=True, color=C_BG,
                    anchor=MSO_ANCHOR.MIDDLE)
        add_bullets(s, Inches(0.6), ttop + Inches(0.55),
                    SW - Inches(1.2), block_h - Inches(0.55),
                    items, size=11, color=C_DARK, line_spacing=1.3,
                    bullet_color=color)
    add_footer(s, no, total)


# ==============================================================================
# SLIDE 15 — Closing
# ==============================================================================
@page
def slide_closing(no, total):
    s = new_slide()
    # Background
    add_rect(s, 0, 0, SW, SH, C_PRIMARY)
    # Side accent
    add_rect(s, 0, 0, Inches(0.4), SH, C_ACCENT)
    # Big "Thanks"
    add_textbox(s, Inches(0.8), Inches(2.3), SW - Inches(1.6), Inches(1.2),
                "THANK YOU",
                size=72, bold=True, color=C_BG)
    add_rect(s, Inches(0.8), Inches(3.55), Inches(1.5), Inches(0.06), C_ACCENT)
    add_textbox(s, Inches(0.8), Inches(3.75), SW - Inches(1.6), Inches(0.6),
                "EUBP Seedling 2025 · 工业可堆肥认证方案深度解读",
                size=20, bold=True, color=C_LIGHT)
    add_textbox(s, Inches(0.8), Inches(4.5), SW - Inches(1.6), Inches(0.5),
                "如需:① 配方合规自检 ② 测试机构推荐 ③ 续证日历定制",
                size=14, color=C_LIGHT)
    add_textbox(s, Inches(0.8), Inches(5.0), SW - Inches(1.6), Inches(0.5),
                "请联系 PHA 研发中心合规组",
                size=14, color=C_LIGHT)
    # Footer
    add_textbox(s, Inches(0.8), SH - Inches(0.6), SW - Inches(1.6), Inches(0.4),
                "© 2026 PHA-RD-System · 内部决策参考",
                size=10, color=C_LIGHT)


# Build deck
total = len(PAGES)
for i, builder in enumerate(PAGES, start=1):
    builder(i, total)


out = "/home/user/pha-rd-system/docs/reports/ppt/EUBP_Seedling_2025_深度解读.pptx"
prs.save(out)
print("Saved:", out, "| slides:", total)
