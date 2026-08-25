# Skills 原理详解：给 Agent 的按需加载知识包

> **一句话定义**：Skill = **一个文件夹，里面放一份 SKILL.md（说明书）**。
> 它不给模型新能力，只在恰当的时机，把恰当的知识注入上下文。
> Anthropic 官方的比喻：给新员工写的**入职手册**（onboarding guide）。

## 0. 本文怎么读

- **零基础**：先读第 1 节的问题和比喻，再看第 11 节动手写一个——Skills 是"看着玄、做着简单"的典型；
- **想写 skill 的人**：第 3（规范）、4（机制）、5（触发）、10（最佳实践）是核心；
- **时间基准**：截至 2026 年中。Skills 已从 Claude 专属演进为跨工具开放标准。

---

## 1. 问题：上下文经济学

> **人话版**：Agent 的脑子（上下文窗口）很小很贵。你有几十个领域的"标准操作流程"想教它——全塞进去脑子就满了，不塞它就用通用知识瞎闯。Skills 的答案：**把每套流程写成一本小册子放进书架，平时只在墙上贴一张目录卡片，用到哪本再取哪本。**

上一篇讲过两个事实：上下文是稀缺资源（context rot），工具定义 58 个就能吃掉 55K token。知识注入面临同样的两难：

- **全塞进去？** 你有 React 性能优化、PR 审查规范、SQL 调优、PDF 处理……几十个领域的最佳实践，全写进系统提示，窗口直接爆炸，正常干活的空间没了。
- **都不放？** 模型用通用知识硬闯专业任务，质量不稳定——它**会做**，但不知道你们团队的标准做法。

注意缺的是**知识，不是能力**：模型本来就能读写文件、跑命令（工具已经给了能力），缺的是"这类任务在我们这儿的标准做法是什么"。

一个准确的类比：**工具是手，Skill 是操作手册（SOP）**。手册不会让你长出新的手，但能让你把手用对。

## 2. 时间线：Skills 怎么来的

| 时间 | 事件 |
| --- | --- |
| 2025-10-16 | Anthropic 发布 **Agent Skills**（博客 + anthropics/skills 开源仓库），覆盖 Claude.ai / Claude Code / Agent SDK / API |
| 2025-12-18 | 发布为**开放标准** agentskills.io（规范 + 参考实现），任何工具都可以实现 |
| 2025-12-19 | Anthropic 官方博客讲清 Skills 与 MCP 的分工（见第 9 节） |
| 2026-01-20 | Vercel 上线 **skills.sh** 生态（`npx skills add` 一条命令装技能，自动探测本机 51 种 agent），头部技能 find-skills 安装量破 300 万 |
| 2026 | Cursor / Codex / Gemini CLI / TRAE / Copilot / Windsurf 等全面原生支持，事实行业标准 |

官方给 Skills 的四个特性，理解了它们就理解了设计取舍：

| 特性 | 含义 |
| --- | --- |
| **Composable 可组合** | 技能之间可以叠加，一个技能也可以指挥模型用多个工具/多个 MCP |
| **Portable 可移植** | 同一个文件夹，Claude.ai、Claude Code、Cursor、Codex、TRAE 都能用（开放标准保证） |
| **Efficient 高效** | 按需加载，不用不占上下文（第 4 节） |
| **Powerful 强大** | 可以携带**可执行脚本**——有些活让代码干比让模型逐字生成可靠得多（第 8 节） |

## 3. Skill 长什么样：结构与规范

### 3.1 目录结构

```text
my-skill/
├── SKILL.md          # 唯一必需：YAML frontmatter（元数据）+ Markdown 正文（指令）
├── references/       # 可选：详细参考文档，模型按需阅读
├── scripts/          # 可选：现成脚本，模型直接调用，不必每次重写
└── assets/           # 可选：模板、样例等静态资源
```

### 3.2 开放标准的 6 个 frontmatter 字段（agentskills.io）

| 字段 | 必需 | 约束与说明 |
| --- | --- | --- |
| `name` | 是 | 1–64 字符；仅小写字母/数字/连字符；不得以连字符开头结尾、不得连续 `--`；**必须与目录名一致**；不得含保留词 anthropic / claude |
| `description` | 是 | 1–1024 字符；说明"做什么"+"何时用"——这是整份文件最重要的字段（第 5 节） |
| `license` | 否 | 许可证，如 `Apache-2.0` |
| `compatibility` | 否 | 环境要求（1–500 字符），如 `Requires git, docker, jq` |
| `metadata` | 否 | 任意 string→string 键值对（author、version 等），建议键名加前缀 |
| `allowed-tools` | 否 | **空格分隔**的预授权工具（实验性），如 `Bash(git:*) Read` |

最小合法示例：

```markdown
---
name: pdf-processing
description: Extract PDF text, fill forms, merge files. Use when handling PDFs.
license: Apache-2.0
---
（正文：写给模型看的操作指令）
```

### 3.3 Claude Code 在标准之上的扩展字段（了解即可）

各工具在标准之上做了私有扩展（这正是"核心互操作 + 各自增强"的生态格局）。Claude Code 的常用扩展：

| 字段 | 作用 |
| --- | --- |
| `when_to_use` | 补充触发场景（与 description 合计在技能清单中截断于 1536 字符） |
| `disable-model-invocation` | 禁止模型自动触发，仅用户 `/name` 可用 |
| `user-invocable: false` | 反向：仅模型可触发，用户不可见 |
| `allowed-tools` / `disallowed-tools` | 技能激活期间预授权/禁用某些工具 |
| `context: fork` | 在隔离子代理上下文中运行该技能 |
| `$ARGUMENTS`、`${CLAUDE_SKILL_DIR}` 等变量 | 支持传参和跨安装位置寻址脚本 |

还有动态上下文注入：正文里写 `` !`git diff HEAD` ``，发送给模型**前**先执行命令、把输出替换进正文。

注意：**上传到 Claude.ai / API 时只接受标准 6 字段**，多余字段直接报错——写跨平台技能时以标准为准。

## 4. 核心机制：渐进式披露（Progressive Disclosure）

> **人话版**：三级火箭。**第一级**：每个技能只把"名字+一句话简介"常驻上下文（像书架墙上的目录卡）；**第二级**：任务匹配上了，才把整本说明书读进来；**第三级**：说明书里指向的厚参考书、可执行脚本，翻到那一页才读。所以你装 100 个技能也不怕——平时它们只是墙上 100 张小卡片。

| 层级 | 内容 | 何时进入上下文 | Token 成本 |
| --- | --- | --- | --- |
| **第 1 层 Metadata** | frontmatter 的 `name + description` | 会话启动时全部预载进系统提示 | 每个技能约 **~100 tokens** |
| **第 2 层 Instructions** | SKILL.md 正文 | 任务匹配、技能被触发时才读入 | 官方建议 **< 5K tokens**（正文 < 500 行） |
| **第 3 层 Resources/Code** | references/、assets/、scripts/ | 正文指路，用到才读；**脚本连代码都不进上下文，只有运行输出进** | 原则上无上限 |

### 4.1 加载时序：没有魔法，全是文件读取

官方工程博客还原了一次 PDF 处理任务的完整时序：

1. 会话启动，初始上下文 = 系统提示 + **所有技能的 name/description** + 用户消息；
2. 用户丢来一个 PDF 任务，模型判断"pdf 技能相关"→ **调用工具读取 `pdf/SKILL.md`**（对，就是普通的文件读取，不是什么框架黑盒；Claude Code 中体现为模型调用 Skill 工具）；
3. SKILL.md 正文说"填表单细节见 `references/forms.md`" → 模型按需再读那一个文件；
4. 继续执行任务，其余几十个技能纹丝未动。

由此得出官方工程结论：**因为 agent 有文件系统 + 代码执行，技能可捆绑的上下文实际上是无限的（effectively unbounded）**——SKILL.md 只是目录页，真正的知识可以塞满整个文件夹。

### 4.2 一笔账

你装了 40 个技能：第 1 层索引总开销约 4000 tokens（40 × ~100），相当于读半个文件，**且大部分工具会做预算控制**——Claude Code 把技能清单预算默认限制为模型上下文的 **1%**，超了就从最少使用的技能开始砍；Codex 是 **2% 或 8000 字符**。而其中某个技能带的 3 万 token 领域手册，只在真正触发它的那个会话、只读用到的章节。

这与操作系统的**虚拟内存/惰性加载**是同一个思想：稀缺资源只放高频小件（索引），大件（正文）用到再取。它正是上一篇 6.2 节"按需检索"在知识管理上的落地。

### 4.3 三个官方推荐的组织模式

| 模式 | 做法 | 例子 |
| --- | --- | --- |
| **高层指南 + 引用** | SKILL.md 只放 Quick start 和导航，细节指向引用文件 | 正文 → `REFERENCE.md` / `EXAMPLES.md` |
| **按领域拆分** | 参考文档按业务域拆开，正文甚至教模型用 grep 定向检索 | BigQuery 技能拆 `reference/{finance,sales,product}.md`，正文写"查营收就 `grep -i revenue reference/finance.md`" |
| **条件性细节** | 简单情况直接做，复杂情况才去读厚参考 | docx 技能：简单改 XML 直接做，修订跟踪才读 `REDLINING.md`，OOXML 深水区才读 `OOXML.md` |

两条硬规矩：**引用保持一层深**（嵌套引用会让模型 `head -100` 式偷懒）；**超过 100 行的引用文件加目录（TOC）**。

## 5. 触发机制：description 是唯一的钩子

> **人话版**：模型怎么知道"该翻哪本手册"？它拿你的请求，跟墙上 100 张目录卡片挨个比对，哪张像就取哪本。所以**卡片上那两行字（description）决定了这个技能的生死**——写得含蓄，模型永远想不起它；正文写得再好也没用，因为模型根本没翻开。

### 5.1 三种触发方式

1. **语义匹配（model-invoked，主路径）**：模型把用户请求与所有技能的 description 做匹配，匹配上就加载（Claude Code 中模型调用 `Skill(name)` 工具）；
2. **显式调用（user-invoked）**：用户输入 `/skill-name` 直接点名，不赌模型自觉——关键流程的兜底手段；
3. **预载（preloaded）**：子代理可以在自己的 frontmatter `skills` 字段里声明预载某些技能全文（启动即注入，而非等触发）。

控制矩阵（谁能调用）：

| 配置 | 模型可触发 | 用户可触发 |
| --- | --- | --- |
| 默认 | ✓ | ✓（`/name`） |
| `disable-model-invocation: true` | ✗（description 也不进上下文） | ✓ |
| `user-invocable: false` | ✓ | ✗ |

### 5.2 触发排障（实战经验）

- **总不触发** → description 里补上"用户会自然说出口的关键词"（中文技能就写中文触发词）；frontmatter YAML 写错会导致空元数据加载，用 `--debug` 看解析错误；
- **总误触发** → 收窄 description，或干脆 `disable-model-invocation` 只留手动。

## 6. 放哪里：目录、优先级与跨工具兼容

各主流工具的技能目录（同名冲突时按各工具的优先级规则生效）：

| 工具 | 项目级 | 用户级 | 备注 |
| --- | --- | --- | --- |
| **Claude Code** | `.claude/skills/` | `~/.claude/skills/` | 企业级 managed 目录优先级最高；支持嵌套发现、会话中改动即时生效 |
| **跨工具标准** | `.agents/skills/` | `~/.agents/skills/` | 开放标准约定的互操作位置，被最多工具识别 |
| **OpenAI Codex** | `.agents/skills/` | `~/.agents/skills/` | 另有 `/etc/codex/skills` 管理员级 |
| **Cursor** | `.cursor/skills/`（兼容读 `.agents/`、`.claude/`、`.codex/`） | `~/.cursor/skills/`、`~/.agents/skills/` | 兼容层最宽 |
| **Gemini CLI** | `.gemini/skills/` 或 `.agents/skills/` | `~/.gemini/skills/` 或 `~/.agents/skills/` | 同层内 `.agents` 优先 |
| **TRAE** | `.trae/skills/`（支持 `.agents/skills/`，重名时 `.trae` 优先） | `~/.trae-cn/skills`（macOS/Linux） | 你正在用的工具 |

两条选位原则：

- 只在这个仓库有意义的放**项目级**（进 git，团队共享）；走到哪都想用的放**用户级**（`~/`）；
- 想覆盖某个已安装的技能？把**同名**技能放进更高优先级目录即可，不必改原文件。

安装生态：`npx skills add <owner>/<repo>`（skills.sh，自动探测本机 agent 并写入正确目录）、Claude Code 的 `/plugin marketplace add anthropics/skills`、以及各工具的技能市场。

## 7. 官方仓库里都有什么（anthropics/skills）

值得拆开看的真实样本：

| 类别 | 技能 | 看点 |
| --- | --- | --- |
| **文档四件套** | `docx` / `pdf` / `pptx` / `xlsx` | 生产级示范：SKILL.md 只写流程导航，重活全在 `scripts/` 里几十个 Python 脚本（提取表单、重算 Excel、加幻灯片……） |
| **开发类** | `mcp-builder`、`webapp-testing`（Playwright）、`frontend-design`、`claude-api` | 教模型生成 MCP server、写端到端测试 |
| **创意类** | `algorithmic-art`、`canvas-design` | 高自由度技能的写法 |
| **元技能** | `skill-creator` | 官方用来"造技能的技能"，其评测方法学见 10.6 节 |

## 8. scripts/：让代码干代码的活

官方设计动机原话大意：LLM 擅长很多事，但**有些操作用传统代码执行更好**——排序这件事，跑一个排序算法远比让模型逐字生成可靠；很多操作需要代码才有的确定性。

机制上最关键的一点：

> **模型运行脚本时，脚本源码和被处理的文件都不进入上下文，只有运行输出进入。**

这就是为什么文档四件套敢处理几百页的文件而不撑爆窗口——确定性、可复现、零上下文成本。

一个官方教学模式（codebase-visualizer 技能）：

```yaml
---
name: codebase-visualizer
description: Generate an interactive visualization of the codebase architecture.
allowed-tools: Bash(python3 *)   # 预授权：运行 python3 不再弹权限框
---
```

```text
正文里写：python3 ${CLAUDE_SKILL_DIR}/scripts/visualize.py .
# ${CLAUDE_SKILL_DIR} 变量保证无论技能装在哪都能找到自己的脚本
```

运行环境差异要留意：Claude API 的代码执行容器**无网络、不能装新包**（只能用预装依赖）；Claude Code / TRAE 在你本机运行，有完整网络和文件系统（所以也更需要注意安全）。

## 9. 概念对照：Skill vs 工具 vs MCP vs 子代理 vs 常驻规则

五个概念各管一段，混在一起就会选错药：

| | 本质 | 给模型什么 | 什么时候用 |
| --- | --- | --- | --- |
| **Skill** | markdown 知识包 | 知识、流程、约定（按需加载） | "怎么做最好"缺指导 |
| **工具（Tool）** | harness 内置函数 | 能力（读写执行） | "能不能做"缺手段 |
| **MCP** | 标准化外部服务协议 | 第三方系统的接入 | 连接外部世界（数据库、SaaS、浏览器） |
| **子代理** | 独立上下文的分身 | 隔离 + 并行 | 探索性脏活，防上下文污染 |
| **AGENTS.md / CLAUDE.md / Rules** | 常驻项目说明文件 | 项目背景（**全程占上下文**） | 每个任务都需要知道的项目约定 |

**Skill 与 MCP 的官方分工**（Anthropic 博客《Extending Claude's capabilities with skills and MCP servers》）用了五金店比喻：**MCP 让你走进货架，Skill 是懂行的店员的专业知识**——库存再多，不知道买什么、怎么用也没用。一句话定位：

> MCP server 给模型**外部系统的连接**（wiring），Skills 给模型**用好这些连接的知识**（instructions）。

机制层面的对照更直观：接 5 个 MCP server / 58 个工具 ≈ 55K token 常驻；40 个 Skill 的索引 ≈ 4K token 常驻。官方经验法则：MCP 里的工具用法提示保持通用，任务专属的工作流知识放 skill。二者常组合——一个 skill 指挥模型调用多个 MCP 工具。

与常驻规则文件的分工（Gemini 文档表述最清楚）：GEMINI.md/CLAUDE.md/Rules 提供**全程常驻的工作区背景**，Skills 是**按需加载的专业能力**。判断标准很简单：这条知识是不是每个任务都要用？是→规则文件；否→skill。

## 10. 编写最佳实践（来自 skill-creator 与官方指南）

### 10.1 description：技能的命（最重要）

- 用**第三人称**写（"Processes Excel files…"，禁止 "I can help…"）；
- 同时覆盖 **what**（干什么）+ **when**（什么话术/场景该触发）；
- 写进用户会自然说出的**关键词**（中文技能就写中文触发词）；
- 模型倾向**漏触发**而非误触发，措辞可以适度"外向"。对比：
  - 弱："如何为内部数据构建仪表盘"
  - 强："构建高性能内部数据仪表盘。**凡**用户提到 dashboards、数据可视化、内部指标，或想展示任何公司数据时**都应使用**——哪怕没明说 dashboard 这个词。"
- 关键用例放前面（清单可能被截断）；≤1024 字符。

### 10.2 正文：克制

- < 500 行 / < 5K tokens；默认假设"模型已经很聪明"，每一段自问"值不值这个 token"；
- 引用文件一层深；>100 行的引用加目录。

### 10.3 指令风格

- **祈使句 + 讲 why**："编辑前先读文件"比"你应该考虑……"有效；规则不明显时解释原因，模型理解了原因会执行得更好（满篇全大写的 MUST/NEVER 通常是规则没讲清的遮羞布）；
- **例子胜过规则**：要结构化输出？直接给一个字面示例；该用哪个工具？直接给调用样例；
- 复杂流程给**可勾选 checklist**；能验证的就建**反馈回路**（跑校验器 → 修复 → 重跑，验证不过不继续）。

### 10.4 自由度三级（TRAE 官方最佳实践也采用此框架）

| 自由度 | 给什么 | 适合 |
| --- | --- | --- |
| 高 | 只给原则和目标 | 代码审查、创意类任务（模型发挥空间大） |
| 中 | 给模板 + 参数说明 | 报告生成、格式化工件 |
| 低 | 给精确脚本，不许改参数 | 数据库迁移、部署等脆弱操作 |

任务越脆弱，自由度越低。

### 10.5 重复劳动固化成脚本

如果每次执行模型都在现场重写同一个辅助脚本，就把它放进 `scripts/`，正文里指个路（配合 `allowed-tools` 预授权，免权限弹窗）。写一次，次次复用，且不过上下文。

### 10.6 测试驱动迭代（skill-creator 的方法学）

- 先想清楚"agent 现在在哪里失败"，再写 skill（评测驱动，不是灵感驱动）；
- 用 2–3 个**真实口吻**的测试提示词跑（带具体路径、口语化、甚至有错别字），**开新会话测**（作者上下文会遮蔽缺陷）；
- skill-creator 的进阶做法：**同一轮并行起两个子代理**，一个带技能、一个不带（baseline），对输出做断言评分（grading.json），聚合出 benchmark（通过率 / 耗时 / token 消耗，均值±标准差），再迭代；
- 观察"过程"和"结果"同样重要：如果技能让模型原地打转、反复读同一个文件，说明规则过拟合了，该删不该加。

### 10.7 版本与命名

- **name 是触发契约**：必须与目录名一致；更新后保持原名，不要 `-v2`（改名 = 一个全新技能）；版本号放 `metadata.version`；
- 命名推荐**动名词**结构（如 `processing-pdfs`）；避免 `helper`/`utils`/`tools` 这种无信息量的名字。

### 10.8 安全

- 技能 ≈ 安装软件：**只装可信来源**，安装前审计捆绑的脚本、依赖和正文里的外链指令；
- 警惕 `allowed-tools` 自授权：仓库里白嫖来的技能可能预授权了危险命令；
- 记得上一篇的工具投毒——技能正文同样可能藏间接注入。

## 11. 动手：15 分钟写一个自己的 Skill

目标：写一个 `weekly-report` 技能——用户说"生成周报"时，自动从 git 历史提取本周提交并产出中文周报。

**第 1 步**：建目录和文件

```text
weekly-report/
├── SKILL.md
└── scripts/
    └── gen.sh
```

**第 2 步**：写 SKILL.md

```markdown
---
name: weekly-report
description: 根据 git 提交历史生成中文工作周报。凡用户提到"周报、weekly report、
  本周总结、汇报一下这周做了什么"时都应使用，输出 Markdown 格式周报。
metadata:
  author: your-name
  version: "1.0"
---

# 周报生成

## 流程

1. 运行脚本提取本周提交（脚本会输出按天分组的提交摘要）：

   bash scripts/gen.sh

2. 把脚本输出整理成以下结构（**严格用这个模板**）：

   ## 本周工作（M月D日 – M月D日）
   ### 完成事项
   - [动词开头的条目，合并零碎提交，提炼意图而非罗列 commit]
   ### 数据/成果
   - [可量化的数字，没有就省略本节]
   ### 下周计划
   - [从提交趋势推断，标注"（待确认）"]

3. 输出前自检：条目是否都来自真实提交？禁止编造没有的工作。
```

**第 3 步**：写 scripts/gen.sh（记住：脚本不进上下文，只有输出进）

```bash
#!/usr/bin/env bash
# 提取最近 7 天的 git 提交，按天分组、去掉合并噪声，供周报技能使用
set -euo pipefail
git log --since="7 days ago" \
  --pretty=format:"%ad|%s" --date=format:"%m-%d %H:%M" \
  --no-merges \
  | awk -F'|' '
      # 按日期分组：第一字段是"月-日 时：分"，取日期部分作 key
      { split($1, t, " "); day=t[1];
        if (day != prev) { print "\n## " day; prev = day }
        print "- " $2 }'
```

**第 4 步**：放进对的位置并测试

- 项目级：`.agents/skills/weekly-report/`（跨工具通用）或 `.trae/skills/weekly-report/`（TRAE 项目级）；
- 测试三连：新开会话说"帮我整理下周报"（测语义触发）→ 说 `/weekly-report`（测显式触发）→ 检查输出是否守模板、有没有编造。

这就是一个完整的技能：**一张目录卡片（description）+ 一页流程（SKILL.md）+ 一个干活脚本（gen.sh）**。

## 12. 局限与边界

诚实起见，skill 不是银弹：

- **不给能力**。模型做不到的事（比如真正渲染一张图），写多少 markdown 都没用，得靠工具；
- **触发是概率性的**。语义匹配就有漏网之鱼，关键流程靠 `/name` 显式触发兜底；
- **质量上限是作者水平**。skill 只是把好做法注入上下文，没有好做法可写时它无米下锅；
- **有维护成本**。约定变了 skill 不跟着变，模型会一直照旧手册办事——过期的 SOP 比没有更糟。

## 13. 小结

| 机制 | 一句话 |
| --- | --- |
| Skill 是什么 | 文件夹 + SKILL.md，给 agent 的按需加载知识包（2025-12 起是开放标准） |
| 渐进式披露 | 索引（~100 token/个）常驻 → 正文（<5K）触发才载 → 引用/脚本按需，上下文"实际无上限" |
| 触发原理 | 模型拿请求和 description 语义匹配；description 是全部曝光预算；`/name` 显式兜底 |
| 放哪里 | 跨工具 `.agents/skills/`，各工具自家目录优先级更高 |
| 脚本机制 | 代码不进上下文，只有输出进；确定性任务交给代码 |
| 与 MCP 分工 | MCP 是接线（wiring），Skills 是说明书（instructions），常组合使用 |
| 写好它 | description 外向、正文克制、例子开路、脚本固化、评测迭代、name 永不变 |

回到上一篇的结尾：agent 工程的核心矛盾是"怎么花好窗口里每一个 token"。Skills 用"索引常驻、正文按需"回答了**知识注入**这一半；压缩和子代理回答了**历史膨胀**那一半。三者合起来，就是一台能带着全部家当干活的机器。

## 延伸阅读（一手来源）

- 发布博客：Equipping agents for the real world with Agent Skills — <https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills>
- Agent Skills 开放标准（含完整规范）— <https://agentskills.io/specification>
- 官方技能仓库（真实样本）— <https://github.com/anthropics/skills>
- Claude Code Skills 文档 — <https://code.claude.com/docs/en/skills>
- Skills 最佳实践（官方）— <https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices>
- Skills 与 MCP 的分工 — <https://website.claude.com/blog/extending-claude-capabilities-with-skills-mcp-servers>
- skills.sh 生态（安装 CLI 与排行榜）— <https://skills.sh>
- TRAE Skills 文档 — <https://docs.trae.cn/ide/skills>
- Cursor / Codex / Gemini 的 Skills 文档 — <https://cursor.com/docs/skills> · <https://developers.openai.com/codex/skills> · <https://geminicli.com/docs/cli/skills/>
- skill-creator（元技能本体，学写技能的最佳教材）— <https://github.com/anthropics/skills/tree/main/skills/skill-creator>
