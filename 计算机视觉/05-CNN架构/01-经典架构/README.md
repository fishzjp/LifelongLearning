# 经典CNN架构深度解析 🚀

> **LeNet → AlexNet → VGG → ResNet → DenseNet**
>
> *从CNN开山之作到深度网络革命，掌握架构演进的核心思想*

**版本**: v3.1 | **最后更新**: 2025-12-23 | **难度**: ⭐-⭐⭐⭐⭐

---

## 📚 文档导航

### 🎯 快速开始
- **[架构总览](#📊-快速对比)** - 2分钟了解核心差异
- **[对比与选择指南](./对比与选择指南.md)** - 快速选择适合的架构
- **[学习检查清单](./学习检查清单.md)** - 系统化学习路径

### 📖 详细解析

| 架构 | 年份 | 核心创新 | 参数量 | Top-1准确率 | 文档 |
|------|------|----------|--------|-------------|------|
| **LeNet-5** | 1998 | CNN开山之作 | 61K | 99.2%* | [📖 阅读](./LeNet-5.md) |
| **AlexNet** | 2012 | ReLU/Dropout | 61M | 79.0% | [📖 阅读](./AlexNet.md) |
| **VGGNet** | 2014 | 小卷积堆叠 | 138M | 71.3% | [📖 阅读](./VGGNet.md) |
| **ResNet** | 2015 | 残差连接 | 25.6M | 76.2% | [📖 阅读](./ResNet.md) |
| **DenseNet** | 2016 | 密集连接 | 8.0M | 75.0% | [📖 阅读](./DenseNet.md) |

*LeNet在MNIST上的准确率

### 🎓 学习资源

| 资源类型 | 内容 | 链接 |
|----------|------|------|
| **学习清单** | 系统化学习路径 | [📋 查看](./学习检查清单.md) |
| **常见问题** | 调试指南 | [🔧 查看](./常见问题与调试.md) |
| **实践项目** | 完整代码示例 | [🚀 查看](./实践项目.md) |
| **扩展资源** | 论文/课程/工具 | [📚 查看](./扩展学习资源.md) |

---

## 🎯 学习路径建议

### 📅 推荐学习计划（4周）

#### **第1周：基础理解**
```
Day 1-2: 阅读README + LeNet-5
  └─ 目标：理解CNN基础概念
  └─ 实践：手写LeNet-5，训练MNIST

Day 3-4: AlexNet
  └─ 目标：理解深度学习突破点
  └─ 实践：实现AlexNet，理解ReLU/Dropout

Day 5-7: VGGNet
  └─ 目标：理解深度探索
  └─ 实践：计算感受野，对比参数量
```

#### **第2周：深度网络**
```
Day 8-10: ResNet
  └─ 目标：掌握残差连接
  └─ 实践：实现ResNet50，分析梯度流动

Day 11-14: DenseNet
  └─ 目标：理解特征复用
  └─ 实践：对比ResNet vs DenseNet
```

#### **第3周：实践项目**
```
项目1: CIFAR-10对比实验
  └─ 训练所有架构，生成对比报告

项目2: 架构修改实验
  └─ 测试残差连接、通道数、增长率的影响
```

#### **第4周：进阶应用**
```
项目3: 迁移学习
  └─ 使用预训练模型，不同微调策略

项目4: 性能分析
  └─ 参数量、计算量、推理速度测试

项目5: 模型优化
  └─ 量化、蒸馏、部署
```

### 🎯 每日学习建议（2周速成）

**每日1-2小时**：
- 30分钟：阅读理论文档
- 30分钟：手写代码实现
- 30分钟：运行实验，观察结果

---

## 📊 快速对比

### 📈 性能对比 (ImageNet Top-1)

| 架构 | 准确率 | 参数量 | 计算量 | 推荐指数 |
|------|--------|--------|--------|----------|
| **LeNet-5** | 99.2%* | 61K | 0.4M | ⭐⭐ |
| **AlexNet** | 79.0% | 61M | 0.72G | ⭐⭐⭐ |
| **VGG16** | 71.3% | 138M | 15.3G | ⭐⭐ |
| **ResNet18** | 70.8% | 11.7M | 1.8G | ⭐⭐⭐ |
| **ResNet50** | 76.2% | 25.6M | 3.9G | ⭐⭐⭐⭐⭐ |
| **ResNet152** | 78.3% | 60.2M | 11.5G | ⭐⭐⭐⭐ |
| **DenseNet121** | 75.0% | 8.0M | 2.9G | ⭐⭐⭐⭐ |
| **DenseNet201** | 77.3% | 20.0M | 4.3G | ⭐⭐⭐⭐ |

*LeNet在MNIST上的准确率

### 🎯 快速选择指南

**新手入门** → **ResNet18**  
理由：参数少、训练快、文档丰富

**工业项目** → **ResNet50**  
理由：最佳平衡、社区支持好、易于部署

**移动端** → **MobileNetV2**  
理由：轻量高效（参考扩展资源）

**高精度** → **ResNet101/152**  
理由：深度够、性能好

**医学图像** → **DenseNet121**  
理由：特征复用重要

### 📊 可视化对比

```
参数量 (对数尺度) vs 准确率
↑ 准确率
90%│
   │      ● DenseNet201 (77.3%)
80%│  ● ResNet152 (78.3%)
   │      ● ResNet50 (76.2%)
70%│  ● AlexNet (79.0%)    ● ResNet18 (70.8%)
   │      ● VGG16 (71.3%)
60%│          ● LeNet (99.2%)
   └────────────────────────────→ 参数量
       10K   100K   1M     10M    100M
```

**结论**：ResNet50在参数量和准确率之间达到最佳平衡

---

## 🚀 快速开始（5分钟上手）

### 1️⃣ 加载预训练模型（推荐）

```python
import torch
import torchvision.models as models
import torch.nn as nn

# 方式1: PyTorch官方（最简单）
model = models.resnet50(pretrained=True)

# 方式2: timm库（模型更多）
import timm
model = timm.create_model('resnet50', pretrained=True)

# 方式3: 自定义实现（学习用）
from resnet import ResNet50
model = ResNet50(num_classes=10)

print(f"模型参数量: {sum(p.numel() for p in model.parameters()) / 1e6:.2f}M")
```

### 2️⃣ 迁移学习（最常用）

```python
# 步骤1: 加载预训练模型
model = models.resnet50(pretrained=True)

# 步骤2: 修改分类头
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, num_classes)  # 改为你的类别数

# 步骤3: 冻结特征提取器（小数据集）
for param in model.parameters():
    param.requires_grad = False
model.fc.requires_grad = True  # 只训练最后一层

# 步骤4: 优化器（只优化可训练参数）
optimizer = torch.optim.Adam(
    filter(lambda p: p.requires_grad, model.parameters()), 
    lr=0.001
)

# 步骤5: 训练循环
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

for epoch in range(num_epochs):
    model.train()
    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
```

### 3️⃣ 完整训练示例

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# 1. 数据准备
transform = transforms.Compose([
    transforms.Resize(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

train_dataset = datasets.CIFAR10('./data', train=True, download=True, transform=transform)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# 2. 模型准备
model = models.resnet50(pretrained=True)
model.fc = nn.Linear(model.fc.in_features, 10)

# 3. 训练配置
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 4. 训练
for epoch in range(10):
    model.train()
    total_loss = 0
    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
    
    print(f"Epoch {epoch+1}: Loss = {total_loss/len(train_loader):.4f}")

# 5. 保存模型
torch.save(model.state_dict(), 'best_model.pth')
```

### 4️⃣ 快速测试

```python
# 加载模型
model = models.resnet50(pretrained=True)
model.eval()

# 随机输入测试
x = torch.randn(1, 3, 224, 224)
with torch.no_grad():
    output = model(x)
    print(f"输出形状: {output.shape}")
    print(f"预测类别: {output.argmax().item()}")
```

---

## 📈 性能基准

### CIFAR-10 准确率
| 模型 | 准确率 | 参数量 | 训练时间 |
|------|--------|--------|----------|
| LeNet-5 | 70% | 61K | 快 |
| AlexNet | 80% | 61M | 中等 |
| VGG16 | 85% | 138M | 慢 |
| ResNet18 | 88% | 11.7M | 中等 |
| DenseNet121 | 89% | 8.0M | 中等 |

### 推荐指数
- ⭐⭐⭐⭐⭐ **ResNet50** - 最佳平衡
- ⭐⭐⭐⭐ **DenseNet121** - 参数效率高
- ⭐⭐⭐ **ResNet18** - 快速原型
- ⭐⭐ **AlexNet** - 学习基础
- ⭐⭐ **VGG16** - 迁移学习
- ⭐ **LeNet-5** - 教学用途

---

## 🔧 常见问题

### 训练问题
- **LeNet不收敛** → 检查学习率和数据标准化
- **VGG训练慢** → 使用预训练+冻结
- **ResNet梯度爆炸** → 添加梯度裁剪
- **DenseNet内存溢出** → 减小batch_size

### 架构问题
- **残差连接维度不匹配** → 使用shortcut调整
- **DenseNet通道爆炸** → 使用TransitionLayer

**详细解决方案**: [查看调试指南](./常见问题与调试.md)

---

## 📝 实践项目

### 项目1: 架构复现与对比
- 在CIFAR-10上训练所有架构
- 对比准确率、参数量、训练速度
- 生成可视化报告

### 项目2: 架构修改实验
- 测试残差连接的影响
- 调整通道数和增长率
- 理解各组件作用

### 项目3: 迁移学习实战
- 使用预训练模型
- 不同微调策略对比
- 部署到实际应用

**完整代码**: [查看实践项目](./实践项目.md)

---

## 📚 扩展学习

### 必读论文
1. LeNet-5 (1998) - CNN基础
2. AlexNet (2012) - 深度学习引爆点
3. VGG (2014) - 深度探索
4. ResNet (2015) - 残差学习
5. DenseNet (2016) - 特征复用

### 推荐资源
- **课程**: CS231n, Deep Learning Specialization
- **库**: PyTorch Vision, timm
- **工具**: torchviz, TensorBoard, Netron

**详细资源**: [查看扩展学习资源.md](./扩展学习资源.md)

---

## 💡 学习建议

### ✅ 应该做的
- [ ] 手写实现每个架构
- [ ] 在CIFAR-10上训练对比
- [ ] 阅读原始论文
- [ ] 理解数学原理
- [ ] 实践迁移学习

### ❌ 避免的
- [ ] 只看不练
- [ ] 跳过基础直接复杂架构
- [ ] 不理解就调参
- [ ] 忽视数据预处理
- [ ] 不记录实验结果

---

## 🎯 选择指南

### 我应该用哪个？

**快速决策**:
- **新手入门**: ResNet18
- **工业项目**: ResNet50
- **移动端**: MobileNetV2
- **高精度**: ResNet101/DenseNet201
- **医学图像**: DenseNet121
- **学术研究**: ResNet50

**详细决策树**: [查看对比指南](./对比与选择指南.md)

---

## 🤝 贡献指南

欢迎贡献！
- 发现错误 → 提交Issue
- 有改进建议 → 提交PR
- 想分享项目 → 添加到实践项目
- 发现好资源 → 更新扩展资源

---

## 🔗 相关链接

- [计算机视觉主页](../README.md)
- [学习计划](../学习计划_从入门到精通.md)
- [参考资料](../参考资料/README.md)

---

**祝你学习愉快！** 🚀

如有问题，欢迎在对应文档中提出Issue或PR。
