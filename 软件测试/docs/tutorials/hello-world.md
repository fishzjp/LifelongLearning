# 🌟 Hello World - 你的第一个测试

> **一句话总结**：在5分钟内，编写并运行你的第一个自动化测试！

---

## 🎯 学习目标

- [ ] 理解测试的基本概念
- [ ] 编写并运行第一个测试用例
- [ ] 掌握pytest的基本用法

**预计学习时间**：5分钟  
**难度等级**：⭐☆☆☆☆

---

## 🚀 为什么需要测试？

测试是确保代码正确性的关键手段。通过测试，我们可以：
- 验证代码是否按预期工作
- 早期发现缺陷，降低修复成本
- 保证代码重构的安全性
- 作为代码的活文档

---

## 📝 第一个测试用例

### 步骤1：创建测试文件

新建文件 `test_hello.py`：

```bash
# test_hello.py
# 这是一个简单的测试函数

def test_hello_world():
    """我的第一个测试：验证1+1=2"""
    # assert 是测试的核心：断言某个条件必须为真
    assert 1 + 1 == 2
    print("✅ 测试通过！")
```

### 步骤2：运行测试

在终端中运行：
```python
pytest test_hello.py -v
```

### 步骤3：查看结果

你应该看到：
```
========================= test session starts =========================
collected 1 item

test_hello.py::test_hello_world PASSED                           [100%]

========================== 1 passed in 0.01s ===========================
✅ 测试通过！
```

**🎉 恭喜！你已经完成了第一个测试！**

---

## 🚀 进阶：真实场景测试

### 场景：测试登录功能

```bash
# test_login_demo.py

def check_login(username, password):
    """模拟登录验证函数"""
    if username == "admin" and password == "123456":
        return {"success": True, "message": "登录成功"}
    else:
        return {"success": False, "message": "用户名或密码错误"}

# 测试用例1：正确登录

def test_login_success():
    """测试正确用户名密码"""
    result = check_login("admin", "123456")
    assert result["success"] == True
    assert result["message"] == "登录成功"

# 测试用例2：错误密码

def test_login_wrong_password():
    """测试错误密码"""
    result = check_login("admin", "wrongpass")
    assert result["success"] == False
    assert "错误" in result["message"]

# 测试用例3：空用户名

def test_login_empty_username():
    """测试空用户名"""
    result = check_login("", "123456")
    assert result["success"] == False
```

运行所有测试：
```python
pytest test_login_demo.py -v
```

---

## 🎓 测试思维培养

### 什么是测试？

```
测试 = 给程序"找茬" + 验证"完美"

输入：你的代码
执行：运行测试
输出：通过✅ 或 失败❌
```

### 测试三要素

1. **输入**：给程序什么数据？
2. **执行**：怎么操作？
3. **预期**：应该得到什么结果？

### 你的第一个测试习惯

每次写代码前，先问自己：
> "如果我要测试这个功能，需要验证哪些情况？"

---

## 🎯 课后练习

### 练习1：修改测试

修改 `test_hello.py`，让它失败：
```python
def test_hello_world():
    assert 1 + 1 == 3  # 故意写错
```

运行后观察错误信息，理解测试失败的含义。

### 练习2：编写新测试

为以下函数编写测试：
```python
def is_even(n):
    """判断是否为偶数"""
    return n % 2 == 0
```

你的测试应该覆盖：
- ✅ 偶数（如：2, 4, 100）
- ✅ 奇数（如：1, 3, 99）
- ✅ 边界值（0, -2）

---

## 📚 下一步学习路径

1. **立即**：[理解测试用例设计](../04-测试用例设计基础.md)
2. **明天**：[学习等价类划分](../04-测试用例设计基础.md#等价类划分)
3. **本周**：[完成练习01](../../实践练习/练习01-测试用例设计.md)

---

## 💡 常见问题

### Q: 为什么测试函数要以 `test_` 开头？

**A**: Pytest会自动识别以 `test_` 开头的函数作为测试用例。

### Q: assert是什么？

**A**: 断言语句，如果条件为假，测试失败并抛出异常。

### Q: 如何测试多个场景？

**A**: 编写多个测试函数，每个函数测试一个场景。

---

## 🏆 成就系统

- ✅ 完成第一个测试
- 🎯 理解测试三要素
- 🚀 掌握基本断言
- 📈 准备进阶学习

---

**文档版本**：v1.0  
**最后更新**：2025-12-29

**下一步**：[环境配置指南](../setup/README.md) | [术语表](../glossary/README.md)
