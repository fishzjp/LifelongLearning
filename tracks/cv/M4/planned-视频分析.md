# 09-视频分析
> 状态：大纲（内容未撰写，以下是写作计划与预备资源）

视频分析回答的问题是：当图片连成时间序列，怎么跟踪同一个物体、识别一段动作？它是安防跟踪、体育动作分析、短视频内容理解的底层技术。

**前置知识**（写完后阅读需要）：[06-目标检测](../M3/L05-%E7%9B%AE%E6%A0%87%E6%A3%80%E6%B5%8B.md)（跟踪的每一步都离不开检测）。

## 写作计划
### 9.1 视频基础
- [ ] 视频数据结构与处理
- [ ] 视频读取与保存
- [ ] 视频帧提取

### 9.2 目标跟踪
- [ ] 目标跟踪概述
- [ ] 传统跟踪算法（Kalman Filter、SORT）
- [ ] 深度学习跟踪（DeepSORT、ByteTrack）

### 9.3 动作识别
- [ ] 动作识别概述
- [ ] 2D CNN 方法（TSN、TSM）
- [ ] 3D CNN 方法（I3D、SlowFast）
- [ ] Transformer 方法（TimeSformer、Video Swin）

### 9.4 应用系统
- [ ] 行为分析系统
- [ ] 视频摘要生成
- [ ] 异常检测

## 预备资源
- [PyTorch Video 模型库](https://pytorch.org/vision/stable/models.html#video-classification)
- [Kinetics-400 数据集](https://deepmind.com/research/open-source/kinetics)
- [UCF101 数据集](https://www.crcv.ucf.edu/data/UCF101.php)
- [MMAction2](https://github.com/open-mmlab/mmaction2)
- [PyTorchVideo](https://github.com/facebookresearch/pytorchvideo)

---

**返回**：[视觉轨道](../TRACK.md)
**上一篇**：[姿态估计（大纲）](planned-姿态估计.md)
**下一篇**：[3D视觉（大纲）](planned-3D视觉.md)
