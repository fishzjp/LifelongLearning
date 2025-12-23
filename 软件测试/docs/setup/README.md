# 🚀 环境配置指南（傻瓜式）

> ⏱️ **预计时间**：15分钟
> 🎯 **目标**：让零基础新人也能快速配置好测试环境

---

## 📋 你将获得什么？

完成本指南后，你将拥有：
- ✅ Python 3.10+ 开发环境
- ✅ 核心测试框架（pytest, selenium等）
- ✅ 第一个可运行的测试用例
- ✅ 验证环境是否配置成功

---

## 🎯 为什么需要配置环境？

### 解决的痛点
| 痛点场景 | 影响 | 本指南解决方案 |
|---------|------|---------------|
| 不知道安装什么工具 | 浪费时间搜索，安装错误版本 | 一键安装所有必需工具 |
| 安装后不知道是否成功 | 运行测试时才发现问题 | 提供验证步骤，立即确认 |
| 遇到安装错误无从下手 | 卡在第一步，丧失学习动力 | 提供常见问题解决方案 |

### 长期价值
- **项目层面**：标准化环境，团队协作无障碍
- **个人层面**：一次配置，长期使用，提升效率

---

## 📦 第一步：安装Python

### Windows用户

#### 1. 下载Python
访问 [python.org/downloads](https://www.python.org/downloads/)，下载 **Python 3.10 或 3.11**（推荐）

#### 2. 关键：安装时必须勾选
```
☑️ Add Python to PATH  ← 必须勾选！
☑️ Install pip
☑️ Install for all users
```

#### 3. 验证安装
打开命令提示符（Win+R，输入cmd），运行：
```bash
python --version
```
应该显示：`Python 3.10.x` 或 `Python 3.11.x`

如果显示"不是内部命令"，说明**没有勾选Add to PATH**，请重新安装。

---

### macOS用户

#### 1. 检查是否已安装
打开终端（Terminal），运行：
```bash
python3 --version
```

如果显示版本号（如 `Python 3.10.x`），跳到第二步。

#### 2. 如果未安装
```bash
# 方法1：使用Homebrew（推荐）
brew install python3

# 方法2：从官网下载安装包
# 访问 https://www.python.org/downloads/macos/
```

#### 3. 验证安装
```bash
python3 --version
pip3 --version
```

---

### Linux用户（Ubuntu/Debian）

```bash
# 更新包管理器
sudo apt update

# 安装Python3和pip
sudo apt install python3 python3-pip python3-venv

# 验证
python3 --version
pip3 --version
```

---

## 🔧 第二步：安装测试工具

### 方式一：一键安装（推荐）

在项目根目录（`/Users/fish/code/学习资料/软件测试`）运行：

```bash
# 创建requirements.txt文件（如果还没有）
cat > requirements.txt << 'EOF'
pytest==7.4.3
pytest-html==4.1.1
selenium==4.15.2
requests==2.31.0
beautifulsoup4==4.12.2
pandas==2.1.3
openpyxl==3.1.2
EOF

# 一键安装所有工具
pip install -r requirements.txt
```

### 方式二：手动逐个安装

如果不想一次性安装所有工具，可以按需安装：

```bash
# 基础测试框架（必装）
pip install pytest pytest-html

# Web自动化（做UI测试时需要）
pip install selenium

# 接口测试（做接口测试时需要）
pip install requests beautifulsoup4

# 数据处理（做数据驱动测试时需要）
pip install pandas openpyxl
```

### 方式三：使用国内镜像（加速）

如果安装速度慢，使用国内镜像源：

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## ✅ 第三步：验证环境

### 创建验证文件

在项目根目录创建 `test_verify_env.py`：

```python
"""
环境验证脚本
运行：pytest test_verify_env.py -v
"""

def test_python_version():
    """验证Python版本"""
    import sys
    version = sys.version_info
    assert version.major == 3
    assert version.minor >= 10, f"需要Python 3.10+，当前为{version.major}.{version.minor}"
    print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")

def test_pytest_installed():
    """验证pytest安装"""
    try:
        import pytest
        print(f"✅ pytest版本: {pytest.__version__}")
    except ImportError:
        raise AssertionError("pytest未安装，请运行: pip install pytest")

def test_selenium_installed():
    """验证selenium安装（可选）"""
    try:
        import selenium
        print(f"✅ selenium版本: {selenium.__version__}")
    except ImportError:
        print("⚠️  selenium未安装（仅在做UI测试时需要）")

def test_requests_installed():
    """验证requests安装（可选）"""
    try:
        import requests
        print(f"✅ requests版本: {requests.__version__}")
    except ImportError:
        print("⚠️  requests未安装（仅在做接口测试时需要）")

def test_first_test():
    """第一个测试：验证环境基本功能"""
    assert 1 + 1 == 2
    assert "hello" == "hello"
    print("✅ 基础测试功能正常")

def test_file_system():
    """验证文件系统权限"""
    import os
    current_dir = os.getcwd()
    assert os.access(current_dir, os.W_OK), "当前目录没有写权限"
    print(f"✅ 文件系统正常: {current_dir}")

if __name__ == "__main__":
    # 直接运行时的输出
    print("=" * 60)
    print("环境验证测试")
    print("=" * 60)
    test_python_version()
    test_pytest_installed()
    test_selenium_installed()
    test_requests_installed()
    test_first_test()
    test_file_system()
    print("=" * 60)
    print("🎉 所有验证通过！环境配置成功！")
    print("=" * 60)
```

### 运行验证

```bash
# 方法1：使用pytest运行（推荐）
pytest test_verify_env.py -v

# 方法2：直接运行Python脚本
python test_verify_env.py
```

### 预期输出

```
============================= test session starts ==============================
collected 5 items

test_verify_env.py::test_python_version PASSED                         [ 20%]
✅ Python版本: 3.10.x
test_verify_env.py::test_pytest_installed PASSED                       [ 40%]
✅ pytest版本: 7.4.3
test_verify_env.py::test_selenium_installed PASSED                     [ 60%]
✅ selenium版本: 4.15.2
test_verify_env.py::test_requests_installed PASSED                     [ 80%]
✅ requests版本: 2.31.0
test_verify_env.py::test_first_test PASSED                             [100%]
✅ 基础测试功能正常

============================== 5 passed in 0.01s ===============================
🎉 所有验证通过！环境配置成功！
```

---

## 🆘 常见问题与解决方案

### Q1: `pip` 命令找不到

**症状**：
```bash
pip: command not found
# 或
'pip' 不是内部或外部命令
```

**解决方案**：
```bash
# Windows
python -m pip --version

# macOS/Linux
python3 -m pip --version

# 如果以上命令正常，使用以下方式安装
python -m pip install pytest
```

---

### Q2: 安装超时或失败

**症状**：
```bash
WARNING: Retrying (5(total): Download failed...
ERROR: Could not install packages due to an EnvironmentError
```

**解决方案**：
```bash
# 使用国内镜像（清华大学源）
pip install pytest -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或使用阿里源
pip install pytest -i https://mirrors.aliyun.com/pypi/simple/

# 永久配置镜像源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

---

### Q3: 版本冲突

**症状**：
```bash
ERROR: Cannot install -r requirements.txt (line 1) because these package versions have conflicting dependencies.
```

**解决方案**：
```bash
# 方法1：创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 然后在虚拟环境中安装
pip install -r requirements.txt

# 方法2：逐个安装，找到冲突的包
pip install pytest
pip install selenium
# ...
```

---

### Q4: Python版本过低

**症状**：
```bash
ERROR: Package 'pytest' requires a different Python: 3.8.10 not in '>=3.9'
```

**解决方案**：
- 卸载旧版本，安装Python 3.10+
- 或使用pyenv管理多版本Python

---

### Q5: 权限问题（Linux/macOS）

**症状**：
```bash
ERROR: Could not install packages due to an EnvironmentError: [Errno 13] Permission denied
```

**解决方案**：
```bash
# 方法1：使用--user参数
pip install --user pytest

# 方法2：使用sudo（不推荐）
sudo pip install pytest

# 方法3：使用虚拟环境（最佳）
python -m venv venv
source venv/bin/activate
pip install pytest
```

---

### Q6: 验证测试失败

**症状**：
```bash
FAILED test_verify_env.py::test_python_version - AssertionError: 需要Python 3.10+
```

**解决方案**：
1. 检查Python版本：`python --version`
2. 如果版本过低，升级Python
3. 如果系统有多个Python版本，确保使用正确的：
   ```bash
   # Windows
   python3.10 -m pytest test_verify_env.py

   # macOS/Linux
   python3.10 -m pytest test_verify_env.py
   ```

---

## 🎯 下一步：Hello World测试

环境配置完成后，立即开始你的第一个测试！

### 快速开始

```bash
# 1. 创建Hello World测试文件
cat > test_hello.py << 'EOF'
def test_hello_world():
    """我的第一个测试"""
    assert 1 + 1 == 2
    print("🎉 测试通过！")

def test_login_demo():
    """模拟登录测试"""
    def login(username, password):
        if username == "admin" and password == "123456":
            return {"success": True}
        return {"success": False}

    # 测试成功登录
    result = login("admin", "123456")
    assert result["success"] == True

    # 测试失败登录
    result = login("admin", "wrong")
    assert result["success"] == False
EOF

# 2. 运行测试
pytest test_hello.py -v -s

# 3. 看到输出
# ============================= test session starts ==============================
# collected 2 items
#
# test_hello.py::test_hello_world PASSED                                 [ 50%]
# 🎉 测试通过！
# test_hello.py::test_login_demo PASSED                                  [100%]
#
# =============================== 2 passed in 0.01s ===============================
```

---

## 📚 完整学习路径

完成环境配置后，按以下顺序学习：

1. **立即**：[Hello World教程](../tutorials/hello-world.md) - 5分钟
2. **今天**：[术语表](../glossary.md) - 遇到不懂就查
3. **明天**：[基础概念](../../01-软件测试基础概念.md) - 2小时
4. **本周**：[练习01](../../实践练习/练习01-测试用例设计.md) - 实践应用

---

## 💡 环境维护建议

### 定期更新工具
```bash
# 每月更新一次
pip list --outdated
pip install --upgrade pytest selenium requests
```

### 备份环境
```bash
# 导出当前环境
pip freeze > requirements.txt

# 下次在新机器上直接安装
pip install -r requirements.txt
```

### 清理环境
```bash
# 如果需要重新开始
pip uninstall -r requirements.txt
# 然后重新安装
```

---

## 🎉 恭喜！

你已经成功配置了测试环境！现在可以开始学习软件测试了。

**记住**：如果遇到任何问题，先查看这里的常见问题，如果还不能解决，随时回来查阅！

---

**下一步**：[Hello World快速上手](../tutorials/hello-world.md)

**返回目录**：[README](../../README.md)

**环境配置版本**：v1.0
**最后更新**：2025-01-01
