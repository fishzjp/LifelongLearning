# 环境配置傻瓜式教程

> **15分钟完成** - 从零开始配置软件测试学习环境

---

## 🎯 配置目标

完成后，你将拥有：
- ✅ Python 3.10+ 环境
- ✅ 核心测试框架（pytest, unittest）
- ✅ 开发工具（VS Code + Python插件）
- ✅ 第一个可运行的测试用例

---

## 📋 前置要求

- 操作系统：macOS / Linux / Windows
- 磁盘空间：至少2GB可用空间
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

### Step 2: 安装测试核心库 (5分钟)

```bash
# 创建虚拟环境（推荐）
python3.10 -m venv testing_env
source testing_env/bin/activate  # macOS/Linux
# 或
testing_env\Scripts\activate  # Windows

# 升级pip
pip install --upgrade pip

# 安装核心测试库
pip install pytest==7.4.3
pip install pytest-html==4.1.1
pip install pytest-cov==4.1.0
pip install requests==2.31.0
pip install beautifulsoup4==4.12.2

# 验证安装
python -c "import pytest; import requests; print('✅ 所有库安装成功！')"
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
   - **pytest Copilot** (LittleFoxTeam)
   - **Markdown All in One** (Mads Frøkier)
   - **GitLens** (GitKraken)

### Step 4: 配置pytest (2分钟)

```bash
# 创建pytest配置文件
cat > pytest.ini << 'EOF'
[pytest]
minversion = 7.0
addopts =
    -v
    --strict-markers
    --tb=short
    --cov=.
    --cov-report=html
    --cov-report=term-missing
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests
EOF

# 创建测试目录结构
mkdir -p tests
touch tests/__init__.py
```

### Step 5: 验证环境 (2分钟)

创建测试文件 `test_env.py`:

```python
import pytest
import sys

def test_python_version():
    """验证Python版本"""
    version = sys.version_info
    assert version.major == 3
    assert version.minor >= 10, f"需要Python 3.10+，当前为{version.major}.{version.minor}"

def test_pytest_installed():
    """验证pytest安装"""
    import pytest
    assert pytest.__version__
    print(f"✅ pytest版本: {pytest.__version__}")

def test_first_test():
    """第一个测试：验证环境基本功能"""
    assert 1 + 1 == 2
    assert "hello" == "hello"
    print("✅ 基础测试功能正常")

def test_requests_installed():
    """验证requests安装"""
    try:
        import requests
        print(f"✅ requests版本: {requests.__version__}")
    except ImportError:
        pytest.fail("requests未安装")

if __name__ == "__main__":
    print("=== 环境验证 ===\n")
    test_python_version()
    test_pytest_installed()
    test_first_test()
    test_requests_installed()
    print("\n🎉 环境配置成功！可以开始学习软件测试了！")
```

运行测试：
```bash
pytest test_env.py -v -s
```

---

## 🔧 常见问题

### Q1: pip安装速度慢？

**A**: 使用国内镜像源

```bash
# 临时使用
pip install pytest -i https://pypi.tuna.tsinghua.edu.cn/simple

# 永久配置
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q2: pytest安装失败？

**A**: 尝试conda安装

```bash
# 安装Miniconda
# macOS/Linux
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh
bash Miniconda3-latest-MacOSX-arm64.sh

# 创建环境
conda create -n testing python=3.10
conda activate testing
conda install pytest
```

### Q3: 权限错误？

**A**: 使用虚拟环境或sudo

```bash
# 推荐：使用虚拟环境（无需sudo）
python3.10 -m venv testing_env
source testing_env/bin/activate

# 或使用--user参数
pip install --user pytest

# 或使用sudo（不推荐）
sudo pip install pytest
```

### Q4: Python版本过低？

**A**: 升级Python或使用pyenv

```bash
# macOS/Linux使用pyenv
brew install pyenv
pyenv install 3.10.13
pyenv global 3.10.13
```

### Q5: pytest命令找不到？

**A**: 检查PATH或使用python -m

```bash
# 使用python模块方式
python -m pytest --version

# 或确保虚拟环境已激活
source testing_env/bin/activate  # macOS/Linux
testing_env\Scripts\activate  # Windows
```

---

## 📦 已安装的库及其用途

| 库 | 版本 | 用途 |
|----|------|------|
| pytest | 7.4.3 | 测试框架，提供强大的测试功能 |
| pytest-html | 4.1.1 | 生成HTML测试报告 |
| pytest-cov | 4.1.0 | 代码覆盖率测试 |
| requests | 2.31.0 | HTTP库，用于接口测试 |
| beautifulsoup4 | 4.12.2 | HTML/XML解析，用于Web测试 |

---

## ✅ 配置完成检查清单

- [ ] Python 3.10+ 已安装
- [ ] 虚拟环境已创建并激活
- [ ] pytest、pytest-html、pytest-cov 已安装
- [ ] VS Code 已安装
- [ ] Python插件已安装
- [ ] pytest.ini 配置文件已创建
- [ ] 测试脚本运行成功

---

## 🚀 下一步

环境配置完成后，建议学习顺序：

1. **Hello World**: [运行第一个测试](../tutorials/hello-world.md)
2. **基础概念**: [学习软件测试基础概念](../../01-软件测试基础概念.md)
3. **测试方法**: [学习黑盒测试方法](../../05-黑盒测试方法.md)
4. **实战练习**: [完成实践练习](../../实践练习/练习01-测试用例设计.md)

---

## 💡 优化建议

### 提升测试效率

```bash
# 安装有用的pytest插件
pip install pytest-xdist  # 并行测试
pip install pytest-timeout  # 超时控制
pip install pytest-rerunfailures  # 失败重试
```

### 方便开发

```bash
# 安装代码质量工具
pip install black  # 代码格式化
pip install flake8  # 代码检查
pip install mypy  # 类型检查
```

---

## 📞 获取帮助

如果遇到问题：

1. 查看上面的常见问题
2. 搜索错误信息
3. 查看官方文档：
   - [Python官方文档](https://docs.python.org/)
   - [pytest文档](https://docs.pytest.org/)
   - [requests文档](https://docs.python-requests.org/)

---

**配置完成！** 🎉

现在可以开始你的软件测试学习之旅了！

---

**更新**: 2025-01-13
**适用于**: Python 3.10+, macOS/Linux/Windows
