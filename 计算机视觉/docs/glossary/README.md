# 计算机视觉术语表

> **快速查找**: 按字母索引查找核心概念和术语

---

## 使用说明

本术语表包含计算机视觉领域的核心概念和技术术语，帮助你快速理解文档中遇到的专业词汇。

---

## A

### Activation Function (激活函数)
- **英文**: Activation Function
- **定义**: 引入非线性变换的函数，使神经网络能够学习复杂的模式
- **难度**: ⭐⭐☆☆☆
- **常见类型**: ReLU, Sigmoid, Tanh, Softmax, Leaky ReLU
- **参考章节**: [深度学习基础](../../04-深度学习基础/README.md)

### AlexNet
- **英文**: AlexNet
- **定义**: 2012年ImageNet竞赛冠军CNN架构，8层深度网络，首次使用ReLU和Dropout
- **难度**: ⭐⭐⭐☆☆
- **相关**: [VGG](#vgg), [ResNet](#resnet)
- **参考章节**: [CNN架构](../../05-CNN架构/README.md)

### Anchors (锚框)
- **英文**: Anchor Boxes
- **定义**: 目标检测中预先定义的一组候选框，用于预测物体位置
- **难度**: ⭐⭐⭐☆☆
- **应用**: YOLO, SSD, Faster R-CNN
- **参考章节**: [目标检测](../../06-目标检测/README.md)

### Attention (注意力机制)
- **英文**: Attention Mechanism
- **定义**: 模拟人类视觉注意力，让模型聚焦于输入中的重要部分
- **难度**: ⭐⭐⭐⭐☆
- **类型**: Self-Attention, Cross-Attention, Multi-Head Attention
- **参考章节**: [注意力机制](../../08-注意力机制/README.md)

### Augmentation (数据增强)
- **英文**: Data Augmentation
- **定义**: 通过对训练数据进行变换（旋转、裁剪、翻转等）来增加数据多样性
- **难度**: ⭐⭐☆☆☆
- **目的**: 防止过拟合，提高模型泛化能力
- **参考章节**: [数据处理](../../03-图像基础/README.md)

---

## B

### Backbone (骨干网络)
- **英文**: Backbone Network
- **定义**: 特征提取网络，通常使用预训练的CNN（如ResNet）
- **难度**: ⭐⭐☆☆☆
- **应用**: 目标检测、图像分割、姿态估计
- **参考章节**: [CNN架构](../../05-CNN架构/README.md)

### Batch Normalization (批归一化)
- **英文**: Batch Normalization
- **定义**: 标准化每层输入的激活值，加速训练，提高稳定性
- **难度**: ⭐⭐⭐☆☆
- **公式**: $$\hat{x} = \frac{x - \mu}{\sqrt{\sigma^2 + \epsilon}}$$
- **参考章节**: [深度学习基础](../../04-深度学习基础/README.md)

### Bias (偏置)
- **英文**: Bias
- **定义**: 神经网络中每个神经元的一个额外参数，允许激活函数左右平移
- **难度**: ⭐☆☆☆☆
- **作用**: 增加模型灵活性
- **参考章节**: [深度学习基础](../../04-深度学习基础/README.md)

### Bounding Box (边界框)
- **英文**: Bounding Box
- **定义**: 用于标定目标位置的矩形框，通常表示为(x, y, width, height)或(x1, y1, x2, y2)
- **难度**: ⭐⭐☆☆☆
- **应用**: 目标检测、目标跟踪
- **参考章节**: [目标检测](../../06-目标检测/README.md)

---

## C

### CNN (卷积神经网络)
- **英文**: Convolutional Neural Network
- **定义**: 专门处理网格数据（如图像）的神经网络，通过卷积层提取特征
- **难度**: ⭐⭐⭐☆☆
- **核心组件**: 卷积层、池化层、激活函数、全连接层
- **参考章节**: [CNN架构](../../05-CNN架构/README.md)

### Confidence (置信度)
- **英文**: Confidence Score
- **定义**: 模型对预测结果的确定程度，通常用概率值表示（0-1）
- **难度**: ⭐⭐☆☆☆
- **应用**: 目标检测、分类任务
- **参考章节**: [目标检测](../../06-目标检测/README.md)

### Convolution (卷积)
- **英文**: Convolution
- **定义**: 通过滑动滤波器（核）在输入上提取特征的操作
- **难度**: ⭐⭐⭐☆☆
- **参数**: Kernel Size, Stride, Padding
- **参考章节**: [CNN架构](../../05-CNN架构/README.md)

### Confusion Matrix (混淆矩阵)
- **英文**: Confusion Matrix
- **定义**: 分类模型性能评估表格，显示TP, TN, FP, FN
- **难度**: ⭐⭐☆☆☆
- **用途**: 计算精确率、召回率、F1分数

### Cost Function (代价函数)
- **英文**: Cost Function
- **定义**: 衡量模型预测与真实标签差异的函数，也称为损失函数
- **难度**: ⭐⭐⭐☆☆
- **类型**: MSE, Cross-Entropy, Hinge Loss
- **参考章节**: [深度学习基础](../../04-深度学习基础/README.md)

---

## D

### Dataset (数据集)
- **英文**: Dataset
- **定义**: 用于训练和测试模型的数据集合，通常分为训练集、验证集和测试集
- **难度**: ⭐☆☆☆☆
- **常见数据集**: ImageNet, COCO, Pascal VOC, CIFAR
- **参考章节**: [图像基础](../../03-图像基础/README.md)

### Dense Layer (全连接层)
- **英文**: Dense Layer / Fully Connected Layer
- **定义**: 每个神经元都与上一层的所有神经元连接的层
- **难度**: ⭐⭐☆☆☆
- **用途**: 分类、回归等最终输出层
- **参考章节**: [CNN架构](../../05-CNN架构/README.md)

### Dropout
- **英文**: Dropout
- **定义**: 训练时随机丢弃部分神经元，防止过拟合的正则化技术
- **难度**: ⭐⭐☆☆☆
- **典型丢弃率**: 0.2-0.5
- **参考章节**: [深度学习基础](../../04-深度学习基础/README.md)

---

## E

### Epoch (训练轮数)
- **英文**: Epoch
- **定义**: 完整遍历整个训练数据集一次
- **难度**: ⭐☆☆☆☆
- **区别**: Epoch vs Batch vs Iteration
- **参考章节**: [深度学习基础](../../04-深度学习基础/README.md)

### Evaluation (评估)
- **英文**: Model Evaluation
- **定义**: 使用测试数据集评估模型性能的过程
- **难度**: ⭐⭐☆☆☆
- **指标**: Accuracy, Precision, Recall, F1, mAP
- **参考章节**: [深度学习基础](../../04-深度学习基础/README.md)

---

## F

### Feature Map (特征图)
- **英文**: Feature Map
- **定义**: 卷积层输出的三维张量，包含提取的空间特征信息
- **难度**: ⭐⭐☆☆☆
- **维度**: (Height × Width × Channels)
- **参考章节**: [CNN架构](../../05-CNN架构/README.md)

### FC Layer (全连接层)
- **英文**: Fully Connected Layer
- **定义**: 见 [Dense Layer](#dense-layer-全连接层)
- **难度**: ⭐⭐☆☆☆
- **参考章节**: [CNN架构](../../05-CNN架构/README.md)

### Fine-tuning (微调)
- **英文**: Fine-tuning
- **定义**: 在预训练模型基础上进行少量训练以适应新任务
- **难度**: ⭐⭐⭐☆☆
- **优势**: 节省训练时间，提高性能
- **参考章节**: [迁移学习](../../10-迁移学习/README.md)

### Focal Loss
- **英文**: Focal Loss
- **定义**: 解决类别不平衡问题的损失函数，聚焦于难分类样本
- **难度**: ⭐⭐⭐⭐☆
- **公式**: $$FL(p_t) = -\alpha_t(1-p_t)^\gamma \log(p_t)$$
- **应用**: 目标检测、单阶段检测器
- **参考章节**: [目标检测](../../06-目标检测/README.md)

---

## G

### Gradient (梯度)
- **英文**: Gradient
- **定义**: 函数变化最快的方向，用于优化算法中更新参数
- **难度**: ⭐⭐☆☆☆
- **计算**: 反向传播算法
- **参考章节**: [深度学习基础](../../04-深度学习基础/README.md)

### Ground Truth (真值)
- **英文**: Ground Truth
- **定义**: 数据的真实标签或标注，用于监督学习
- **难度**: ⭐☆☆☆☆
- **用途**: 训练模型、计算损失
- **参考章节**: [图像基础](../../03-图像基础/README.md)

---

## I

### IoU (交并比)
- **英文**: Intersection over Union
- **定义**: 两个边界框重叠面积与联合面积的比值，用于评估定位精度
- **难度**: ⭐⭐☆☆☆
- **公式**: $$IoU = \frac{Area(A \cap B)}{Area(A \cup B)}$$
- **参考章节**: [目标检测](../../06-目标检测/README.md)

### Inference (推理)
- **英文**: Inference
- **定义**: 使用训练好的模型对新数据进行预测的过程
- **难度**: ⭐⭐☆☆☆
- **区别**: Training vs Inference
- **参考章节**: [模型部署](../../11-模型部署/README.md)

---

## L

### Learning Rate (学习率)
- **英文**: Learning Rate
- **定义**: 控制参数更新步长的超参数
- **难度**: ⭐⭐☆☆☆
- **典型值**: 0.001, 0.0001
- **策略**: 学习率衰减、Warmup
- **参考章节**: [深度学习基础](../../04-深度学习基础/README.md)

### Loss Function (损失函数)
- **英文**: Loss Function
- **定义**: 见 [Cost Function](#cost-function-代价函数)
- **难度**: ⭐⭐⭐☆☆
- **参考章节**: [深度学习基础](../../04-深度学习基础/README.md)

### LSTM (长短期记忆网络)
- **英文**: Long Short-Term Memory
- **定义**: 能够学习长期依赖关系的循环神经网络变体
- **难度**: ⭐⭐⭐⭐☆
- **应用**: 视频分析、序列标注
- **参考章节**: [循环神经网络](../../09-序列模型/README.md)

---

## M

### MSE (均方误差)
- **英文**: Mean Squared Error
- **定义**: 预测值与真实值差值平方的平均值
- **难度**: ⭐⭐☆☆☆
- **公式**: $$MSE = \frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2$$
- **应用**: 回归任务
- **参考章节**: [深度学习基础](../../04-深度学习基础/README.md)

### Momentum (动量)
- **英文**: Momentum
- **定义**: 优化算法中使用历史梯度信息加速收敛的技术
- **难度**: ⭐⭐⭐☆☆
- **优势**: 加速收敛、减少震荡
- **参考章节**: [深度学习基础](../../04-深度学习基础/README.md)

---

## N

### Normalization (归一化)
- **英文**: Normalization
- **定义**: 将数据缩放到标准范围（通常[0,1]或[-1,1]）的过程
- **难度**: ⭐⭐☆☆☆
- **方法**: Min-Max, Z-score, Batch Norm, Layer Norm
- **参考章节**: [深度学习基础](../../04-深度学习基础/README.md)

---

## O

### Overfitting (过拟合)
- **英文**: Overfitting
- **定义**: 模型在训练集上表现很好，但在测试集上表现差的现象
- **难度**: ⭐⭐☆☆☆
- **解决方法**: Dropout, 正则化, 数据增强
- **参考章节**: [深度学习基础](../../04-深度学习基础/README.md)

### Optimizer (优化器)
- **英文**: Optimizer
- **定义**: 根据梯度更新模型参数的算法
- **难度**: ⭐⭐⭐☆☆
- **常见类型**: SGD, Adam, RMSprop, AdaGrad
- **参考章节**: [深度学习基础](../../04-深度学习基础/README.md)

---

## P

### Pooling (池化)
- **英文**: Pooling
- **定义**: 降低特征图空间维度的操作，减少参数和计算量
- **难度**: ⭐⭐☆☆☆
- **类型**: Max Pooling, Average Pooling, Global Pooling
- **参考章节**: [CNN架构](../../05-CNN架构/README.md)

### Precision (精确率)
- **英文**: Precision
- **定义**: 预测为正类的样本中真正为正类的比例
- **难度**: ⭐⭐☆☆☆
- **公式**: $$Precision = \frac{TP}{TP + FP}$$
- **参考章节**: [评估指标](../metrics/README.md)

### Preprocessing (预处理)
- **英文**: Preprocessing
- **定义**: 在输入模型之前对数据进行清洗和转换的操作
- **难度**: ⭐⭐☆☆☆
- **步骤**: 归一化, 调整大小, 颜色转换
- **参考章节**: [图像基础](../../03-图像基础/README.md)

### PR Curve (精确率-召回率曲线)
- **英文**: Precision-Recall Curve
- **定义**: 不同阈值下精确率和召回率之间关系的可视化曲线
- **难度**: ⭐⭐⭐☆☆
- **用途**: 评估分类器性能、选择最优阈值
- **参考章节**: [评估指标](../metrics/README.md)

---

## R

### Recall (召回率)
- **英文**: Recall / Sensitivity
- **定义**: 真正为正类的样本中被正确预测为正类的比例
- **难度**: ⭐⭐☆☆☆
- **公式**: $$Recall = \frac{TP}{TP + FN}$$
- **参考章节**: [评估指标](../metrics/README.md)

### ReLU (线性整流单元)
- **英文**: Rectified Linear Unit
- **定义**: f(x) = max(0, x)，最常用的激活函数
- **难度**: ⭐⭐☆☆☆
- **优势**: 计算简单、缓解梯度消失
- **变体**: Leaky ReLU, PReLU, ELU
- **参考章节**: [深度学习基础](../../04-深度学习基础/README.md)

### ResNet (残差网络)
- **英文**: Residual Network
- **定义**: 使用残差连接解决深层网络训练问题的CNN架构
- **难度**: ⭐⭐⭐⭐☆
- **创新**: 残差块、跳跃连接
- **参考章节**: [CNN架构](../../05-CNN架构/README.md)

### ROI (感兴趣区域)
- **英文**: Region of Interest
- **定义**: 图像中需要特别关注的区域
- **难度**: ⭐⭐☆☆☆
- **应用**: 目标检测、图像分割
- **参考章节**: [目标检测](../../06-目标检测/README.md)

### RPN (区域提议网络)
- **英文**: Region Proposal Network
- **定义**: Faster R-CNN中用于生成候选区域的网络
- **难度**: ⭐⭐⭐⭐☆
- **输出**: 候选框 + 目标概率
- **参考章节**: [目标检测](../../06-目标检测/README.md)

---

## S

### Semantic Segmentation (语义分割)
- **英文**: Semantic Segmentation
- **定义**: 像素级分类任务，为图像中每个像素分配类别标签
- **难度**: ⭐⭐⭐⭐☆
- **区别**: 语义分割 vs 实例分割 vs 全景分割
- **参考章节**: [图像分割](../../07-图像分割/README.md)

### Stride (步长)
- **英文**: Stride
- **定义**: 卷积核或池化窗口在输入上滑动的步距
- **难度**: ⭐⭐☆☆☆
- **影响**: 输出尺寸、下采样倍数
- **参考章节**: [CNN架构](../../05-CNN架构/README.md)

---

## 更多术语持续更新中...

> **注意**: 本术语表正在持续完善中，更多术语将逐步添加。

---

## 参考资源

### 术语表资源
- [斯坦福CS231n术语表](https://cs231n.github.io/)
- [深度学习术语表 - Deep Learning Glossary](https://deeplearning-ai.github.io/)
- [PyTorch官方文档术语](https://pytorch.org/docs/stable/)

### 字典和百科
- [Wikipedia - Computer Vision](https://en.wikipedia.org/wiki/Computer_vision)
- [Machine Learning Glossary - Google AI](https://developers.google.com/machine-learning/glossary)

### 学习资源
- [CS231n: CNNs for Visual Recognition](http://cs231n.stanford.edu/)
- [Fast.ai Practical Deep Learning for Coders](https://course.fast.ai/)
- [PyTorch Tutorials](https://pytorch.org/tutorials/)

---

**返回**: [主目录](../../README.md) | [学习计划](../../学习计划_从入门到精通.md)
