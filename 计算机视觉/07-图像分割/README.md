# 第七章：图像分割

> 系统学习图像分割的核心技术，从语义分割到实例分割，掌握FCN、U-Net、DeepLab、Mask R-CNN等经典算法，理解Dice系数、IoU等评估指标。

## 📚 章节概览

图像分割是计算机视觉的核心任务之一，旨在为图像中的每个像素分配类别标签。

### 📄 本章内容

1. **语义分割**：FCN、U-Net、DeepLab系列
2. **实例分割**：Mask R-CNN、SOLO、YOLACT
3. **全景分割**：Panoptic FPN
4. **评估指标**：Dice系数、IoU、mIoU
5. **实战项目**：医学图像分割、遥感图像分割

---

## 🎯 学习路径

### 阶段一：基础概念（1天）

#### 1. 图像分割任务定义
```python
"""
图像分割类型：

1. 语义分割（Semantic Segmentation）
   - 相同类别像素共享同一标签
   - 输出：每个像素的类别
   - 示例：所有"人"像素标记为同一类

2. 实例分割（Instance Segmentation）
   - 区分同一类别的不同实例
   - 输出：每个像素的实例ID + 类别
   - 示例：人1、人2、人3分别标记

3. 全景分割（Panoptic Segmentation）
   - 语义 + 实例的结合
   - 输出：所有像素的类别和实例ID
"""

import numpy as np
import matplotlib.pyplot as plt

def visualize_segmentation_types():
    """可视化三种分割类型"""
    
    # 创建示例图像
    image = np.zeros((256, 256, 3), dtype=np.uint8)
    image[50:150, 50:150] = [255, 0, 0]  # 人1
    image[100:200, 150:250] = [0, 255, 0]  # 人2
    
    # 语义分割：所有"人"都是同一类
    semantic = np.zeros((256, 256), dtype=np.uint8)
    semantic[50:150, 50:150] = 1
    semantic[100:200, 150:250] = 1
    
    # 实例分割：每个人是不同实例
    instance = np.zeros((256, 256), dtype=np.uint8)
    instance[50:150, 50:150] = 1  # 实例1
    instance[100:200, 150:250] = 2  # 实例2
    
    # 全景分割：类别 + 实例
    panoptic = np.zeros((256, 256), dtype=np.uint8)
    panoptic[50:150, 50:150] = 11  # 类别1 + 实例1
    panoptic[100:200, 150:250] = 12  # 类别1 + 实例2
    
    fig, axes = plt.subplots(1, 4, figsize=(16, 4))
    axes[0].imshow(image)
    axes[0].set_title('原始图像')
    axes[1].imshow(semantic, cmap='tab10')
    axes[1].set_title('语义分割')
    axes[2].imshow(instance, cmap='tab10')
    axes[2].set_title('实例分割')
    axes[3].imshow(panoptic, cmap='tab10')
    axes[3].set_title('全景分割')
    
    for ax in axes:
        ax.axis('off')
    
    plt.tight_layout()
    return fig

# 数据格式示例
def segmentation_data_format():
    """分割数据格式"""
    
    # 输入图像
    image = np.random.rand(3, 224, 224)  # (C, H, W)
    
    # 语义分割标签
    semantic_label = np.random.randint(0, 21, (224, 224))  # (H, W)
    
    # 实例分割标签
    instance_label = {
        'masks': np.random.randint(0, 10, (224, 224)),  # (H, W)
        'labels': np.array([1, 2, 3]),  # 类别
        'bboxes': np.array([[50, 50, 100, 100], [150, 150, 200, 200]])  # 边界框
    }
    
    return image, semantic_label, instance_label
```

---

### 阶段二：语义分割（3-4天）

#### 2. FCN (Fully Convolutional Network)
**核心创新**：全卷积网络，任意尺寸输入

```python
class FCN32s(nn.Module):
    """
    FCN-32s：最基础的全卷积网络
    将全连接层替换为卷积层，输出32倍下采样的分割图
    """
    
    def __init__(self, num_classes=21):
        super(FCN32s, self).__init__()
        self.num_classes = num_classes
        
        # VGG16骨干网络（简化）
        self.features = nn.Sequential(
            # Block 1
            nn.Conv2d(3, 64, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(64, 64, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            
            # Block 2
            nn.Conv2d(64, 128, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(128, 128, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            
            # Block 3
            nn.Conv2d(128, 256, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(256, 256, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(256, 256, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            
            # Block 4
            nn.Conv2d(256, 512, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(512, 512, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(512, 512, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            
            # Block 5
            nn.Conv2d(512, 512, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(512, 512, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(512, 512, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
        )
        
        # 分类器
        self.classifier = nn.Sequential(
            nn.Conv2d(512, 4096, 7),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Conv2d(4096, 4096, 1),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Conv2d(4096, num_classes, 1),
        )
        
        # 上采样（32倍）
        self.upsample = nn.Upsample(scale_factor=32, mode='bilinear', align_corners=True)
    
    def forward(self, x):
        # 下采样特征提取
        features = self.features(x)
        
        # 分类预测
        scores = self.classifier(features)
        
        # 上采样到输入尺寸
        output = self.upsample(scores)
        
        return output

# FCN-8s：融合多层特征
class FCN8s(nn.Module):
    """
    FCN-8s：融合pool3, pool4, pool5的特征
    提高分割精度
    """
    
    def __init__(self, num_classes=21):
        super(FCN8s, self).__init__()
        self.num_classes = num_classes
        
        # 骨干网络（需要保留中间层）
        self.features = nn.Sequential(
            # ... VGG16结构 ...
        )
        
        # 1x1卷积用于不同层
        self.score_pool3 = nn.Conv2d(256, num_classes, 1)
        self.score_pool4 = nn.Conv2d(512, num_classes, 1)
        self.score_pool5 = nn.Conv2d(512, num_classes, 1)
        
        # 上采样
        self.upsample2 = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)
        self.upsample8 = nn.Upsample(scale_factor=8, mode='bilinear', align_corners=True)
    
    def forward(self, x):
        # 提取多层特征（简化）
        pool3 = torch.randn(x.size(0), 256, x.size(2)//8, x.size(3)//8).to(x.device)
        pool4 = torch.randn(x.size(0), 512, x.size(2)//16, x.size(3)//16).to(x.device)
        pool5 = torch.randn(x.size(0), 512, x.size(2)//32, x.size(3)//32).to(x.device)
        
        # 1x1卷积
        score3 = self.score_pool3(pool3)
        score4 = self.score_pool4(pool4)
        score5 = self.score_pool5(pool5)
        
        # 融合
        score4_up = self.upsample2(score4)
        fused = score5 + score4_up
        
        fused_up = self.upsample2(fused)
        fused = score3 + fused_up
        
        # 最终上采样
        output = self.upsample8(fused)
        
        return output
```

---

#### 3. U-Net
**核心创新**：编码器-解码器 + 跳跃连接

```python
class UNet(nn.Module):
    """
    U-Net：医学图像分割的经典网络
    特点：对称结构，跳跃连接保留细节
    """
    
    def __init__(self, in_channels=3, out_channels=1, init_features=64):
        super(UNet, self).__init__()
        
        features = init_features
        
        # 编码器（下采样）
        self.encoder1 = self._block(in_channels, features, name='enc1')
        self.pool1 = nn.MaxPool2d(2)
        
        self.encoder2 = self._block(features, features * 2, name='enc2')
        self.pool2 = nn.MaxPool2d(2)
        
        self.encoder3 = self._block(features * 2, features * 4, name='enc3')
        self.pool3 = nn.MaxPool2d(2)
        
        self.encoder4 = self._block(features * 4, features * 8, name='enc4')
        self.pool4 = nn.MaxPool2d(2)
        
        # 瓶颈层
        self.bottleneck = self._block(features * 8, features * 16, name='bottleneck')
        
        # 解码器（上采样）
        self.upconv4 = nn.ConvTranspose2d(features * 16, features * 8, 2, stride=2)
        self.decoder4 = self._block(features * 16, features * 8, name='dec4')
        
        self.upconv3 = nn.ConvTranspose2d(features * 8, features * 4, 2, stride=2)
        self.decoder3 = self._block(features * 8, features * 4, name='dec3')
        
        self.upconv2 = nn.ConvTranspose2d(features * 4, features * 2, 2, stride=2)
        self.decoder2 = self._block(features * 4, features * 2, name='dec2')
        
        self.upconv1 = nn.ConvTranspose2d(features * 2, features, 2, stride=2)
        self.decoder1 = self._block(features * 2, features, name='dec1')
        
        # 输出层
        self.conv_out = nn.Conv2d(features, out_channels, 1)
        
        # 激活函数
        self.sigmoid = nn.Sigmoid() if out_channels == 1 else nn.Softmax(dim=1)
    
    def _block(self, in_channels, out_channels, name):
        """双卷积块"""
        return nn.Sequential(
            nn.Conv2d(in_channels, out_channels, 3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, 3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
        )
    
    def forward(self, x):
        # 编码
        enc1 = self.encoder1(x)
        enc2 = self.encoder2(self.pool1(enc1))
        enc3 = self.encoder3(self.pool2(enc2))
        enc4 = self.encoder4(self.pool3(enc3))
        
        # 瓶颈
        bottleneck = self.bottleneck(self.pool4(enc4))
        
        # 解码 + 跳跃连接
        dec4 = self.upconv4(bottleneck)
        dec4 = torch.cat([enc4, dec4], dim=1)  # 跳跃连接
        dec4 = self.decoder4(dec4)
        
        dec3 = self.upconv3(dec4)
        dec3 = torch.cat([enc3, dec3], dim=1)
        dec3 = self.decoder3(dec3)
        
        dec2 = self.upconv2(dec3)
        dec2 = torch.cat([enc2, dec2], dim=1)
        dec2 = self.decoder2(dec2)
        
        dec1 = self.upconv1(dec2)
        dec1 = torch.cat([enc1, dec1], dim=1)
        dec1 = self.decoder1(dec1)
        
        # 输出
        output = self.conv_out(dec1)
        output = self.sigmoid(output)
        
        return output

# U-Net++：嵌套U-Net
class UNetPlusPlus(nn.Module):
    """
    U-Net++：嵌套的U-Net结构
    通过密集跳跃连接提升性能
    """
    
    def __init__(self, in_channels=3, out_channels=1, init_features=64):
        super(UNetPlusPlus, self).__init__()
        
        features = init_features
        
        # 嵌套结构（简化版）
        self.x_0_0 = self._block(in_channels, features)
        self.x_1_0 = self._block(features, features * 2)
        self.x_2_0 = self._block(features * 2, features * 4)
        self.x_3_0 = self._block(features * 4, features * 8)
        
        # 上采样和融合
        self.up_1_0 = nn.ConvTranspose2d(features * 2, features, 2, stride=2)
        self.up_2_0 = nn.ConvTranspose2d(features * 4, features * 2, 2, stride=2)
        self.up_3_0 = nn.ConvTranspose2d(features * 8, features * 4, 2, stride=2)
        
        # 输出层
        self.final = nn.Conv2d(features, out_channels, 1)
    
    def _block(self, in_channels, out_channels):
        return nn.Sequential(
            nn.Conv2d(in_channels, out_channels, 3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, 3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
        )
    
    def forward(self, x):
        # 简化的前向传播
        x00 = self.x_0_0(x)
        x10 = self.x_1_0(F.max_pool2d(x00, 2))
        x20 = self.x_2_0(F.max_pool2d(x10, 2))
        x30 = self.x_3_0(F.max_pool2d(x20, 2))
        
        # 上采样融合
        x21 = self.up_2_0(x30) + x20
        x11 = self.up_1_0(x21) + x10
        
        output = self.final(x11)
        return output
```

---

#### 4. DeepLab系列

##### 4.1 DeepLabv1/v2
**核心创新**：空洞卷积 + ASPP

```python
class DeepLabv2(nn.Module):
    """
    DeepLabv2：空洞卷积 + ASPP
    解决分辨率下降问题
    """
    
    def __init__(self, num_classes=21):
        super(DeepLabv2, self).__init__()
        self.num_classes = num_classes
        
        # VGG16骨干网络（空洞卷积）
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(64, 64, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            
            nn.Conv2d(64, 128, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(128, 128, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            
            # Block 3：使用空洞卷积
            nn.Conv2d(128, 256, 3, padding=2, dilation=2),
            nn.ReLU(),
            nn.Conv2d(256, 256, 3, padding=2, dilation=2),
            nn.ReLU(),
            nn.Conv2d(256, 256, 3, padding=2, dilation=2),
            nn.ReLU(),
            
            # Block 4：更大空洞率
            nn.Conv2d(256, 512, 3, padding=4, dilation=4),
            nn.ReLU(),
            nn.Conv2d(512, 512, 3, padding=4, dilation=4),
            nn.ReLU(),
            nn.Conv2d(512, 512, 3, padding=4, dilation=4),
            nn.ReLU(),
            
            # Block 5：最大空洞率
            nn.Conv2d(512, 512, 3, padding=4, dilation=4),
            nn.ReLU(),
            nn.Conv2d(512, 512, 3, padding=4, dilation=4),
            nn.ReLU(),
            nn.Conv2d(512, 512, 3, padding=4, dilation=4),
            nn.ReLU(),
        )
        
        # ASPP（空洞空间金字塔池化）
        self.aspp = nn.ModuleDict({
            'aspp0': nn.Conv2d(512, 256, 1),
            'aspp1': nn.Conv2d(512, 256, 3, padding=6, dilation=6),
            'aspp2': nn.Conv2d(512, 256, 3, padding=12, dilation=12),
            'aspp3': nn.Conv2d(512, 256, 3, padding=18, dilation=18),
            'aspp4': nn.Conv2d(512, 256, 1),  # 全局平均池化
        })
        
        self.classifier = nn.Sequential(
            nn.Conv2d(256 * 5, 256, 1),
            nn.ReLU(),
            nn.Conv2d(256, num_classes, 1),
        )
        
        self.upsample = nn.Upsample(scale_factor=8, mode='bilinear', align_corners=True)
    
    def forward(self, x):
        # 特征提取
        features = self.features(x)
        
        # ASPP
        aspp_features = []
        for name, module in self.aspp.items():
            if name == 'aspp4':
                # 全局平均池化
                pool = nn.AdaptiveAvgPool2d(1)
                aspp_features.append(module(pool(features)))
            else:
                aspp_features.append(module(features))
        
        # 融合
        fused = torch.cat(aspp_features, dim=1)
        
        # 分类
        output = self.classifier(fused)
        
        # 上采样
        output = self.upsample(output)
        
        return output
```

---

##### 4.2 DeepLabv3+
**核心创新**：编码器-解码器结构

```python
class DeepLabv3Plus(nn.Module):
    """
    DeepLabv3+：编码器-解码器 + ASPP
    结合多尺度特征和空间细节
    """
    
    def __init__(self, num_classes=21):
        super(DeepLabv3Plus, self).__init__()
        self.num_classes = num_classes
        
        # 编码器：Xception或ResNet
        self.backbone = self._build_backbone()
        
        # ASPP模块
        self.aspp = self._build_aspp(2048, 256)
        
        # 解码器
        self.decoder = self._build_decoder(256, 48)
        
        # 分类器
        self.classifier = nn.Conv2d(256, num_classes, 1)
        
        self.upsample = nn.Upsample(scale_factor=4, mode='bilinear', align_corners=True)
    
    def _build_backbone(self):
        """使用ResNet作为骨干网络"""
        # 简化：返回修改的ResNet
        return nn.Sequential(
            nn.Conv2d(3, 64, 7, stride=2, padding=3),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(3, stride=2, padding=1),
            # ... ResNet块 ...
        )
    
    def _build_aspp(self, in_channels, out_channels):
        """ASPP模块"""
        return nn.ModuleDict({
            'aspp0': nn.Conv2d(in_channels, out_channels, 1),
            'aspp1': nn.Conv2d(in_channels, out_channels, 3, padding=6, dilation=6),
            'aspp2': nn.Conv2d(in_channels, out_channels, 3, padding=12, dilation=12),
            'aspp3': nn.Conv2d(in_channels, out_channels, 3, padding=18, dilation=18),
            'aspp4': nn.Sequential(
                nn.AdaptiveAvgPool2d(1),
                nn.Conv2d(in_channels, out_channels, 1),
            ),
        })
    
    def _build_decoder(self, aspp_channels, low_level_channels):
        """解码器"""
        return nn.Sequential(
            nn.Conv2d(aspp_channels + low_level_channels, 256, 3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.Conv2d(256, 256, 3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
        )
    
    def forward(self, x):
        # 编码器特征
        low_level_features = self.backbone(x)  # 浅层特征
        high_level_features = low_level_features  # 深层特征（简化）
        
        # ASPP
        aspp_features = []
        for name, module in self.aspp.items():
            if name == 'aspp4':
                aspp_features.append(module(high_level_features))
            else:
                aspp_features.append(module(high_level_features))
        
        aspp_out = torch.cat(aspp_features, dim=1)
        
        # 解码器
        # 低层特征处理
        low_level = nn.Conv2d(64, 48, 1)(low_level_features)
        
        # 上采样ASPP输出
        aspp_up = nn.Upsample(scale_factor=4, mode='bilinear', align_corners=True)(aspp_out)
        
        # 融合
        fused = torch.cat([aspp_up, low_level], dim=1)
        
        # 解码
        decoded = self.decoder(fused)
        
        # 输出
        output = self.classifier(decoded)
        output = self.upsample(output)
        
        return output
```

---

### 阶段三：实例分割（2-3天）

#### 5. Mask R-CNN
**核心创新**：Faster R-CNN + 掩码分支

```python
class MaskRCNN(nn.Module):
    """
    Mask R-CNN：实例分割经典算法
    在Faster R-CNN基础上增加掩码预测分支
    """
    
    def __init__(self, backbone, num_classes=81):
        super(MaskRCNN, self).__init__()
        
        # 特征提取
        self.backbone = backbone
        
        # RPN（区域建议网络）
        self.rpn = RPN(in_channels=256, num_anchors=3)
        
        # ROI Align（改进ROI Pooling）
        self.roi_align = RoIAlign(output_size=(7, 7), spatial_scale=1/16, sampling_ratio=2)
        
        # 分类和回归头
        self.box_head = nn.Sequential(
            nn.Linear(256 * 7 * 7, 1024),
            nn.ReLU(),
            nn.Linear(1024, 1024),
            nn.ReLU(),
        )
        self.cls_score = nn.Linear(1024, num_classes)
        self.bbox_pred = nn.Linear(1024, num_classes * 4)
        
        # 掩码头
        self.mask_head = nn.Sequential(
            nn.Conv2d(256, 256, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(256, 256, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(256, 256, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(256, 256, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(256, num_classes, 1),
            nn.Sigmoid(),
        )
    
    def forward(self, x, targets=None):
        # 特征提取
        features = self.backbone(x)
        
        # RPN生成建议
        rpn_scores, rpn_bbox_preds = self.rpn(features)
        
        # 生成ROI
        if targets is None:
            rois = self._generate_rois_inference(rpn_scores, rpn_bbox_preds)
        else:
            rois = self._generate_rois_training(rpn_scores, rpn_bbox_preds, targets)
        
        # ROI Align
        pooled_features = self.roi_align(features, rois)
        
        # 分类和回归
        box_features = self.box_head(pooled_features.view(pooled_features.size(0), -1))
        cls_scores = self.cls_score(box_features)
        bbox_preds = self.bbox_pred(box_features)
        
        # 掩码预测
        mask_preds = self.mask_head(pooled_features)
        
        return cls_scores, bbox_preds, mask_preds, rois
    
    def _generate_rois_inference(self, scores, bbox_preds):
        """推理时生成ROI"""
        # 简化：返回前N个建议
        return torch.tensor([[0, 100, 100, 200, 200]], dtype=torch.float32)
    
    def _generate_rois_training(self, scores, bbox_preds, targets):
        """训练时生成ROI"""
        # 简化：使用GT + 采样
        labels, boxes, masks = targets
        rois = []
        for i, box in enumerate(boxes):
            rois.append([0] + box.tolist())
        return torch.tensor(rois, dtype=torch.float32)

# ROI Align实现
class RoIAlign(nn.Module):
    def __init__(self, output_size, spatial_scale, sampling_ratio):
        super(RoIAlign, self).__init__()
        self.output_size = output_size
        self.spatial_scale = spatial_scale
        self.sampling_ratio = sampling_ratio
    
    def forward(self, features, rois):
        """
        Args:
            features: (B, C, H, W)
            rois: (N, 5) [batch_id, x1, y1, x2, y2]
        """
        pooled_features = []
        for roi in rois:
            batch_id, x1, y1, x2, y2 = roi
            
            # 缩放ROI到特征图尺寸
            x1, y1, x2, y2 = x1 * self.spatial_scale, y1 * self.spatial_scale, \
                            x2 * self.spatial_scale, y2 * self.spatial_scale
            
            # 裁剪特征
            roi_features = features[batch_id, :, 
                                   int(y1):int(y2)+1, 
                                   int(x1):int(x2)+1]
            
            # 双线性插值上采样
            if roi_features.numel() > 0:
                roi_features = nn.functional.interpolate(
                    roi_features.unsqueeze(0),
                    size=self.output_size,
                    mode='bilinear',
                    align_corners=True
                )
                pooled_features.append(roi_features.squeeze(0))
            else:
                pooled_features.append(torch.zeros.output_size[0], self.output_size[1]).zero_())
        
        return torch.stack(pooled_features)
```

---

#### 6. SOLO (Segmenting Objects by Locations)
**核心创新**：位置感知分割

```python
class SOLO(nn.Module):
    """
    SOLO：按位置分割物体
    核心思想：物体位置决定类别
    """
    
    def __init__(self, num_classes=80, num_grids=[40, 36, 24, 16, 12]):
        super(SOLO, self).__init__()
        self.num_classes = num_classes
        self.num_grids = num_grids
        
        # 特征金字塔
        self.backbone = self._build_backbone()
        self.fpn = self._build_fpn()
        
        # 分割头
        self.seg_heads = nn.ModuleList()
        for grid in num_grids:
            # 分类分支
            cls_head = nn.Sequential(
                nn.Conv2d(256, 256, 3, padding=1),
                nn.ReLU(),
                nn.Conv2d(256, grid * grid * num_classes, 1),
            )
            # 掩码分支
            mask_head = nn.Sequential(
                nn.Conv2d(256, 256, 3, padding=1),
                nn.ReLU(),
                nn.Conv2d(256, 256, 3, padding=1),
                nn.ReLU(),
                nn.Conv2d(256, grid * grid, 1),
            )
            self.seg_heads.append(nn.ModuleDict({
                'cls': cls_head,
                'mask': mask_head,
            }))
    
    def _build_backbone(self):
        # 简化：ResNet骨干
        return nn.Sequential(
            nn.Conv2d(3, 64, 7, stride=2, padding=3),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(3, stride=2, padding=1),
        )
    
    def _build_fpn(self):
        # 简化：特征金字塔
        return nn.ModuleDict({
            'p5': nn.Conv2d(64, 256, 1),
            'p4': nn.Conv2d(64, 256, 1),
            'p3': nn.Conv2d(64, 256, 1),
        })
    
    def forward(self, x):
        # 特征提取
        c3 = self.backbone(x)
        
        # FPN
        p3 = self.fpn['p3'](c3)
        p4 = self.fpn['p4'](c3)  # 简化
        p5 = self.fpn['p5'](c3)
        
        # 多尺度预测
        predictions = []
        for i, (p, head) in enumerate(zip([p3, p4, p5], self.seg_heads)):
            cls_pred = head['cls'](p)
            mask_pred = head['mask'](p)
            
            # 重塑
            grid = self.num_grids[i]
            cls_pred = cls_pred.view(-1, grid, grid, self.num_classes)
            mask_pred = mask_pred.view(-1, grid, grid, grid)
            
            predictions.append({
                'cls': cls_pred,
                'mask': mask_pred,
            })
        
        return predictions
```

---

### 阶段四：评估指标（1天）

#### 7. Dice系数和IoU
```python
def dice_coefficient(pred, target, smooth=1e-6):
    """
    Dice系数：衡量分割相似度
    Dice = 2 * |pred ∩ target| / (|pred| + |target|)
    """
    pred_flat = pred.contiguous().view(-1)
    target_flat = target.contiguous().view(-1)
    
    intersection = (pred_flat * target_flat).sum()
    dice = (2. * intersection + smooth) / (pred_flat.sum() + target_flat.sum() + smooth)
    
    return dice

def iou_score(pred, target, smooth=1e-6):
    """
    IoU：交并比
    IoU = |pred ∩ target| / |pred ∪ target|
    """
    pred_flat = pred.contiguous().view(-1)
    target_flat = target.contiguous().view(-1)
    
    intersection = (pred_flat * target_flat).sum()
    union = pred_flat.sum() + target_flat.sum() - intersection
    
    iou = (intersection + smooth) / (union + smooth)
    return iou

def miou_score(pred, target, num_classes):
    """
    mIoU：平均IoU
    计算每个类别的IoU然后取平均
    """
    ious = []
    for cls in range(num_classes):
        pred_cls = (pred == cls).float()
        target_cls = (target == cls).float()
        
        if target_cls.sum() > 0:
            iou = iou_score(pred_cls, target_cls)
            ious.append(iou.item())
    
    return np.mean(ious) if ious else 0

# 使用示例
def evaluate_segmentation():
    """评估分割结果"""
    # 模拟预测和真实标签
    pred = torch.randint(0, 2, (1, 1, 224, 224)).float()
    target = torch.randint(0, 2, (1, 1, 224, 224)).float()
    
    dice = dice_coefficient(pred, target)
    iou = iou_score(pred, target)
    miou = miou_score(pred, target, num_classes=2)
    
    print(f"Dice系数: {dice:.4f}")
    print(f"IoU: {iou:.4f}")
    print(f"mIoU: {miou:.4f}")
    
    return dice, iou, miou
```

#### 8. 完整评估器
```python
class SegmentationMetrics:
    """分割评估器"""
    
    def __init__(self, num_classes):
        self.num_classes = num_classes
        self.reset()
    
    def reset(self):
        self.total_pixels = 0
        self.correct_pixels = 0
        self.confusion_matrix = np.zeros((self.num_classes, self.num_classes))
    
    def update(self, pred, target):
        """更新统计"""
        pred = pred.argmax(dim=1).cpu().numpy()
        target = target.cpu().numpy()
        
        for i in range(self.num_classes):
            for j in range(self.num_classes):
                self.confusion_matrix[i, j] += np.sum((pred == i) & (target == j))
        
        self.total_pixels += target.size
        self.correct_pixels += np.sum(pred == target)
    
    def get_metrics(self):
        """计算所有指标"""
        # Pixel Accuracy
        pixel_acc = self.correct_pixels / self.total_pixels if self.total_pixels > 0 else 0
        
        # Mean IoU
        miou = 0
        for i in range(self.num_classes):
            intersection = self.confusion_matrix[i, i]
            union = np.sum(self.confusion_matrix[i, :]) + np.sum(self.confusion_matrix[:, i]) - intersection
            if union > 0:
                miou += intersection / union
        miou /= self.num_classes
        
        # Frequency Weighted IoU
        fw_miou = 0
        for i in range(self.num_classes):
            intersection = self.confusion_matrix[i, i]
            union = np.sum(self.confusion_matrix[i, :]) + np.sum(self.confusion_matrix[:, i]) - intersection
            weight = np.sum(self.confusion_matrix[i, :])
            if union > 0:
                fw_miou += weight * (intersection / union)
        fw_miou /= self.total_pixels if self.total_pixels > 0 else 1
        
        return {
            'pixel_accuracy': pixel_acc,
            'mean_iou': miou,
            'frequency_weighted_iou': fw_miou,
        }

# 使用示例
def evaluate_model_performance(model, dataloader, num_classes):
    """评估模型性能"""
    metrics = SegmentationMetrics(num_classes)
    model.eval()
    
    with torch.no_grad():
        for images, targets in dataloader:
            outputs = model(images)
            metrics.update(outputs, targets)
    
    return metrics.get_metrics()
```

---

## 🎯 实战项目

### 项目1：医学图像分割（细胞分割）

```python
"""
目标：使用U-Net分割细胞图像
数据集：细胞显微镜图像
"""

import torch
from torch.utils.data import Dataset, DataLoader
import cv2
import numpy as np

class CellDataset(Dataset):
    """细胞分割数据集"""
    
    def __init__(self, image_dir, mask_dir, transform=None):
        self.image_dir = image_dir
        self.mask_dir = mask_dir
        self.transform = transform
        self.image_files = os.listdir(image_dir)
    
    def __len__(self):
        return len(self.image_files)
    
    def __getitem__(self, idx):
        # 读取图像
        img_name = self.image_files[idx]
        img_path = os.path.join(self.image_dir, img_name)
        mask_path = os.path.join(self.mask_dir, img_name.replace('.png', '_mask.png'))
        
        image = cv2.imread(img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        
        # 归一化
        image = image.astype(np.float32) / 255.0
        mask = (mask > 127).astype(np.float32)
        
        if self.transform:
            augmented = self.transform(image=image, mask=mask)
            image = augmented['image']
            mask = augmented['mask']
        
        return image, mask

def train_cell_segmentation():
    """训练细胞分割模型"""
    # 1. 数据准备
    from albumentations import Compose, Resize, HorizontalFlip, VerticalFlip, Normalize
    
    train_transform = Compose([
        Resize(256, 256),
        HorizontalFlip(p=0.5),
        VerticalFlip(p=0.5),
        Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    
    train_dataset = CellDataset(
        image_dir='data/cell/train/images',
        mask_dir='data/cell/train/masks',
        transform=train_transform
    )
    
    train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
    
    # 2. 模型
    model = UNet(in_channels=3, out_channels=1, init_features=32)
    
    # 3. 损失函数
    criterion = nn.BCELoss()
    
    # 4. 优化器
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
    
    # 5. 训练循环
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    
    for epoch in range(100):
        model.train()
        epoch_loss = 0
        
        for images, masks in train_loader:
            images = images.permute(0, 3, 1, 2).to(device)
            masks = masks.unsqueeze(1).to(device)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, masks)
            loss.backward()
            optimizer.step()
            
            epoch_loss += loss.item()
        
        print(f'Epoch {epoch+1}, Loss: {epoch_loss/len(train_loader):.4f}')
        
        # 验证
        if (epoch + 1) % 10 == 0:
            validate_cell_model(model, device)

def validate_cell_model(model, device):
    """验证模型"""
    model.eval()
    val_dataset = CellDataset('data/cell/val/images', 'data/cell/val/masks')
    val_loader = DataLoader(val_dataset, batch_size=4)
    
    metrics = SegmentationMetrics(num_classes=2)
    
    with torch.no_grad():
        for images, masks in val_loader:
            images = images.permute(0, 3, 1, 2).to(device)
            masks = masks.unsqueeze(1).to(device)
            
            outputs = model(images)
            metrics.update(outputs, masks)
    
    results = metrics.get_metrics()
    print(f"Validation - Pixel Acc: {results['pixel_accuracy']:.4f}, mIoU: {results['mean_iou']:.4f}")
```

### 项目2：遥感图像分割

```python
"""
目标：分割遥感图像中的建筑物
数据集：SpaceNet或自定义遥感数据
"""

class RemoteSensingDataset(Dataset):
    """遥感图像分割数据集"""
    
    def __init__(self, image_dir, mask_dir, patch_size=256, stride=128):
        self.image_dir = image_dir
        self.mask_dir = mask_dir
        self.patch_size = patch_size
        self.stride = stride
        self.patches = []
        
        # 滑动窗口生成patch
        for img_file in os.listdir(image_dir):
            img_path = os.path.join(image_dir, img_file)
            mask_path = os.path.join(mask_dir, img_file.replace('.tif', '_mask.tif'))
            
            image = cv2.imread(img_path, cv2.IMREAD_COLOR)
            mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
            
            h, w = image.shape[:2]
            for y in range(0, h - patch_size + 1, stride):
                for x in range(0, w - patch_size + 1, stride):
                    self.patches.append({
                        'image': image[y:y+patch_size, x:x+patch_size],
                        'mask': mask[y:y+patch_size, x:x+patch_size],
                        'file': img_file,
                        'pos': (x, y)
                    })
    
    def __len__(self):
        return len(self.patches)
    
    def __getitem__(self, idx):
        patch = self.patches[idx]
        image = patch['image'].astype(np.float32) / 255.0
        mask = (patch['mask'] > 127).astype(np.float32)
        
        # 转换为Tensor
        image = torch.from_numpy(image).permute(2, 0, 1)
        mask = torch.from_numpy(mask).unsqueeze(0)
        
        return image, mask

def train_remote_sensing_segmentation():
    """训练遥感图像分割"""
    # 数据集
    train_dataset = RemoteSensingDataset(
        image_dir='data/remotesensing/train/images',
        mask_dir='data/remotesensing/train/masks'
    )
    
    train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True)
    
    # 模型：使用DeepLabv3+
    model = DeepLabv3Plus(num_classes=2)
    
    # 损失函数：Dice + BCE
    class DiceBCELoss(nn.Module):
        def __init__(self):
            super(DiceBCELoss, self).__init__()
            self.bce = nn.BCEWithLogitsLoss()
        
        def forward(self, pred, target):
            bce_loss = self.bce(pred, target)
            dice_loss = 1 - dice_coefficient(torch.sigmoid(pred), target)
            return bce_loss + dice_loss
    
    criterion = DiceBCELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=1e-3, momentum=0.9, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=20, gamma=0.1)
    
    # 训练
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    
    for epoch in range(50):
        model.train()
        total_loss = 0
        
        for images, masks in train_loader:
            images, masks = images.to(device), masks.to(device)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, masks)
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
        
        scheduler.step()
        print(f'Epoch {epoch+1}, Loss: {total_loss/len(train_loader):.4f}')
```

---

## 🔍 调试技巧

### 1. 分割质量分析
```python
def analyze_segmentation_errors(pred, target):
    """分析分割错误类型"""
    errors = {
        'false_positive': 0,  # 过分割
        'false_negative': 0,  # 欠分割
        'boundary_error': 0,  # 边界不准
    }
    
    # 计算误差图
    fp = (pred == 1) & (target == 0)  # 假阳性
    fn = (pred == 0) & (target == 1)  # 假阴性
    
    errors['false_positive'] = fp.sum().item()
    errors['false_negative'] = fn.sum().item()
    
    # 边界误差（简化）
    from scipy.ndimage import binary_dilation
    boundary = binary_dilation(target) & ~target
    boundary_error = (pred & boundary).sum().item()
    errors['boundary_error'] = boundary_error
    
    return errors

# 可视化错误
def visualize_errors(pred, target):
    """可视化分割错误"""
    fig, axes = plt.subplots(1, 4, figsize=(12, 3))
    
    axes[0].imshow(pred.cpu().numpy()[0, 0], cmap='gray')
    axes[0].set_title('预测')
    
    axes[1].imshow(target.cpu().numpy()[0, 0], cmap='gray')
    axes[1].set_title('真实')
    
    # 假阳性（红色）
    fp = (pred == 1) & (target == 0)
    axes[2].imshow(fp.cpu().numpy()[0, 0], cmap='Reds')
    axes[2].set_title('过分割')
    
    # 假阴性（蓝色）
    fn = (pred == 0) & (target == 1)
    axes[3].imshow(fn.cpu().numpy()[0, 0], cmap='Blues')
    axes[3].set_title('欠分割')
    
    for ax in axes:
        ax.axis('off')
    
    plt.tight_layout()
    return fig
```

### 2. 训练监控
```python
def monitor_segmentation_training(log_file):
    """监控分割训练过程"""
    import re
    
    with open(log_file, 'r') as f:
        lines = f.readlines()
    
    epochs = []
    losses = []
    dice_scores = []
    iou_scores = []
    
    for line in lines:
        # 解析日志格式
        match = re.search(r'Epoch (\d+).*Loss ([\d.]+).*Dice ([\d.]+).*IoU ([\d.]+)', line)
        if match:
            epochs.append(int(match.group(1)))
            losses.append(float(match.group(2)))
            dice_scores.append(float(match.group(3)))
            iou_scores.append(float(match.group(4)))
    
    # 绘制曲线
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    axes[0].plot(epochs, losses, 'r-', linewidth=2)
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Loss')
    axes[0].set_title('Training Loss')
    axes[0].grid(True)
    
    axes[1].plot(epochs, dice_scores, 'b-', linewidth=2)
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Dice')
    axes[1].set_title('Dice Coefficient')
    axes[1].grid(True)
    
    axes[2].plot(epochs, iou_scores, 'g-', linewidth=2)
    axes[2].set_xlabel('Epoch')
    axes[2].set_ylabel('IoU')
    axes[2].set_title('IoU Score')
    axes[2].grid(True)
    
    plt.tight_layout()
    return fig
```

---

## 📚 学习检查清单

### 理解层面
- [ ] 理解语义分割和实例分割的区别
- [ ] 掌握U-Net的编码器-解码器结构
- [ ] 理解空洞卷积的作用
- [ ] 掌握ASPP的工作原理
- [ ] 了解Dice系数和IoU的计算

### 实践层面
- [ ] 能实现U-Net网络
- [ ] 会训练医学图像分割模型
- [ ] 能调试分割质量问题
- [ ] 会计算评估指标
- [ ] 掌握数据预处理技巧

### 进阶层面
- [ ] 理解DeepLab系列演进
- [ ] 掌握实例分割技术
- [ ] 会优化分割边界
- [ ] 了解实时分割部署

---

## 🚀 下一步学习

完成本章后，你可以继续学习：

### 08-姿态估计
- 人体关键点检测
- OpenPose、HRNet
- 行为识别

### 09-视频分析
- 目标跟踪
- 动作识别
- 视频分割

---

## 📖 扩展资源

### 经典论文
1. **FCN**: "Fully Convolutional Networks for Semantic Segmentation" (2015)
2. **U-Net**: "U-Net: Convolutional Networks for Biomedical Image Segmentation" (2015)
3. **DeepLabv1**: "Semantic Image Segmentation with Deep Convolutional Nets and Fully Connected CRFs" (2015)
4. **DeepLabv2**: "DeepLab: Semantic Image Segmentation with Deep Convolutional Nets, Atrous Convolution, and Fully Connected CRFs" (2017)
5. **DeepLabv3+**: "Encoder-Decoder with Atrous Separable Convolution for Semantic Image Segmentation" (2018)
6. **Mask R-CNN**: "Mask R-CNN" (2017)
7. **SOLO**: "SOLO: Segmenting Objects by Locations" (2020)

### 开源实现
- **Segmentation Models**: https://github.com/qubvel/segmentation_models
- **MMSegmentation**: https://github.com/open-mmlab/mmsegmentation
- **Detectron2**: https://github.com/facebookresearch/detectron2

### 数据集
- **Cityscapes**: 城市街景语义分割
- **ADE20K**: 场景解析
- **PASCAL VOC**: 语义分割
- **COCO**: 实例分割
- **ISBI**: 医学图像分割
- **Kvasir-SEG**: 内窥镜图像分割

---

**本章结束，建议学习时间：1-2周**

*最后更新：2025年12月*
