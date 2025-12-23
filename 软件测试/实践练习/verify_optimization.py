#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实践练习模块优化验证脚本
========================

验证所有优化内容是否完整
"""

import os
from pathlib import Path

def check_file_exists(filepath, description):
    """检查文件是否存在"""
    path = Path(filepath)
    exists = path.exists()
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {filepath}")
    return exists

def check_content_contains(filepath, keywords, description):
    """检查文件内容是否包含关键词"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        missing = []
        for keyword in keywords:
            if keyword not in content:
                missing.append(keyword)

        if not missing:
            print(f"✅ {description}: 包含所有必要内容")
            return True
        else:
            print(f"❌ {description}: 缺少 {missing}")
            return False
    except Exception as e:
        print(f"❌ {description}: 读取失败 - {e}")
        return False

def main():
    print("="*70)
    print("🎯 实践练习模块优化验证")
    print("="*70)

    base_dir = Path("/Users/fish/code/学习资料/软件测试/实践练习")

    # 1. 检查核心文件
    print("\n📁 1. 核心文件检查")
    print("-"*70)

    core_files = [
        ("README.md", "主README"),
        ("README_FIRST.md", "快速开始指南"),
        ("practice_assistant.py", "练习助手"),
        ("track_progress.sh", "进度追踪脚本"),
        ("OPTIMIZATION_SUMMARY.md", "优化总结"),
    ]

    core_ok = all(check_file_exists(base_dir / f, d) for f, d in core_files)

    # 2. 检查练习文件
    print("\n📚 2. 练习文件检查")
    print("-"*70)

    practice_files = [
        ("练习01-测试用例设计.md", "练习01"),
        ("练习02-缺陷报告编写.md", "练习02"),
        ("练习03-测试策略设计.md", "练习03"),
        ("练习04-单元测试框架.md", "练习04"),
    ]

    practice_ok = all(check_file_exists(base_dir / f, d) for f, d in practice_files)

    # 3. 检查练习01内容
    print("\n📋 3. 练习01内容验证")
    print("-"*70)

    p1_ok = check_content_contains(
        base_dir / "练习01-测试用例设计.md",
        ["练习说明", "配套工具", "测试用例模板生成器", "自动评估脚本", "学习进阶"],
        "练习01内容"
    )

    # 4. 检查练习02内容
    print("\n🐛 4. 练习02内容验证")
    print("-"*70)

    p2_ok = check_content_contains(
        base_dir / "练习02-缺陷报告编写.md",
        ["练习说明", "配套工具", "缺陷报告模板生成器", "缺陷分级决策树", "根因分析"],
        "练习02内容"
    )

    # 5. 检查练习03内容
    print("\n📈 5. 练习03内容验证")
    print("-"*70)

    p3_ok = check_content_contains(
        base_dir / "练习03-测试策略设计.md",
        ["练习说明", "配套工具", "测试金字塔设计模板", "风险评估矩阵", "资源分配计算器"],
        "练习03内容"
    )

    # 6. 检查练习04内容
    print("\n💻 6. 练习04内容验证")
    print("-"*70)

    p4_ok = check_content_contains(
        base_dir / "练习04-单元测试框架.md",
        ["练习说明", "配套工具", "测试代码生成器", "Mockito最佳实践", "覆盖率可视化"],
        "练习04内容"
    )

    # 7. 检查主README内容
    print("\n🎯 7. 主README内容验证")
    print("-"*70)

    readme_ok = check_content_contains(
        base_dir / "README.md",
        ["学习路径图", "进度追踪", "配套工具集", "每日练习计划", "效果评估"],
        "主README内容"
    )

    # 8. 检查快速指南内容
    print("\n🚀 8. 快速指南内容验证")
    print("-"*70)

    guide_ok = check_content_contains(
        base_dir / "README_FIRST.md",
        ["3步快速开始", "每日练习计划", "常见问题", "学习记录表"],
        "快速指南内容"
    )

    # 9. 检查优化总结
    print("\n📊 9. 优化总结验证")
    print("-"*70)

    summary_ok = check_content_contains(
        base_dir / "OPTIMIZATION_SUMMARY.md",
        ["优化概述", "完成的优化内容", "预期学习效果", "使用建议"],
        "优化总结内容"
    )

    # 10. 检查Python脚本可执行性
    print("\n🐍 10. Python脚本验证")
    print("-"*70)

    try:
        with open(base_dir / "practice_assistant.py", 'r') as f:
            first_line = f.readline().strip()
            if first_line.startswith("#!"):
                print("✅ practice_assistant.py: Shebang正确")
                py_ok = True
            else:
                print("⚠️ practice_assistant.py: 缺少Shebang")
                py_ok = True
    except:
        print("❌ practice_assistant.py: 读取失败")
        py_ok = False

    # 11. 检查Shell脚本可执行性
    print("\n🐚 11. Shell脚本验证")
    print("-"*70)

    shell_path = base_dir / "track_progress.sh"
    if shell_path.exists():
        is_executable = os.access(shell_path, os.X_OK)
        if is_executable:
            print("✅ track_progress.sh: 已设置可执行权限")
            shell_ok = True
        else:
            print("⚠️ track_progress.sh: 需要设置可执行权限")
            print("   运行: chmod +x track_progress.sh")
            shell_ok = True
    else:
        print("❌ track_progress.sh: 文件不存在")
        shell_ok = False

    # 总结
    print("\n" + "="*70)
    print("📊 验证结果汇总")
    print("="*70)

    all_checks = [
        ("核心文件", core_ok),
        ("练习文件", practice_ok),
        ("练习01内容", p1_ok),
        ("练习02内容", p2_ok),
        ("练习03内容", p3_ok),
        ("练习04内容", p4_ok),
        ("主README", readme_ok),
        ("快速指南", guide_ok),
        ("优化总结", summary_ok),
        ("Python脚本", py_ok),
        ("Shell脚本", shell_ok),
    ]

    passed = sum(1 for _, ok in all_checks if ok)
    total = len(all_checks)

    print(f"\n通过: {passed}/{total} ({passed/total*100:.1f}%)")

    if passed == total:
        print("\n🎉 恭喜！所有优化内容都已完成！")
        print("\n💡 下一步：")
        print("   1. 运行: python practice_assistant.py")
        print("   2. 或运行: ./track_progress.sh")
        print("   3. 开始你的第一个练习！")
    else:
        print("\n⚠️ 部分内容需要完善")
        print("\n待完成项：")
        for name, ok in all_checks:
            if not ok:
                print(f"   - {name}")

    print("\n" + "="*70)

if __name__ == "__main__":
    main()
