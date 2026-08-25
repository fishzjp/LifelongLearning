#!/bin/bash

# 实践练习进度追踪脚本

echo "=========================================="
echo "🎯 软件测试实践练习进度追踪"
echo "=========================================="

# 检查是否在正确的目录
if [ ! -f "README.md" ]; then
    echo "❌ 请在实践练习目录下运行此脚本"
    exit 1
fi

# 创建进度文件
PROGRESS_FILE="my_progress.md"

if [ ! -f "$PROGRESS_FILE" ]; then
    cat > "$PROGRESS_FILE" << 'EOF'
# 我的练习进度

## 基础阶段
- [ ] 练习01: 测试用例设计
  - 完成时间: ______
  - 自评分数: ______
  - 收获总结: ______

- [ ] 练习02: 缺陷报告编写
  - 完成时间: ______
  - 自评分数: ______
  - 收获总结: ______

## 进阶阶段
- [ ] 练习03: 测试策略设计
  - 完成时间: ______
  - 自评分数: ______
  - 收获总结: ______

- [ ] 练习04: 单元测试框架
  - 完成时间: ______
  - 自评分数: ______
  - 收获总结: ______

## 实战应用
- [ ] 在真实项目中应用
- [ ] 分享给团队成员
- [ ] 编写个人最佳实践

## 学习记录

| 日期 | 练习 | 用时 | 分数 | 收获 |
|------|------|------|------|------|
|      |      |      |      |      |
|      |      |      |      |      |
|      |      |      |      |      |

## 本周计划
- [ ] ______
- [ ] ______
- [ ] ______

## 总结反思
______

EOF
    echo "✅ 已创建进度文件: $PROGRESS_FILE"
fi

echo ""
echo "请选择操作："
echo "1. 查看当前进度"
echo "2. 记录完成练习"
echo "3. 查看练习说明"
echo "4. 启动练习助手 (Python)"
echo "0. 退出"

read -p "请输入选择 (0-4): " choice

case $choice in
    1)
        echo ""
        echo "📊 当前进度："
        cat "$PROGRESS_FILE"
        ;;
    2)
        echo ""
        echo "📝 记录完成练习"
        echo "请选择练习："
        echo "1. 练习01 - 测试用例设计"
        echo "2. 练习02 - 缺陷报告编写"
        echo "3. 练习03 - 测试策略设计"
        echo "4. 练习04 - 单元测试框架"
        read -p "请输入选择 (1-4): " practice

        case $practice in
            1) name="练习01: 测试用例设计" ;;
            2) name="练习02: 缺陷报告编写" ;;
            3) name="练习03: 测试策略设计" ;;
            4) name="练习04: 单元测试框架" ;;
            *) echo "无效选择"; exit 1 ;;
        esac

        read -p "请输入完成时间 (YYYY-MM-DD): " date
        read -p "请输入自评分数 (0-100): " score
        read -p "请输入收获总结: " summary

        # 更新进度文件
        sed -i "s/- \\[ \\] $name/- \\[x\\] $name/" "$PROGRESS_FILE"
        sed -i "/$name/{n;s/完成时间: ______/完成时间: $date/}" "$PROGRESS_FILE"
        sed -i "/$name/{n;n;s/自评分数: ______/自评分数: $score/}" "$PROGRESS_FILE"
        sed -i "/$name/{n;n;n;s/收获总结: ______/收获总结: $summary/}" "$PROGRESS_FILE"

        # 添加到记录表
        echo "| $date | $name | - | $score | $summary |" >> "$PROGRESS_FILE"

        echo "✅ 记录完成！"
        ;;
    3)
        echo ""
        echo "📚 练习说明："
        echo "练习01: 测试用例设计 - 掌握等价类、边界值、场景法"
        echo "练习02: 缺陷报告编写 - 掌握缺陷分析、根因分析"
        echo "练习03: 测试策略设计 - 掌握测试金字塔、风险管理"
        echo "练习04: 单元测试框架 - 掌握TDD、Mock、并发测试"
        echo ""
        echo "建议学习路径："
        echo "  初学者：练习01 → 练习02 → 实战应用"
        echo "  进阶者：练习03 → 练习04 → 团队分享"
        ;;
    4)
        if command -v python3 &> /dev/null || command -v python &> /dev/null; then
            echo "启动练习助手..."
            python3 practice_assistant.py 2>/dev/null || python practice_assistant.py
        else
            echo "❌ 未找到Python，请安装后使用"
        fi
        ;;
    0)
        echo "👋 再见！"
        exit 0
        ;;
    *)
        echo "❌ 无效选择"
        ;;
esac

echo ""
echo "💡 提示：你也可以手动编辑 $PROGRESS_FILE 来记录进度"
