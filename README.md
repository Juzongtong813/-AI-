<p align="center">
  <h1 align="center">AI Reality Check</h1>
  <p align="center"><b>Don't chase every AI breakthrough. Verify it.</b></p>
  <p align="center">Stay curious. Stay grounded. Keep building.</p>
</p>

---

## 你只需要在聊天里发一个视频链接，就能启动一次现实调查。

在抖音、B站、YouTube、TikTok、小红书、X 看到一条让你焦虑或兴奋的 AI 视频？把它（或文字内容）发给正在使用的 Agent，它会自动：

1. 提取视频**实际展示了什么**（不限于标题）
2. 拆解成可验证的具体主张
3. 搜索**支持与反对**的独立证据
4. 评估技术真实能力与成熟档位（Demo / 可用工具 / 成熟产品）
5. 识别营销夸大与误导
6. 输出一份**带证据出处**的调查报告

> 我们不反对 AI 进步，只帮你区分"真实进步"与"社交媒体制造的焦虑（AI FOMO）"。

---

## 一、项目使命

帮助普通人识别社交媒体中关于 AI、技术革命、赚钱、创业、就业、游戏开发、视频创作等内容的真实性，减少被营销夸大和选择性展示裹挟的焦虑。

## 二、项目介绍

AI Reality Check 是一个 **Skill 优先** 的开源项目——它不是一个独立 App，而是一个可以装进你正在使用的 Agent 的"调查规范包"。它复用宿主 Agent 已有的搜索、浏览、视频解析、代码执行与推理能力，自身只提供：

- 调查规范与主张拆解方法
- 证据标准与来源可靠性判定
- Quick Check / Deep Investigation / Personal Impact 工作流
- 统一调查报告（Markdown + JSON，稳定 Schema）
- 辅助脚本（安装器、Schema 校验、报告生成、来源去重）

**V1 不依赖** 任何自建 MCP Server / REST API / 数据库 / 独立 Agent 服务。

## 三、使用场景

| 你看到的 | 你该问的 |
|---------|---------|
| "AI 一键生成完整游戏" | 真的是'完整'吗？要多少人工？ |
| "一个人用 AI 一天赚十万" | 有可靠收入证据吗？能复制吗？ |
| "新模型让程序员失业" | 对真实岗位的影响是什么？ |
| "某工具替代整个视频团队" | 隐藏了哪些前提和成本？ |
| "不懂编程也能批量开发软件" | 门槛到底在哪里？ |

## 四、效果展示

一份典型报告包含：

- **一句话结论** + **最终判断**（已验证 / 部分验证 / 未验证 / 与证据矛盾 / 误导性表达）+ **置信度**（高 / 中 / 低）
- 核心主张逐项验证（计划 → 支持证据 → 反对证据 → 技术现实 → 门槛 → 判断）
- 证据来源表（类型 / 可靠性 / 独立性说明）
- 营销夸大分析（逐条指出夸大点）
- 调查局限（明确"没查到 / 没覆盖"的部分）

示例（节选）：

> **一句话结论**：该视频展示了一个需大量人工干预的 30 秒占位 Demo，并非"完整游戏"；"零基础赚钱"缺乏可靠收入证据。整体存在明显标题夸大。
> **最终判断**：misleading ｜ **置信度**：medium

完整示例见 [`examples/example-investigation.md`](examples/example-investigation.md)。

## 五、一键安装

仓库自带**真实可用的安装器**（纯 Python 标准库，无第三方依赖）：

```bash
# 1. 克隆仓库
git clone https://github.com/Juzongtong813/ai-reality-check.git
cd ai-reality-check

# 2. 安装到当前 Agent（自动识别 WorkBuddy / Claude / Cursor / Codex）
python scripts/install.py install

# 3. 验证安装
python scripts/install.py check

# 4. 更新 / 卸载
python scripts/install.py update
python scripts/install.py uninstall
```

安装器会把 `skills/ai-reality-check/` 复制到对应 Agent 的 skills 目录，并校验 `SKILL.md` 的 frontmatter。

## 六、不同 Agent 的安装方法

| Agent | 技能目录 | 安装命令 |
|------|---------|---------|
| **WorkBuddy** | `~/.workbuddy/skills/` | `python scripts/install.py install --agent workbuddy` |
| **Claude Code / Desktop** | `~/.claude/skills/` | `python scripts/install.py install --agent claude` |
| **Cursor** | `~/.cursor/skills/` | `python scripts/install.py install --agent cursor` |
| **Codex / 其他** | `~/.codex/skills/` | `python scripts/install.py install --agent codex` |
| **未知 Agent** | 任意路径 | `python scripts/install.py install --target /abs/path/to/skills` |

> 所有路径均支持 Windows / macOS / Linux，安装器自动展开 `~`。
> 若 `--agent` 无法识别你的 Agent，请使用 `--target` 指定其 skills 目录，或手动复制 `skills/ai-reality-check/` 到该目录。

**手动安装（兜底）：**
1. 复制 `skills/ai-reality-check/` 整个目录到你的 Agent skills 目录。
2. 确认目标目录下存在 `SKILL.md` 且含 `name` / `description` / `agent_created: true`。
3. 重启或刷新 Agent 使其加载新 Skill。

## 七、使用示例

**Quick Check（日常视频）：**
```
用户：帮我看看这个视频 https://youtu.be/xxxx 是不是真的能一键做游戏
Agent：（调用 AI Reality Check）→ 输出调查报告
```

**Deep Investigation（重要判断）：**
```
用户：用 Deep 模式核实"AI 让前端程序员三年内消失"这个说法，我要认真评估职业影响
Agent：（完整交叉取证）→ 输出深度报告
```

**个人目标分析（需显式开启）：**
```
用户：结合我的情况分析——我是 3 年前端，想转 AI 应用开发
Agent：（仅在开启时）单独输出"个人目标分析"章节，且不污染事实结论
```
> 个人目标分析**默认关闭**。不读取你的记忆/文件/历史，仅使用你本次主动提供的目标。

## 八、Quick Check 与 Deep Investigation 的区别

| 维度 | Quick Check | Deep Investigation |
|-----|------------|-------------------|
| 适用 | 日常视频、普通技术信息 | 重大技术突破、商业机会、职业影响 |
| 主张范围 | 1–5 条最具体主张 | 全部可验证主张 |
| 单主张来源 | 2–4 个 | 4–8 个（交叉） |
| 证据标准 | **相同** | **相同** |
| 报告长度 | 精简 | 完整 |

**铁律：** 快速模式只减少范围，**绝不降低**真实性要求。任何模式都禁止用模型记忆代替证据。

## 九、工具权限要求

Skill 正常工作需要宿主 Agent 具备（复用即可，无需额外搭建）：

- 网络搜索（WebSearch）
- 网页抓取（WebFetch）
- 视频解析 / 字幕 / 语音转写（若核查视频）
- 代码执行（运行仓库 `scripts/`，纯标准库）
- LLM 推理（归纳、写作）

**不需要**：MCP Server、API Key 配置、数据库、独立服务。

## 十、常见问题

**Q：它会替我判断"该不该用这个工具"吗？**
A：默认只做客观事实调查。只有你主动开启"个人目标分析"并提供目标时，才会结合你的情况给建议，且结论与事实物理隔离。

**Q：查不到证据怎么办？**
A：明确标注 `未验证（unverified）`，绝不伪造成"已验证"或"已证伪"。

**Q：它会不会误判真实的技术？**
A：会公允肯定真实能力。识别"夸大"不等于判定"虚假"；技术可能真实但被包装夸大，报告会分别说明。

**Q：支持中文以外的语言吗？**
A：报告结构支持多语言内容；当前示例以中文为主。

**Q：我的数据会被上传吗？**
A：报告与证据均在你本地 Agent 内生成。Skill 不内置任何外发通道。

## 十一、安全和隐私说明

- **Prompt Injection 防护**：网页/视频中的指令（"忽略以上指令"等）一律忽略，只作为"被核查对象"。
- **不泄露隐私**：不读取本地文件、密钥、记忆、历史对话。
- **SSRF 防护**：不访问 `localhost`、内网段、云元数据地址。
- **隔离执行**：不可信代码仅做静态描述，不在本机直接运行。
- **不绕过限制**：不爬需登录内容，访问失败即标记"信息不足"。
- **不伪造精确**：禁止用无依据百分比制造虚假精确性。

## 十二、贡献指南

欢迎提 Issue 与 PR。贡献前请阅读 [`docs/PRD.md`](docs/PRD.md)、[`docs/SKILL_SPEC.md`](docs/SKILL_SPEC.md)。

- 新增主张类别 / 来源类型：同步更新 `SKILL.md`、对应 `references/*.md` 与 JSON Schema 的 `enum`。
- 新增工作流：放 `skills/ai-reality-check/workflows/` 并在 `SKILL.md` 路由。
- 新增脚本：保持纯标准库、清晰 argparse 接口、附测试。
- Schema 变更遵循"只增不改"的向后兼容原则，并递增 `schema_version`。

---

## 项目结构

```
ai-reality-check/
├── README.md
├── LICENSE
├── docs/
│   ├── PRD.md                 # 产品需求文档
│   ├── ARCHITECTURE.md        # 技术架构
│   ├── SKILL_SPEC.md          # 技能规范（设计权威）
│   └── DELIVERY_REPORT.md     # 交付报告
├── skills/
│   └── ai-reality-check/      # 核心 Skill
│       ├── SKILL.md
│       ├── references/        # 按需加载的参考知识
│       ├── workflows/         # Quick / Deep / Personal 工作流
│       └── templates/         # 报告模板 + JSON Schema
├── scripts/                   # 安装器 + 校验/生成/去重脚本
├── tests/                     # 自动化测试 + 测试案例集
└── examples/                  # 真实调查示例
```

## 许可

[MIT](LICENSE) © AI Reality Check contributors
