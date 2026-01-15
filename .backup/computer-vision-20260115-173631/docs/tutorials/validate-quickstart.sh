#!/bin/bash

# 快速开始流程验证脚本
# 验证新学习者能否在15分钟内完成环境配置并运行第一个示例

echo "=========================================="
echo "🎯 计算机视觉学习环境 - 快速开始验证"
echo "=========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 计数器
PASS=0
FAIL=0
WARN=0

# 检查函数
check_pass() {
    echo -e "${GREEN}✅ $1${NC}"
    ((PASS++))
}

check_fail() {
    echo -e "${RED}❌ $1${NC}"
    ((FAIL++))
}

check_warn() {
    echo -e "${YELLOW}⚠️  $1${NC}"
    ((WARN++))
}

echo "📋 第一步: 检查Python环境"
echo "-------------------------------------------"

# 检查Python版本
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

    echo "发现Python版本: $PYTHON_VERSION"

    if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 10 ]; then
        check_pass "Python版本符合要求 (>= 3.10)"
    else
        check_warn "Python版本偏低，建议升级到3.10+"
    fi
else
    check_fail "未找到Python3，请先安装Python 3.10+"
    echo ""
    echo "安装方法:"
    echo "  macOS:   brew install python@3.10"
    echo "  Ubuntu:  sudo apt install python3.10"
    echo "  Windows: https://www.python.org/downloads/"
    echo ""
    exit 1
fi

echo ""
echo "📚 第二步: 检查核心库安装"
echo "-------------------------------------------"

# 检查NumPy
if python3 -c "import numpy; print('NumPy:', numpy.__version__)" 2>/dev/null; then
    NUMPY_VERSION=$(python3 -c "import numpy; print(numpy.__version__)" 2>/dev/null)
    check_pass "NumPy已安装 (版本: $NUMPY_VERSION)"
else
    check_fail "NumPy未安装"
    echo "  安装命令: pip install numpy==1.24.3"
fi

# 检查OpenCV
if python3 -c "import cv2; print('OpenCV:', cv2.__version__)" 2>/dev/null; then
    OPENCV_VERSION=$(python3 -c "import cv2; print(cv2.__version__)" 2>/dev/null)
    check_pass "OpenCV已安装 (版本: $OPENCV_VERSION)"
else
    check_fail "OpenCV未安装"
    echo "  安装命令: pip install opencv-python==4.8.1.78"
fi

# 检查PyTorch
if python3 -c "import torch; print('PyTorch:', torch.__version__)" 2>/dev/null; then
    PYTORCH_VERSION=$(python3 -c "import torch; print(torch.__version__)" 2>/dev/null)
    check_pass "PyTorch已安装 (版本: $PYTORCH_VERSION)"

    # 检查CUDA
    if python3 -c "import torch; exit(0 if torch.cuda.is_available() else 1)" 2>/dev/null; then
        CUDA_VERSION=$(python3 -c "import torch; print(torch.version.cuda)" 2>/dev/null)
        check_pass "CUDA可用 (版本: $CUDA_VERSION)"
    else
        echo "  ℹ️  CUDA不可用（CPU模式足够学习使用）"
    fi
else
    check_fail "PyTorch未安装"
    echo "  安装命令: pip install torch==2.0.1"
fi

# 检查Matplotlib
if python3 -c "import matplotlib; print('Matplotlib:', matplotlib.__version__)" 2>/dev/null; then
    MATPLOTLIB_VERSION=$(python3 -c "import matplotlib; print(matplotlib.__version__)" 2>/dev/null)
    check_pass "Matplotlib已安装 (版本: $MATPLOTLIB_VERSION)"
else
    check_fail "Matplotlib未安装"
    echo "  安装命令: pip install matplotlib==3.7.2"
fi

# 检查Jupyter
if command -v jupyter &> /dev/null; then
    JUPYTER_VERSION=$(jupyter --version 2>&1 | head -n 1)
    check_pass "Jupyter已安装 ($JUPYTER_VERSION)"
else
    check_warn "Jupyter未安装（可选）"
    echo "  安装命令: pip install jupyter"
fi

echo ""
echo "📁 第三步: 检查文档结构"
echo "-------------------------------------------"

# 检查关键文档
DOCS=(
    "计算机视觉/docs/setup/README.md"
    "计算机视觉/docs/tutorials/hello-world.md"
    "计算机视觉/docs/glossary/README.md"
    "计算机视觉/docs/progress/README.md"
)

for doc in "${DOCS[@]}"; do
    if [ -f "$doc" ]; then
        check_pass "文档存在: $doc"
    else
        check_fail "文档缺失: $doc"
    fi
done

echo ""
echo "🧪 第四步: 运行Hello World测试"
echo "-------------------------------------------"

# 创建测试目录
TEST_DIR="cv_quickstart_test"
mkdir -p "$TEST_DIR"
cd "$TEST_DIR" || exit 1

# 创建测试图像
cat > create_test_image.py << 'EOF'
import numpy as np
import cv2

# 创建测试图像
img = np.zeros((100, 100, 3), dtype=np.uint8)
img[:, :50, 2] = 255  # 红色通道
img[:, 50:, 0] = 255  # 蓝色通道
cv2.imwrite('test_image.jpg', img)
print("✅ 测试图像已创建")
EOF

if python3 create_test_image.py 2>/dev/null; then
    check_pass "测试图像创建成功"
else
    check_fail "测试图像创建失败"
fi

# 创建Hello World测试
cat > test_hello_world.py << 'EOF'
import cv2
import numpy as np
import sys

try:
    # 1. 读取图像
    img = cv2.imread('test_image.jpg')
    assert img is not None, "无法读取图像"
    assert img.shape == (100, 100, 3), f"图像形状错误: {img.shape}"
    print("✅ 1. 图像读取成功: ", img.shape)

    # 2. 转换灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    assert gray.shape == (100, 100), f"灰度图形状错误: {gray.shape}"
    print("✅ 2. 灰度转换成功: ", gray.shape)

    # 3. 调整尺寸
    resized = cv2.resize(img, (200, 200))
    assert resized.shape == (200, 200, 3), f"调整后形状错误: {resized.shape}"
    print("✅ 3. 尺寸调整成功: ", resized.shape)

    # 4. 保存图像
    cv2.imwrite('gray_test.jpg', gray)
    cv2.imwrite('resized_test.jpg', resized)
    print("✅ 4. 图像保存成功")

    print("\n🎉 所有测试通过！环境配置正确。")
    sys.exit(0)

except Exception as e:
    print(f"\n❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
EOF

if python3 test_hello_world.py 2>/dev/null; then
    check_pass "Hello World测试通过"
else
    check_fail "Hello World测试失败"
fi

# 返回上级目录
cd ..

echo ""
echo "📊 验证结果汇总"
echo "=========================================="
echo -e "${GREEN}✅ 通过: $PASS${NC}"
echo -e "${YELLOW}⚠️  警告: $WARN${NC}"
echo -e "${RED}❌ 失败: $FAIL${NC}"
echo ""

# 清理测试目录
echo "🧹 清理测试文件..."
rm -rf "$TEST_DIR"

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}🎉 恭喜！快速开始验证通过！${NC}"
    echo ""
    echo "你现在可以："
    echo "  1. 阅读 [环境配置教程](计算机视觉/docs/setup/README.md)"
    echo "  2. 运行 [Hello World示例](计算机视觉/docs/tutorials/hello-world.md)"
    echo "  3. 查看 [学习路径](计算机视觉/README.md#3分钟快速定位)"
    echo ""
    echo "下一步建议："
    echo "  → 开始学习 [01-基础概念](计算机视觉/01-基础概念/README.md)"
    echo ""
    exit 0
else
    echo -e "${RED}❌ 验证未通过，请先解决上述问题${NC}"
    echo ""
    echo "解决方案："
    echo "  1. 查看 [环境配置教程](计算机视觉/docs/setup/README.md) 的详细说明"
    echo "  2. 运行以下命令安装缺失的库："
    echo ""
    echo "     pip install numpy==1.24.3"
    echo "     pip install opencv-python==4.8.1.78"
    echo "     pip install torch==2.0.1"
    echo "     pip install matplotlib==3.7.2"
    echo ""
    echo "  3. 重新运行此验证脚本"
    echo ""
    exit 1
fi
