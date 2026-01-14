# 环境配置傻瓜式教程

> **15分钟完成** - 从零开始配置计算机视觉学习环境

---

## 🎯 配置目标

完成后，你将拥有：
- ✅ Python 3.10+ 环境
- ✅ 核心CV库（OpenCV, PyTorch, NumPy等）
- ✅ 开发工具（VS Code + Python插件）
- ✅ 第一个可运行的示例

---

## 📋 前置要求

- 操作系统：macOS / Linux / Windows
- 磁盘空间：至少5GB可用空间
- 网络：能够访问互联网

---

## 🚀 快速配置（15分钟）

### Step 1: 安装Python (3分钟)

#### macOS

```bash
# 使用Homebrew安装
brew install python@3.10

# 验证安装
python3.10 --version
```

#### Windows

1. 访问 https://www.python.org/downloads/
2. 下载 Python 3.10+ 安装包
3. 运行安装程序，**务必勾选"Add Python to PATH"**
4. 验证：打开命令提示符，输入 `python --version`

#### Linux

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.10 python3-pip python3-venv

# 验证
python3.10 --version
```

### Step 2: 安装CV核心库 (5分钟)

```bash
# 创建虚拟环境（推荐）
python3.10 -m venv cv_env
source cv_env/bin/activate  # macOS/Linux
# 或
cv_env\Scripts\activate  # Windows

# 升级pip
pip install --upgrade pip

# 安装核心库
pip install numpy==1.24.3
pip install opencv-python==4.8.1.78
pip install torch==2.0.1
pip install torchvision==0.15.2
pip install matplotlib==3.7.2
pip install jupyter==1.0.0

# 验证安装
python -c "import cv2; import torch; import numpy; print('✅ 所有库安装成功！')"
```

**预期输出**:
```
✅ 所有库安装成功！
```

### Step 3: 安装VS Code和插件 (3分钟)

#### 安装VS Code

1. 访问 https://code.visualstudio.com/
2. 下载并安装适合你系统的版本
3. 打开VS Code

#### 安装Python插件

1. 打开VS Code
2. 按 `Cmd+Shift+X` (Mac/Linux) 或 `Ctrl+Shift+X` (Windows)
3. 搜索并安装以下插件：
   - **Python** (Microsoft)
   - **Jupyter** (Microsoft)
   - **Markdown All in One** (Mads Frøkier)
   - **Mermaid Preview** (bierner)

### Step 4: 配置Jupyter (2分钟)

```bash
# 安装Jupyter支持
pip install jupyterlab notebook ipykernel

# 注册Python内核
python -m ipykernel install --user --name=cv

# 启动Jupyter
jupyter notebook

# 浏览器会自动打开
```

### Step 5: 验证环境 (2分钟)

创建测试文件 `test_env.py`:

```python
import numpy as np
import cv2
import torch
import matplotlib.pyplot as plt

print("=== 环境验证 ===\n")

# 检查NumPy
print(f"✅ NumPy: {np.__version__}")

# 检查OpenCV
print(f"✅ OpenCV: {cv2.__version__}")

# 检查PyTorch
print(f"✅ PyTorch: {torch.__version__}")
print(f"   CUDA可用: {torch.cuda.is_available()}")

# 创建测试图像
img = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)

# 测试OpenCV
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print(f"✅ OpenCV转换测试通过: {gray.shape}")

# 测试PyTorch
tensor = torch.from_numpy(img).permute(2, 0, 1).unsqueeze(0).float() / 255.0
print(f"✅ PyTorch张量测试通过: {tensor.shape}")

print("\n🎉 环境配置成功！可以开始学习计算机视觉了！")
```

运行测试：
```bash
python test_env.py
```

---

## 🔧 常见问题

### Q1: pip安装速度慢？

**A**: 使用国内镜像源

```bash
# 临时使用
pip install numpy -i https://pypi.tuna.tsinghua.edu.cn/simple

# 永久配置
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q2: OpenCV安装失败？

**A**: 尝试conda安装

```bash
# 安装Miniconda
# macOS/Linux
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh
bash Miniconda3-latest-MacOSX-arm64.sh

# 创建环境
conda create -n cv python=3.10
conda activate cv
conda install -c conda-forge opencv
```

### Q3: PyTorch安装失败？

**A**: 根据系统选择合适的安装命令

访问 https://pytorch.org/get-started/locally/
选择你的系统配置，获取安装命令

### Q4: 权限错误？

**A**: 使用虚拟环境或sudo

```bash
# 推荐：使用虚拟环境（无需sudo）
python3.10 -m venv cv_env
source cv_env/bin/activate

# 或使用sudo（不推荐）
sudo pip install numpy
```

---

## 📦 已安装的库及其用途

| 库 | 版本 | 用途 |
|----|------|------|
| NumPy | 1.24.3 | 数组运算、图像数据处理 |
| OpenCV | 4.8.1 | 图像读取、处理、显示 |
| PyTorch | 2.0.1 | 深度学习框架 |
| Matplotlib | 3.7.2 | 可视化、绘图 |
| Jupyter | 1.0.0 | 交互式开发环境 |

---

## ✅ 配置完成检查清单

- [ ] Python 3.10+ 已安装
- [ ] 虚拟环境已创建并激活
- [ ] NumPy、OpenCV、PyTorch 已安装
- [ ] VS Code 已安装
- [ ] Python插件已安装
- [ ] Jupyter 已配置
- [ ] 测试脚本运行成功

---

## 🚀 下一步

环境配置完成后，建议学习顺序：

1. **Hello World**: [运行第一个示例](tutorials/hello-world.md)
2. **基础概念**: [学习NumPy和图像基础](../01-基础概念/README.md)
3. **图像处理**: [学习OpenCV基础操作](../02-图像处理基础/README.md)
4. **深度学习**: [学习神经网络和CNN](../04-深度学习基础/README.md)

---

## 💡 优化建议

### 提升性能

```bash
# 如果有NVIDIA GPU，安装GPU版本的PyTorch
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### 方便开发

```bash
# 安装常用工具
pip install jupyterlab  # 更好的Jupyter界面
pip install ipywidgets  # Jupyter交互组件
pip install tqdm  # 进度条
pip install pillow  # 图像IO增强
```

---

## 📞 获取帮助

如果遇到问题：

1. 查看上面的常见问题
2. 搜索错误信息
3. 查看官方文档：
   - [Python官方文档](https://docs.python.org/)
   - [NumPy文档](https://numpy.org/doc/)
   - [OpenCV文档](https://docs.opencv.org/)
   - [PyTorch文档](https://pytorch.org/docs/stable/)

---

**配置完成！** 🎉

现在可以开始你的计算机视觉学习之旅了！

---

**更新**: 2025-01-13
**适用于**: Python 3.10+, macOS/Linux/Windows
