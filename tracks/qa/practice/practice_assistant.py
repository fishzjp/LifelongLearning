#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
软件测试实践练习助手
====================

功能：
1. 练习进度追踪
2. 自动评分评估
3. 学习建议生成
4. 练习报告生成

使用方法：
    python practice_assistant.py
"""

import os
import json
import datetime
from pathlib import Path

class PracticeAssistant:
    """练习助手"""

    def __init__(self, practice_dir="."):
        self.practice_dir = Path(practice_dir)
        self.progress_file = self.practice_dir / "practice_progress.json"
        self.user_data = self._load_progress()

    def _load_progress(self):
        """加载进度数据"""
        if self.progress_file.exists():
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "user_info": {},
            "progress": {},
            "scores": {},
            "notes": {},
            "start_date": datetime.datetime.now().isoformat()
        }

    def _save_progress(self):
        """保存进度"""
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(self.user_data, f, ensure_ascii=False, indent=2)

    def show_menu(self):
        """显示主菜单"""
        print("\n" + "="*60)
        print("🎯 软件测试实践练习助手")
        print("="*60)
        print("1. 📝 开始新练习")
        print("2. 📊 查看进度")
        print("3. ✅ 练习自测评估")
        print("4. 📈 生成学习报告")
        print("5. 🎯 制定学习计划")
        print("6. 💡 获取学习建议")
        print("0. 退出")
        print("="*60)

    def start_practice(self):
        """开始新练习"""
        print("\n📚 选择要开始的练习：")
        print("1. 练习01 - 测试用例设计")
        print("2. 练习02 - 缺陷报告编写")
        print("3. 练习03 - 测试策略设计")
        print("4. 练习04 - 单元测试框架")
        print("0. 返回")

        choice = input("\n请输入选择 (1-4): ").strip()

        practices = {
            "1": {"name": "测试用例设计", "file": "练习01-测试用例设计.md", "difficulty": "⭐⭐", "time": "60-90分钟"},
            "2": {"name": "缺陷报告编写", "file": "练习02-缺陷报告编写.md", "difficulty": "⭐⭐⭐", "time": "90-120分钟"},
            "3": {"name": "测试策略设计", "file": "练习03-测试策略设计.md", "difficulty": "⭐⭐⭐⭐", "time": "120-180分钟"},
            "4": {"name": "单元测试框架", "file": "练习04-单元测试框架.md", "difficulty": "⭐⭐⭐⭐", "time": "150-180分钟"}
        }

        if choice in practices:
            practice = practices[choice]
            print(f"\n✅ 你选择了：{practice['name']}")
            print(f"   难度: {practice['difficulty']}")
            print(f"   建议时间: {practice['time']}")
            print(f"   文件: {practice['file']}")

            # 记录开始时间
            practice_id = f"practice_{choice}"
            if practice_id not in self.user_data["progress"]:
                self.user_data["progress"][practice_id] = {
                    "name": practice['name'],
                    "start_time": datetime.datetime.now().isoformat(),
                    "status": "进行中",
                    "completed": False
                }
                self._save_progress()

            print(f"\n💡 提示：打开 {practice['file']} 开始练习")
            print("   完成后记得回来记录进度和自测哦！")

            # 显示配套工具
            self._show_tools(choice)

    def _show_tools(self, practice_num):
        """显示配套工具"""
        tools = {
            "1": ["测试用例模板生成器", "等价类划分检查表", "自动评估脚本"],
            "2": ["缺陷报告模板生成器", "缺陷分级决策树", "质量检查清单"],
            "3": ["测试金字塔设计模板", "风险评估矩阵", "资源分配计算器"],
            "4": ["测试代码生成器", "Mockito最佳实践模板", "覆盖率可视化工具"]
        }

        if practice_num in tools:
            print(f"\n🛠️ 配套工具：")
            for tool in tools[practice_num]:
                print(f"   - {tool}")

    def show_progress(self):
        """显示进度"""
        print("\n📊 练习进度")
        print("="*60)

        if not self.user_data["progress"]:
            print("暂无进度记录")
            return

        for practice_id, data in self.user_data["progress"].items():
            status = "✅" if data.get("completed") else "⏳"
            print(f"{status} {data['name']}")
            print(f"   状态: {data['status']}")

            if "start_time" in data:
                start = datetime.datetime.fromisoformat(data["start_time"])
                print(f"   开始: {start.strftime('%Y-%m-%d %H:%M')}")

            if "end_time" in data:
                end = datetime.datetime.fromisoformat(data["end_time"])
                print(f"   完成: {end.strftime('%Y-%m-%d %H:%M')}")

            if practice_id in self.user_data["scores"]:
                score = self.user_data["scores"][practice_id]
                print(f"   评分: {score}/100")

            print()

        # 总体进度
        total = len(self.user_data["progress"])
        completed = sum(1 for p in self.user_data["progress"].values() if p.get("completed"))
        print(f"总体进度: {completed}/{total} ({completed/total*100:.1f}%)")

    def self_assessment(self):
        """练习自测评估"""
        print("\n✅ 练习自测评估")
        print("="*60)

        print("请选择要评估的练习：")
        print("1. 练习01 - 测试用例设计")
        print("2. 练习02 - 缺陷报告编写")
        print("3. 练习03 - 测试策略设计")
        print("4. 练习04 - 单元测试框架")
        print("0. 返回")

        choice = input("\n请输入选择 (1-4): ").strip()

        if choice == "1":
            self._assess_test_cases()
        elif choice == "2":
            self._assess_defect_reports()
        elif choice == "3":
            self._assess_test_strategy()
        elif choice == "4":
            self._assess_unit_tests()

    def _assess_test_cases(self):
        """评估测试用例设计"""
        print("\n📝 测试用例设计评估")
        print("-"*60)

        score = 0

        # 完整性检查
        print("\n📋 完整性检查 (40分)")
        if self._ask_yes_no("  - 是否覆盖所有等价类？"):
            score += 10
        if self._ask_yes_no("  - 是否包含边界值测试？"):
            score += 10
        if self._ask_yes_no("  - 是否包含异常场景？"):
            score += 10
        if self._ask_yes_no("  - 格式是否规范？"):
            score += 10

        # 覆盖度检查
        print("\n🎯 覆盖度检查 (30分)")
        if self._ask_yes_no("  - 是否覆盖正常场景？"):
            score += 10
        if self._ask_yes_no("  - 是否覆盖边界场景？"):
            score += 10
        if self._ask_yes_no("  - 是否考虑安全性和性能？"):
            score += 10

        # 质量检查
        print("\n⭐ 质量检查 (30分)")
        if self._ask_yes_no("  - 测试步骤是否清晰？"):
            score += 10
        if self._ask_yes_no("  - 预期结果是否明确？"):
            score += 10
        if self._ask_yes_no("  - 是否有前置条件？"):
            score += 10

        self._show_assessment_result("练习01", score)

    def _assess_defect_reports(self):
        """评估缺陷报告"""
        print("\n🐛 缺陷报告编写评估")
        print("-"*60)

        score = 0

        # 完整性
        print("\n📋 完整性 (30分)")
        if self._ask_yes_no("  - 包含缺陷ID和基本信息？"):
            score += 10
        if self._ask_yes_no("  - 环境信息完整？"):
            score += 10
        if self._ask_yes_no("  - 附件齐全？"):
            score += 10

        # 清晰度
        print("\n🎯 清晰度 (30分)")
        if self._ask_yes_no("  - 标题简洁准确？"):
            score += 10
        if self._ask_yes_no("  - 复现步骤可执行？"):
            score += 10
        if self._ask_yes_no("  - 实际/期望结果明确？"):
            score += 10

        # 专业性
        print("\n⭐ 专业性 (25分)")
        if self._ask_yes_no("  - 严重程度和优先级合理？"):
            score += 10
        if self._ask_yes_no("  - 有根因分析？"):
            score += 10
        if self._ask_yes_no("  - 有影响范围分析？"):
            score += 5

        # 附加价值
        print("\n💎 附加价值 (15分)")
        if self._ask_yes_no("  - 提供解决方案建议？"):
            score += 10
        if self._ask_yes_no("  - 包含测试建议？"):
            score += 5

        self._show_assessment_result("练习02", score)

    def _assess_test_strategy(self):
        """评估测试策略"""
        print("\n📈 测试策略设计评估")
        print("-"*60)

        score = 0

        # 完整性
        print("\n📋 完整性 (40分)")
        if self._ask_yes_no("  - 测试金字塔设计合理？"):
            score += 10
        if self._ask_yes_no("  - 专项测试覆盖全面？"):
            score += 10
        if self._ask_yes_no("  - 有测试左移右移策略？"):
            score += 10
        if self._ask_yes_no("  - 风险管理完善？"):
            score += 10

        # 专业性
        print("\n⭐ 专业性 (30分)")
        if self._ask_yes_no("  - 符合行业最佳实践？"):
            score += 10
        if self._ask_yes_no("  - 针对项目特点定制？"):
            score += 10
        if self._ask_yes_no("  - 可执行性强？"):
            score += 10

        # 可行性
        print("\n✅ 可行性 (20分)")
        if self._ask_yes_no("  - 资源配置合理？"):
            score += 10
        if self._ask_yes_no("  - 时间计划可行？"):
            score += 10

        # 创新性
        print("\n💡 创新性 (10分)")
        if self._ask_yes_no("  - 有独特见解？"):
            score += 5
        if self._ask_yes_no("  - 有优化建议？"):
            score += 5

        self._show_assessment_result("练习03", score)

    def _assess_unit_tests(self):
        """评估单元测试"""
        print("\n💻 单元测试框架评估")
        print("-"*60)

        score = 0

        # 完整性
        print("\n📋 完整性 (30分)")
        if self._ask_yes_no("  - 覆盖所有主要场景？"):
            score += 10
        if self._ask_yes_no("  - 包含边界条件测试？"):
            score += 10
        if self._ask_yes_no("  - 包含异常场景测试？"):
            score += 10

        # Mock使用
        print("\n🎭 Mock使用 (20分)")
        if self._ask_yes_no("  - 正确使用Mockito？"):
            score += 10
        if self._ask_yes_no("  - 验证了Mock调用？"):
            score += 10

        # 代码质量
        print("\n⭐ 代码质量 (30分)")
        if self._ask_yes_no("  - 测试命名清晰？"):
            score += 10
        if self._ask_yes_no("  - 使用Given-When-Then结构？"):
            score += 10
        if self._ask_yes_no("  - 断言完整？"):
            score += 10

        # 覆盖率
        print("\n📊 覆盖率 (20分)")
        if self._ask_yes_no("  - 覆盖率 > 85%？"):
            score += 20
        elif self._ask_yes_no("  - 覆盖率 > 70%？"):
            score += 15
        elif self._ask_yes_no("  - 覆盖率 > 60%？"):
            score += 10

        self._show_assessment_result("练习04", score)

    def _ask_yes_no(self, question):
        """询问是/否"""
        while True:
            answer = input(f"{question} (y/n): ").strip().lower()
            if answer in ['y', 'yes', '是', 'y']:
                return True
            elif answer in ['n', 'no', '否', 'n']:
                return False
            else:
                print("请输入 y 或 n")

    def _show_assessment_result(self, practice_name, score):
        """显示评估结果"""
        print("\n" + "="*60)
        print(f"📊 {practice_name} 评估结果")
        print("="*60)
        print(f"总分: {score}/100")

        if score >= 90:
            level = "优秀 ✅"
            advice = "太棒了！你的练习质量非常高，可以直接用于生产环境。"
        elif score >= 70:
            level = "良好 ✅"
            advice = "做得不错！少量修改后即可达到优秀水平。"
        elif score >= 60:
            level = "及格 ⚠️"
            advice = "基本合格，建议补充部分内容，提升质量。"
        else:
            level = "不合格 ❌"
            advice = "需要继续努力，建议重新学习相关知识点。"

        print(f"等级: {level}")
        print(f"建议: {advice}")

        # 保存评分
        practice_id = practice_name.replace("练习", "practice_")
        self.user_data["scores"][practice_id] = score

        # 标记完成
        if score >= 60:
            if practice_id in self.user_data["progress"]:
                self.user_data["progress"][practice_id]["completed"] = True
                self.user_data["progress"][practice_id]["end_time"] = datetime.datetime.now().isoformat()
                self.user_data["progress"][practice_id]["status"] = "已完成"

        self._save_progress()

        print("\n💡 改进建议：")
        if score < 90:
            if score < 60:
                print("  - 需要补充更多测试场景")
                print("  - 完善测试用例格式")
                print("  - 学习相关理论知识")
            elif score < 70:
                print("  - 增加边界值测试")
                print("  - 补充异常场景")
                print("  - 优化测试步骤描述")
            else:
                print("  - 考虑安全性和性能测试")
                print("  - 优化测试用例描述")
                print("  - 增加根因分析")

    def generate_report(self):
        """生成学习报告"""
        print("\n📈 学习报告")
        print("="*60)

        # 基本信息
        start_date = self.user_data.get("start_date", datetime.datetime.now().isoformat())
        start = datetime.datetime.fromisoformat(start_date)
        days_passed = (datetime.datetime.now() - start).days

        print(f"学习天数: {days_passed}天")

        # 练习进度
        total = len(self.user_data["progress"])
        completed = sum(1 for p in self.user_data["progress"].values() if p.get("completed"))

        print(f"练习进度: {completed}/{total}")

        if total > 0:
            progress_bar = "█" * completed + "░" * (total - completed)
            print(f"进度条:   [{progress_bar}] {completed/total*100:.1f}%")

        # 平均分数
        if self.user_data["scores"]:
            avg_score = sum(self.user_data["scores"].values()) / len(self.user_data["scores"])
            print(f"平均分数: {avg_score:.1f}/100")

            if avg_score >= 90:
                level = "专家级"
            elif avg_score >= 70:
                level = "进阶级"
            elif avg_score >= 60:
                level = "入门级"
            else:
                level = "初学级"

            print(f"能力等级: {level}")

        # 详细进度
        print("\n详细进度:")
        for practice_id, data in self.user_data["progress"].items():
            status = "✅" if data.get("completed") else "⏳"
            score = self.user_data["scores"].get(practice_id, "未评估")
            print(f"  {status} {data['name']}: {score}/100")

        # 学习建议
        print("\n💡 学习建议:")
        self._generate_advice()

    def _generate_advice(self):
        """生成学习建议"""
        scores = self.user_data["scores"]

        if not scores:
            print("  - 还未开始练习，建议从练习01开始")
            return

        # 找出薄弱环节
        low_scores = {k: v for k, v in scores.items() if v < 70}

        if low_scores:
            print("  - 需要加强的练习:")
            for practice_id, score in low_scores.items():
                practice_name = self.user_data["progress"][practice_id]["name"]
                print(f"    * {practice_name} ({score}分)")

        # 找出已完成的练习
        completed = [p for p in self.user_data["progress"].values() if p.get("completed")]

        if len(completed) >= 2:
            print("  - 可以尝试将所学应用到实际项目中")

        if len(completed) >= 4:
            print("  - 恭喜完成所有练习！可以开始进阶学习")

        # 时间建议
        start_date = self.user_data.get("start_date")
        if start_date:
            days = (datetime.datetime.now() - datetime.datetime.fromisoformat(start_date)).days
            if days > 30 and len(completed) < 2:
                print("  - 建议制定更紧凑的学习计划")

    def make_study_plan(self):
        """制定学习计划"""
        print("\n🎯 制定学习计划")
        print("="*60)

        # 当前进度
        completed = sum(1 for p in self.user_data["progress"].values() if p.get("completed"))
        total = len(self.user_data["progress"])

        if completed == 0:
            print("建议学习路径:")
            print("第1周:")
            print("  - 周一/二: 完成练习01（测试用例设计）")
            print("  - 周三/四: 完成练习02（缺陷报告编写）")
            print("  - 周五: 复习前两个练习")
            print("  - 周末: 在实际项目中应用")

            print("\n第2周:")
            print("  - 周一/二: 完成练习03（测试策略设计）")
            print("  - 周三/四: 完成练习04（单元测试框架）")
            print("  - 周五: 整体复习")
            print("  - 周末: 团队分享")

        elif completed < 2:
            print("当前进度较慢，建议:")
            print("  - 每天增加30分钟练习时间")
            print("  - 周末集中完成")
            print("  - 寻找学习伙伴互相监督")

        elif completed < 4:
            print("进度良好，继续加油！")
            print("  - 保持每天练习的习惯")
            print("  - 尝试将练习应用到工作中")
            print("  - 开始记录个人最佳实践")

        else:
            print("恭喜完成所有练习！")
            print("下一步建议:")
            print("  - 深入学习专项测试（性能/安全）")
            print("  - 学习自动化测试框架")
            print("  - 参与开源项目")
            print("  - 培养新人，分享经验")

        # 个性化建议
        if completed > 0:
            print("\n个性化建议:")
            for practice_id, data in self.user_data["progress"].items():
                if not data.get("completed"):
                    print(f"  - 尽快完成 {data['name']}")

    def get_learning_tips(self):
        """获取学习建议"""
        print("\n💡 学习建议")
        print("="*60)

        tips = [
            ("🎯 目标设定", "每天完成一个小目标，积少成多"),
            ("⏰ 时间管理", "使用番茄工作法，25分钟专注 + 5分钟休息"),
            ("📝 主动学习", "先独立思考，再对照答案，形成自己的方法论"),
            ("🔄 实践应用", "将练习应用到实际项目中，加深理解"),
            ("👥 团队交流", "与团队成员分享练习心得，互相学习"),
            ("📊 持续追踪", "记录进度和分数，看到自己的成长"),
            ("💪 刻意练习", "针对薄弱环节重复练习，突破瓶颈"),
            ("🎓 费曼技巧", "用自己的话解释概念，检验掌握程度"),
        ]

        for category, tip in tips:
            print(f"{category}: {tip}")

        print("\n📚 推荐学习顺序:")
        print("  1. 练习01 - 测试用例设计（基础）")
        print("  2. 练习02 - 缺陷报告编写（沟通）")
        print("  3. 练习03 - 测试策略设计（规划）")
        print("  4. 练习04 - 单元测试框架（技术）")

        print("\n⚡ 高效技巧:")
        print("  - 每天固定时间练习（如晚上8点）")
        print("  - 完成后立即记录心得")
        print("  - 每周回顾一次学习成果")
        print("  - 将练习成果分享给团队")

def main():
    """主函数"""
    assistant = PracticeAssistant()

    while True:
        assistant.show_menu()
        choice = input("\n请输入选择 (0-6): ").strip()

        if choice == "1":
            assistant.start_practice()
        elif choice == "2":
            assistant.show_progress()
        elif choice == "3":
            assistant.self_assessment()
        elif choice == "4":
            assistant.generate_report()
        elif choice == "5":
            assistant.make_study_plan()
        elif choice == "6":
            assistant.get_learning_tips()
        elif choice == "0":
            print("\n👋 感谢使用，再见！")
            break
        else:
            print("\n❌ 无效选择，请重新输入")

        if choice != "0":
            input("\n按回车键继续...")

if __name__ == "__main__":
    print("="*60)
    print("🎯 软件测试实践练习助手")
    print("版本: v1.0")
    print("作者: Practice Assistant")
    print("="*60)
    main()
