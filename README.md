# LifelongLearning · 一套让人真正学会的知识系统

这不是一个文档堆，而是一套按学习科学设计的**过关式学习系统**：四条能力轨道，每个里程碑以项目收尾、以"你能做什么"的清单验收。看完了不等于学会了——**做出来才算。**

## 三步开始

1. **[START.md](START.md)** · 回答三个问题，3 分钟找到你的起点
2. **[ROADMAP.md](ROADMAP.md)** · 全局地图，勾选你的进度
3. 进轨道，按里程碑过关

## 四条轨道

| 轨道 | 回答的问题 | 过关产出 | 全程 |
| --- | --- | --- | --- |
| [计算机视觉](tracks/cv/TRACK.md) | 计算机怎么"看懂"图像？ | MNIST 分类器 → CIFAR-10 → YOLO 检测 → capstone | 6-9 月 |
| [软件测试](tracks/qa/TRACK.md) | 怎么系统地找出缺陷？ | 用例集 → 测试计划 → 自动化套件 → 测试方案 | 3-5 月 |
| [机器学习](tracks/ml/TRACK.md) | 表格数据怎么建模？ | Kaggle 提交 + 调参报告 | 1-2 月 |
| [AI 编程助手](tracks/agent/TRACK.md) | AI 助手为什么能干活？ | 亲手写一个 skill | 1-2 周 |

## 这套系统的不一样之处

- **过关制，不是读完制**：每个里程碑有项目验收和行为动词清单，不达标不前进
- **项目驱动**：M0 第三课就能跑出第一个程序；数学不再前置，而是卡壳时按需补（[prep/](prep/README.md)）
- **对抗遗忘**：每周用 [tools/quiz.py](tools/quiz.py) 做间隔检索练习（依据：检索练习与间隔重复的实证研究）
- **诚实标注**：没写的内容明说"计划中"，绝不虚构

## 目录结构

```
START.md / ROADMAP.md     # 诊断入口与全局进度
tracks/                   # 四条轨道（cv / qa / ml / agent）
prep/                     # 按需补课（Python / 数学）
references/               # 速查、术语、公式、排障、模板
tools/quiz.py             # 间隔检索练习
system/METHOD.md          # 这套系统为什么这样设计（证据→决策）
docs/写作规范.md          # 内容写作标准
.backup/                  # 旧架构完整存档（2026-08 前的版本）
```

## 为什么这样设计

每个架构决策对应一条学习科学证据（检索练习、掌握学习、项目驱动、认知负荷…），完整论证见 [system/METHOD.md](system/METHOD.md)。

## 参与共建

内容遵循 [docs/写作规范.md](docs/写作规范.md)，新内容的角色定位见 [system/METHOD.md](system/METHOD.md) 的"文档角色"表。提交前运行检查（坏链 / AI 味 / 代码围栏必须全绿）：

```bash
python3 .trae/skills/tutorial-writing/scripts/check_docs.py
```

## 许可

内容采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)：可分享、可改编，需署名、非商业、同许可。
