# 08-姿态估计
> 状态：大纲（内容未撰写，以下是写作计划与预备资源）

姿态估计回答的问题是：给定一张人物图片，人体关键点（头、肩、肘、腕、膝……）分别在哪个像素位置？它是健身 App 动作计数、短视频肢体特效、康复训练评估的底层技术。

**前置知识**（写完后阅读需要）：[05-CNN架构](../M3/README.md)，特别是 [03-注意力机制](../M3/L03-%E6%B3%A8%E6%84%8F%E5%8A%9B%E6%9C%BA%E5%88%B6.md)。

## 写作计划
### 8.1 基础概念
- [ ] 人体关键点检测简介
- [ ] 姿态估计的应用场景
- [ ] 主流数据集介绍（COCO、MPII）

### 8.2 经典方法
- [ ] OpenPose 原理详解（自底向上路线）
- [ ] AlphaPose 介绍（自顶向下路线）
- [ ] 多人姿态估计的两种范式对比

### 8.3 现代方法
- [ ] HRNet（High-Resolution Net）
- [ ] Lightweight OpenPose（移动端）
- [ ] ViTPose（Transformer-based）

### 8.4 实战项目
- [ ] 项目1：实时人体姿态检测
- [ ] 项目2：姿态动作识别

## 预备资源
- [HRNet 论文](https://arxiv.org/abs/1908.07919)
- [COCO Keypoints 数据集](https://cocodataset.org/#keypoints-2020)
- [MPII Human Pose 数据集](http://human-pose.mpi-inf.mpg.de/)

---

**返回**：[视觉轨道](../TRACK.md)
**下一篇**：[视频分析（大纲）](planned-视频分析.md)
