# 计算机视觉参考资料大全

> 精选的计算机视觉学习资源，包括经典论文、优质教程、开源项目和数据集。按主题分类，便于系统学习。

## 📚 目录结构

```
参考资料/
├── 论文/              # 经典论文列表与解读
├── 教程/              # 在线课程与视频教程
├── 开源项目/          # 优秀GitHub项目
├── 数据集/            # 常用数据集资源
└── 工具库/            # 实用工具和框架
```

---

## 📄 经典论文

### 1. 深度学习基础

| 论文 | 年份 | 核心贡献 | 难度 | 阅读建议 |
|------|------|----------|------|----------|
| **AlexNet** | 2012 | 深度CNN在ImageNet上的突破 | ⭐⭐ | 入门必读 |
| **VGG** | 2014 | 深度=性能，小卷积核堆叠 | ⭐⭐ | 理解架构设计 |
| **ResNet** | 2015 | 残差连接解决退化问题 | ⭐⭐⭐ | 核心创新 |
| **BatchNorm** | 2015 | 加速训练，防止过拟合 | ⭐⭐ | 训练技巧 |

**推荐阅读顺序**：
1. AlexNet → 2. VGG → 3. ResNet → 4. BatchNorm

**论文链接**：
- AlexNet: https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html
- VGG: https://arxiv.org/abs/1409.1556
- ResNet: https://arxiv.org/abs/1512.03385
- BatchNorm: https://arxiv.org/abs/1502.03167

---

### 2. 目标检测

| 论文 | 年份 | 核心贡献 | 难度 | 代码实现 |
|------|------|----------|------|----------|
| **R-CNN** | 2014 | 区域建议 + CNN特征 | ⭐⭐⭐ | [GitHub](https://github.com/rbgirshick/rcnn) |
| **Fast R-CNN** | 2015 | ROI Pooling + 端到端 | ⭐⭐⭐ | [GitHub](https://github.com/rbgirshick/fast-rcnn) |
| **Faster R-CNN** | 2016 | RPN实现端到端检测 | ⭐⭐⭐⭐ | [GitHub](https://github.com/rbgirshick/py-faster-rcnn) |
| **YOLOv1** | 2016 | 单阶段实时检测 | ⭐⭐⭐ | [GitHub](https://github.com/pjreddie/darknet) |
| **SSD** | 2016 | 多尺度默认框 | ⭐⭐⭐ | [GitHub](https://github.com/weiliu89/caffe/tree/ssd) |
| **RetinaNet** | 2017 | Focal Loss解决不平衡 | ⭐⭐⭐⭐ | [GitHub](https://github.com/facebookresearch/Detectron) |

**推荐阅读顺序**：
1. YOLOv1 → 2. SSD → 3. Faster R-CNN → 4. RetinaNet

**代码学习建议**：
- 先运行官方实现
- 逐步调试理解
- 尝试简化版本
- 自己重新实现

---

### 3. 图像分割

| 论文 | 年份 | 核心贡献 | 难度 | 代码实现 |
|------|------|----------|------|----------|
| **FCN** | 2015 | 全卷积网络 | ⭐⭐⭐ | [GitHub](https://github.com/shelhamer/fcn.berkeleyvision.org) |
| **U-Net** | 2015 | 编码器-解码器 + 跳跃连接 | ⭐⭐⭐ | [GitHub](https://github.com/zhixuhao/unet) |
| **DeepLabv1** | 2015 | 空洞卷积 + CRF | ⭐⭐⭐⭐ | [GitHub](https://github.com/speedinghz/DeepLab-ResNet-TensorFlow) |
| **DeepLabv3+** | 2018 | 编码器-解码器 + ASPP | ⭐⭐⭐⭐ | [GitHub](https://github.com/tensorflow/models/tree/master/research/deeplab) |
| **Mask R-CNN** | 2017 | 实例分割 | ⭐⭐⭐⭐⭐ | [GitHub](https://github.com/facebookresearch/maskrcnn-benchmark) |

**推荐阅读顺序**：
1. U-Net → 2. FCN → 3. DeepLabv3+ → 4. Mask R-CNN

**实践建议**：
- 医学图像：从U-Net开始
- 自然图像：从FCN开始
- 实例分割：从Mask R-CNN开始

---

### 4. 现代架构

| 论文 | 年份 | 核心贡献 | 难度 | 应用价值 |
|------|------|----------|------|----------|
| **MobileNetV1** | 2017 | 深度可分离卷积 | ⭐⭐⭐ | 移动端部署 |
| **EfficientNet** | 2019 | 复合缩放 | ⭐⭐⭐⭐ | 高效模型 |
| **Vision Transformer** | 2020 | Transformer用于CV | ⭐⭐⭐⭐⭐ | 前沿研究 |
| **Swin Transformer** | 2021 | 分层Transformer | ⭐⭐⭐⭐⭐ | SOTA性能 |

---

## 📺 优质教程

### 在线课程

#### 1. 斯坦福 CS231n
- **链接**: http://cs231n.stanford.edu/
- **内容**: CNN基础、图像分类、目标检测
- **特点**: 理论深入，作业经典
- **适合**: 有Python基础，想深入理解原理

#### 2. Fast.ai
- **链接**: https://www.fast.ai/
- **内容**: 实用深度学习，从实践到理论
- **特点**: 自顶向下教学，代码驱动
- **适合**: 想快速上手项目的学习者

#### 3. 吴恩达深度学习
- **链接**: https://www.coursera.org/specializations/deep-learning
- **内容**: 神经网络基础、优化算法、CNN
- **特点**: 系统性强，讲解清晰
- **适合**: 零基础系统学习

#### 4. PyTorch官方教程
- **链接**: https://pytorch.org/tutorials/
- **内容**: PyTorch基础、CV应用、生成模型
- **特点**: 官方维护，代码质量高
- **适合**: PyTorch用户

---

### 视频教程

#### B站优质频道

1. **李沐《动手学深度学习》**
   - 链接: https://space.bilibili.com/156774849
   - 特点: 理论+代码，中文讲解
   - 推荐: 深度学习入门

2. **同济子豪兄**
   - 链接: https://space.bilibili.com/1900783
   - 特点: 计算机视觉实战
   - 推荐: YOLO、OpenCV教程

3. **DeepLearningAI**
   - 链接: https://space.bilibili.com/572733062
   - 特点: 吴恩达课程中文版
   - 推荐: 系统学习

#### YouTube优质频道

1. **Aladdin Persson**
   - 链接: https://www.youtube.com/c/AladdinPersson
   - 特点: PyTorch从零实现
   - 推荐: 算法实现

2. **Two Minute Papers**
   - 链接: https://www.youtube.com/c/TwoMinutePapers
   - 特点: 论文速览
   - 推荐: 了解前沿

---

### 书籍推荐

#### 入门书籍

1. **《Python计算机视觉编程》**
   - 作者: Jan Erik Solem
   - 特点: OpenCV实战，代码丰富
   - 适合: 初学者

2. **《深度学习入门：基于Python的理论与实现》**
   - 作者: 斋藤康毅
   - 特点: 从零实现神经网络
   - 适合: 理解底层原理

#### 进阶书籍

3. **《深度学习》（花书）**
   - 作者: Ian Goodfellow
   - 特点: 理论权威，内容全面
   - 适合: 深入研究

4. **《计算机视觉：算法与应用》**
   - 作者: Richard Szeliski
   - 特点: 传统CV权威
   - 适合: 系统学习传统方法

---

## 🛠️ 开源项目

### 1. 综合框架

#### **MMDetection** - 目标检测工具箱
- **链接**: https://github.com/open-mmlab/mmdetection
- **特点**: 模块化设计，支持众多算法
- **使用**: 
  ```bash
  pip install mmdet
  # 配置文件 + 命令行训练
  ```

#### **MMSegmentation** - 图像分割工具箱
- **链接**: https://github.com/open-mmlab/mmsegmentation
- **特点**: 统一接口，易于扩展
- **使用**:
  ```bash
  pip install mmseg
  ```

#### **Detectron2** - Facebook检测框架
- **链接**: https://github.com/facebookresearch/detectron2
- **特点**: PyTorch实现，性能优秀
- **使用**:
  ```python
  from detectron2 import model_zoo
  from detectron2.engine import DefaultPredictor
  ```

---

### 2. 专项项目

#### **YOLOv8** - 最新YOLO实现
- **链接**: https://github.com/ultralytics/ultralytics
- **特点**: 易用性强，支持检测/分割/姿态
- **使用**:
  ```python
  from ultralytics import YOLO
  model = YOLO('yolov8n.pt')
  model.train(data='coco.yaml', epochs=100)
  ```

#### **Segmentation Models** - 分割模型库
- **链接**: https://github.com/qubvel/segmentation_models
- **特点**: 预训练模型，简单API
- **使用**:
  ```python
  import segmentation_models as sm
  model = sm.Unet('resnet34', classes=1)
  ```

#### **OpenMMLab** 系列
- **MMDetection**: 目标检测
- **MMSegmentation**: 语义分割
- **MMAction2**: 视频分析
- **MMPose**: 姿态估计
- **MMEditing**: 图像生成

---

### 3. 实用工具

#### **Albumentations** - 数据增强
- **链接**: https://github.com/albumentations-team/albumentations
- **特点**: 速度快，功能丰富
- **使用**:
  ```python
  import albumentations as A
  transform = A.Compose([
      A.HorizontalFlip(p=0.5),
      A.RandomBrightnessContrast(p=0.2),
  ])
  ```

#### **Weights & Biases** - 实验跟踪
- **链接**: https://github.com/wandb/wandb
- **特点**: 可视化训练过程
- **使用**:
  ```python
  import wandb
  wandb.init(project="my-project")
  ```

#### **TensorBoard** - 可视化
- **链接**: https://www.tensorflow.org/tensorboard
- **特点**: 官方可视化工具
- **使用**:
  ```python
  from torch.utils.tensorboard import SummaryWriter
  writer = SummaryWriter()
  ```

---

## 📊 数据集

### 1. 通用图像分类

#### **ImageNet**
- **规模**: 1400万图像，1000类
- **链接**: https://www.image-net.org/
- **用途**: 预训练基准
- **下载**: 需申请，约150GB

#### **CIFAR-10/100**
- **规模**: 6万图像，10/100类
- **链接**: https://www.cs.toronto.edu/~kriz/cifar.html
- **用途**: 快速实验
- **特点**: 小尺寸，易下载

#### **MNIST**
- **规模**: 7万手写数字
- **链接**: http://yann.lecun.com/exdb/mnist/
- **用途**: 入门练习
- **特点**: 简单，经典

---

### 2. 目标检测

#### **COCO (Common Objects in Context)**
- **规模**: 33万图像，80类，150万实例
- **链接**: https://cocodataset.org/
- **用途**: 检测/分割/姿态估计
- **特点**: 场景丰富，标注详细

#### **PASCAL VOC**
- **规模**: 1.1万图像，20类
- **链接**: http://host.robots.ox.ac.uk/pascal/VOC/
- **用途**: 检测/分割
- **特点**: 经典，易上手

#### **Open Images**
- **规模**: 900万图像，600类
- **链接**: https://storage.googleapis.com/openimages/web/index.html
- **用途**: 大规模检测
- **特点**: 数据量大，类别多

---

### 3. 图像分割

#### **Cityscapes**
- **规模**: 2.5万图像，19类
- **链接**: https://www.cityscapes-dataset.com/
- **用途**: 语义分割
- **特点**: 城市街景，精细标注

#### **ADE20K**
- **规模**: 2.5万图像，150类
- **链接**: https://groups.csail.mit.edu/vision/datasets/ADE20K/
- **用途**: 场景解析
- **特点**: 场景多样，标注全面

#### **ISBI Challenge**
- **规模**: 细胞显微镜图像
- **链接**: https://biomedicalimaging.org/2012/challenge/
- **用途**: 医学图像分割
- **特点**: 医学领域经典

---

### 4. 人脸数据集

#### **LFW (Labeled Faces in the Wild)**
- **规模**: 1.3万图像，5749人
- **链接**: http://vis-www.cs.umass.edu/lfw/
- **用途**: 人脸识别
- **特点**: 自然场景

#### **CelebA**
- **规模**: 20万图像，1万名人
- **链接**: https://mmlab.ie.cuhk.edu.hk/projects/CelebA.html
- **用途**: 人脸属性
- **特点**: 属性标注丰富

---

### 5. 视频数据集

#### **Kinetics**
- **规模**: 30万视频片段，400/600/700类
- **链接**: https://deepmind.com/research/open-source/kinetics
- **用途**: 动作识别
- **特点**: 高质量，大规模

#### **UCF101**
- **规模**: 1.3万视频，101类
- **链接**: https://www.crcv.ucf.edu/data/UCF101.php
- **用途**: 动作识别
- **特点**: 中等规模

---

## 🧰 工具库

### 1. 深度学习框架

#### **PyTorch**
- **官网**: https://pytorch.org/
- **特点**: 动态图，易调试
- **推荐**: 研究和开发

#### **TensorFlow**
- **官网**: https://www.tensorflow.org/
- **特点**: 生态完善，部署方便
- **推荐**: 工业部署

#### **Keras**
- **官网**: https://keras.io/
- **特点**: 高级API，简洁易用
- **推荐**: 快速原型

---

### 2. 图像处理

#### **OpenCV**
- **官网**: https://opencv.org/
- **特点**: 功能全面，C++/Python
- **核心**: 图像处理、计算机视觉

#### **Pillow (PIL)**
- **官网**: https://python-pillow.org/
- **特点**: 简单图像处理
- **核心**: 读写、基本变换

#### **scikit-image**
- **官网**: https://scikit-image.org/
- **特点**: 科学计算风格
- **核心**: 算法实现

---

### 3. 科学计算

#### **NumPy**
- **官网**: https://numpy.org/
- **特点**: 数组运算基础
- **核心**: 矩阵操作

#### **SciPy**
- **官网**: https://scipy.org/
- **特点**: 科学计算工具箱
- **核心**: 信号处理、优化

#### **Matplotlib**
- **官网**: https://matplotlib.org/
- **特点**: 绘图可视化
- **核心**: 2D绘图

---

### 4. 部署工具

#### **ONNX**
- **官网**: https://onnx.ai/
- **特点**: 模型格式标准
- **用途**: 跨框架部署

#### **TensorRT**
- **官网**: https://developer.nvidia.com/tensorrt
- **特点**: NVIDIA推理加速
- **用途**: 生产部署

#### **OpenVINO**
- **官网**: https://software.intel.com/openvino-toolkit
- **特点**: Intel硬件优化
- **用途**: 边缘部署

---

## 🔗 重要链接汇总

### 学习社区
- **Papers With Code**: https://paperswithcode.com/
- **arXiv**: https://arxiv.org/
- **GitHub Trending**: https://github.com/trending/python
- **Kaggle**: https://www.kaggle.com/

### 会议期刊
- **CVPR**: https://cvpr.thecvf.com/
- **ICCV**: https://iccv2023.thecvf.com/
- **ECCV**: https://www.eccv2024.eu/
- **TPAMI**: https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=34

### 博客教程
- **Medium**: https://medium.com/topic/computer-vision
- **Towards Data Science**: https://towardsdatascience.com/
- **PyImageSearch**: https://www.pyimagesearch.com/
- **Distill.pub**: https://distill.pub/

---

## 📖 学习路径建议

### 阶段一：基础入门（1-2个月）
1. **理论**: 学习CS231n前3周内容
2. **编程**: 完成NumPy + OpenCV练习
3. **实践**: 实现MNIST分类器
4. **阅读**: AlexNet, VGG论文

### 阶段二：核心算法（2-3个月）
1. **目标检测**: YOLOv5实战
2. **图像分割**: U-Net医学图像
3. **阅读**: ResNet, FCN, U-Net论文
4. **项目**: 完成1-2个完整项目

### 阶段三：进阶提升（2-3个月）
1. **架构**: 理解EfficientNet, ViT
2. **优化**: 模型压缩、部署
3. **阅读**: 最新顶会论文
4. **竞赛**: 参加Kaggle比赛

### 阶段四：专家水平（持续）
1. **研究**: 复现SOTA算法
2. **创新**: 提出改进方案
3. **分享**: 写博客、开源代码
4. **社区**: 参与开源贡献

---

## 💡 使用建议

### 如何高效使用参考资料

1. **论文阅读**:
   - 先读摘要和结论
   - 理解核心创新点
   - 重点看实验部分
   - 尝试复现关键实验

2. **教程学习**:
   - 动手运行所有代码
   - 修改参数观察变化
   - 尝试扩展功能
   - 写学习笔记

3. **项目实践**:
   - 从简单项目开始
   - 理解每行代码
   - 逐步增加复杂度
   - 参与开源项目

4. **数据集使用**:
   - 先用小数据集测试
   - 理解数据格式
   - 设计合适的数据增强
   - 注意数据泄露

---

## 🔄 持续更新

本参考资料库会持续更新，添加：
- 最新论文解读
- 优质开源项目
- 实用工具和技巧
- 学习路径优化

---

**祝你学习顺利，早日成为计算机视觉专家！** 🚀

*最后更新：2025年12月*
