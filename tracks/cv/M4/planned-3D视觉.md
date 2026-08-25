# 10-3D视觉
> 状态：大纲（内容未撰写，以下是写作计划与预备资源）

3D 视觉回答的问题是：怎么从 2D 图片恢复世界的三维结构——相机在哪、物体在哪、表面长什么样？它是自动驾驶、AR、工业扫描的核心技术。

**前置知识**（写完后阅读需要）：[03-传统计算机视觉](../M1/README.md) 的相机模型与立体视觉（本章是它的延伸）。

## 写作计划
### 10.1 几何基础
- [ ] 3D 视觉概述
- [ ] 相机模型与标定
- [ ] 坐标系变换

### 10.2 立体视觉
- [ ] 双目视觉原理
- [ ] 视差计算
- [ ] 深度估计

### 10.3 点云处理
- [ ] 点云基础
- [ ] 点云滤波
- [ ] 点云分割
- [ ] 点云配准

### 10.4 神经辐射场
- [ ] NeRF 原理
- [ ] NeRF 变体（Instant-NGP、Gaussian Splatting）

### 10.5 实战项目
- [ ] 项目1：双目深度估计
- [ ] 项目2：点云目标检测
- [ ] 项目3：3D 场景重建

## 预备资源
- [Open3D 教程](https://docs.open3d.org/)
- [PyTorch3D 教程](https://pytorch3d.org/)
- [KITTI 数据集](http://www.cvlibs.net/datasets/kitti/)
- [ShapeNet 数据集](https://shapenet.org/)
- [Open3D](https://github.com/isl-org/Open3D)
- [PyTorch3D](https://github.com/facebookresearch/pytorch3d)

---

**返回**：[视觉轨道](../TRACK.md)
**上一篇**：[视频分析（大纲）](planned-视频分析.md)
**下一篇**：[Capstone 项目集](capstones.md)
