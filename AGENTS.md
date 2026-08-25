# AGENTS.md — 本仓库的强制规则

这是一个过关式学习知识库（四条轨道：视觉 / 测试 / 建模 / AI 助手），交付物是 Markdown 教程与学习工具。任何 AI 助手在本仓库工作前，必须先读完本文。

## 强制约束（MUST）

1. **写作前加载规范**：新建或修改任何 `.md` 内容前，必须先加载 `tutorial-writing` skill（`.trae/skills/tutorial-writing/SKILL.md`），或通读 [docs/写作规范.md](docs/写作规范.md)；新增/修改里程碑或课时，还须读 [system/METHOD.md](system/METHOD.md) 的"文档角色"表——先想清楚这份文件扮演什么角色。冲突时以 docs/写作规范.md 为准。
2. **AI 味零容忍**：产出物中不得出现自评分数、无来源百分比、shields.io 徽章、标题装饰 emoji、"待补充"占位符、复读式总结、占位联系方式、指向不存在文件的链接。完整禁止清单见写作规范第三节。
3. **代码块规则**：语言标记必须与内容一致（Python 代码标 `python` 而非 `bash`）；示例代码带函数级注释和预期输出。
4. **链接必须可达**：涉及仓库内路径的改动，提交前运行检查脚本，坏链数必须为 0：

   ```bash
   python3 .trae/skills/tutorial-writing/scripts/check_docs.py
   ```

5. **删除/移动文件前先备份**：复制到 `.backup/<日期-操作>/` 后再操作，禁止直接删除（用户明确要求）。
6. **诚实标注状态**：章节完成度只允许"完整 / 大纲 / 计划中"三档真实状态，禁止把未写的内容描述为已完成或虚构章节列表。
7. **变更留痕**：结构性改动（新增/移动/删除文件、重写导航）须同步更新 CHANGELOG.md，只记事实、不打分。
8. **维护系统结构**：新增内容必须落入现有角色（TRACK / 里程碑 README / 课 L* / PROJECT / practice / references / prep），不得在 tracks 外新建平行知识目录；过关清单必须用行为动词，里程碑必须有项目验收。

## 架构约定（详见 system/METHOD.md）

- `tracks/<track>/TRACK.md`：轨道定位与里程碑表；`tracks/<track>/<M0|T0…>/`：里程碑，README 含课表+项目+过关清单
- 课命名 `L*.md`、项目 `PROJECT*.md`、练习 `practice*.md`；参考类内容一律进 `references/`，基础补课进 `prep/`
- 图片统一放 `tracks/cv/assets/`（当前共享图池）
- 旧架构（2026-08 前）完整存档于 `.backup/legacy-20260826/`，勿改动、勿引用

## 仓库地形（速览）

```
├── START.md               # 诊断入口（背景×目标×时间 → 起点路径）
├── ROADMAP.md             # 全局技能树 + 进度勾选 + 周复习循环
├── tracks/                # cv（M0-M4+extras）/ qa（T0-T3）/ ml（M0）/ agent（M0）
├── prep/                  # python / math 按需补课
├── references/            # env、glossary×2、quickref、loss-math、debug、templates、links
├── tools/quiz.py          # 间隔检索练习（题源=过关清单）
├── system/METHOD.md       # 教学法依据与文档角色
├── docs/写作规范.md       # 写作标准（唯一权威）
└── .backup/               # 历史存档，勿动
```
