# 损失函数数学总结

> [03-损失函数与正则化](../tracks/cv/M2/L03-%E6%8D%9F%E5%A4%B1%E4%B8%8E%E6%AD%A3%E5%88%99%E5%8C%96.md)的数学附录：各损失函数的完整推导、导数形式与选择决策树。推导卡住时来查。

---

## 损失函数对比表
| 损失函数 | 公式 | 适用场景 | 优点 | 缺点 |
|---------|------|---------|------|------|
| **MSE** | $\frac{1}{n}\sum(y-\hat{y})^2$ | 回归 | 可导，凸优化 | 对异常值敏感 |
| **MAE** | $\frac{1}{n}\sum|y-\hat{y}|$ | 回归 | 鲁棒 | 零点不可导 |
| **Huber** | 分段定义 | 回归 | 结合MSE/MAE优点 | 需要调参 |
| **BCE** | $-\sum[y\log\hat{y}+(1-y)\log(1-\hat{y})]$ | 二分类 | 概率解释 | - |
| **交叉熵** | $-\sum\sum y\log\hat{y}$ | 多分类 | 概率解释 | - |
| **Focal Loss** | $-\alpha(1-p_t)^\gamma\log(p_t)$ | 类别不平衡 | 聚焦难样本 | 需要调参 |

## 选择决策树
```
问题类型？
├─ 回归
│  ├─ 数据干净 → MSE
│  ├─ 有异常值 → MAE / Huber
│  └─ 需要鲁棒性 → Huber Loss
│
├─ 二分类
│  ├─ 平衡数据 → BCE
│  └─ 不平衡数据 → BCE + 权重 / Focal Loss
│
└─ 多分类
   ├─ 平衡数据 → 交叉熵
   └─ 不平衡数据 → 加权交叉熵 / Focal Loss
```

## 核心数学公式速查
### 1. 回归损失
**MSE（均方误差）：**
$$
\mathcal{L}_{MSE} = \frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2
$$

梯度：
$$
\frac{\partial \mathcal{L}}{\partial \hat{y}_i} = -2(y_i - \hat{y}_i)
$$

**MAE（平均绝对误差）：**
$$
\mathcal{L}_{MAE} = \frac{1}{n}\sum_{i=1}^{n}|y_i - \hat{y}_i|
$$

梯度：
$$
\frac{\partial \mathcal{L}}{\partial \hat{y}_i} = -\text{sign}(y_i - \hat{y}_i)
$$

**Huber Loss：**
$$
\mathcal{L}_{\delta}(y, \hat{y}) = \begin{cases}
\frac{1}{2}(y - \hat{y})^2, & |y - \hat{y}| \leq \delta \\
\delta(|y - \hat{y}| - \frac{1}{2}\delta), & \text{otherwise}
\end{cases}
$$

### 2. 分类损失
**BCE（二元交叉熵）：**
$$
\mathcal{L}_{BCE} = -\frac{1}{n}\sum_{i=1}^{n}[y_i\log(\hat{y}_i) + (1-y_i)\log(1-\hat{y}_i)]
$$

梯度：
$$
\frac{\partial \mathcal{L}}{\partial \hat{y}_i} = \frac{\hat{y}_i - y_i}{\hat{y}_i(1-\hat{y}_i)}
$$

**CCE（多分类交叉熵）：**
$$
\mathcal{L}_{CCE} = -\sum_{i=1}^{n}\sum_{c=1}^{C} y_{i,c}\log(\hat{y}_{i,c})
$$

梯度（Softmax + CCE）：
$$
\frac{\partial \mathcal{L}}{\partial z_c} = \hat{y}_c - y_c
$$

**Focal Loss：**
$$
\mathcal{L}_{FL} = -\alpha_t(1-p_t)^\gamma\log(p_t)
$$

其中：
$$
p_t = \begin{cases}
\hat{y}, & y=1 \\
1-\hat{y}, & y=0
\end{cases}
$$

## 实践建议
### 1. 数值稳定性
**问题：** $\log(0)$ 导致数值溢出

**解决方案：** 添加小的epsilon
```python
epsilon = 1e-10
y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
loss = -np.sum(y_true * np.log(y_pred))
```

### 2. 梯度裁剪
防止梯度爆炸：
```python
grad_norm = np.linalg.norm(grad)
if grad_norm > max_norm:
    grad = grad * max_norm / grad_norm
```

### 3. 损失函数组合
例如，在目标检测中：
$$
\mathcal{L} = \mathcal{L}_{cls} + \lambda \mathcal{L}_{reg}
$$

其中：
- $\mathcal{L}_{cls}$：分类损失（如Focal Loss）
- $\mathcal{L}_{reg}$：回归损失（如Smooth L1）
- $\lambda$：平衡系数

### 4. 类别不平衡处理
**方法1：加权损失**
```python
class_weights = {0: 1.0, 1: 10.0}  # 正样本权重更大
loss = -sum(w[c] * y[c] * log(y_pred[c]) for c in classes)
```

**方法2：Focal Loss**
```python
# 自动聚焦难分类样本
focal_loss = -(1 - p_t)**gamma * log(p_t)
```

**方法3：采样**
```python
# 过采样少数类或欠采样多数类
```

## 性能对比
### 回归损失对比
```python

# 依赖: matplotlib, numpy
# 安装: pip install matplotlib numpy
import numpy as np
import matplotlib.pyplot as plt

# 测试数据
errors = np.linspace(-5, 5, 100)

mse_loss = errors**2
mae_loss = np.abs(errors)
huber_loss = np.where(np.abs(errors) <= 1, 0.5*errors**2, np.abs(errors)-0.5)

plt.figure(figsize=(10, 6))
plt.plot(errors, mse_loss, label='MSE', linewidth=2)
plt.plot(errors, mae_loss, label='MAE', linewidth=2)
plt.plot(errors, huber_loss, label='Huber (δ=1)', linewidth=2)
plt.xlabel('Error (y - ŷ)')
plt.ylabel('Loss')
plt.title('Regression Loss Functions Comparison')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

**观察：**
- MSE：二次增长，大误差惩罚重
- MAE：线性增长，对异常值鲁棒
- Huber：小误差用MSE，大误差用MAE

### 分类损失对比
```python
# 二分类，y=1
probabilities = np.linspace(0.01, 0.99, 100)

bce_loss = -np.log(probabilities)
focal_loss_gamma1 = -(1-probabilities)**1 * np.log(probabilities)
focal_loss_gamma2 = -(1-probabilities)**2 * np.log(probabilities)

plt.figure(figsize=(10, 6))
plt.plot(probabilities, bce_loss, label='BCE', linewidth=2)
plt.plot(probabilities, focal_loss_gamma1, label='Focal (γ=1)', linewidth=2)
plt.plot(probabilities, focal_loss_gamma2, label='Focal (γ=2)', linewidth=2)
plt.xlabel('Predicted Probability (ŷ)')
plt.ylabel('Loss')
plt.title('Classification Loss Functions Comparison (y=1)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

**观察：**
- BCE：所有样本同等对待
- Focal Loss：降低易分类样本的权重
- γ越大，聚焦效果越明显

## 高级话题
### 1. 损失函数与概率分布的对应
| 损失函数 | 对应的概率分布 | 假设 |
|---------|--------------|------|
| MSE | 高斯分布 | 噪声服从 $\mathcal{N}(0, \sigma^2)$ |
| MAE | 拉普拉斯分布 | 噪声服从 $\text{Laplace}(0, b)$ |
| BCE | 伯努利分布 | 标签服从 $\text{Bernoulli}(p)$ |
| 交叉熵 | 分类分布 | 标签服从 $\text{Categorical}(p)$ |

### 2. 从最大似然推导损失
**步骤：**
1. 假设数据的概率分布
2. 写出似然函数 $L(\theta) = \prod P(y|x;\theta)$
3. 取对数：$\log L(\theta) = \sum \log P(y|x;\theta)$
4. 最大化似然 = 最小化负对数似然

**示例：MSE**

假设 $y = f(x;\theta) + \epsilon$，其中 $\epsilon \sim \mathcal{N}(0, \sigma^2)$

$$
P(y|x;\theta) = \frac{1}{\sqrt{2\pi\sigma^2}}\exp\left(-\frac{(y-f(x;\theta))^2}{2\sigma^2}\right)
$$

$$
\log L(\theta) = \sum \left[-\frac{(y-f(x;\theta))^2}{2\sigma^2} + \text{constant}\right]
$$

$$
-\log L(\theta) = \sum (y-f(x;\theta))^2 + \text{constant}
$$

即MSE！

### 3. 损失函数设计原则
1. **可微性**：便于梯度下降
2. **凸性**：避免局部最优
3. **鲁棒性**：对异常值不敏感
4. **概率解释**：与数据分布一致
5. **计算效率**：易于实现

## 参考资料
1. **信息论**：Cover, T. M. (2006). Elements of Information Theory
2. **Focal Loss**：Lin et al. (2017). Focal Loss for Dense Object Detection
3. **损失函数综述**：Janocha & Czarnecki (2017). On Loss Functions for Deep Neural Networks in Classification

## 练习
### 练习1：推导Huber Loss的梯度
$$
\frac{\partial \mathcal{L}_{\delta}}{\partial \hat{y}} = ?
$$

**提示：** 分段求导

### 练习2：实现加权交叉熵
```python
def weighted_cross_entropy(y_true, y_pred, class_weights):
    """
    y_true: one-hot labels, shape (n_samples, n_classes)
    y_pred: predicted probabilities, shape (n_samples, n_classes)
    class_weights: dict {class_idx: weight}
    """
    # TODO: 实现
    pass
```

### 练习3：对比BCE和Focal Loss在类别不平衡数据上的表现
```python
# 生成不平衡数据
n_samples = 1000
X = np.random.randn(n_samples, 2)
y = np.zeros(n_samples)
y[:100] = 1  # 10% 正样本

# 训练两个模型
# 1. 使用BCE
# 2. 使用Focal Loss
# 对比性能
```

---

**总结：**

选择损失函数的关键是：
1. 理解问题的概率本质
2. 考虑数据的特点（噪声、不平衡等）
3. 平衡理论性质和实践效果
4. 通过实验验证选择

