#!/usr/bin/env python3
"""generate_report.py — Render a Markdown report from a report JSON.

The Markdown layout mirrors templates/investigation-report.md. Both formats
are generated from the same JSON so they never drift. Pure stdlib.

Usage:
    python scripts/generate_report.py --json report.json --out report.md
    python scripts/generate_report.py --json report.json            # stdout

Exit codes: 0 = ok, 2 = usage/IO error.
"""
import argparse
import json
import os
import sys

VERDICT_LABELS = {
    "verified": "已验证",
    "partially_verified": "部分验证",
    "unverified": "未验证",
    "contradicts_evidence": "与证据矛盾",
    "misleading": "误导性表达",
}
CONF_LABELS = {"高": "high", "中": "medium", "低": "low"}


def _conf_cn(conf):
    return {"high": "高", "medium": "中", "low": "低"}.get(conf, conf or "")


def _verdict_cn(v):
    return VERDICT_LABELS.get(v, v or "")


def render(data):
    meta = data.get("meta", {})
    lines = []
    a = lines.append
    a("# AI Reality Check 调查报告")
    a("")
    a("> 生成时间：%s" % meta.get("generated_at", ""))
    a("> 调查模式：%s" % meta.get("mode", ""))
    a("> 内容来源：%s" % meta.get("content_url", ""))
    a("> 内容标题：%s" % meta.get("content_title", ""))
    a("> 平台：%s ｜ 作者：%s" % (meta.get("platform", ""), meta.get("content_author", "")))
    a("> Skill 版本：%s ｜ Schema：%s" % (meta.get("skill_version", ""), meta.get("schema_version", "")))
    a("")
    a("---")
    a("")
    a("## 一句话结论")
    a(data.get("summary", ""))
    a("")
    a("**最终判断：** %s ｜ **置信度：** %s" % (_verdict_cn(data.get("verdict")), _conf_cn(data.get("confidence"))))
    a("")
    a("> verdict 取值：verified（已验证）/ partially_verified（部分验证）/ unverified（未验证）/ contradicts_evidence（与证据矛盾）/ misleading（误导性表达）")
    a("> confidence 取值：high / medium / low（独立于 verdict，禁止无依据百分比）")
    a("")
    a("---")
    a("")
    # 1
    a("## 1. 内容基本信息")
    a("- 平台：%s" % meta.get("platform", ""))
    a("- 作者：%s" % meta.get("content_author", ""))
    a("- 标题：%s" % meta.get("content_title", ""))
    a("- 链接：%s" % meta.get("content_url", ""))
    a("- 实际展示内容（客观描述）：%s" % data.get("content_summary", ""))
    a("")
    # 2
    a("## 2. 视频/内容核心主张")
    a("| 编号 | 主张（中性重述） | 类别 | 可验证 |")
    a("|-----|----------------|------|-------|")
    for c in data.get("core_claims", []):
        a("| %s | %s | %s | %s |" % (c.get("id", ""), c.get("claim", ""), c.get("category", ""), c.get("verifiable", "")))
    a("")
    # 3
    a("## 3. 主张逐项验证")
    for d in data.get("claims_detail", []):
        a("### %s — %s" % (d.get("claim_id", ""), d.get("claim", "")))
        a("- **调查计划**：%s" % d.get("investigation_plan", ""))
        a("- **支持证据**：%s" % "; ".join(d.get("evidence_for", [])) or "（无）")
        a("- **反对证据**：%s" % "; ".join(d.get("evidence_against", [])) or "（无）")
        a("- **技术真实能力**：%s" % d.get("technical_reality", ""))
        a("- **实际应用门槛**：%s" % d.get("practical_barriers", ""))
        a("- **判断**：%s ｜ 置信度：%s" % (_verdict_cn(d.get("verdict")), _conf_cn(d.get("confidence"))))
        a("- **备注**：%s" % d.get("notes", ""))
        a("")
    # 4/5
    a("## 4. 支持证据")
    a(_collect_evidence(data, "for"))
    a("")
    a("## 5. 反对证据")
    a(_collect_evidence(data, "against"))
    a("")
    # 6
    a("## 6. 证据来源")
    a("| ID | 标题 | 发布方 | 类型 | 可靠性 | 独立性说明 | 链接 |")
    a("|----|------|-------|------|-------|-----------|------|")
    for s in data.get("evidence_sources", []):
        a("| %s | %s | %s | %s | %s | %s | %s |" % (
            s.get("id", ""), s.get("title", ""), s.get("publisher", ""),
            s.get("type", ""), s.get("reliability", ""), s.get("independence_note", ""), s.get("url", "")))
    a("")
    # 7-11
    a("## 7. 技术真实能力")
    a(data.get("technical_reality", ""))
    a("")
    a("## 8. 实际应用门槛")
    a(data.get("practical_barriers", ""))
    a("")
    a("## 9. 营销夸大分析")
    a(data.get("marketing_analysis", ""))
    a("")
    a("## 10. 调查局限")
    a(data.get("limitations", ""))
    a("")
    a("## 11. 最终判断")
    a("- **整体结论**：%s" % _verdict_cn(data.get("verdict")))
    a("- **置信度**：%s" % _conf_cn(data.get("confidence")))
    a("- **核心要点**：%s" % data.get("summary", ""))
    a("")
    # 12 personal
    a("## 12. 个人目标分析（仅开启时显示）")
    pi = data.get("personal_impact")
    if pi:
        a("- **用户目标**：%s" % pi.get("user_goal", ""))
        a("- **相关性**：%s" % pi.get("relevance", ""))
        a("- **建议**：%s" % pi.get("recommendation", ""))
        a("- **风险提示**：%s" % pi.get("caveats", ""))
    else:
        a("（未开启个人目标分析。如需结合你的目标分析，请提供目标并开启该模式。）")
    a("")
    a("---")
    a("")
    a("*本报告由 AI Reality Check Skill 生成。所有重要结论均带来源引用；未验证内容明确标注，不伪装为已验证事实。Stay curious. Stay grounded. Keep building.*")
    return "\n".join(lines)


def _collect_evidence(data, direction):
    """Collect evidence strings for a direction ('for'/'against') from claims_detail."""
    out = []
    for d in data.get("claims_detail", []):
        key = "evidence_for" if direction == "for" else "evidence_against"
        items = d.get(key, [])
        if items:
            out.append("**%s**：%s" % (d.get("claim_id", ""), "; ".join(items)))
    return "\n".join(out) if out else "（无）"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Render Markdown from report JSON.")
    parser.add_argument("--json", required=True, help="Path to report JSON.")
    parser.add_argument("--out", help="Output Markdown path (default stdout).")
    args = parser.parse_args(argv)
    try:
        with open(args.json, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print("ERROR: %s" % e, file=sys.stderr)
        return 2
    md = render(data)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(md)
        print("Wrote %s (%d bytes)" % (args.out, len(md)))
    else:
        print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
