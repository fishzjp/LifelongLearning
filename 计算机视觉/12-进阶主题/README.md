# 第十二章：进阶主题

> 探索计算机视觉的前沿技术和高级主题，包括Transformer、自监督学习、多模态学习、模型压缩与部署等，帮助你站在技术发展的最前沿。

## 📚 章节概览

本章涵盖当前计算机视觉领域最热门和最具前景的研究方向：

### 📄 本章内容

1. **Transformer在CV中的应用**：ViT、Swin Transformer、DETR
2. **自监督学习**：对比学习、掩码图像建模
3. **多模态学习**：CLIP、BLIP、图文生成
4. **模型压缩与部署**：剪枝、量化、知识蒸馏
5. **生成模型**：GAN、Diffusion Models
6. **3D视觉进阶**：NeRF、点云处理
7. **具身智能**：视觉导航、机器人控制

---

## 🎯 学习路径

### 阶段一：Transformer革命（2-3天）

#### 1. Vision Transformer (ViT)
**核心思想**：将Transformer用于图像分类

```python
import torch
import torch.nn as nn
import numpy as np

class PatchEmbedding(nn.Module):
    """图像分块嵌入"""
    def __init__(self, img_size=224, patch_size=16, in_channels=3, embed_dim=768):
        super(PatchEmbedding, self).__init__()
        self.patch_size = patch_size
        self.num_patches = (img_size // patch_size) ** 2
        
        # 卷积实现分块嵌入
        self.proj = nn.Conv2d(in_channels, embed_dim, 
                             kernel_size=patch_size, stride=patch_size)
        
        # CLS token
        self.cls_token = nn.Parameter(torch.zeros(1, 1, embed_dim))
        
        # 位置编码
        self.pos_embed = nn.Parameter(torch.zeros(1, self.num_patches + 1, embed_dim))
        
    def forward(self, x):
        # x: (B, C, H, W)
        x = self.proj(x)  # (B, E, H', W')
        x = x.flatten(2).transpose(1, 2)  # (B, N, E)
        
        # 扩展CLS token
        cls_tokens = self.cls_token.expand(x.shape[0], -1, -1)
        x = torch.cat([cls_tokens, x], dim=1)
        
        # 添加位置编码
        x = x + self.pos_embed
        
        return x

class TransformerEncoder(nn.Module):
    """Transformer编码器"""
    def __init__(self, embed_dim=768, depth=12, num_heads=12, mlp_ratio=4.0, dropout=0.1):
        super(TransformerEncoder, self).__init__()
        
        self.layers = nn.ModuleList([
            TransformerBlock(embed_dim, num_heads, mlp_ratio, dropout)
            for _ in range(depth)
        ])
        
        self.norm = nn.LayerNorm(embed_dim)
    
    def forward(self, x):
        for layer in self.layers:
            x = layer(x)
        return self.norm(x)

class TransformerBlock(nn.Module):
    """Transformer块"""
    def __init__(self, embed_dim, num_heads, mlp_ratio=4.0, dropout=0.1):
        super(TransformerBlock, self).__init__()
        
        self.norm1 = nn.LayerNorm(embed_dim)
        self.attn = nn.MultiheadAttention(embed_dim, num_heads, dropout)
        
        self.norm2 = nn.LayerNorm(embed_dim)
        mlp_hidden_dim = int(embed_dim * mlp_ratio)
        self.mlp = nn.Sequential(
            nn.Linear(embed_dim, mlp_hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(mlp_hidden_dim, embed_dim),
            nn.Dropout(dropout),
        )
    
    def forward(self, x):
        # 多头注意力 + 残差
        x = x + self.attn(self.norm1(x), self.norm1(x), self.norm1(x))[0]
        
        # MLP + 残差
        x = x + self.mlp(self.norm2(x))
        
        return x

class VisionTransformer(nn.Module):
    """Vision Transformer"""
    def __init__(self, img_size=224, patch_size=16, in_channels=3, 
                 num_classes=1000, embed_dim=768, depth=12, num_heads=12):
        super(VisionTransformer, self).__init__()
        
        self.patch_embed = PatchEmbedding(img_size, patch_size, in_channels, embed_dim)
        self.encoder = TransformerEncoder(embed_dim, depth, num_heads)
        self.head = nn.Linear(embed_dim, num_classes)
        
        # 初始化
        self._init_weights()
    
    def _init_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.trunc_normal_(m.weight, std=0.02)
                if m.bias is not None:
                    nn.init.zeros_(m.bias)
            elif isinstance(m, nn.LayerNorm):
                nn.init.ones_(m.weight)
                nn.init.zeros_(m.bias)
    
    def forward(self, x):
        x = self.patch_embed(x)
        x = self.encoder(x)
        
        # 取CLS token
        cls_token = x[:, 0]
        x = self.head(cls_token)
        
        return x

# 创建不同规模的ViT
def vit_base():
    return VisionTransformer(patch_size=16, embed_dim=768, depth=12, num_heads=12)

def vit_large():
    return VisionTransformer(patch_size=16, embed_dim=1024, depth=24, num_heads=16)

def vit_huge():
    return VisionTransformer(patch_size=16, embed_dim=1280, depth=32, num_heads=16)

# 使用示例
if __name__ == '__main__':
    model = vit_base()
    x = torch.randn(1, 3, 224, 224)
    output = model(x)
    print(f"ViT输出: {output.shape}")  # (1, 1000)
```

**ViT vs CNN对比**：
```python
def compare_vit_cnn():
    """对比ViT和CNN的特性"""
    comparison = {
        'ViT': {
            '优点': ['全局感受野', '可扩展性强', '适合大数据', 'Transformer成熟'],
            '缺点': ['数据需求大', '计算复杂度高', '小数据易过拟合', '缺乏归纳偏置'],
            '适用场景': ['大规模分类', '预训练模型', '迁移学习']
        },
        'CNN': {
            '优点': ['局部感受野', '平移不变性', '参数共享', '小数据表现好'],
            '缺点': ['局部视野', '难以建模长距离依赖', '架构设计复杂'],
            '适用场景': ['小数据集', '实时应用', '资源受限']
        }
    }
    
    return comparison
```

---

#### 2. Swin Transformer
**核心创新**：分层结构 + 窗口注意力

```python
class SwinTransformerBlock(nn.Module):
    """Swin Transformer块"""
    def __init__(self, embed_dim, num_heads, window_size=7, shift_size=0):
        super(SwinTransformerBlock, self).__init__()
        
        self.norm1 = nn.LayerNorm(embed_dim)
        self.attn = WindowAttention(embed_dim, num_heads, window_size)
        
        self.norm2 = nn.LayerNorm(embed_dim)
        self.mlp = nn.Sequential(
            nn.Linear(embed_dim, embed_dim * 4),
            nn.GELU(),
            nn.Linear(embed_dim * 4, embed_dim),
        )
        
        self.shift_size = shift_size
        self.window_size = window_size
    
    def forward(self, x):
        B, H, W, C = x.shape
        
        # 窗口划分
        if self.shift_size > 0:
            shifted_x = torch.roll(x, shifts=(-self.shift_size, -self.shift_size), dims=(1, 2))
        else:
            shifted_x = x
        
        # 窗口注意力
        x_windows = window_partition(shifted_x, self.window_size)
        attn_windows = self.attn(x_windows)
        shifted_x = window_reverse(attn_windows, self.window_size, H, W)
        
        # 还原
        if self.shift_size > 0:
            x = torch.roll(shifted_x, shifts=(self.shift_size, self.shift_size), dims=(1, 2))
        else:
            x = shifted_x
        
        # 残差
        x = x + self.mlp(self.norm2(x))
        return x

class WindowAttention(nn.Module):
    """窗口注意力"""
    def __init__(self, embed_dim, num_heads, window_size):
        super(WindowAttention, self).__init__()
        
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.scale = (embed_dim // num_heads) ** -0.5
        
        self.qkv = nn.Linear(embed_dim, embed_dim * 3)
        self.proj = nn.Linear(embed_dim, embed_dim)
        
        # 相对位置偏置
        self.relative_position_bias_table = nn.Parameter(
            torch.zeros((2 * window_size - 1) * (2 * window_size - 1), num_heads)
        )
        
        # 生成相对位置索引
        coords = torch.arange(window_size)
        coords = torch.stack(torch.meshgrid(coords, coords, indexing='ij'))
        coords_flatten = torch.flatten(coords, 1)
        relative_coords = coords_flatten[:, :, None] - coords_flatten[:, None, :]
        relative_coords = relative_coords.permute(1, 2, 0).contiguous()
        relative_coords[:, :, 0] += window_size - 1
        relative_coords[:, :, 1] += window_size - 1
        relative_coords[:, :, 0] *= 2 * window_size - 1
        relative_position_index = relative_coords.sum(-1)
        
        self.register_buffer("relative_position_index", relative_position_index)
        
        # 初始化
        nn.init.trunc_normal_(self.relative_position_bias_table, std=0.02)
    
    def forward(self, x):
        B_, N, C = x.shape
        
        qkv = self.qkv(x).reshape(B_, N, 3, self.num_heads, C // self.num_heads).permute(2, 0, 3, 1, 4)
        q, k, v = qkv.unbind(0)
        
        # 注意力分数
        attn = (q @ k.transpose(-2, -1)) * self.scale
        
        # 相对位置偏置
        relative_position_bias = self.relative_position_bias_table[
            self.relative_position_index.view(-1)
        ].view(self.window_size, self.window_size, -1)
        relative_position_bias = relative_position_bias.permute(2, 0, 1).contiguous()
        attn = attn + relative_position_bias.unsqueeze(0)
        
        attn = attn.softmax(dim=-1)
        x = (attn @ v).transpose(1, 2).reshape(B_, N, C)
        x = self.proj(x)
        
        return x

def window_partition(x, window_size):
    """窗口划分"""
    B, H, W, C = x.shape
    x = x.view(B, H // window_size, window_size, W // window_size, window_size, C)
    windows = x.permute(0, 1, 3, 2, 4, 5).contiguous().view(-1, window_size, window_size, C)
    return windows

def window_reverse(windows, window_size, H, W):
    """窗口还原"""
    B = int(windows.shape[0] / (H * W / window_size / window_size))
    x = windows.view(B, H // window_size, W // window_size, window_size, window_size, -1)
    x = x.permute(0, 1, 3, 2, 4, 5).contiguous().view(B, H, W, -1)
    return x

class PatchMerging(nn.Module):
    """Patch Merging层"""
    def __init__(self, embed_dim):
        super(PatchMerging, self).__init__()
        self.norm = nn.LayerNorm(4 * embed_dim)
        self.reduction = nn.Linear(4 * embed_dim, 2 * embed_dim, bias=False)
    
    def forward(self, x):
        B, H, W, C = x.shape
        
        # 合并相邻patch
        x0 = x[:, 0::2, 0::2, :]
        x1 = x[:, 1::2, 0::2, :]
        x2 = x[:, 0::2, 1::2, :]
        x3 = x[:, 1::2, 1::2, :]
        
        x = torch.cat([x0, x1, x2, x3], -1)
        x = self.norm(x)
        x = self.reduction(x)
        
        return x

class SwinTransformer(nn.Module):
    """Swin Transformer"""
    def __init__(self, img_size=224, patch_size=4, in_channels=3, num_classes=1000,
                 embed_dim=96, depths=[2, 2, 6, 2], num_heads=[3, 6, 12, 24],
                 window_size=7):
        super(SwinTransformer, self).__init__()
        
        self.num_layers = len(depths)
        self.embed_dim = embed_dim
        
        # 初始Patch Embedding
        self.patch_embed = nn.Conv2d(in_channels, embed_dim, 
                                    kernel_size=patch_size, stride=patch_size)
        
        # 绝对位置编码
        self.pos_embed = nn.Parameter(torch.zeros(1, img_size // patch_size, 
                                                 img_size // patch_size, embed_dim))
        
        # Swin Layers
        self.layers = nn.ModuleList()
        for i in range(self.num_layers):
            layer = SwinTransformerStage(
                embed_dim=embed_dim * (2 ** i),
                depth=depths[i],
                num_heads=num_heads[i],
                window_size=window_size
            )
            self.layers.append(layer)
        
        self.norm = nn.LayerNorm(embed_dim * (2 ** (self.num_layers - 1)))
        self.head = nn.Linear(embed_dim * (2 ** (self.num_layers - 1)), num_classes)
        
        self._init_weights()
    
    def _init_weights(self):
        nn.init.trunc_normal_(self.pos_embed, std=0.02)
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.trunc_normal_(m.weight, std=0.02)
                if m.bias is not None:
                    nn.init.zeros_(m.bias)
            elif isinstance(m, nn.LayerNorm):
                nn.init.ones_(m.weight)
                nn.init.zeros_(m.bias)
    
    def forward(self, x):
        x = self.patch_embed(x)
        x = x + self.pos_embed
        x = x.flatten(1, 2)
        
        for layer in self.layers:
            x = layer(x)
        
        x = self.norm(x)
        x = x.mean(dim=1)
        x = self.head(x)
        
        return x

class SwinTransformerStage(nn.Module):
    """Swin Transformer阶段"""
    def __init__(self, embed_dim, depth, num_heads, window_size):
        super(SwinTransformerStage, self).__init__()
        
        self.blocks = nn.ModuleList()
        for i in range(depth):
            shift_size = 0 if (i % 2 == 0) else window_size // 2
            self.blocks.append(
                SwinTransformerBlock(embed_dim, num_heads, window_size, shift_size)
            )
        
        self.patch_merge = PatchMerging(embed_dim) if depth > 0 else None
    
    def forward(self, x):
        B, N, C = x.shape
        H = W = int(N ** 0.5)
        x = x.view(B, H, W, C)
        
        for block in self.blocks:
            x = block(x)
        
        if self.patch_merge is not None:
            x = self.patch_merge(x)
        
        return x.view(B, -1, x.shape[-1])

# 使用示例
if __name__ == '__main__':
    model = SwinTransformer()
    x = torch.randn(1, 3, 224, 224)
    output = model(x)
    print(f"Swin Transformer输出: {output.shape}")
```

---

#### 3. DETR (DEtection TRansformer)
**核心创新**：端到端目标检测，无需NMS

```python
class DETR(nn.Module):
    """DETR: Detection Transformer"""
    def __init__(self, num_classes, num_queries, hidden_dim=256, nheads=8, num_encoder_layers=6, num_decoder_layers=6):
        super(DETR, self).__init__()
        
        # 骨干网络（简化为ResNet）
        self.backbone = nn.Sequential(
            nn.Conv2d(3, 64, 7, stride=2, padding=3),
            nn.ReLU(),
            nn.MaxPool2d(3, stride=2, padding=1),
            nn.Conv2d(64, 128, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(128, 256, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(256, hidden_dim, 1),
        )
        
        # Transformer
        self.transformer = nn.Transformer(
            d_model=hidden_dim,
            nhead=nheads,
            num_encoder_layers=num_encoder_layers,
            num_decoder_layers=num_decoder_layers,
            dim_feedforward=2048,
            dropout=0.1,
        )
        
        # 查询嵌入
        self.query_embed = nn.Embedding(num_queries, hidden_dim)
        
        # 输入投影
        self.input_proj = nn.Conv2d(256, hidden_dim, 1)
        
        # 预测头
        self.class_embed = nn.Linear(hidden_dim, num_classes + 1)  # +1 for background
        self.bbox_embed = nn.Linear(hidden_dim, 4)  # (x, y, w, h)
        
        # 位置编码
        self.pos_embed = PositionalEncoding2D(hidden_dim)
    
    def forward(self, x):
        # 特征提取
        features = self.backbone(x)  # (B, hidden_dim, H', W')
        
        # 展平并转置
        spatial_dims = features.shape[2:]
        features = features.flatten(2).permute(2, 0, 1)  # (H'*W', B, hidden_dim)
        
        # 位置编码
        pos_embed = self.pos_embed(features.shape[0], spatial_dims).flatten(2).permute(2, 0, 1)
        
        # 查询嵌入
        query_embed = self.query_embed.weight.unsqueeze(1).repeat(1, x.shape[0], 1)
        
        # Transformer
        tgt = torch.zeros_like(query_embed)
        memory = self.transformer.encoder(features + pos_embed)
        output = self.transformer.decoder(tgt, memory, query_embed=query_embed)
        
        # 预测
        output = output.transpose(0, 1)  # (B, num_queries, hidden_dim)
        
        classes = self.class_embed(output)
        bboxes = self.bbox_embed(output).sigmoid()  # 归一化到[0, 1]
        
        return classes, bboxes

class PositionalEncoding2D(nn.Module):
    """2D位置编码"""
    def __init__(self, d_model, max_h=100, max_w=100):
        super(PositionalEncoding2D, self).__init__()
        self.d_model = d_model
        
        pe = torch.zeros(d_model, max_h, max_w)
        
        # 生成位置编码
        position_h = torch.arange(0, max_h).unsqueeze(1)
        position_w = torch.arange(0, max_w).unsqueeze(0)
        
        div_term = torch.exp(torch.arange(0, d_model, 2) * -(np.log(10000.0) / d_model))
        
        pe[0::2, :, :] = torch.sin(position_h * div_term.unsqueeze(1).unsqueeze(1))
        pe[1::2, :, :] = torch.cos(position_h * div_term.unsqueeze(1).unsqueeze(1))
        
        pe_w = torch.zeros(d_model, max_h, max_w)
        pe_w[0::2, :, :] = torch.sin(position_w * div_term.unsqueeze(1).unsqueeze(1))
        pe_w[1::2, :, :] = torch.cos(position_w * div_term.unsqueeze(1).unsqueeze(1))
        
        self.register_buffer('pe', pe + pe_w)
    
    def forward(self, h, w):
        return self.pe[:, :h, :w]

# DETR损失函数
class DETRLoss(nn.Module):
    """DETR损失函数"""
    def __init__(self, num_classes, cost_class=1, cost_box=5, cost_giou=2):
        super(DETRLoss, self).__init__()
        self.num_classes = num_classes
        self.cost_class = cost_class
        self.cost_box = cost_box
        self.cost_giou = cost_giou
        
        self.bce_loss = nn.BCEWithLogitsLoss()
        self.l1_loss = nn.L1Loss()
    
    def forward(self, outputs, targets):
        """
        outputs: {'pred_logits': ..., 'pred_boxes': ...}
        targets: [{'labels': ..., 'boxes': ...}]
        """
        # 匈牙利匹配
        indices = self.hungarian_match(outputs, targets)
        
        # 分类损失
        idx = self._get_src_permutation_idx(indices)
        target_classes_o = torch.cat([t["labels"][J] for t, (_, J) in zip(targets, indices)])
        target_classes = torch.full(outputs['pred_logits'].shape[:2], self.num_classes,
                                   dtype=torch.int64, device=outputs['pred_logits'].device)
        target_classes[idx] = target_classes_o
        
        loss_ce = self.bce_loss(outputs['pred_logits'], F.one_hot(target_classes, self.num_classes + 1))
        
        # 框回归损失
        src_boxes = outputs['pred_boxes'][idx]
        target_boxes = torch.cat([t["boxes"][I] for t, (_, I) in zip(targets, indices)], dim=0)
        
        loss_bbox = self.l1_loss(src_boxes, target_boxes)
        
        # GIoU损失
        loss_giou = 1 - self.giou_loss(src_boxes, target_boxes)
        
        total_loss = self.cost_class * loss_ce + self.cost_box * loss_bbox + self.cost_giou * loss_giou
        
        return total_loss
    
    def hungarian_match(self, outputs, targets):
        """匈牙利匹配（简化版）"""
        # 实际实现需要scipy.optimize.linear_sum_assignment
        # 这里简化为随机匹配
        batch_size = outputs['pred_logits'].shape[0]
        indices = []
        for b in range(batch_size):
            indices.append((torch.arange(outputs['pred_logits'].shape[1]), 
                           torch.arange(len(targets[b]['labels']))))
        return indices
    
    def _get_src_permutation_idx(self, indices):
        batch_idx = torch.cat([torch.full_like(src, i) for i, (src, _) in enumerate(indices)])
        src_idx = torch.cat([src for (src, _) in indices])
        return batch_idx, src_idx
    
    def giou_loss(self, boxes1, boxes2):
        """GIoU损失"""
        # 简化实现
        return torch.mean(torch.abs(boxes1 - boxes2))

# 使用示例
if __name__ == '__main__':
    model = DETR(num_classes=20, num_queries=100)
    x = torch.randn(1, 3, 800, 800)
    classes, bboxes = model(x)
    print(f"DETR输出 - 类别: {classes.shape}, 边界框: {bboxes.shape}")
```

---

### 阶段二：自监督学习（2-3天）

#### 4. 对比学习 (SimCLR)
```python
class SimCLR(nn.Module):
    """SimCLR: 简单对比学习框架"""
    
    def __init__(self, encoder, projection_dim=128):
        super(SimCLR, self).__init__()
        self.encoder = encoder
        
        # 投影头
        in_features = encoder.head.in_features
        self.encoder.head = nn.Identity()  # 移除分类头
        
        self.projection_head = nn.Sequential(
            nn.Linear(in_features, in_features * 2),
            nn.ReLU(),
            nn.Linear(in_features * 2, projection_dim)
        )
    
    def forward(self, x):
        features = self.encoder(x)
        projections = self.projection_head(features)
        return projections

class NTXentLoss(nn.Module):
    """归一化温度缩放交叉熵损失"""
    
    def __init__(self, temperature=0.5):
        super(NTXentLoss, self).__init__()
        self.temperature = temperature
    
    def forward(self, projections, labels=None):
        """
        projections: (2N, D) - 正负样本对
        """
        # 归一化
        projections = F.normalize(projections, dim=1)
        
        # 相似度矩阵
        sim_matrix = torch.mm(projections, projections.T) / self.temperature
        
        # 对角线设为极小值（避免自身相似）
        sim_matrix = sim_matrix - torch.eye(sim_matrix.shape[0], device=sim_matrix.device) * 1e9
        
        # 正样本对（2N个样本，每对相邻的是正样本）
        labels = torch.arange(sim_matrix.shape[0], device=sim_matrix.device)
        labels = (labels + 1) % 2 * (labels // 2)  # 0,1,0,1,... -> 0,0,1,1,...
        
        # 交叉熵
        loss = F.cross_entropy(sim_matrix, labels)
        
        return loss

# 数据增强（SimCLR需要强增强）
class SimCLRAugmentation:
    def __init__(self, image_size=224):
        self.transform = A.Compose([
            A.RandomResizedCrop(image_size, image_size),
            A.HorizontalFlip(p=0.5),
            A.RandomBrightnessContrast(p=0.8),
            A.GaussianBlur(p=0.5),
            A.ColorJitter(p=0.8),
            A.ToTensorV2(),
            A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
    
    def __call__(self, image):
        # 生成两个不同的增强视图
        view1 = self.transform(image=image)['image']
        view2 = self.transform(image=image)['image']
        return view1, view2

def train_simclr(model, dataloader, optimizer, epochs=100):
    """训练SimCLR"""
    criterion = NTXentLoss(temperature=0.5)
    model.train()
    
    for epoch in range(epochs):
        total_loss = 0
        
        for images, _ in dataloader:
            # images: (B, C, H, W)
            # 生成正负样本对
            batch_size = images.shape[0]
            images = images.repeat(2, 1, 1, 1)  # 2B个样本
            
            # 前向传播
            projections = model(images)  # (2B, projection_dim)
            
            # 计算损失
            loss = criterion(projections)
            
            # 反向传播
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
        
        print(f"Epoch {epoch+1}: Loss = {total_loss / len(dataloader):.4f}")

# 使用示例
if __name__ == '__main__':
    # 创建编码器
    encoder = VisionTransformer(num_classes=1000)
    
    # SimCLR模型
    model = SimCLR(encoder, projection_dim=128)
    
    # 优化器
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
    
    # 训练（需要数据加载器）
    # train_simclr(model, dataloader, optimizer)
```

---

#### 5. 掩码图像建模 (MAE)
```python
class MAE(nn.Module):
    """Masked Autoencoder"""
    
    def __init__(self, encoder, decoder_dim=512, mask_ratio=0.75):
        super(MAE, self).__init__()
        self.encoder = encoder
        self.mask_ratio = mask_ratio
        
        # 解码器
        self.decoder = nn.Sequential(
            nn.Linear(encoder.embed_dim, decoder_dim),
            nn.ReLU(),
            nn.Linear(decoder_dim, decoder_dim),
            nn.ReLU(),
            nn.Linear(decoder_dim, encoder.patch_embed.patch_size ** 2 * 3),
        )
        
        # 解码器位置编码
        self.decoder_pos_embed = nn.Parameter(torch.zeros(1, 196, decoder_dim))
        
        # 掩码token
        self.mask_token = nn.Parameter(torch.zeros(1, 1, decoder_dim))
    
    def forward(self, x):
        # 生成掩码
        B, C, H, W = x.shape
        patches = self.encoder.patch_embed(x)  # (B, N, D)
        N = patches.shape[1]
        
        # 随机掩码
        len_keep = int(N * (1 - self.mask_ratio))
        noise = torch.rand(B, N, device=x.device)
        ids_shuffle = torch.argsort(noise, dim=1)
        ids_restore = torch.argsort(ids_shuffle, dim=1)
        
        ids_keep = ids_shuffle[:, :len_keep]
        mask = torch.ones(B, N, device=x.device)
        mask[:, :len_keep] = 0
        
        # 编码可见patch
        x_masked = patches[torch.arange(B).unsqueeze(1), ids_keep]
        
        # 添加位置编码
        x_masked = x_masked + self.encoder.pos_embed[:, 1:, :][:, ids_keep, :]
        
        # 编码器
        encoded = self.encoder.encoder(x_masked)
        
        # 解码器输入
        decoder_input = torch.zeros(B, N, encoded.shape[-1], device=x.device)
        decoder_input[torch.arange(B).unsqueeze(1), ids_keep] = encoded
        
        # 添加解码器位置编码
        decoder_input = decoder_input + self.decoder_pos_embed
        
        # 解码
        decoded = self.decoder(decoder_input)
        
        # 重建图像
        pred = self.unpatchify(decoded, H, W)
        
        return pred, mask
    
    def unpatchify(self, x, H, W):
        """将patch还原为图像"""
        p = self.encoder.patch_embed.patch_size
        h = H // p
        w = W // p
        
        x = x.reshape(x.shape[0], h, w, p, p, 3)
        x = torch.einsum('nhwpqc->nchpwq', x)
        images = x.reshape(shape=(x.shape[0], 3, H, W))
        return images

class MAELoss(nn.Module):
    """MAE损失函数"""
    
    def __init__(self):
        super(MAELoss, self).__init__()
        self.l1_loss = nn.L1Loss()
    
    def forward(self, pred, target, mask):
        # 只计算掩码区域的重建损失
        loss = self.l1_loss(pred, target)
        return loss

def train_mae(model, dataloader, optimizer, epochs=100):
    """训练MAE"""
    criterion = MAELoss()
    model.train()
    
    for epoch in range(epochs):
        total_loss = 0
        
        for images, _ in dataloader:
            images = images.to(next(model.parameters()).device)
            
            # 前向传播
            pred, mask = model(images)
            
            # 计算损失
            loss = criterion(pred, images, mask)
            
            # 反向传播
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
        
        print(f"Epoch {epoch+1}: Loss = {total_loss / len(dataloader):.4f}")

# 使用示例
if __name__ == '__main__':
    encoder = VisionTransformer(num_classes=1000)
    model = MAE(encoder)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
    
    # 训练
    # train_mae(model, dataloader, optimizer)
```

---

### 阶段三：多模态学习（2-3天）

#### 6. CLIP (Contrastive Language-Image Pre-training)
```python
class CLIP(nn.Module):
    """CLIP模型"""
    
    def __init__(self, image_encoder, text_encoder, embed_dim=512):
        super(CLIP, self).__init__()
        
        # 图像编码器
        self.image_encoder = image_encoder
        self.image_projection = nn.Linear(image_encoder.head.in_features, embed_dim)
        image_encoder.head = nn.Identity()
        
        # 文本编码器（简化为Transformer）
        self.text_encoder = text_encoder
        self.text_projection = nn.Linear(text_encoder.output_dim, embed_dim)
        
        # 温度参数
        self.logit_scale = nn.Parameter(torch.ones([]) * np.log(1 / 0.07))
    
    def forward(self, images, texts):
        # 图像特征
        image_features = self.image_encoder(images)
        image_features = self.image_projection(image_features)
        image_features = F.normalize(image_features, dim=-1)
        
        # 文本特征
        text_features = self.text_encoder(texts)
        text_features = self.text_projection(text_features)
        text_features = F.normalize(text_features, dim=-1)
        
        # 相似度
        logit_scale = self.logit_scale.exp()
        logits_per_image = logit_scale * image_features @ text_features.T
        logits_per_text = logits_per_image.T
        
        return logits_per_image, logits_per_text

class TextEncoder(nn.Module):
    """文本编码器（简化版Transformer）"""
    
    def __init__(self, vocab_size, embed_dim=512, max_length=77, num_layers=6, num_heads=8):
        super(TextEncoder, self).__init__()
        
        self.token_embedding = nn.Embedding(vocab_size, embed_dim)
        self.position_embedding = nn.Embedding(max_length, embed_dim)
        
        encoder_layer = nn.TransformerEncoderLayer(embed_dim, num_heads, dim_feedforward=2048)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers)
        
        self.output_dim = embed_dim
    
    def forward(self, texts):
        # texts: (B, seq_len)
        seq_len = texts.shape[1]
        
        # 嵌入
        token_emb = self.token_embedding(texts)
        pos_emb = self.position_embedding(torch.arange(seq_len, device=texts.device))
        
        x = token_emb + pos_emb
        
        # Transformer
        x = x.permute(1, 0, 2)  # (seq_len, B, embed_dim)
        x = self.transformer(x)
        x = x.permute(1, 0, 2)  # (B, seq_len, embed_dim)
        
        # 取[CLS] token或平均
        features = x.mean(dim=1)
        
        return features

class CLIPLoss(nn.Module):
    """CLIP损失函数"""
    
    def __init__(self):
        super(CLIPLoss, self).__init__()
    
    def forward(self, logits_per_image, logits_per_text):
        # 图像到文本的损失
        labels = torch.arange(logits_per_image.shape[0], device=logits_per_image.device)
        loss_i = F.cross_entropy(logits_per_image, labels)
        
        # 文本到图像的损失
        loss_t = F.cross_entropy(logits_per_text, labels)
        
        return (loss_i + loss_t) / 2

def train_clip(model, dataloader, optimizer, epochs=100):
    """训练CLIP"""
    criterion = CLIPLoss()
    model.train()
    
    for epoch in range(epochs):
        total_loss = 0
        
        for images, texts in dataloader:
            images = images.to(next(model.parameters()).device)
            texts = texts.to(next(model.parameters()).device)
            
            # 前向传播
            logits_i, logits_t = model(images, texts)
            
            # 计算损失
            loss = criterion(logits_i, logits_t)
            
            # 反向传播
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
        
        print(f"Epoch {epoch+1}: Loss = {total_loss / len(dataloader):.4f}")

# 使用示例
if __name__ == '__main__':
    image_encoder = VisionTransformer(num_classes=1000)
    text_encoder = TextEncoder(vocab_size=50000)
    
    model = CLIP(image_encoder, text_encoder)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
    
    # 训练
    # train_clip(model, dataloader, optimizer)
    
    # 推理
    # with torch.no_grad():
    #     logits_i, logits_t = model(images, texts)
    #     probs = logits_i.softmax(dim=1)
```

---

### 阶段四：模型压缩与部署（2-3天）

#### 7. 知识蒸馏
```python
class DistillationLoss(nn.Module):
    """知识蒸馏损失"""
    
    def __init__(self, temperature=3.0, alpha=0.7):
        super(DistillationLoss, self).__init__()
        self.temperature = temperature
        self.alpha = alpha
        self.kl_loss = nn.KLDivLoss(reduction='batchmean')
        self.ce_loss = nn.CrossEntropyLoss()
    
    def forward(self, student_logits, teacher_logits, labels):
        # 软标签蒸馏
        soft_loss = self.kl_loss(
            F.log_softmax(student_logits / self.temperature, dim=1),
            F.softmax(teacher_logits / self.temperature, dim=1)
        ) * (self.temperature ** 2)
        
        # 硬标签损失
        hard_loss = self.ce_loss(student_logits, labels)
        
        return self.alpha * soft_loss + (1 - self.alpha) * hard_loss

def distill_model(teacher_model, student_model, dataloader, optimizer, epochs=50):
    """知识蒸馏训练"""
    criterion = DistillationLoss(temperature=3.0, alpha=0.7)
    teacher_model.eval()
    student_model.train()
    
    for epoch in range(epochs):
        total_loss = 0
        
        for images, labels in dataloader:
            images = images.to(next(student_model.parameters()).device)
            labels = labels.to(next(student_model.parameters()).device)
            
            with torch.no_grad():
                teacher_logits = teacher_model(images)
            
            student_logits = student_model(images)
            
            loss = criterion(student_logits, teacher_logits, labels)
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
        
        print(f"Epoch {epoch+1}: Loss = {total_loss / len(dataloader):.4f}")

# 使用示例
if __name__ == '__main__':
    # 教师模型（大模型）
    teacher = VisionTransformer(embed_dim=1024, depth=24, num_heads=16)
    teacher.load_state_dict(torch.load('teacher.pth'))
    
    # 学生模型（小模型）
    student = VisionTransformer(embed_dim=384, depth=12, num_heads=6)
    
    # 蒸馏训练
    optimizer = torch.optim.Adam(student.parameters(), lr=1e-4)
    # distill_model(teacher, student, dataloader, optimizer)
```

---

#### 8. 模型量化
```python
class QuantizedConv2d(nn.Module):
    """量化卷积层"""
    
    def __init__(self, conv_layer):
        super(QuantizedConv2d, self).__init__()
        self.weight = conv_layer.weight
        self.bias = conv_layer.bias
        self.stride = conv_layer.stride
        self.padding = conv_layer.padding
        self.dilation = conv_layer.dilation
        self.groups = conv_layer.groups
        
        # 量化参数
        self.register_buffer('scale', torch.tensor(1.0))
        self.register_buffer('zero_point', torch.tensor(0))
    
    def forward(self, x):
        # 量化输入
        x_quant = torch.round(x / self.scale + self.zero_point)
        x_quant = torch.clamp(x_quant, 0, 255)
        
        # 反量化
        x_dequant = (x_quant - self.zero_point) * self.scale
        
        # 卷积
        out = F.conv2d(x_dequant, self.weight, self.bias, 
                      self.stride, self.padding, self.dilation, self.groups)
        
        return out

def quantize_model(model, dataloader):
    """后训练量化"""
    model.eval()
    
    # 收集统计信息
    scales = {}
    zero_points = {}
    
    def hook_fn(name):
        def hook(module, input, output):
            if isinstance(module, nn.Conv2d):
                # 计算scale和zero_point
                scale = (output.max() - output.min()) / 255
                zero_point = -output.min() / scale
                scales[name] = scale
                zero_points[name] = zero_point
        return hook
    
    # 注册hook
    hooks = []
    for name, module in model.named_modules():
        if isinstance(module, nn.Conv2d):
            hooks.append(module.register_forward_hook(hook_fn(name)))
    
    # 前向传播收集统计
    with torch.no_grad():
        for images, _ in dataloader:
            model(images)
            break
    
    # 移除hooks
    for h in hooks:
        h.remove()
    
    # 替换为量化层（简化）
    print("量化参数:")
    for name in scales:
        print(f"{name}: scale={scales[name]:.6f}, zero_point={zero_points[name]:.2f}")
    
    return scales, zero_points

# 使用示例
if __name__ == '__main__':
    model = VisionTransformer()
    model.load_state_dict(torch.load('model.pth'))
    
    # 量化
    scales, zero_points = quantize_model(model, dataloader)
    
    # 保存量化模型
    torch.save({
        'state_dict': model.state_dict(),
        'scales': scales,
        'zero_points': zero_points
    }, 'quantized_model.pth')
```

---

### 阶段五：生成模型（2-3天）

#### 9. Diffusion Models
```python
class DiffusionModel(nn.Module):
    """扩散模型"""
    
    def __init__(self, in_channels=3, out_channels=3, time_dim=128):
        super(DiffusionModel, self).__init__()
        
        # 时间嵌入
        self.time_mlp = nn.Sequential(
            nn.Linear(1, time_dim),
            nn.ReLU(),
            nn.Linear(time_dim, time_dim),
        )
        
        # U-Net结构
        self.down1 = self._block(in_channels, 64, time_dim)
        self.down2 = self._block(64, 128, time_dim)
        self.down3 = self._block(128, 256, time_dim)
        
        self.bottleneck = self._block(256, 512, time_dim)
        
        self.up1 = self._block(512 + 256, 256, time_dim)
        self.up2 = self._block(256 + 128, 128, time_dim)
        self.up3 = self._block(128 + 64, 64, time_dim)
        
        self.final_conv = nn.Conv2d(64, out_channels, 1)
        
        self.pool = nn.MaxPool2d(2)
        self.upsample = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)
    
    def _block(self, in_channels, out_channels, time_dim):
        return nn.Sequential(
            nn.Conv2d(in_channels, out_channels, 3, padding=1),
            nn.GroupNorm(8, out_channels),
            nn.SiLU(),
            nn.Conv2d(out_channels, out_channels, 3, padding=1),
            nn.GroupNorm(8, out_channels),
            nn.SiLU(),
            TimeEmbedding(out_channels, time_dim),
        )
    
    def forward(self, x, t):
        # 时间嵌入
        t_emb = self.time_mlp(t)
        
        # 下采样
        d1 = self.down1(x, t_emb)
        d2 = self.down2(self.pool(d1), t_emb)
        d3 = self.down3(self.pool(d2), t_emb)
        
        # 瓶颈
        b = self.bottleneck(self.pool(d3), t_emb)
        
        # 上采样
        u1 = self.up1(self.upsample(b), t_emb, d3)
        u2 = self.up2(self.upsample(u1), t_emb, d2)
        u3 = self.up3(self.upsample(u2), t_emb, d1)
        
        return self.final_conv(u3)

class TimeEmbedding(nn.Module):
    """时间嵌入层"""
    
    def __init__(self, channels, time_dim):
        super(TimeEmbedding, self).__init__()
        self.mlp = nn.Sequential(
            nn.SiLU(),
            nn.Linear(time_dim, channels),
        )
    
    def forward(self, x, t_emb):
        return x + self.mlp(t_emb).unsqueeze(-1).unsqueeze(-1)

class Diffusion:
    """扩散过程"""
    
    def __init__(self, timesteps=1000, beta_start=0.0001, beta_end=0.02):
        self.timesteps = timesteps
        
        # 线性beta调度
        self.betas = torch.linspace(beta_start, beta_end, timesteps)
        self.alphas = 1. - self.betas
        self.alpha_bars = torch.cumprod(self.alphas, dim=0)
    
    def q_sample(self, x_0, t, noise=None):
        """前向扩散过程"""
        if noise is None:
            noise = torch.randn_like(x_0)
        
        alpha_bar_t = self.alpha_bars[t].reshape(-1, 1, 1, 1)
        sqrt_alpha_bar_t = torch.sqrt(alpha_bar_t)
        sqrt_one_minus_alpha_bar_t = torch.sqrt(1 - alpha_bar_t)
        
        return sqrt_alpha_bar_t * x_0 + sqrt_one_minus_alpha_bar_t * noise
    
    def p_losses(self, model, x_0, t):
        """训练损失"""
        noise = torch.randn_like(x_0)
        x_noisy = self.q_sample(x_0, t, noise)
        
        # 预测噪声
        predicted_noise = model(x_noisy, t)
        
        # MSE损失
        loss = F.mse_loss(predicted_noise, noise)
        return loss
    
    def p_sample(self, model, x, t, t_index):
        """采样过程"""
        betas_t = self.betas[t_index]
        alphas_t = self.alphas[t_index]
        alpha_bar_t = self.alpha_bars[t_index]
        
        if t_index > 0:
            z = torch.randn_like(x)
        else:
            z = torch.zeros_like(x)
        
        # 预测噪声
        noise_pred = model(x, t)
        
        # 去噪
        x = (1 / torch.sqrt(alphas_t)) * (x - (betas_t / torch.sqrt(1 - alpha_bar_t)) * noise_pred) + torch.sqrt(betas_t) * z
        
        return x
    
    def sample(self, model, image_size, batch_size=1, channels=3):
        """生成样本"""
        model.eval()
        
        # 从纯噪声开始
        x = torch.randn((batch_size, channels, image_size, image_size))
        
        for i in reversed(range(self.timesteps)):
            t = torch.full((batch_size,), i, device=x.device, dtype=torch.long)
            x = self.p_sample(model, x, t, i)
        
        return x

def train_diffusion(model, dataloader, optimizer, epochs=100):
    """训练扩散模型"""
    diffusion = Diffusion(timesteps=1000)
    model.train()
    
    for epoch in range(epochs):
        total_loss = 0
        
        for images, _ in dataloader:
            images = images.to(next(model.parameters()).device)
            
            # 随机时间步
            t = torch.randint(0, diffusion.timesteps, (images.shape[0],), device=images.device)
            
            # 计算损失
            loss = diffusion.p_losses(model, images, t)
            
            # 反向传播
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
        
        print(f"Epoch {epoch+1}: Loss = {total_loss / len(dataloader):.4f}")

# 使用示例
if __name__ == '__main__':
    model = DiffusionModel()
    optimizer = torch.optim.AdamW(model.parameters(), lr=2e-4)
    
    # 训练
    # train_diffusion(model, dataloader, optimizer)
    
    # 采样
    diffusion = Diffusion()
    # generated = diffusion.sample(model, image_size=64, batch_size=8)
```

---

### 阶段六：3D视觉进阶（2-3天）

#### 10. NeRF (Neural Radiance Fields)
```python
class NeRF(nn.Module):
    """NeRF模型"""
    
    def __init__(self, D=8, W=256, input_ch=3, input_ch_views=3, output_ch=4, skips=[4]):
        super(NeRF, self).__init__()
        
        self.D = D
        self.W = W
        self.input_ch = input_ch
        self.input_ch_views = input_ch_views
        self.skips = skips
        
        # 位置编码
        self.embed_fn = None
        self.embed_fn_fn = None
        
        # 网络层
        self.layers = nn.ModuleList()
        self.layers.append(nn.Linear(input_ch, W))
        
        for i in range(D - 1):
            if i in skips:
                self.layers.append(nn.Linear(W + input_ch, W))
            else:
                self.layers.append(nn.Linear(W, W))
        
        # 输出层
        self.feature_layer = nn.Linear(W, W)
        self.density_layer = nn.Linear(W, 1)
        self.rgb_layer = nn.Linear(W + input_ch_views, 3)
        
        # 激活函数
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x):
        input_pts = x[:, :self.input_ch]
        input_views = x[:, self.input_ch:]
        
        h = input_pts
        for i, layer in enumerate(self.layers):
            h = self.relu(layer(h))
            if i in self.skips:
                h = torch.cat([h, input_pts], dim=-1)
        
        feature = self.feature_layer(h)
        density = self.density_layer(feature)
        rgb = self.rgb_layer(torch.cat([feature, input_views], dim=-1))
        
        return torch.cat([rgb, density], dim=-1)

class NeRFTrainer:
    """NeRF训练器"""
    
    def __init__(self, model, lr=5e-4):
        self.model = model
        self.optimizer = torch.optim.Adam(model.parameters(), lr=lr)
        self.loss_fn = nn.MSELoss()
    
    def render_rays(self, rays, t_near, t_far, n_samples=64):
        """渲染光线"""
        # 采样点
        t = torch.linspace(t_near, t_far, n_samples, device=rays.device)
        t = t + torch.rand_like(t) * (t_far - t_near) / n_samples
        
        # 采样位置
        rays = rays.unsqueeze(1)  # (N, 1, 3)
        pts = rays * t.unsqueeze(0).unsqueeze(-1)  # (N, n_samples, 3)
        
        # 输入网络
        view_dirs = rays / torch.norm(rays, dim=-1, keepdim=True)
        view_dirs = view_dirs.expand_as(pts)
        
        # 位置编码
        pts_encoded = self.positional_encoding(pts)
        view_dirs_encoded = self.positional_encoding(view_dirs)
        
        # 扩展维度
        input_pts = pts_encoded.view(-1, pts_encoded.shape[-1])
        input_views = view_dirs_encoded.view(-1, view_dirs_encoded.shape[-1])
        
        # 网络前向
        network_input = torch.cat([input_pts, input_views], dim=-1)
        outputs = self.model(network_input)
        
        # 重塑
        outputs = outputs.view(pts.shape[0], pts.shape[1], -1)
        
        # 密度和颜色
        sigma = outputs[..., 3]
        rgb = torch.sigmoid(outputs[..., :3])
        
        # 体积渲染
        delta = t[1] - t[0]
        alpha = 1 - torch.exp(-sigma * delta)
        
        weights = alpha * torch.cumprod(torch.cat([
            torch.ones_like(alpha[:, :1]),
            1 - alpha[:, :-1]
        ], dim=1), dim=1)
        
        # 颜色加权和
        rgb_map = torch.sum(weights.unsqueeze(-1) * rgb, dim=1)
        
        # 深度
        depth_map = torch.sum(weights * t, dim=1)
        
        return rgb_map, depth_map, weights
    
    def positional_encoding(self, x, L=10):
        """位置编码"""
        encodings = [x]
        for i in range(L):
            encodings.append(torch.sin(2 ** i * torch.pi * x))
            encodings.append(torch.cos(2 ** i * torch.pi * x))
        return torch.cat(encodings, dim=-1)
    
    def train_step(self, rays, rgbs, t_near, t_far):
        """训练一步"""
        self.optimizer.zero_grad()
        
        rgb_map, _, _ = self.render_rays(rays, t_near, t_far)
        
        loss = self.loss_fn(rgb_map, rgbs)
        loss.backward()
        
        self.optimizer.step()
        
        return loss.item()

# 使用示例
if __name__ == '__main__':
    model = NeRF()
    trainer = NeRFTrainer(model)
    
    # 训练循环
    # for epoch in range(epochs):
    #     for rays, rgbs in dataloader:
    #         loss = trainer.train_step(rays, rgbs, t_near=2.0, t_far=6.0)
    #         print(f"Loss: {loss:.4f}")
```

---

### 阶段七：具身智能（2-3天）

#### 11. 视觉导航
```python
class VisualNavigation(nn.Module):
    """视觉导航网络"""
    
    def __init__(self, action_dim=4, hidden_dim=256):
        super(VisualNavigation, self).__init__()
        
        # 视觉编码器
        self.visual_encoder = nn.Sequential(
            nn.Conv2d(3, 32, 8, stride=4),
            nn.ReLU(),
            nn.Conv2d(32, 64, 4, stride=2),
            nn.ReLU(),
            nn.Conv2d(64, 64, 3, stride=1),
            nn.ReLU(),
            nn.Flatten(),
        )
        
        # 状态编码器
        self.state_encoder = nn.Linear(7, hidden_dim)  # 位置(x,y,z) + 朝向(quaternion)
        
        # 融合层
        self.fusion = nn.Linear(64 * 7 * 7 + hidden_dim, hidden_dim)
        
        # 策略网络
        self.policy = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim),
        )
        
        # 价值网络
        self.value = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )
    
    def forward(self, image, state):
        # 视觉特征
        vis_feat = self.visual_encoder(image)
        
        # 状态特征
        state_feat = self.state_encoder(state)
        
        # 融合
        fused = torch.cat([vis_feat, state_feat], dim=-1)
        fused = self.fusion(fused)
        
        # 策略和价值
        action_logits = self.policy(fused)
        value = self.value(fused)
        
        return action_logits, value

class NavigationAgent:
    """导航智能体"""
    
    def __init__(self, model, gamma=0.99, lr=1e-4):
        self.model = model
        self.optimizer = torch.optim.Adam(model.parameters(), lr=lr)
        self.gamma = gamma
    
    def act(self, image, state, deterministic=False):
        """选择动作"""
        with torch.no_grad():
            action_logits, value = self.model(image, state)
            
            if deterministic:
                action = torch.argmax(action_logits, dim=-1)
            else:
                probs = F.softmax(action_logits, dim=-1)
                action = torch.multinomial(probs, 1)
            
            return action, value
    
    def update(self, memory):
        """PPO风格更新"""
        # 收集的经验: (state, action, reward, next_state, done)
        
        # 计算优势
        advantages = []
        returns = []
        
        # 简化的PPO更新
        for batch in memory.sample_batch():
            images, states, actions, rewards, next_images, next_states, dones = batch
            
            # 当前值和下一个值
            _, values = self.model(images, states)
            _, next_values = self.model(next_images, next_states)
            
            # 计算返回
            returns_batch = rewards + self.gamma * next_values * (1 - dones)
            
            # 优势
            advantages_batch = returns_batch - values
            
            # 策略损失
            action_logits, _ = self.model(images, states)
            probs = F.softmax(action_logits, dim=-1)
            action_probs = probs.gather(1, actions)
            
            policy_loss = -torch.log(action_probs) * advantages_batch.detach()
            
            # 价值损失
            value_loss = F.mse_loss(values, returns_batch.detach())
            
            # 总损失
            loss = policy_loss.mean() + 0.5 * value_loss.mean()
            
            # 更新
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

# 使用示例
if __name__ == '__main__':
    model = VisualNavigation()
    agent = NavigationAgent(model)
    
    # 训练循环
    # for episode in range(1000):
    #     obs = env.reset()
    #     done = False
    #     while not done:
    #         action, value = agent.act(obs['image'], obs['state'])
    #         next_obs, reward, done, info = env.step(action)
    #         memory.add(obs, action, reward, next_obs, done)
    #         obs = next_obs
    #     
    #     if episode % 10 == 0:
    #         agent.update(memory)
```

---

## 🎯 实践项目

### 项目1：ViT图像分类器
```python
"""
目标：使用ViT在CIFAR-10上达到85%+准确率
步骤：
1. 实现ViT模型
2. 数据增强
3. 训练循环
4. 与ResNet对比
"""
```

### 项目2：自监督预训练
```python
"""
目标：使用SimCLR在无标签数据上预训练，然后在有标签数据上微调
步骤：
1. SimCLR预训练
2. 线性评估
3. 对比有无预训练的性能
"""
```

### 项目3：CLIP零样本分类
```python
"""
目标：使用CLIP实现零样本图像分类
步骤：
1. 加载预训练CLIP
2. 构建文本提示
3. 计算相似度
4. 评估零样本性能
"""
```

### 项目4：模型压缩实战
```python
"""
目标：将ResNet50压缩到1/4大小，精度损失<2%
步骤：
1. 知识蒸馏
2. 量化
3. 剪枝
4. 性能对比
"""
```

---

## 📊 性能对比

| 技术 | 参数量 | 计算量 | 准确率 | 适用场景 |
|------|--------|--------|--------|----------|
| ViT-Base | 86M | 17.6G | 81.8% | 大规模分类 |
| Swin-Tiny | 28M | 4.5G | 81.2% | 通用任务 |
| DETR | 40M | - | 42.0 mAP | 目标检测 |
| SimCLR | 28M | 1.3G | 76.5% | 自监督 |
| CLIP | 151M | - | 76.2% | 多模态 |
| MobileNetV2 | 3.4M | 0.3G | 72.0% | 移动端 |

---

## 🔍 调试技巧

### 1. 训练不稳定
```python
# 检查梯度
def check_gradients(model):
    for name, param in model.named_parameters():
        if param.grad is not None:
            grad_norm = param.grad.norm().item()
            if grad_norm > 1e3:
                print(f"⚠️ {name}: 梯度爆炸 {grad_norm:.2e}")
            elif grad_norm < 1e-5:
                print(f"⚠️ {name}: 梯度消失 {grad_norm:.2e}")
```

### 2. 内存优化
```python
# 梯度累积
def train_with_accumulation(model, dataloader, optimizer, accumulation_steps=4):
    optimizer.zero_grad()
    
    for i, (images, labels) in enumerate(dataloader):
        outputs = model(images)
        loss = criterion(outputs, labels) / accumulation_steps
        loss.backward()
        
        if (i + 1) % accumulation_steps == 0:
            optimizer.step()
            optimizer.zero_grad()
```

### 3. 性能分析
```python
# 使用torch.profiler
from torch.profiler import profile, record_function

with profile() as prof:
    with record_function("model_inference"):
        model(images)

prof.export_chrome_trace("trace.json")  # 在chrome://tracing查看
```

---

## 📚 学习检查清单

### Transformer
- [ ] 理解自注意力机制
- [ ] 掌握位置编码
- [ ] 实现ViT
- [ ] 理解Swin的窗口注意力
- [ ] 掌握DETR的匹配机制

### 自监督
- [ ] 理解对比学习
- [ ] 实现SimCLR
- [ ] 理解掩码建模
- [ ] 实现MAE
- [ ] 掌握预训练-微调流程

### 多模态
- [ ] 理解CLIP原理
- [ ] 掌握图文对齐
- [ ] 实现零样本推理
- [ ] 了解BLIP等扩展

### 模型压缩
- [ ] 理解知识蒸馏
- [ ] 掌握量化方法
- [ ] 了解剪枝技术
- [ ] 实现部署流程

### 生成模型
- [ ] 理解扩散过程
- [ ] 掌握采样算法
- [ ] 了解GAN原理
- [ ] 实现简单生成器

### 3D视觉
- [ ] 理解NeRF原理
- [ ] 掌握体积渲染
- [ ] 了解点云处理
- [ ] 实现3D重建

### 具身智能
- [ ] 理解强化学习
- [ ] 掌握策略梯度
- [ ] 了解视觉导航
- [ ] 实现简单智能体

---

## 🚀 下一步学习

### 研究方向
1. **通用人工智能**：多任务学习、元学习
2. **具身智能**：机器人控制、视觉-语言-动作
3. **AIGC**：文生图、文生视频
4. **边缘智能**：轻量化、实时推理

### 工程方向
1. **大规模训练**：分布式训练、混合精度
2. **模型部署**：TensorRT、ONNX Runtime
3. **MLOps**：实验跟踪、模型版本管理
4. **生产系统**：微服务、API设计

---

## 📖 扩展资源

### 论文
1. **ViT**: "An Image is Worth 16x16 Words" (2020)
2. **Swin**: "Swin Transformer" (2021)
3. **DETR**: "End-to-End Object Detection with Transformers" (2020)
4. **SimCLR**: "A Simple Framework for Contrastive Learning" (2020)
5. **MAE**: "Masked Autoencoders Are Scalable Vision Learners" (2021)
6. **CLIP**: "Learning Transferable Visual Models From Natural Language Supervision" (2021)
7. **Diffusion**: "Denoising Diffusion Probabilistic Models" (2020)
8. **NeRF**: "NeRF: Representing Scenes as Neural Radiance Fields" (2020)

### 开源项目
- **timm**: https://github.com/rwightman/pytorch-image-models
- **open_clip**: https://github.com/mlfoundations/open_clip
- **diffusers**: https://github.com/huggingface/diffusers
- **nerfstudio**: https://github.com/nerfstudio-project/nerfstudio

---

**恭喜！完成进阶主题学习，你已经站在了计算机视觉的前沿！** 🎉

*最后更新：2025年12月*
