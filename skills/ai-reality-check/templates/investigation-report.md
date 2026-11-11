# AI Reality Check 调查报告

> 生成时间：{{meta.generated_at}}
> 调查模式：{{meta.mode}}（Quick / Deep）
> 内容来源：{{meta.content_url}}
> 内容标题：{{meta.content_title}}
> 平台：{{meta.platform}} ｜ 作者：{{meta.content_author}}
> Skill 版本：{{meta.skill_version}} ｜ Schema：{{meta.schema_version}}

---

## 一句话结论
{{summary}}

**最终判断：** {{verdict}} ｜ **置信度：** {{confidence}}

> verdict 取值：verified（已验证）/ partially_verified（部分验证）/ unverified（未验证）/ contradicts_evidence（与证据矛盾）/ misleading（误导性表达）
> confidence 取值：high / medium / low（独立于 verdict，禁止无依据百分比）

---

## 1. 内容基本信息
- 平台：{{meta.platform}}
- 作者：{{meta.content_author}}
- 标题：{{meta.content_title}}
- 链接：{{meta.content_url}}
- 实际展示内容（客观描述）：{{content_summary}}

---

## 2. 视频/内容核心主张
| 编号 | 主张（中性重述） | 类别 | 可验证 |
|-----|----------------|------|-------|
| {{claim.id}} | {{claim.claim}} | {{claim.category}} | {{claim.verifiable}} |

---

## 3. 主张逐项验证
{% for d in claims_detail %}
### {{d.claim_id}} — {{d.claim}}
- **调查计划**：{{d.investigation_plan}}
- **支持证据**：{{d.evidence_for}}
- **反对证据**：{{d.evidence_against}}
- **技术真实能力**：{{d.technical_reality}}
- **实际应用门槛**：{{d.practical_barriers}}
- **判断**：{{d.verdict}} ｜ 置信度：{{d.confidence}}
- **备注**：{{d.notes}}
{% endfor %}

---

## 4. 支持证据
{{evidence_for_summary}}

## 5. 反对证据
{{evidence_against_summary}}

---

## 6. 证据来源
| ID | 标题 | 发布方 | 类型 | 可靠性 | 独立性说明 | 链接 |
|----|------|-------|------|-------|-----------|------|
| {{s.id}} | {{s.title}} | {{s.publisher}} | {{s.type}} | {{s.reliability}} | {{s.independence_note}} | {{s.url}} |

---

## 7. 技术真实能力
{{technical_reality}}

## 8. 实际应用门槛
{{practical_barriers}}

## 9. 营销夸大分析
{{marketing_analysis}}

## 10. 调查局限
{{limitations}}

## 11. 最终判断
- **整体结论**：{{verdict}}
- **置信度**：{{confidence}}
- **核心要点**：{{summary}}

---

## 12. 个人目标分析（仅开启时显示）
{% if personal_impact %}
- **用户目标**：{{personal_impact.user_goal}}
- **相关性**：{{personal_impact.relevance}}
- **建议**：{{personal_impact.recommendation}}
- **风险提示**：{{personal_impact.caveats}}
{% else %}
（未开启个人目标分析。如需结合你的目标分析，请提供目标并开启该模式。）
{% endif %}

---

*本报告由 AI Reality Check Skill 生成。所有重要结论均带来源引用；未验证内容明确标注，不伪装为已验证事实。Stay curious. Stay grounded. Keep building.*
