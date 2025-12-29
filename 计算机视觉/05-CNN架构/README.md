# 第五章：卷积神经网络架构

> 系统学习CNN经典架构与现代设计，从LeNet到Vision Transformer

## 📚 快速导航

| 章节 | 内容 | 难度 |
|------|------|------|
| **[01-经典架构](01-经典架构.md)** | LeNet, AlexNet, VGG, ResNet, DenseNet | ⭐-⭐⭐⭐ |
| **[02-高效架构](02-高效架构.md)** | MobileNet, EfficientNet, GhostNet, ShuffleNet | ⭐⭐-⭐⭐⭐ |
| **[03-注意力机制](03-注意力机制.md)** | SE-Net, CBAM, ConvNeXt, Swin, ViT | ⭐⭐⭐-⭐⭐⭐⭐⭐ |
| **[04-架构对比与选择](04-架构对比与选择指南.md)** | 性能对比、选择决策树、场景推荐 | ⭐⭐⭐ |
| **[05-实践项目](05-实践项目.md)** | 完整训练pipeline、对比实验、压缩技术 | ⭐⭐⭐⭐ |
| **[06-调试与优化](06-调试与优化.md)** | 训练诊断、性能监控、部署优化 | ⭐⭐⭐⭐ |

---

## 📖 内容概览

### 1. 经典架构演进

- **LeNet-5** (1998): CNN开山之作
- **AlexNet** (2012): 深度学习引爆点
- **VGG** (2014): 深度=性能
- **ResNet** (2015): 残差连接（里程碑）
- **DenseNet** (2016): 密集连接

### 2. 现代高效架构

- **MobileNet系列**: 深度可分离卷积
- **EfficientNet**: 复合缩放策略
- **ShuffleNet**: 通道混洗
- **GhostNet**: Ghost模块设计

### 3. 注意力机制与Transformer

- **SE-Net**: 通道注意力
- **CBAM**: 通道+空间注意力
- **ConvNeXt**: 现代CNN
- **Swin Transformer**: 分层Transformer
- **Vision Transformer**: Transformer视觉

---

## 🎯 学习路径建议

### 阶段一：经典架构（2-3天）

1. 学习LeNet、AlexNet、VGG的基础概念
2. 深入理解ResNet的残差连接
3. 掌握DenseNet的特征复用

### 阶段二：高效架构（2-3天）

1. 理解深度可分离卷积
2. 学习复合缩放策略
3. 掌握通道混洗和Ghost模块

### 阶段三：注意力机制（2-3天）

1. 理解注意力机制原理
2. 学习Transformer在视觉中的应用
3. 掌握现代CNN设计

### 阶段四：实践应用（3-4天）

1. 完成架构对比实验
2. 设计自定义架构
3. 进行模型压缩和部署

---

## 🚀 快速开始

### 1. 选择合适架构

```bash
# 根据场景选择

from 04-架构对比与选择指南 import choose_architecture

recommendations = choose_architecture(
    task_type='classification',
    hardware='mobile',
    data_size='medium',
    accuracy_req='high',
    latency_req=30
)
```

### 2. 加载预训练模型

```python
from torchvision.models import resnet50, mobilenet_v2

# 经典架构

model = resnet50(weights='DEFAULT')

# 高效架构

model = mobilenet_v2(weights='DEFAULT')
```

### 3. 完整训练流程

```bash
# 参考 05-实践项目.py

from 05-实践项目 import TrainingPipeline

pipeline = TrainingPipeline(model, train_loader, val_loader)
best_acc = pipeline.train()
```

---

## 📊 架构对比速查

| 架构 | 参数量 | 计算量 | Top-1 | 适用场景 |
|------|--------|--------|-------|----------|
| LeNet-5 | 0.06M | 0.4M | 99.2% | 手写数字 |
| ResNet50 | 25.6M | 3.9G | 76.2% | 通用深度 |
| MobileNetV2 | 3.4M | 0.3G | 72.0% | 移动端 |
| EfficientNet-B0 | 5.3M | 0.39G | 77.1% | 高效通用 |
| ConvNeXt-T | 29M | 4.5G | 82.1% | 高精度 |
| ViT-Base | 86.6M | 17.6G | 81.8% | 大数据 |

---

## 🛠️ 实用工具

### 架构复杂度分析

```python
from 06-调试与优化 import analyze_architecture_complexity

metrics = analyze_architecture_complexity(model)
# 输出: 参数量、计算量、内存占用、层数统计

```

### 训练过程监控

```python
from 06-调试与优化 import TrainingMonitor

monitor = TrainingMonitor(model, log_dir='./logs')
# 自动记录指标、早停、保存最佳模型

```

### 模型量化部署

```python
from 06-调试与优化 import quantize_model, export_to_onnx

# 量化压缩

quantized = quantize_model(model, calibration_loader)

# ONNX导出

export_to_onnx(model, (3, 224, 224), 'model.onnx')
```

---

## 📈 性能基准

### 经典架构对比

| 架构 | 参数量(M) | 计算量(G) | Top-1 | 核心创新 |
|------|-----------|-----------|-------|----------|
| LeNet-5 | 0.06 | 0.0004 | 99.2% | CNN开山 |
| AlexNet | 61.1 | 0.72 | 79.0% | ReLU/Dropout |
| VGG16 | 138.4 | 15.3 | 71.3% | 小卷积堆叠 |
| ResNet50 | 25.6 | 3.9 | 76.2% | 残差连接 |
| DenseNet121 | 8.0 | 2.9 | 75.0% | 密集连接 |

### 高效架构对比

| 架构 | 参数量(M) | 计算量(G) | Top-1 | 核心创新 |
|------|-----------|-----------|-------|----------|
| SqueezeNet | 4.8 | 0.7 | 58.0% | 极致轻量 |
| MobileNetV2 | 3.4 | 0.3 | 72.0% | 深度可分离 |
| GhostNet | 5.2 | 0.3 | 75.7% | Ghost模块 |
| EfficientNet-B0 | 5.3 | 0.39 | 77.1% | 复合缩放 |

### 现代架构对比

| 架构 | 参数量(M) | 计算量(G) | Top-1 | 核心创新 |
|------|-----------|-----------|-------|----------|
| ConvNeXt-T | 29 | 4.5 | 82.1% | 现代CNN |
| Swin-Tiny | 29 | 4.5 | 81.2% | 分层Transformer |
| ViT-Base | 86.6 | 17.6 | 81.8% | Transformer |

---

## 🎯 实践项目

### 项目1: 架构对比实验

**目标**: 在CIFAR-10上对比不同架构  
**代码**: [05-实践项目.md](05-实践项目.md) - 项目1  
**指标**: 准确率、参数量、推理速度

### 项目2: 自定义架构设计

**目标**: 设计参数量<5M，准确率>85%的模型  
**代码**: [05-实践项目.md](05-实践项目.md) - 项目2  
**技术**: 深度可分离 + 瓶颈 + 注意力

### 项目3: 迁移学习对比

**目标**: 对比预训练模型的迁移效果  
**代码**: [05-实践项目.md](05-实践项目.md) - 项目3  
**数据**: 自定义小数据集

### 项目4: 模型压缩

**目标**: 量化、剪枝、知识蒸馏  
**代码**: [05-实践项目.md](05-实践项目.md) - 项目4  
**指标**: 模型大小、速度、精度

---

## 🔧 调试与优化

### 常见问题

1. **训练不收敛**: 检查学习率、损失函数、数据预处理
2. **过拟合**: 增加Dropout、权重衰减、数据增强
3. **梯度问题**: 梯度裁剪、BatchNorm、残差连接
4. **内存不足**: 减小batch_size、混合精度、梯度检查点
5. **训练慢**: GPU加速、多进程、混合精度

### 诊断工具

```python
from 06-调试与优化 import TrainingDiagnostics

diagnostics = TrainingDiagnostics(model)
issues = diagnostics.full_diagnosis(val_loader)
# 自动诊断梯度、激活、权重分布

```

---

## 📖 扩展资源

### 经典论文

1. **LeNet-5**: "Gradient-Based Learning Applied to Document Recognition" (1998)
2. **AlexNet**: "ImageNet Classification with Deep Convolutional Neural Networks" (2012)
3. **VGG**: "Very Deep Convolutional Networks for Large-Scale Image Recognition" (2014)
4. **ResNet**: "Deep Residual Learning for Image Recognition" (2015)
5. **ViT**: "An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale" (2020)

### 开源实现

- **PyTorch官方**: `torchvision.models`
- **timm库**: 丰富的预训练模型
- **MMDetection**: 目标检测工具箱

---

## 🏆 学习检查清单

### 理解层面

- [ ] 能解释每个架构的核心创新点
- [ ] 理解残差连接的作用原理
- [ ] 掌握深度可分离卷积的计算优势
- [ ] 了解注意力机制的工作方式
- [ ] 能根据场景选择合适架构

### 实践层面

- [ ] 能独立实现每个架构
- [ ] 会修改架构适应不同任务
- [ ] 能调试架构训练问题
- [ ] 掌握模型压缩技术
- [ ] 会进行架构性能对比
- [ ] 能使用预训练模型进行迁移学习
- [ ] 会进行模型量化和部署
- [ ] 能编写完整的训练pipeline

### 项目实战

- [ ] 在MNIST/CIFAR上复现至少3个架构
- [ ] 完成端到端的架构对比实验
- [ ] 设计并实现自定义轻量级架构
- [ ] 将模型部署到移动端或Web服务
- [ ] 参加Kaggle竞赛应用CNN架构

---

## 🚀 下一步学习

完成本章后，你可以继续学习：

### 06-目标检测

- 两阶段检测器：R-CNN系列
- 单阶段检测器：YOLO系列
- 检测评估指标

### 07-图像分割

- 语义分割：U-Net、DeepLab
- 实例分割：Mask R-CNN
- 医学图像应用

### 08-姿态估计

- OpenPose、HRNet
- 关键点检测
- 3D姿态估计

---

## 📋 快速参考

### 架构选择速查表

| 场景 | 首选 | 备选 | 避免 |
|------|------|------|------|
| **快速原型** | ResNet18 | MobileNetV2 | ViT |
| **移动端** | MobileNetV3 | GhostNet | VGG |
| **高精度** | ConvNeXt | EfficientNet-B7 | LeNet |
| **实时检测** | YOLOv8n | SSD-MobileNet | Faster R-CNN |
| **医学影像** | DenseNet121 | U-Net++ | AlexNet |
| **小数据集** | ResNet50 | DenseNet121 | ViT |
| **边缘设备** | SqueezeNet | MobileNetV2 | ResNet101 |

### 常用代码片段

```bash
# 1. 快速加载预训练模型

from torchvision.models import resnet50
model = resnet50(weights='DEFAULT')

# 2. 冻结/解冻层

for param in model.parameters():
    param.requires_grad = False  # 冻结

# 3. 学习率调度

scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=100)

# 4. 梯度裁剪

torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

# 5. 混合精度训练

scaler = torch.cuda.amp.GradScaler()
with torch.cuda.amp.autocast():
    outputs = model(inputs)
    loss = criterion(outputs, labels)

# 6. 模型保存与加载

torch.save(model.state_dict(), 'model.pth')
model.load_state_dict(torch.load('model.pth'))

# 7. 多GPU训练

if torch.cuda.device_count() > 1:
    model = nn.DataParallel(model)

# 8. 模型量化

model.qconfig = torch.quantization.get_default_qconfig('fbgemm')
model_prepared = torch.quantization.prepare(model)
model_quantized = torch.quantization.convert(model_prepared)
```

---

## 🎯 成就系统

完成本章后，你将获得：
- ✅ **架构理解能力**: 能解释10+种CNN架构的设计思想
- ✅ **实践编码能力**: 独立实现所有经典架构
- ✅ **调试诊断能力**: 快速定位和解决训练问题
- ✅ **架构选择能力**: 根据场景选择最优架构
- ✅ **优化部署能力**: 模型压缩和部署到生产环境

---

## 📅 学习计划

**建议学习时间：1-2周**

### 第1-2天: 经典架构

- 掌握LeNet、AlexNet、VGG
- 理解ResNet残差连接
- 实践：在MNIST上训练这些模型

### 第3-4天: 高效架构

- 学习MobileNet、EfficientNet
- 理解深度可分离卷积
- 实践：对比参数量和计算量

### 第5-6天: 注意力机制

- 研究SE-Net、CBAM
- 学习ViT和Swin Transformer
- 实践：集成注意力到ResNet

### 第7-8天: 架构对比

- 进行系统化对比实验
- 绘制性能曲线
- 分析不同场景的最优选择

### 第9-14天: 实战项目

- 完成完整训练pipeline
- 设计自定义架构
- 进行模型压缩和部署

---

**最后更新：2025年12月**

*本章内容持续更新中，欢迎反馈和贡献！*

---

## 📞 问题反馈

如果在学习过程中遇到问题，可以：
1. 查看 [06-调试与优化.md](06-调试与优化.md) 的常见问题部分
2. 参考 [05-实践项目.md](05-实践项目.md) 的完整代码示例
3. 使用 [04-架构对比与选择指南.md](04-架构对比与选择指南.md) 的决策工具

**祝你学习顺利！🚀**