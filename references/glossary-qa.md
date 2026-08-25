# 软件测试术语表
> 🎯 **目标**：一站式查询所有专业术语，让新人不再被术语困扰

---

## 快速索引
- [A](#a) | [B](#b) | [C](#c) | [D](#d) | [E](#e) | [F](#f) | [G](#g) | [H](#h)
- [I](#i) | [J](#j) | [K](#k) | [L](#l) | [M](#m) | [N](#n) | [O](#o) | [P](#p)
- [Q](#q) | [R](#r) | [S](#s) | [T](#t) | [U](#u) | [V](#v) | [W](#w) | [X](#x)
- [Y](#y) | [Z](#z)

---

## A
### Acceptance Testing (验收测试)
**定义**：由客户或最终用户执行的测试，验证系统是否满足业务需求和用户期望。

**场景**：
- 项目交付前的最终确认
- 用户验收阶段（UAT）
- 合同约定的交付标准验证

**难度**：⭐⭐

**相关术语**：UAT, Beta Testing, User Testing

**示例**：
```python
# 验收测试示例：用户能否成功下单
def test_user_can_create_order():
    """用户能够成功创建订单（验收标准）"""
    user = User("test@example.com")
    order = user.create_order(items=["iPhone", "MacBook"])

    # 验收标准
    assert order.status == "confirmed"
    assert order.total_price == 29998
    assert order.payment_status == "paid"
```

**为什么重要**：
- 确保软件满足用户真实需求
- 避免交付后大量返工
- 建立用户对产品的信心

---

### Alpha Testing (α测试)
**定义**：在开发环境内部进行的测试，通常由开发团队或公司内部测试人员执行。

**场景**：
- 开发完成后，发布给用户前的内部测试
- 早期功能验证

**难度**：⭐⭐

**对比**：Beta Testing（β测试）

---

### API Testing (接口测试)
**定义**：直接测试应用程序接口（API）的功能、性能、安全性，不涉及用户界面。

**场景**：
- 前后端分离架构
- 微服务架构
- 第三方服务集成

**难度**：⭐⭐⭐

**相关工具**：Postman, RestAssured, JMeter

**示例**：
```python
import requests

def test_login_api():
    """测试登录API"""
    response = requests.post(
        "https://api.example.com/login",
        json={"username": "admin", "password": "123456"}
    )

    assert response.status_code == 200
    assert response.json()["success"] == True
    assert "token" in response.json()
```

**为什么需要**：
- 比UI测试更快、更稳定
- 早期发现集成问题
- 支持持续集成

---

### Automation Testing (自动化测试)
**定义**：使用脚本和工具自动执行测试用例，替代人工重复操作。

**场景**：
- 回归测试（频繁迭代）
- 性能测试（并发、压力）
- 数据驱动测试（大量测试数据）
- 兼容性测试（多浏览器/设备）

**难度**：⭐⭐⭐

**相关术语**：Selenium, Pytest, CI/CD

**优势**：
- 效率高：24小时不间断执行
- 可重复：避免人为失误
- 覆盖广：能执行更多场景

**局限性**：
- 初期投入大
- 维护成本高
- 无法完全替代人工（用户体验、探索性测试）

**示例**：
```text
# 重复执行100次登录测试
# 人工：2小时
# 自动化：2分钟
```

---

## B
### Black Box Testing (黑盒测试)
**定义**：不关心内部实现细节，只验证输入输出是否符合预期的测试方法。

**场景**：
- 功能测试
- 用户视角测试
- 集成测试

**难度**：⭐⭐

**对比**：White Box Testing（白盒测试）

**特点**：
- 不需要看代码
- 模拟真实用户操作
- 关注功能正确性

**示例**：
```python
# 黑盒测试：只关心输入输出
def test_login_black_box():
    result = login_service.login("user", "pass")
    assert result.success == True  # 不关心内部如何验证
```

**为什么使用**：
- 测试人员不需要懂代码
- 更接近真实用户场景
- 验证需求是否实现

---

### Beta Testing (β测试)
**定义**：在真实环境中，由真实用户进行的测试，用于收集反馈和发现隐藏问题。

**场景**：
- 产品正式发布前的公测
- 收集用户反馈
- 验证产品在真实环境的表现

**难度**：⭐⭐⭐

**对比**：Alpha Testing

---

### Bug (缺陷)
**定义**：软件中的错误、缺陷或问题，导致软件行为与预期不符。

**别名**：Defect, Issue, Fault

**严重程度**：
- 🔴 **致命（Critical）**：系统崩溃、数据丢失、安全漏洞
- 🟠 **严重（Major）**：核心功能不可用
- 🟡 **一般（Minor）**：非核心功能异常
- 🔵 **轻微（Trivial）**：界面问题、错别字

**相关术语**：Defect, Issue, Fault

**缺陷生命周期**：
```
新建 → 分析 → 修复 → 验证 → 关闭
  ↓
  拒绝（不是缺陷）
```

---

## C
### Compatibility Testing (兼容性测试)
**定义**：验证软件在不同环境（浏览器、操作系统、设备、网络）下能否正常工作。

**测试维度**：
- **浏览器**：Chrome, Firefox, Safari, Edge
- **操作系统**：Windows, macOS, Linux, iOS, Android
- **设备**：PC, 手机, 平板
- **分辨率**：不同屏幕尺寸
- **网络**：WiFi, 4G, 5G, 慢速网络

**难度**：⭐⭐⭐

**相关术语**：Cross-browser Testing, Mobile Testing

**示例**：
```python
# 测试在不同浏览器的登录功能
@pytest.mark.parametrize("browser", ["chrome", "firefox", "safari"])
def test_login_on_different_browsers(browser):
    driver = get_driver(browser)
    driver.get("https://example.com/login")
    # ... 登录测试
```

**为什么重要**：
- 确保用户体验一致
- 覆盖更多用户群体
- 避免环境相关的问题

---

### CI/CD (持续集成/持续交付)
**定义**：Continuous Integration / Continuous Delivery，自动化构建、测试、部署流程。

**流程**：
```
代码提交 → 自动构建 → 自动测试 → 自动部署 → 监控
```

**难度**：⭐⭐⭐⭐

**相关工具**：Jenkins, GitLab CI, GitHub Actions

**为什么需要测试**：
- 自动化测试是CI/CD的核心
- 快速反馈代码质量
- 保证每次发布都可靠

---

### Code Coverage (代码覆盖率)
**定义**：测试用例覆盖了多少代码，通常用百分比表示。

**类型**：
- **行覆盖率**：执行了多少行代码
- **分支覆盖率**：执行了多少个分支（if/else）
- **函数覆盖率**：调用了多少函数
- **语句覆盖率**：执行了多少条语句

**难度**：⭐⭐

**目标**：
- 单元测试：> 70%
- 核心模块：> 80%
- 整体：> 60%

**示例**：
```bash
# 生成覆盖率报告
pytest --cov=src --cov-report=html

# 查看报告
open htmlcov/index.html
```

---

### Cross-browser Testing (跨浏览器测试)
**定义**：在多种浏览器上测试Web应用，确保兼容性。

**常见浏览器**：
- Chrome（市场份额最大）
- Firefox（开发者友好）
- Safari（iOS/macOS默认）
- Edge（Windows默认）

**难度**：⭐⭐⭐

**工具**：
- Selenium Grid（分布式执行）
- BrowserStack（云端真机）
- Sauce Labs

---

## D
### Data-driven Testing (数据驱动测试)
**定义**：将测试数据与测试逻辑分离，用多组数据驱动同一个测试逻辑。

**场景**：
- 同一功能需要验证多种输入
- 边界值测试
- 等价类测试

**难度**：⭐⭐⭐

**示例**：
```python
# 使用pytest的parametrize
import pytest

test_data = [
    ("admin", "123456", True, "正常账号"),
    ("", "123456", False, "空用户名"),
    ("admin", "", False, "空密码"),
    ("wrong", "wrong", False, "错误账号")
]

@pytest.mark.parametrize("username,password,expected,desc", test_data)
def test_login(username, password, expected, result_desc):
    result = login(username, password)
    assert result.success == expected
```

**优势**：
- 减少代码重复
- 易于维护
- 测试覆盖全面

---

### Debugging (调试)
**定义**：发现、定位和修复软件缺陷的过程。

**常用方法**：
- 打印日志（print/logging）
- 断点调试（IDE调试器）
- 单元测试定位
- 代码审查

**难度**：⭐⭐⭐

---

### Defect (缺陷)
**定义**：软件中的错误或问题，导致软件行为与预期不符。

**同义词**：Bug, Issue, Fault

**严重程度**：
1. 致命（Critical）- 系统崩溃、数据丢失
2. 严重（Major）- 核心功能不可用
3. 一般（Minor）- 非核心功能异常
4. 轻微（Trivial）- 界面问题

**缺陷报告**：见[缺陷报告模板](templates/bug-report.md)

---

## E
### End-to-End Testing (端到端测试)
**定义**：模拟真实用户操作流程，从开始到结束完整测试。

**场景**：
- 用户注册 → 登录 → 下单 → 支付 → 退出
- 跨系统、跨模块的完整流程

**难度**：⭐⭐⭐⭐

**相关术语**：E2E Testing, UI Testing

**示例**：
```python
def test_complete_shopping_flow():
    """完整的购物流程测试"""
    # 1. 登录
    login("user", "pass")

    # 2. 搜索商品
    search("iPhone")

    # 3. 添加到购物车
    add_to_cart()

    # 4. 结算
    checkout()

    # 5. 支付
    pay()

    # 6. 验证订单
    assert order_exists()
```

---

### Equivalence Partitioning (等价类划分)
**定义**：将输入数据分成若干个等价类，从每个等价类中选取代表值进行测试。

**场景**：输入验证测试

**难度**：⭐⭐

**示例**：
```text
# 用户名：6-20位字符
# 有效等价类
- 6位：abcdef
- 10位：abcdefghij
- 20位：abcdefghijklmnopqrst

# 无效等价类
- 5位：abcde（太短）
- 21位：abcdefghijklmnopqrstu（太长）
- 空值：""（空字符串）
- 特殊字符：abc@123（非法字符）
```

**为什么使用**：
- 减少测试用例数量
- 保证测试覆盖率
- 系统化测试设计

---

### Exploratory Testing (探索性测试)
**定义**：测试人员基于经验和直觉，自由探索软件，发现缺陷。

**特点**：
- 没有固定测试用例
- 依赖测试人员经验
- 发现非预期缺陷

**难度**：⭐⭐⭐

**适用场景**：
- 新功能快速验证
- 发现隐藏问题
- 补充自动化测试

---

## F
### Functional Testing (功能测试)
**定义**：验证软件功能是否符合需求规格说明。

**测试内容**：
- 用户界面
- API接口
- 数据处理
- 业务逻辑

**难度**：⭐⭐

**相关术语**：Smoke Testing, Regression Testing

**示例**：
```python
def test_search_function():
    """测试搜索功能"""
    results = search("iPhone")
    assert len(results) > 0
    assert all("iPhone" in r.name for r in results)
```

---

### Failure Rate (失败率)
**定义**：测试用例或系统运行中失败的比例。

**计算公式**：
```
失败率 = (失败的测试数 / 总测试数) × 100%
```

**监控指标**：
- 测试失败率 < 5%
- 生产环境失败率 < 0.1%

---

## G
### GUI Testing (图形界面测试)
**定义**：测试用户界面的功能和用户体验。

**测试内容**：
- 控件功能
- 布局显示
- 用户交互
- 响应速度

**难度**：⭐⭐⭐

**相关工具**：Selenium, Appium

---

### Gray Box Testing (灰盒测试)
**定义**：介于黑盒和白盒之间，了解部分内部结构的测试方法。

**特点**：
- 知道部分代码结构
- 了解数据库设计
- 关注接口和数据流

**难度**：⭐⭐⭐

**相关术语**：Integration Testing

---

## H
### Happy Path (快乐路径)
**定义**：软件正常工作的最佳路径，所有输入都正确。

**场景**：正常流程测试

**示例**：
```python
# 用户登录的快乐路径
def test_login_happy_path():
    """快乐路径：正确用户名+正确密码"""
    result = login("admin", "123456")
    assert result.success == True
    assert result.user.role == "admin"
```

**对比**：Sad Path（异常路径）

---

### Hybrid Testing (混合测试)
**定义**：结合多种测试方法的策略。

**示例**：
- 自动化 + 手工测试
- 黑盒 + 白盒测试
- 单元 + 集成测试

---

## I
### Integration Testing (集成测试)
**定义**：将多个模块组合在一起进行测试，验证模块间的接口和协作。

**场景**：
- 模块A + 模块B
- 服务A + 服务B
- 前端 + 后端

**难度**：⭐⭐⭐

**相关术语**：API Testing, Gray Box Testing

**示例**：
```python
def test_user_order_integration():
    """用户和订单模块集成测试"""
    user = create_user("test")
    order = create_order(user, items=["iPhone"])

    # 验证两个模块的协作
    assert order.user_id == user.id
    assert user.order_count == 1
```

---

### ISTQB (国际软件测试资格认证)
**定义**：International Software Testing Qualifications Board，国际软件测试认证机构。

**认证级别**：
- Foundation Level（基础级）
- Advanced Level（高级）
- Expert Level（专家级）

---

## J
### JUnit (Java测试框架)
**定义**：Java语言的单元测试框架。

**相关**：TestNG, pytest（Python）

---

### JSON (JavaScript Object Notation)
**定义**：轻量级的数据交换格式，常用于API测试。

**示例**：
```json
{
  "username": "admin",
  "password": "123456",
  "success": true
}
```

---

## K
### Keyword-Driven Testing (关键字驱动测试)
**定义**：使用关键字描述测试步骤，实现测试与实现分离。

**示例**：
```
测试步骤：
  打开浏览器
  输入用户名 "admin"
  输入密码 "123456"
  点击登录
  验证登录成功
```

---

## L
### Load Testing (负载测试)
**定义**：测试系统在正常负载下的性能表现。

**指标**：
- 响应时间
- 吞吐量（TPS）
- 资源利用率

**难度**：⭐⭐⭐⭐

**相关术语**：Performance Testing, Stress Testing

---

### Localization Testing (本地化测试)
**定义**：测试软件在不同语言、地区设置下的表现。

**测试内容**：
- 语言翻译
- 日期格式
- 货币符号
- 字符编码

---

## M
### Manual Testing (手工测试)
**定义**：人工执行测试用例，不使用自动化工具。

**优点**：
- 灵活，适合探索性测试
- 能发现自动化遗漏的问题
- 适合用户体验测试

**缺点**：
- 重复工作多
- 效率低
- 容易出错

**难度**：⭐⭐

---

### Mobile Testing (移动端测试)
**定义**：测试移动应用的功能、性能、兼容性。

**测试内容**：
- 功能测试
- 兼容性测试（不同设备、系统版本）
- 性能测试
- 安全测试
- 中断测试（来电、消息）

**难度**：⭐⭐⭐⭐

**相关工具**：Appium, Espresso, XCTest

---

## N
### Negative Testing (负面测试)
**定义**：测试软件在异常输入或条件下的表现。

**目的**：验证软件的健壮性和错误处理能力。

**示例**：
```python
def test_login_negative():
    """负面测试：各种异常情况"""
    # 空用户名
    assert login("", "pass").success == False

    # 空密码
    assert login("user", "").success == False

    # SQL注入
    assert login("admin' OR '1'='1", "pass").success == False
```

**对比**：Positive Testing（正面测试）

---

## O
### Object Repository (对象库)
**定义**：集中管理UI元素定位信息的机制。

**示例**：
```python
# 不使用对象库
driver.find_element(By.ID, "username")
driver.find_element(By.ID, "password")

# 使用对象库
class LoginPage:
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")

driver.find_element(*LoginPage.USERNAME)
```

---

### Onion Testing (洋葱测试)
**定义**：从内到外逐层测试的策略（单元 → 集成 → 系统 → 验收）。

---

## P
### Page Object Model (页面对象模式)
**定义**：将页面元素和操作封装成类，提高代码复用性和可维护性。

**难度**：⭐⭐⭐

**示例**：
```python
class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_input = (By.ID, "username")
        self.password_input = (By.ID, "password")
        self.login_btn = (By.ID, "login_btn")

    def login(self, username, password):
        self.driver.find_element(*self.username_input).send_keys(username)
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.login_btn).click()
        return HomePage(self.driver)

# 使用
login_page = LoginPage(driver)
login_page.login("admin", "123456")
```

**优势**：
- 代码复用
- 易于维护
- 清晰的结构

---

### Performance Testing (性能测试)
**定义**：测试系统在不同负载下的性能指标。

**类型**：
- **负载测试**：正常负载
- **压力测试**：极限负载
- **并发测试**：多用户同时访问
- **稳定性测试**：长时间运行

**指标**：
- 响应时间（< 2秒）
- 吞吐量（TPS）
- 并发用户数
- 错误率（< 0.1%）

**难度**：⭐⭐⭐⭐

**工具**：JMeter, k6, Locust

---

### Postman (接口测试工具)
**定义**：流行的API测试和开发工具。

**功能**：
- 发送HTTP请求
- 自动化测试
- Mock Server
- 环境管理

**难度**：⭐⭐

---

### Priority (优先级)
**定义**：缺陷修复的紧急程度。

**级别**：
- P0 - 紧急（立即修复）
- P1 - 高（本周内修复）
- P2 - 中（下个版本修复）
- P3 - 低（有空再修复）

---

### Pyramid Testing (测试金字塔)
**定义**：测试策略的分层模型。

```
        少量
    ┌─────────────┐
    │   E2E测试   │  UI自动化
    ├─────────────┤
    │  接口测试   │  API自动化
    ├─────────────┤
    │  单元测试   │  代码级别
    └─────────────┘
        大量
```

**原则**：
- 单元测试最多（快速、稳定）
- 接口测试适中（平衡速度和覆盖）
- E2E测试最少（慢、不稳定）

---

## Q
### Quality Assurance (质量保证)
**定义**：预防缺陷的过程，关注过程改进。

**相关术语**：QA, QC, Quality Control

**对比**：
- **QA（质量保证）**：预防缺陷，关注过程
- **QC（质量控制）**：发现缺陷，关注产品

---

### Quality Control (质量控制)
**定义**：发现缺陷的过程，关注产品检查。

**相关术语**：QC, Testing

---

## R
### Regression Testing (回归测试)
**定义**：修改代码后，重新测试原有功能，确保没有引入新问题。

**场景**：
- 修复Bug后
- 添加新功能后
- 代码重构后

**难度**：⭐⭐⭐

**自动化价值**：⭐⭐⭐⭐⭐（非常适合自动化）

**示例**：
```python
# 每次代码提交后自动运行
def test_regression_login():
    """回归测试：登录功能"""
    # 确保登录功能在代码修改后仍然正常
    assert login("admin", "123456").success == True
```

---

### Reliability Testing (可靠性测试)
**定义**：测试软件在长时间运行中的稳定性和可靠性。

**目标**：
- 无崩溃
- 无内存泄漏
- 数据一致性

**难度**：⭐⭐⭐⭐

---

### Response Time (响应时间)
**定义**：从发送请求到收到响应的时间。

**标准**：
- 优秀：< 1秒
- 良好：1-2秒
- 一般：2-5秒
- 较差：> 5秒

---

## S
### Sanity Testing (健全测试)
**定义**：快速验证软件最基本功能是否正常的测试。

**特点**：
- 范围小
- 时间短
- 快速判断是否值得进一步测试

**难度**：⭐⭐

**对比**：Smoke Testing（冒烟测试）

---

### Security Testing (安全测试)
**定义**：发现系统安全漏洞的测试。

**测试内容**：
- SQL注入
- XSS攻击
- CSRF攻击
- 权限越权
- 敏感信息泄露

**难度**：⭐⭐⭐⭐⭐

**相关工具**：OWASP ZAP, Burp Suite

**示例**：
```python
def test_sql_injection():
    """测试SQL注入"""
    result = login("admin' OR '1'='1", "anything")
    assert result.success == False  # 应该被拦截
```

---

### Smoke Testing (冒烟测试)
**定义**：测试软件最基本、最重要的功能是否正常。

**目的**：快速判断版本是否可测。

**示例**：
```python
def test_smoke():
    """冒烟测试：核心功能"""
    # 1. 能否启动
    assert app.is_running()

    # 2. 能否登录
    assert login("admin", "123456").success

    # 3. 能否访问首页
    assert home_page.is_displayed()
```

**难度**：⭐⭐

---

### Stress Testing (压力测试)
**定义**：测试系统在极限负载下的表现。

**目标**：
- 找出系统瓶颈
- 验证系统崩溃点
- 测试恢复能力

**难度**：⭐⭐⭐⭐

**示例**：
```text
# 1000并发用户访问
# 观察响应时间、错误率、资源使用
```

---

### System Testing (系统测试)
**定义**：对整个系统进行完整的测试，包括功能、性能、安全等。

**阶段**：集成测试之后，验收测试之前。

**难度**：⭐⭐⭐⭐

---

## T
### Test Case (测试用例)
**定义**：一组测试输入、执行条件和预期结果，用于验证特定功能。

**包含要素**：
- 用例编号
- 测试目标
- 前置条件
- 测试步骤
- 预期结果
- 实际结果

**难度**：⭐⭐

**模板**：见[测试用例模板](templates/test-case.md)

**示例**：
```python
用例编号：TC-LOGIN-001
测试目标：验证正确凭证登录成功
前置条件：用户账号已注册
测试步骤：
  1. 输入用户名：admin
  2. 输入密码：123456
  3. 点击登录
预期结果：登录成功，跳转到首页
```

---

### Test Plan (测试计划)
**定义**：描述测试范围、策略、资源、进度的文档。

**包含内容**：
- 测试目标
- 测试范围
- 测试策略
- 资源安排
- 进度计划
- 风险分析

**难度**：⭐⭐⭐

**模板**：见[测试策略模板](templates/test-strategy.md)

---

### Test Pyramid (测试金字塔)
**定义**：测试策略的分层模型，底层多，顶层少。

**层级**：
1. **单元测试**（底层，最多）
2. **集成测试**（中层，适中）
3. **E2E测试**（顶层，最少）

**优势**：
- 快速反馈
- 稳定可靠
- 维护成本低

---

### Test Strategy (测试策略)
**定义**：指导测试活动的总体方法和原则。

**包含**：
- 测试范围
- 测试方法
- 工具选择
- 风险分析
- 进度安排

**难度**：⭐⭐⭐⭐

---

### Test Suite (测试套件)
**定义**：一组相关的测试用例的集合。

**示例**：
```text
# 登录相关的所有测试
test_suite = [
    test_login_success,
    test_login_wrong_password,
    test_login_empty_username,
    test_login_empty_password,
    test_login_sql_injection
]
```

---

### Test-driven Development (测试驱动开发)
**定义**：先写测试，再写代码的开发方法。

**流程**：
1. 写失败的测试
2. 写最少的代码让测试通过
3. 重构代码
4. 重复

**难度**：⭐⭐⭐⭐

**优势**：
- 代码质量高
- 文档化
- 快速反馈

---

### TestRail (测试管理工具)
**定义**：专业的测试用例管理工具。

**功能**：
- 用例管理
- 测试计划
- 缺陷跟踪
- 报告统计

---

## U
### UAT (用户验收测试)
**定义**：User Acceptance Testing，最终用户验证软件是否满足需求。

**执行者**：最终用户或客户

**难度**：⭐⭐⭐

**相关术语**：Acceptance Testing

---

### UI Testing (用户界面测试)
**定义**：测试用户界面的功能和交互。

**测试内容**：
- 控件功能
- 页面布局
- 用户交互
- 响应速度

**难度**：⭐⭐⭐

**工具**：Selenium, Cypress, Playwright

---

### Unit Testing (单元测试)
**定义**：测试代码的最小单元（函数、方法）。

**特点**：
- 速度快
- 隔离性好
- 由开发人员编写

**难度**：⭐⭐

**示例**：
```python
def test_calculate_total():
    """测试计算总价函数"""
    assert calculate_total(100, 2, 10) == 190  # 100*2-10
```

---

## V
### Validation (验证)
**定义**：检查软件是否满足用户需求和预期。

**问题**：我们在做正确的事吗？

---

### Verification (确认)
**定义**：检查软件是否正确地实现了需求。

**问题**：我们正确地做事了吗？

**对比**：
- **验证**：过程正确
- **确认**：结果正确

---

### Version Control (版本控制)
**定义**：管理代码变更的系统。

**工具**：Git, SVN

**为什么重要**：
- 回滚错误代码
- 追踪变更历史
- 团队协作

---

## W
### White Box Testing (白盒测试)
**定义**：基于代码内部结构的测试方法。

**测试内容**：
- 语句覆盖
- 分支覆盖
- 路径覆盖

**难度**：⭐⭐⭐⭐

**要求**：需要懂代码

**对比**：Black Box Testing

**示例**：
```python
def test_internal_logic():
    """白盒测试：了解内部逻辑"""
    # 知道内部有if-else分支
    # 测试两个分支
    assert func(1) == "A"  # 分支1
    assert func(2) == "B"  # 分支2
```

---

### Workaround (临时解决方案)
**定义**：绕过缺陷的临时方法。

**场景**：缺陷暂时无法修复，但业务需要继续

---

## X
### XSS (跨站脚本攻击)
**定义**：Cross-Site Scripting，注入恶意脚本到网页。

**测试方法**：
```python
def test_xss_prevention():
    """测试XSS防护"""
    result = search("<script>alert('xss')</script>")
    assert "<script>" not in result  # 脚本被转义
```

---

## Y
### Yellow Box Testing (黄盒测试)
**定义**：介于黑盒和白盒之间，了解部分内部信息的测试。

---

## Z
### Zero-day Vulnerability (零日漏洞)
**定义**：被发现但还未修复的安全漏洞。

**风险**：极高

**应对**：快速响应、紧急修复

---

## 使用指南
### 如何查找术语？
1. **按字母索引**：点击上方字母快速定位
2. **搜索功能**：使用浏览器搜索（Ctrl+F / Cmd+F）
3. **相关链接**：每个术语都有相关术语链接

### 术语难度标识
- ⭐：基础概念，必须掌握
- ⭐⭐：常用概念，建议掌握
- ⭐⭐⭐：进阶概念，推荐掌握
- ⭐⭐⭐⭐：高级概念，按需学习
- ⭐⭐⭐⭐⭐：专家级，深入研究

### 术语关联
每个术语都包含：
- **相关术语**：点击跳转
- **示例代码**：可直接运行
- **使用场景**：何时使用

---

## 新人学习路径
### 第一周：掌握基础术语
1. 阅读 A-C 部分
2. 理解核心概念：Test Case, Bug, Black Box Testing
3. 实践：编写第一个测试用例

### 第二周：扩展知识
1. 阅读 D-H 部分
2. 理解：Automation, Integration, Performance
3. 实践：运行自动化测试

### 第三周：进阶概念
1. 阅读 I-Q 部分
2. 理解：Pyramid, Strategy, TDD
3. 实践：设计测试策略

### 第四周：高级主题
1. 阅读 R-Z 部分
2. 理解：Security, Stress, Reliability
3. 实践：性能测试

---

## 常见问题
### Q: 术语太多记不住怎么办？
**A**: 不需要死记硬背，遇到不懂的再查。用多了自然就记住了。

### Q: 有些术语看起来很相似，怎么区分？
**A**: 查看对比部分，如：
- QA vs QC
- Validation vs Verification
- Alpha vs Beta Testing

### Q: 如何快速查找？
**A**:
1. 使用浏览器搜索（Ctrl+F）
2. 按字母索引定位
3. 查看相关术语

---

## 术语更新
### 新增术语
如果你发现新的术语或更好的解释，欢迎贡献！

### 术语反馈
- 哪些术语最常用？
- 哪些解释不清楚？
- 需要添加哪些新术语？

---

**版本**：v1.0
**最后更新**：2026-01-01
**维护者**：文档团队

---

**返回目录**：[README](../tracks/qa/TRACK.md)
