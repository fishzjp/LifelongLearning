# Hello World - 你的第一个测试程序

> **5分钟完成** - 从零开始运行第一个测试程序

---

## 🎯 学习目标

通过这个教程，你将：
- ✅ 编写第一个测试用例
- ✅ 理解测试的基本结构
- ✅ 运行并查看测试结果
- ✅ 掌握pytest的基本用法
- ✅ 学习断言（assert）的使用

**难度**: ⭐☆☆☆☆ (入门)
**预计时间**: 5-10分钟
**前置知识**: Python基础，已完成环境配置

---

## 📖 准备工作

### 1. 确保环境已配置

如果你还没有配置环境，请先完成[环境配置](../setup/README.md)

```bash
# 验证环境
python -c "import pytest; print('✅ 环境配置成功！')"
```

### 2. 创建测试目录

```bash
# 创建测试目录
mkdir -p tests
cd tests

# 创建__init__.py文件
touch __init__.py
```

---

## 🚀 Hello World程序

### 完整代码

创建文件 `tests/test_hello_world.py`：

```python
"""
软件测试 Hello World
这是你的第一个测试程序
"""

import pytest


def test_hello_world():
    """我的第一个测试：验证1+1=2"""
    # assert 是测试的核心：断言某个条件必须为真
    assert 1 + 1 == 2
    print("✅ 测试通过！")


def test_string_operations():
    """测试字符串操作"""
    # 测试字符串拼接
    assert "hello" + " " + "world" == "hello world"

    # 测试字符串重复
    assert "ha" * 3 == "hahahaha"

    # 测试字符串大小写转换
    assert "hello".upper() == "HELLO"
    assert "WORLD".lower() == "world"


def test_list_operations():
    """测试列表操作"""
    # 测试列表创建
    numbers = [1, 2, 3, 4, 5]

    # 测试列表长度
    assert len(numbers) == 5

    # 测试列表元素访问
    assert numbers[0] == 1
    assert numbers[-1] == 5

    # 测试列表切片
    assert numbers[1:3] == [2, 3]


def test_calculator():
    """测试简单计算器功能"""
    def add(a, b):
        """加法函数"""
        return a + b

    def subtract(a, b):
        """减法函数"""
        return a - b

    def multiply(a, b):
        """乘法函数"""
        return a * b

    # 测试加法
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

    # 测试减法
    assert subtract(5, 3) == 2
    assert subtract(10, 5) == 5

    # 测试乘法
    assert multiply(2, 3) == 6
    assert multiply(-2, 3) == -6


def test_login_function():
    """测试登录功能"""
    def login(username, password):
        """模拟登录验证函数"""
        if username == "admin" and password == "123456":
            return {"success": True, "message": "登录成功"}
        elif username == "" or password == "":
            return {"success": False, "message": "用户名或密码不能为空"}
        else:
            return {"success": False, "message": "用户名或密码错误"}

    # 测试用例1：正确登录
    result = login("admin", "123456")
    assert result["success"] == True
    assert result["message"] == "登录成功"

    # 测试用例2：错误密码
    result = login("admin", "wrongpass")
    assert result["success"] == False
    assert "错误" in result["message"]

    # 测试用例3：空用户名
    result = login("", "123456")
    assert result["success"] == False
    assert "不能为空" in result["message"]

    # 测试用例4：空密码
    result = login("admin", "")
    assert result["success"] == False
    assert "不能为空" in result["message"]


def test_edge_cases():
    """测试边界情况"""
    # 测试除零错误
    def divide(a, b):
        if b == 0:
            raise ValueError("除数不能为零")
        return a / b

    # 正常情况
    assert divide(10, 2) == 5

    # 测试异常
    with pytest.raises(ValueError) as excinfo:
        divide(10, 0)
    assert "除数不能为零" in str(excinfo.value)

    # 测试空列表
    empty_list = []
    assert len(empty_list) == 0
    assert not empty_list  # 空列表为False

    # 测试None值
    def process_data(data):
        if data is None:
            return "no data"
        return f"processed: {data}"

    assert process_data(None) == "no data"
    assert process_data("test") == "processed: test"


if __name__ == "__main__":
    # 可以直接运行此文件
    pytest.main([__file__, "-v", "-s"])
```

---

## 📋 代码说明

### 1. 测试函数命名 `test_*`

```python
def test_hello_world():
    """测试函数必须以test_开头"""
    pass
```

**关键点**:
- pytest会自动识别以 `test_` 开头的函数
- 测试函数通常使用描述性命名，如 `test_login_success`
- 良好的命名能让测试失败时更容易定位问题

### 2. 断言 `assert`

```python
assert 1 + 1 == 2  # 如果条件为False，测试失败
assert "hello" == "hello"  # 验证字符串相等
assert result["success"] == True  # 验证字典值
```

**断言的作用**:
- 验证实际结果是否符合预期
- 如果条件为False，立即抛出AssertionError
- pytest会捕获并显示详细的失败信息

### 3. 测试函数的三要素

```python
def test_login_success():
    """测试登录成功场景"""

    # 1. 准备测试数据（Arrange）
    username = "admin"
    password = "123456"

    # 2. 执行被测功能（Act）
    result = login(username, password)

    # 3. 验证结果（Assert）
    assert result["success"] == True
    assert result["message"] == "登录成功"
```

**AAA模式**:
- **Arrange**（准备）：设置测试数据和环境
- **Act**（执行）：调用被测函数
- **Assert**（验证）：检查结果是否符合预期

### 4. 异常测试 `pytest.raises`

```python
def test_zero_division():
    with pytest.raises(ValueError) as excinfo:
        divide(10, 0)
    assert "除数不能为零" in str(excinfo.value)
```

**作用**: 测试函数是否按预期抛出异常

---

## 🎯 运行程序

### 方法1: 使用pytest命令

```bash
# 运行所有测试
pytest tests/test_hello_world.py -v

# 运行并显示print输出
pytest tests/test_hello_world.py -v -s

# 运行特定测试函数
pytest tests/test_hello_world.py::test_hello_world -v

# 运行并显示详细输出
pytest tests/test_hello_world.py -vv -s
```

### 方法2: 直接运行Python文件

```bash
python tests/test_hello_world.py
```

### 预期输出

```
======================== test session starts =========================
collected 6 items

test_hello_world.py::test_hello_world PASSED                      [ 16%]
✅ 测试通过！
test_hello_world.py::test_string_operations PASSED               [ 33%]
test_hello_world.py::test_list_operations PASSED                 [ 50%]
test_hello_world.py::test_calculator PASSED                      [ 66%]
test_hello_world.py::test_login_function PASSED                  [ 83%]
test_hello_world.py::test_edge_cases PASSED                      [100%]

======================== 6 passed in 0.02s ==========================
🎉 所有测试通过！
```

---

## 🔍 理解测试输出

### 测试通过

```
test_hello_world.py::test_hello_world PASSED                      [ 16%]
```
- ✅ **PASSED**: 测试通过
- `[16%]`: 进度百分比

### 测试失败

```python
# 修改测试让它失败
def test_hello_world():
    assert 1 + 1 == 3  # 故意写错
```

运行后会看到：

```
FAILED test_hello_world.py::test_hello_world - assert 2 == 3
```

pytest会显示：
- 失败的测试名称
- 失败的断言
- 期望值 vs 实际值
- 失败位置的代码

### 测试错误

```python
def test_with_error():
    result = undefined_variable  # 变量未定义
```

运行后会看到：

```
ERROR test_hello_world.py::test_with_error - NameError: name 'undefined_variable' is not defined
```

---

## 🎨 常见测试场景

### 1. 参数化测试

使用不同输入运行同一个测试：

```python
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
])
def test_add(a, b, expected):
    """参数化测试：测试不同输入"""
    assert a + b == expected
```

### 2. 测试夹具（Fixture）

在测试前后执行设置和清理：

```python
@pytest.fixture
def sample_data():
    """测试夹具：提供测试数据"""
    data = {"name": "Test", "value": 100}
    yield data
    # 清理代码（如果需要）

def test_with_fixture(sample_data):
    """使用测试夹具"""
    assert sample_data["name"] == "Test"
    assert sample_data["value"] == 100
```

### 3. 跳过测试

某些条件下跳过测试：

```python
@pytest.mark.skip(reason="功能未实现")
def test_not_implemented():
    pass

@pytest.mark.skipif(sys.version_info < (3, 10), reason="需要Python 3.10+")
def test_python_310_feature():
    pass
```

### 4. 标记测试

给测试打标签，便于分类运行：

```python
@pytest.mark.unit
def test_unit_test():
    """单元测试"""
    pass

@pytest.mark.integration
def test_integration_test():
    """集成测试"""
    pass

# 运行时只运行单元测试
# pytest -m unit
```

---

## 🐛 常见问题

### Q1: 找不到测试？

**原因**: 文件名或函数名不符合pytest规范

**解决方案**:
```python
# ✅ 正确的命名
test_hello_world.py  # 文件以test_开头
def test_something():  # 函数以test_开头
    pass

# ❌ 错误的命名
hello_test.py
def something_test():
    pass
```

### Q2: 测试通过但看不到输出？

**原因**: pytest默认隐藏print输出

**解决方案**:
```bash
# 使用-s参数显示print输出
pytest test_hello_world.py -v -s
```

### Q3: 如何测试私有方法？

**方案**: 可以直接测试，但建议通过公共接口测试

```python
class Calculator:
    def _add(self, a, b):  # 私有方法
        return a + b

    def public_add(self, a, b):  # 公共方法
        return self._add(a, b)

# ✅ 推荐：测试公共接口
def test_public_add():
    calc = Calculator()
    assert calc.public_add(1, 2) == 3

# ⚠️ 可以但不推荐：直接测试私有方法
def test_private_add():
    calc = Calculator()
    assert calc._add(1, 2) == 3
```

### Q4: 测试之间相互影响？

**原因**: 测试共享了可变状态

**解决方案**:
```python
# 每个测试使用独立的测试数据
def test_with_isolated_data():
    data = [1, 2, 3]  # 局部数据，不影响其他测试
    assert len(data) == 3

# 或使用fixture提供干净的数据
@pytest.fixture
def fresh_data():
    return [1, 2, 3]

def test_with_fresh_data(fresh_data):
    assert len(fresh_data) == 3
```

---

## 🎉 恭喜！

你已经完成了第一个测试程序！

### 你学会了什么？

- ✅ 编写测试函数
- ✅ 使用assert断言
- ✅ 运行pytest测试
- ✅ 理解测试输出
- ✅ 处理异常测试
- ✅ 使用参数化测试

### 下一步学习

1. **测试基础**: [学习软件测试基础概念](../../01-软件测试基础概念.md)
2. **测试用例设计**: [学习测试用例设计方法](../../04-测试用例设计基础.md)
3. **实战练习**: 完成更多练习

### 练习挑战

**难度**: ⭐⭐☆☆☆
**预计时间**: 15分钟

**任务**:
1. 为以下函数编写完整的测试用例：
   - [ ] 正常情况
   - [ ] 边界情况
   - [ ] 异常情况

```python
def calculate_grade(score):
    """
    计算成绩等级
    score: 0-100的分数
    返回: 'A', 'B', 'C', 'D', 'F'
    """
    if score < 0 or score > 100:
        raise ValueError("分数必须在0-100之间")

    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'
```

**提示**:
```python
def test_calculate_grade():
    # 测试A等级
    assert calculate_grade(90) == 'A'
    assert calculate_grade(95) == 'A'
    assert calculate_grade(100) == 'A'

    # 测试B等级
    assert calculate_grade(80) == 'B'
    assert calculate_grade(85) == 'B'

    # 测试边界值
    assert calculate_grade(89) == 'B'  # 89分是B不是A
    assert calculate_grade(90) == 'A'  # 90分是A

    # 测试异常情况
    with pytest.raises(ValueError):
        calculate_grade(-1)
    with pytest.raises(ValueError):
        calculate_grade(101)

    # 测试F等级
    assert calculate_grade(0) == 'F'
    assert calculate_grade(59) == 'F'
```

---

## 📚 参考资料

- [pytest官方文档](https://docs.pytest.org/)
- [pytest中文文档](https://www.osgeo.cn/pytest/)
- [Python unittest文档](https://docs.python.org/3/library/unittest.html)

---

**更新**: 2026-01-13
**适用于**: Python 3.10+, pytest 7.4+

---

**返回**: [环境配置](../setup/README.md) | [主目录](../../README.md) | [下一章: 基础概念](../../01-软件测试基础概念.md)
