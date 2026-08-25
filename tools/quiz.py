#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
quiz.py · 间隔检索练习工具（学习科学依据：检索练习 + 间隔重复）
用法：
    python3 tools/quiz.py tracks/cv          # 抽 10 题（默认）
    python3 tools/quiz.py tracks/qa 5        # 抽 5 题
    python3 tools/quiz.py --all 20           # 全库抽 20 题

题目来源：各里程碑 README 与 practice.md 中的自测/过关清单条目（`- [ ] 你能…`）。
答题后显示出处，答错的题给出文件位置供回读。
无外部依赖，纯标准库。
"""

import random
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
# 链接目标存在性校验时排除备份目录
EXCLUDED_PARTS = {".backup", ".trae"}
ITEM_RE = re.compile(r"^- \[ \] (.+)$", re.M)
# 过关清单条目里出现的相对链接，用于提示"去哪补"
LINK_IN_ITEM = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def collect_items(scope_dir):
    """扫描范围内的里程碑 README 与 practice 文件，采集过关/自测条目。

    只认两类来源（题面质量有保障）：
    - tracks/<track>/<M0|T0…>/README.md 的过关清单
    - practice*.md / P*.md / 检查清单.md 的自测条目
    """
    items = []
    for md in sorted(scope_dir.rglob("*.md")):
        rel = md.relative_to(ROOT)
        if any(p in EXCLUDED_PARTS for p in rel.parts):
            continue
        name = md.name
        is_gate = (name == "README.md" and md.parent.parent.name != "tracks"
                   and md.parent.name[0] in "MTmt" and md.parent.name[1:2].isdigit())
        is_practice = (name.startswith("practice") or name.startswith("P")
                       or name == "检查清单.md")
        if not (is_gate or is_practice):
            continue
        text = md.read_text(encoding="utf-8")
        for m in ITEM_RE.finditer(text):
            body = m.group(1).strip()
            # 跳过评分细则类条目与过短条目
            if len(body) < 10 or "分）" in body or body.startswith("["):
                continue
            # 提取条目内第一个有效相对链接作为补课入口
            hint = ""
            for label, target in LINK_IN_ITEM.findall(body):
                t = unquote(target.split("#")[0])
                if t.startswith(("http", "#")):
                    continue
                if (md.parent / t).resolve().exists():
                    hint = f"{md.parent / t}"
                    break
            items.append((body, rel.as_posix(), hint))
    return items


def run_quiz(items, n):
    """随机抽题，逐题作答并统计。"""
    random.shuffle(items)
    picked = items[:n]
    right = 0
    print(f"共 {len(items)} 题在库，本次抽 {len(picked)} 题。")
    print("答题方式：看题 -> 先在心里回答 -> 回车看参考出处 -> 自评 y/n\n")
    for i, (q, src, hint) in enumerate(picked, 1):
        print(f"[{i}/{len(picked)}] {q}")
        input("  （先回答，回车看出处）> ")
        loc = hint if hint else f"{ROOT / src}"
        print(f"  出处：{src}")
        if hint:
            print(f"  回读：{Path(hint).relative_to(ROOT)}")
        ans = input("  自评答对了吗？(y/N) > ").strip().lower()
        if ans == "y":
            right += 1
        print()
    print(f"结果：{right}/{len(picked)}。")
    if right < len(picked):
        print("答错的题请回出处重读——检索失败的地方就是记忆的缺口。")
        print("建议：3 天后重跑本题库（间隔重复），直到全对。")


def main():
    """解析参数并启动练习。"""
    args = [a for a in sys.argv[1:]]
    n = 10
    if args and args[-1].isdigit():
        n = int(args.pop())
    if args and args[0] == "--all":
        scope = ROOT
    elif args:
        scope = ROOT / args[0]
        if not scope.exists():
            print(f"目录不存在：{args[0]}（相对仓库根，如 tracks/cv）")
            sys.exit(1)
    else:
        print(__doc__)
        sys.exit(0)
    items = collect_items(scope)
    if not items:
        print("该范围内没有找到自测条目（- [ ] 开头的过关/自测清单）。")
        sys.exit(0)
    run_quiz(items, n)


if __name__ == "__main__":
    main()
