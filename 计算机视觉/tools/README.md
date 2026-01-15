# 计算机视觉工具软件大全

> **一句话总结**: 计算机视觉工具软件大全的详细讲解与实战指南

> **难度等级**: ⭐⭐⭐ (中级)
> **预计学习时间**: 4-5天
> **前置知识**: 待补充
> **学习目标**:
> - 理论: 待补充
> - 实践: 待补充
> - 应用: 待补充

---


> 实用的脚本、模板和工具集合，帮助你快速搭建开发环境、提高工作效率。

## 📁 目录结构

```
工具软件/
├── 环境配置/
│   ├── setup_env.sh          # 一键环境配置
│   ├── requirements.txt      # 依赖包列表
│   └── conda_env.yml        # Conda环境配置
├── 代码模板/
│   ├── train_template.py     # 训练脚本模板
│   ├── model_template.py     # 模型定义模板
│   └── dataset_template.py   # 数据集模板
├── 实用脚本/
│   ├── data_utils.py         # 数据处理工具
│   ├── model_utils.py        # 模型工具
│   └── vis_utils.py          # 可视化工具
├── 性能分析/
│   ├── profiler.py           # 性能分析器
│   ├── memory_check.py       # 内存检查
│   └── benchmark.py          # 基准测试
└── 自动化/
    ├── train.sh              # 训练自动化
    ├── evaluate.sh           # 评估自动化
    └── deploy.sh             # 部署脚本
```

---

## 🛠️ 环境配置

### 1. 一键环境配置脚本

```python
#!/bin/bash
# setup_env.sh - 计算机视觉环境一键配置

echo "🚀 开始配置计算机视觉开发环境..."

# 1. 创建Conda环境

echo "📦 创建Conda环境..."
conda create -n cv python=3.9 -y
conda activate cv

# 2. 安装PyTorch

echo "🔥 安装PyTorch..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 3. 安装计算机视觉库

echo "📷 安装CV库..."
pip install opencv-python pillow matplotlib seaborn
pip install scikit-learn scikit-image
pip install pandas numpy scipy

# 4. 安装深度学习工具

echo "🧠 安装DL工具..."
pip install tensorboard wandb tqdm
pip install albumentations timm

# 5. 安装检测和分割库

echo "🎯 安装检测分割库..."
pip install ultralytics  # YOLOv8
pip install segmentation-models-pytorch

# 6. 安装部署工具

echo "🚀 安装部署工具..."
pip install onnx onnxruntime
pip install tensorrt  # 需要单独安装TensorRT

# 7. 验证安装

echo "✅ 验证安装..."
python -c "import torch; print(f'PyTorch版本: {torch.__version__}')"
python -c "import cv2; print(f'OpenCV版本: {cv2.__version__}')"
python -c "import ultralytics; print('YOLOv8可用')"

echo "🎉 环境配置完成！"
echo "激活环境: conda activate cv"
```

**使用方法**：
```python
chmod +x setup_env.sh
./setup_env.sh
```

---

### 2. Conda环境配置文件

```bash
# conda_env.yml

name: cv
channels:
  - pytorch
  - nvidia
  - conda-forge
  - defaults
dependencies:
  - python=3.9
  - pytorch=2.0.1
  - torchvision=0.15.2
  - torchaudio=2.0.2
  - cudatoolkit=11.8
  - pip
  - pip:
    - opencv-python==4.8.1.78
    - pillow==10.0.1
    - matplotlib==3.7.2
    - seaborn==0.12.2
    - numpy==1.24.3
    - pandas==2.0.3
    - scikit-learn==1.3.0
    - scikit-image==0.21.0
    - tensorboard==2.14.0
    - wandb==0.15.8
    - tqdm==4.66.1
    - albumentations==1.3.1
    - ultralytics==8.0.176
    - segmentation-models-pytorch==0.3.3
    - onnx==1.14.1
    - onnxruntime==1.15.1
```

**使用方法**：
```python
conda env create -f conda_env.yml
conda activate cv
```

---

### 3. 依赖包列表

```bash
# requirements.txt
# 基础科学计算

numpy>=1.21.0
pandas>=1.3.0
scipy>=1.7.0

# 图像处理

opencv-python>=4.5.0
Pillow>=8.3.0
scikit-image>=0.18.0

# 深度学习

torch>=1.9.0
torchvision>=0.10.0
timm>=0.9.0

# 可视化

matplotlib>=3.3.0
seaborn>=0.11.0
tensorboard>=2.7.0

# 训练工具

tqdm>=4.62.0
wandb>=0.12.0
albumentations>=1.0.0

# 部署

onnx>=1.10.0
onnxruntime>=1.10.0

# 检测分割

ultralytics>=8.0.0
segmentation-models-pytorch>=0.3.0
```

**使用方法**：
```bash
pip install -r requirements.txt
```

---

## 📝 代码模板

### 1. 训练脚本模板

```bash
# train_template.py

"""
通用训练脚本模板
支持：PyTorch训练、日志记录、模型保存、断点续训
"""

import argparse
import os
import time
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm
import logging

def get_args():
    parser = argparse.ArgumentParser(description='训练脚本')
    
    # 数据相关
    parser.add_argument('--data_dir', type=str, default='./data')
    parser.add_argument('--batch_size', type=int, default=32)
    parser.add_argument('--num_workers', type=int, default=4)
    
    # 模型相关
    parser.add_argument('--model_name', type=str, default='resnet50')
    parser.add_argument('--num_classes', type=int, default=10)
    parser.add_argument('--pretrained', action='store_true', default=True)
    
    # 训练相关
    parser.add_argument('--epochs', type=int, default=100)
    parser.add_argument('--lr', type=float, default=1e-3)
    parser.add_argument('--optimizer', type=str, default='adam')
    parser.add_argument('--device', type=str, default='cuda')
    
    # 保存相关
    parser.add_argument('--save_dir', type=str, default='./checkpoints')
    parser.add_argument('--log_dir', type=str, default='./logs')
    parser.add_argument('--save_freq', type=int, default=10)
    
    # 断点续训
    parser.add_argument('--resume', type=str, default=None)
    
    return parser.parse_args()

def setup_logging(save_dir):
    """设置日志"""
    os.makedirs(save_dir, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(save_dir, 'train.log')),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def build_model(args):
    """构建模型"""
    # 这里替换为实际模型
    model = nn.Sequential(
        nn.Conv2d(3, 64, 3, padding=1),
        nn.ReLU(),
        nn.MaxPool2d(2),
        nn.Flatten(),
        nn.Linear(64 * 16 * 16, args.num_classes)
    )
    return model

def build_dataset(args):
    """构建数据集"""
    # 这里替换为实际数据集
    from torch.utils.data import TensorDataset
    import numpy as np
    
    # 模拟数据
    x_train = torch.randn(1000, 3, 32, 32)
    y_train = torch.randint(0, args.num_classes, (1000,))
    x_val = torch.randn(200, 3, 32, 32)
    y_val = torch.randint(0, args.num_classes, (200,))
    
    train_dataset = TensorDataset(x_train, y_train)
    val_dataset = TensorDataset(x_val, y_val)
    
    return train_dataset, val_dataset

def train_one_epoch(model, dataloader, criterion, optimizer, device, epoch, writer, logger):
    """训练一个epoch"""
    model.train()
    total_loss = 0
    total_correct = 0
    
    progress_bar = tqdm(dataloader, desc=f'Epoch {epoch}')
    
    for batch_idx, (data, target) in enumerate(progress_bar):
        data, target = data.to(device), target.to(device)
        
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
        _, predicted = output.max(1)
        total_correct += predicted.eq(target).sum().item()
        
        # 更新进度条
        progress_bar.set_postfix({
            'loss': loss.item(),
            'acc': 100. * predicted.eq(target).sum().item() / target.size(0)
        })
        
        # 记录到TensorBoard
        global_step = epoch * len(dataloader) + batch_idx
        writer.add_scalar('Train/Loss', loss.item(), global_step)
        writer.add_scalar('Train/Accuracy', 100. * predicted.eq(target).sum().item() / target.size(0), global_step)
    
    epoch_loss = total_loss / len(dataloader)
    epoch_acc = 100. * total_correct / len(dataloader.dataset)
    
    logger.info(f'Train Epoch {epoch}: Loss={epoch_loss:.4f}, Acc={epoch_acc:.2f}%')
    
    return epoch_loss, epoch_acc

def validate(model, dataloader, criterion, device, epoch, writer, logger):
    """验证"""
    model.eval()
    total_loss = 0
    total_correct = 0
    
    with torch.no_grad():
        for data, target in dataloader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            loss = criterion(output, target)
            
            total_loss += loss.item()
            _, predicted = output.max(1)
            total_correct += predicted.eq(target).sum().item()
    
    val_loss = total_loss / len(dataloader)
    val_acc = 100. * total_correct / len(dataloader.dataset)
    
    writer.add_scalar('Val/Loss', val_loss, epoch)
    writer.add_scalar('Val/Accuracy', val_acc, epoch)
    
    logger.info(f'Val Epoch {epoch}: Loss={val_loss:.4f}, Acc={val_acc:.2f}%')
    
    return val_loss, val_acc

def save_checkpoint(state, is_best, save_dir, epoch):
    """保存检查点"""
    os.makedirs(save_dir, exist_ok=True)
    
    # 保存最新模型
    torch.save(state, os.path.join(save_dir, 'latest.pth'))
    
    # 保存最佳模型
    if is_best:
        torch.save(state, os.path.join(save_dir, 'best.pth'))
    
    # 定期保存
    if epoch % 10 == 0:
        torch.save(state, os.path.join(save_dir, f'epoch_{epoch}.pth'))

def main():
    args = get_args()
    
    # 设置
    device = torch.device(args.device if torch.cuda.is_available() else 'cpu')
    logger = setup_logging(args.save_dir)
    writer = SummaryWriter(args.log_dir)
    
    logger.info(f'配置: {args}')
    logger.info(f'设备: {device}')
    
    # 数据
    logger.info('加载数据...')
    train_dataset, val_dataset = build_dataset(args)
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, 
                             shuffle=True, num_workers=args.num_workers)
    val_loader = DataLoader(val_dataset, batch_size=args.batch_size, 
                           shuffle=False, num_workers=args.num_workers)
    
    # 模型
    logger.info('构建模型...')
    model = build_model(args).to(device)
    
    # 损失和优化器
    criterion = nn.CrossEntropyLoss()
    if args.optimizer == 'adam':
        optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)
    elif args.optimizer == 'sgd':
        optimizer = torch.optim.SGD(model.parameters(), lr=args.lr, momentum=0.9)
    
    # 断点续训
    start_epoch = 0
    best_acc = 0
    if args.resume:
        logger.info(f'加载检查点: {args.resume}')
        checkpoint = torch.load(args.resume)
        model.load_state_dict(checkpoint['model'])
        optimizer.load_state_dict(checkpoint['optimizer'])
        start_epoch = checkpoint['epoch'] + 1
        best_acc = checkpoint.get('best_acc', 0)
    
    # 训练循环
    logger.info('开始训练...')
    for epoch in range(start_epoch, args.epochs):
        # 训练
        train_loss, train_acc = train_one_epoch(
            model, train_loader, criterion, optimizer, device, epoch, writer, logger
        )
        
        # 验证
        val_loss, val_acc = validate(model, val_loader, criterion, device, epoch, writer, logger)
        
        # 保存
        is_best = val_acc > best_acc
        if is_best:
            best_acc = val_acc
        
        save_checkpoint({
            'epoch': epoch,
            'model': model.state_dict(),
            'optimizer': optimizer.state_dict(),
            'train_loss': train_loss,
            'train_acc': train_acc,
            'val_loss': val_loss,
            'val_acc': val_acc,
            'best_acc': best_acc,
            'args': args
        }, is_best, args.save_dir, epoch)
        
        logger.info(f'Epoch {epoch}: Val Acc={val_acc:.2f}%, Best={best_acc:.2f}%')
    
    writer.close()
    logger.info('训练完成！')

if __name__ == '__main__':
    main()
```

**使用方法**：
```python
python train_template.py --data_dir ./data --batch_size 32 --epochs 100 --lr 1e-3
```

---

### 2. 模型定义模板

```bash
# model_template.py

"""
模型定义模板
支持：自定义模型、预训练模型、模型保存与加载
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models
import timm

class BaseModel(nn.Module):
    """基础模型类"""
    
    def __init__(self, num_classes=10, pretrained=True):
        super(BaseModel, self).__init__()
        self.num_classes = num_classes
        
    def forward(self, x):
        raise NotImplementedError
    
    def count_params(self):
        """计算参数量"""
        return sum(p.numel() for p in self.parameters() if p.requires_grad)
    
    def count_flops(self, input_size=(1, 3, 224, 224)):
        """估算FLOPs（简化版）"""
        # 实际使用时使用thop库
        from thop import profile
        dummy_input = torch.randn(input_size)
        flops, params = profile(self, inputs=(dummy_input,))
        return flops, params

class CustomCNN(BaseModel):
    """自定义CNN"""
    
    def __init__(self, num_classes=10, pretrained=False):
        super(CustomCNN, self).__init__(num_classes, pretrained)
        
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            
            nn.Conv2d(64, 128, 3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            
            nn.Conv2d(128, 256, 3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
        )
        
        self.classifier = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(256 * 4 * 4, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(512, num_classes),
        )
        
        # 初始化
        self._initialize_weights()
    
    def _initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                nn.init.constant_(m.bias, 0)
    
    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x

class PretrainedModel(BaseModel):
    """预训练模型"""
    
    def __init__(self, model_name='resnet50', num_classes=10, pretrained=True):
        super(PretrainedModel, self).__init__(num_classes, pretrained)
        
        # 使用timm库
        if model_name in timm.list_models():
            self.backbone = timm.create_model(
                model_name, 
                pretrained=pretrained, 
                num_classes=num_classes
            )
        else:
            # 使用torchvision
            model_func = getattr(models, model_name, None)
            if model_func is None:
                raise ValueError(f"不支持的模型: {model_name}")
            
            self.backbone = model_func(pretrained=pretrained)
            
            # 替换最后的全连接层
            if hasattr(self.backbone, 'fc'):
                in_features = self.backbone.fc.in_features
                self.backbone.fc = nn.Linear(in_features, num_classes)
            elif hasattr(self.backbone, 'classifier'):
                in_features = self.backbone.classifier.in_features
                self.backbone.classifier = nn.Linear(in_features, num_classes)
    
    def forward(self, x):
        return self.backbone(x)

class EnsembleModel(BaseModel):
    """模型集成"""
    
    def __init__(self, models_list, num_classes=10):
        super(EnsembleModel, self).__init__(num_classes, False)
        self.models = nn.ModuleList(models_list)
        self.num_classes = num_classes
    
    def forward(self, x):
        outputs = []
        for model in self.models:
            outputs.append(F.softmax(model(x), dim=1))
        
        # 平均集成
        avg_output = torch.stack(outputs).mean(dim=0)
        return avg_output

def get_model(model_name, num_classes=10, pretrained=True):
    """获取模型工厂函数"""
    if model_name in ['resnet18', 'resnet34', 'resnet50', 'resnet101', 'resnet152']:
        return PretrainedModel(model_name, num_classes, pretrained)
    elif model_name in ['mobilenet_v2', 'efficientnet_b0', 'efficientnet_b3']:
        return PretrainedModel(model_name, num_classes, pretrained)
    elif model_name == 'custom':
        return CustomCNN(num_classes, pretrained)
    else:
        raise ValueError(f"未知模型: {model_name}")

def save_model(model, path, optimizer=None, epoch=None, metrics=None):
    """保存模型"""
    checkpoint = {
        'model_state_dict': model.state_dict(),
        'num_classes': model.num_classes,
    }
    
    if optimizer:
        checkpoint['optimizer_state_dict'] = optimizer.state_dict()
    if epoch:
        checkpoint['epoch'] = epoch
    if metrics:
        checkpoint['metrics'] = metrics
    
    torch.save(checkpoint, path)
    print(f"模型已保存: {path}")

def load_model(path, model=None, device='cuda'):
    """加载模型"""
    checkpoint = torch.load(path, map_location=device)
    
    if model is None:
        # 重建模型
        num_classes = checkpoint.get('num_classes', 10)
        model = CustomCNN(num_classes)
    
    model.load_state_dict(checkpoint['model_state_dict'])
    model.to(device)
    
    return model, checkpoint

# 使用示例

if __name__ == '__main__':
    # 创建模型
    model = get_model('resnet50', num_classes=10)
    print(f"参数量: {model.count_params():,}")
    
    # 测试前向传播
    x = torch.randn(1, 3, 224, 224)
    output = model(x)
    print(f"输出形状: {output.shape}")
    
    # 保存模型
    save_model(model, 'model.pth', metrics={'acc': 0.95})
    
    # 加载模型
    loaded_model, checkpoint = load_model('model.pth')
    print(f"加载完成，检查点: {checkpoint.keys()}")
```

---

### 3. 数据集模板

```bash
# dataset_template.py

"""
数据集模板
支持：自定义数据集、数据增强、数据可视化
"""

import os
import cv2
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
import albumentations as A
from albumentations.pytorch import ToTensorV2
import matplotlib.pyplot as plt

class BaseDataset(Dataset):
    """基础数据集类"""
    
    def __init__(self, data_dir, transform=None, mode='train'):
        self.data_dir = data_dir
        self.transform = transform
        self.mode = mode
        self.samples = []
        
        self._load_samples()
    
    def _load_samples(self):
        """加载样本列表"""
        raise NotImplementedError
    
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        raise NotImplementedError
    
    def visualize(self, idx=0, num_samples=5):
        """可视化样本"""
        fig, axes = plt.subplots(1, num_samples, figsize=(15, 3))
        
        for i in range(min(num_samples, len(self))):
            img, label = self[i]
            if isinstance(img, torch.Tensor):
                img = img.permute(1, 2, 0).cpu().numpy()
            
            axes[i].imshow(img)
            axes[i].set_title(f'Label: {label}')
            axes[i].axis('off')
        
        plt.tight_layout()
        plt.show()

class ImageClassificationDataset(BaseDataset):
    """图像分类数据集"""
    
    def __init__(self, data_dir, transform=None, mode='train'):
        super().__init__(data_dir, transform, mode)
    
    def _load_samples(self):
        """假设目录结构: data_dir/class_name/image.jpg"""
        self.class_names = sorted(os.listdir(self.data_dir))
        self.class_to_idx = {name: idx for idx, name in enumerate(self.class_names)}
        
        for class_name in self.class_names:
            class_dir = os.path.join(self.data_dir, class_name)
            if not os.path.isdir(class_dir):
                continue
            
            for img_name in os.listdir(class_dir):
                if img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    img_path = os.path.join(class_dir, img_name)
                    self.samples.append((img_path, self.class_to_idx[class_name]))
    
    def __getitem__(self, idx):
        img_path, label = self.samples[idx]
        
        # 读取图像
        image = cv2.imread(img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # 应用变换
        if self.transform:
            image = self.transform(image=image)['image']
        
        return image, label

class SegmentationDataset(BaseDataset):
    """语义分割数据集"""
    
    def __init__(self, image_dir, mask_dir, transform=None, mode='train'):
        self.image_dir = image_dir
        self.mask_dir = mask_dir
        super().__init__(image_dir, transform, mode)
    
    def _load_samples(self):
        """假设图像和掩码文件名对应"""
        for img_name in os.listdir(self.image_dir):
            if img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(self.image_dir, img_name)
                mask_path = os.path.join(self.mask_dir, img_name)
                
                if os.path.exists(mask_path):
                    self.samples.append((img_path, mask_path))
    
    def __getitem__(self, idx):
        img_path, mask_path = self.samples[idx]
        
        # 读取图像和掩码
        image = cv2.imread(img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        
        # 应用变换
        if self.transform:
            transformed = self.transform(image=image, mask=mask)
            image = transformed['image']
            mask = transformed['mask']
        
        return image, mask

class DetectionDataset(BaseDataset):
    """目标检测数据集（支持COCO格式）"""
    
    def __init__(self, data_dir, annotation_file, transform=None, mode='train'):
        self.annotation_file = annotation_file
        super().__init__(data_dir, transform, mode)
    
    def _load_samples(self):
        """加载COCO格式标注"""
        import json
        
        with open(self.annotation_file, 'r') as f:
            self.coco = json.load(f)
        
        # 构建图像到标注的映射
        self.img_to_anns = {}
        for ann in self.coco['annotations']:
            img_id = ann['image_id']
            if img_id not in self.img_to_anns:
                self.img_to_anns[img_id] = []
            self.img_to_anns[img_id].append(ann)
        
        # 收集样本
        for img_info in self.coco['images']:
            img_path = os.path.join(self.data_dir, img_info['file_name'])
            if os.path.exists(img_path):
                self.samples.append((img_path, img_info['id']))
    
    def __getitem__(self, idx):
        img_path, img_id = self.samples[idx]
        
        # 读取图像
        image = cv2.imread(img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # 获取标注
        annotations = self.img_to_anns.get(img_id, [])
        boxes = []
        labels = []
        
        for ann in annotations:
            x, y, w, h = ann['bbox']
            boxes.append([x, y, x + w, y + h])
            labels.append(ann['category_id'])
        
        boxes = np.array(boxes, dtype=np.float32)
        labels = np.array(labels, dtype=np.int64)
        
        # 应用变换
        if self.transform:
            transformed = self.transform(image=image, bboxes=boxes, labels=labels)
            image = transformed['image']
            boxes = transformed['bboxes']
            labels = transformed['labels']
        
        return image, {'boxes': boxes, 'labels': labels}

def get_train_transform(img_size=224):
    """训练数据增强"""
    return A.Compose([
        A.Resize(img_size, img_size),
        A.HorizontalFlip(p=0.5),
        A.VerticalFlip(p=0.3),
        A.RandomRotate90(p=0.5),
        A.RandomBrightnessContrast(p=0.3),
        A.GaussNoise(p=0.2),
        A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ToTensorV2(),
    ])

def get_val_transform(img_size=224):
    """验证数据增强"""
    return A.Compose([
        A.Resize(img_size, img_size),
        A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ToTensorV2(),
    ])

def get_dataloader(dataset, batch_size=32, num_workers=4, shuffle=True):
    """获取数据加载器"""
    return DataLoader(
        dataset,
        batch_size=batch_size,
        num_workers=num_workers,
        shuffle=shuffle,
        pin_memory=True,
        drop_last=True if shuffle else False
    )

# 使用示例

if __name__ == '__main__':
    # 分类数据集
    train_transform = get_train_transform(224)
    train_dataset = ImageClassificationDataset(
        data_dir='./data/train',
        transform=train_transform,
        mode='train'
    )
    
    train_loader = get_dataloader(train_dataset, batch_size=32)
    
    # 可视化
    train_dataset.visualize(num_samples=5)
    
    # 测试加载
    for images, labels in train_loader:
        print(f"Batch shape: {images.shape}, Labels: {labels}")
        break
```

---

## 🔧 实用脚本

### 1. 数据处理工具

```bash
# data_utils.py

"""
数据处理实用工具
"""

import os
import cv2
import numpy as np
from pathlib import Path
import shutil
from tqdm import tqdm
import json
import random

class DataProcessor:
    """数据处理器"""
    
    @staticmethod
    def split_dataset(data_dir, train_ratio=0.8, val_ratio=0.1, seed=42):
        """
        划分数据集为train/val/test
        假设目录结构: data_dir/class_name/images
        """
        random.seed(seed)
        
        train_dir = Path(data_dir) / 'train'
        val_dir = Path(data_dir) / 'val'
        test_dir = Path(data_dir) / 'test'
        
        for class_dir in Path(data_dir).iterdir():
            if not class_dir.is_dir() or class_dir.name in ['train', 'val', 'test']:
                continue
            
            images = list(class_dir.glob('*.jpg')) + list(class_dir.glob('*.png'))
            random.shuffle(images)
            
            n_train = int(len(images) * train_ratio)
            n_val = int(len(images) * val_ratio)
            
            train_images = images[:n_train]
            val_images = images[n_train:n_train+n_val]
            test_images = images[n_train+n_val:]
            
            # 创建目录
            for split_dir in [train_dir, val_dir, test_dir]:
                class_split_dir = split_dir / class_dir.name
                class_split_dir.mkdir(parents=True, exist_ok=True)
            
            # 复制文件
            for img in train_images:
                shutil.copy(img, train_dir / class_dir.name / img.name)
            for img in val_images:
                shutil.copy(img, val_dir / class_dir.name / img.name)
            for img in test_images:
                shutil.copy(img, test_dir / class_dir.name / img.name)
        
        print(f"数据集划分完成: Train={train_ratio}, Val={val_ratio}, Test={1-train_ratio-val_ratio}")
    
    @staticmethod
    def resize_images(input_dir, output_dir, size=(512, 512)):
        """批量调整图像大小"""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        image_files = list(Path(input_dir).glob('*.jpg')) + list(Path(input_dir).glob('*.png'))
        
        for img_path in tqdm(image_files, desc="调整大小"):
            img = cv2.imread(str(img_path))
            img_resized = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
            cv2.imwrite(str(Path(output_dir) / img_path.name), img_resized)
    
    @staticmethod
    def convert_format(input_dir, output_dir, target_format='jpg'):
        """转换图像格式"""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        for img_path in Path(input_dir).glob('*'):
            if img_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                img = cv2.imread(str(img_path))
                new_name = img_path.stem + '.' + target_format
                cv2.imwrite(str(Path(output_dir) / new_name), img)
    
    @staticmethod
    def analyze_dataset(data_dir):
        """分析数据集统计信息"""
        stats = {
            'total_images': 0,
            'classes': {},
            'image_sizes': [],
            'mean': [],
            'std': []
        }
        
        for class_dir in Path(data_dir).iterdir():
            if not class_dir.is_dir():
                continue
            
            images = list(class_dir.glob('*.jpg')) + list(class_dir.glob('*.png'))
            class_name = class_dir.name
            stats['classes'][class_name] = len(images)
            stats['total_images'] += len(images)
            
            # 采样计算统计
            sample_images = random.sample(images, min(10, len(images)))
            for img_path in sample_images:
                img = cv2.imread(str(img_path))
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                stats['image_sizes'].append(img.shape[:2])
                stats['mean'].append(img_rgb.mean(axis=(0, 1)))
                stats['std'].append(img_rgb.std(axis=(0, 1)))
        
        # 计算平均统计
        if stats['mean']:
            stats['dataset_mean'] = np.mean(stats['mean'], axis=0) / 255.0
            stats['dataset_std'] = np.mean(stats['std'], axis=0) / 255.0
            stats['avg_size'] = np.mean(stats['image_sizes'], axis=0)
        
        return stats

class AnnotationConverter:
    """标注格式转换器"""
    
    @staticmethod
    def coco_to_yolo(coco_json, output_dir, image_dir):
        """COCO转YOLO格式"""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        with open(coco_json, 'r') as f:
            coco = json.load(f)
        
        # 构建映射
        img_id_to_info = {img['id']: img for img in coco['images']}
        cat_id_to_idx = {cat['id']: idx for idx, cat in enumerate(coco['categories'])}
        
        # 按图像分组标注
        annotations_by_image = {}
        for ann in coco['annotations']:
            img_id = ann['image_id']
            if img_id not in annotations_by_image:
                annotations_by_image[img_id] = []
            annotations_by_image[img_id].append(ann)
        
        # 转换
        for img_id, anns in annotations_by_image.items():
            img_info = img_id_to_info[img_id]
            img_w, img_h = img_info['width'], img_info['height']
            
            yolo_lines = []
            for ann in anns:
                x, y, w, h = ann['bbox']
                class_id = cat_id_to_idx[ann['category_id']]
                
                # COCO: [x, y, w, h] -> YOLO: [x_center, y_center, width, height]
                x_center = (x + w / 2) / img_w
                y_center = (y + h / 2) / img_h
                w_norm = w / img_w
                h_norm = h / img_h
                
                yolo_lines.append(f"{class_id} {x_center} {y_center} {w_norm} {h_norm}")
            
            # 保存
            txt_path = Path(output_dir) / (img_info['file_name'].replace('.jpg', '.txt'))
            with open(txt_path, 'w') as f:
                f.write('\n'.join(yolo_lines))
    
    @staticmethod
    def yolo_to_coco(yolo_dir, image_dir, output_json, class_names):
        """YOLO转COCO格式"""
        # 实现略复杂，需要遍历所有标注文件
        pass

# 使用示例

if __name__ == '__main__':
    # 划分数据集
    DataProcessor.split_dataset('./data/raw', train_ratio=0.7, val_ratio=0.15)
    
    # 分析数据集
    stats = DataProcessor.analyze_dataset('./data/train')
    print(f"数据集统计: {stats}")
    
    # 调整大小
    DataProcessor.resize_images('./data/train', './data/train_512', size=(512, 512))
```

---

### 2. 模型工具

```bash
# model_utils.py

"""
模型实用工具
"""

import torch
import torch.nn as nn
from torchsummary import summary
import numpy as np

class ModelAnalyzer:
    """模型分析器"""
    
    @staticmethod
    def model_info(model, input_size=(3, 224, 224)):
        """显示模型详细信息"""
        print("=" * 60)
        print("模型信息")
        print("=" * 60)
        
        # 参数量
        total_params = sum(p.numel() for p in model.parameters())
        trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
        
        print(f"总参数量: {total_params:,}")
        print(f"可训练参数: {trainable_params:,}")
        print(f"冻结参数: {total_params - trainable_params:,}")
        
        # 计算量（估算）
        # 需要安装thop: pip install thop
        try:
            from thop import profile
            dummy_input = torch.randn(1, *input_size)
            flops, params = profile(model, inputs=(dummy_input,))
            print(f"FLOPs: {flops / 1e9:.2f} G")
            print(f"参数量: {params / 1e6:.2f} M")
        except ImportError:
            print("提示: 安装 thop 以显示FLOPs: pip install thop")
        
        # 层级统计
        print("\n层级统计:")
        print("-" * 40)
        for name, module in model.named_modules():
            if isinstance(module, (nn.Conv2d, nn.Linear, nn.BatchNorm2d)):
                params = sum(p.numel() for p in module.parameters())
                print(f"{name:<30} {type(module).__name__:<15} {params:,}")
        
        return {
            'total_params': total_params,
            'trainable_params': trainable_params,
            'frozen_params': total_params - trainable_params
        }
    
    @staticmethod
    def count_params_by_layer(model):
        """按层统计参数量"""
        params_dict = {}
        for name, param in model.named_parameters():
            params_dict[name] = param.numel()
        
        return params_dict
    
    @staticmethod
    def visualize_model_structure(model, input_size=(3, 224, 224)):
        """可视化模型结构（简化版）"""
        print("\n模型结构:")
        print("-" * 50)
        
        def print_layer(module, indent=0):
            for name, child in module.named_children():
                prefix = "  " * indent
                print(f"{prefix}{name}: {type(child).__name__}")
                if hasattr(child, 'named_children'):
                    print_layer(child, indent + 1)
        
        print_layer(model)

class ModelOptimizer:
    """模型优化工具"""
    
    @staticmethod
    def freeze_layers(model, freeze_until=None):
        """
        冻结指定层之前的参数
        freeze_until: 层名，冻结直到该层（不包括）
        """
        freeze = True
        for name, param in model.named_parameters():
            if freeze_until and freeze_until in name:
                freeze = False
            
            param.requires_grad = not freeze
        
        # 打印冻结状态
        trainable = sum(p.requires_grad for p in model.parameters())
        frozen = sum(not p.requires_grad for p in model.parameters())
        print(f"冻结参数: {frozen:,}, 可训练参数: {trainable:,}")
    
    @staticmethod
    def set_lr(model, lr):
        """设置学习率"""
        for param_group in model.param_groups:
            param_group['lr'] = lr
    
    @staticmethod
    def add_weight_decay(model, weight_decay=1e-5, skip_list=()):
        """添加权重衰减（排除某些层）"""
        decay = []
        no_decay = []
        
        for name, param in model.named_parameters():
            if not param.requires_grad:
                continue
            
            if len(param.shape) == 1 or name.endswith(".bias") or name in skip_list:
                no_decay.append(param)
            else:
                decay.append(param)
        
        return [
            {'params': no_decay, 'weight_decay': 0.},
            {'params': decay, 'weight_decay': weight_decay}
        ]

class ModelEnsemble:
    """模型集成工具"""
    
    @staticmethod
    def load_models(model_paths, model_class, device='cuda'):
        """加载多个模型"""
        models = []
        for path in model_paths:
            model = model_class()
            checkpoint = torch.load(path, map_location=device)
            model.load_state_dict(checkpoint['model_state_dict'])
            model.to(device)
            model.eval()
            models.append(model)
        return models
    
    @staticmethod
    def predict_ensemble(models, inputs, method='mean'):
        """集成预测"""
        predictions = []
        with torch.no_grad():
            for model in models:
                pred = model(inputs)
                predictions.append(pred)
        
        if method == 'mean':
            return torch.stack(predictions).mean(dim=0)
        elif method == 'vote':
            # 分类投票
            preds = torch.stack([p.argmax(dim=1) for p in predictions])
            return torch.mode(preds, dim=0).values
        else:
            raise ValueError(f"不支持的方法: {method}")

# 使用示例

if __name__ == '__main__':
    # 创建示例模型
    model = nn.Sequential(
        nn.Conv2d(3, 64, 3),
        nn.ReLU(),
        nn.Conv2d(64, 128, 3),
        nn.ReLU(),
        nn.AdaptiveAvgPool2d(1),
        nn.Flatten(),
        nn.Linear(128, 10)
    )
    
    # 模型信息
    ModelAnalyzer.model_info(model, input_size=(3, 32, 32))
    
    # 冻结前两层
    ModelOptimizer.freeze_layers(model, freeze_until='2')
```

---

### 3. 可视化工具

```bash
# vis_utils.py

"""
可视化工具
"""

import matplotlib.pyplot as plt
import numpy as np
import cv2
import torch
from torchvision.utils import make_grid
import seaborn as sns
from sklearn.metrics import confusion_matrix, roc_curve, auc

class ImageVisualizer:
    """图像可视化工具"""
    
    @staticmethod
    def show_images(images, titles=None, cols=4, figsize=(12, 8)):
        """
        显示多张图像
        images: list of images or tensor (B, C, H, W)
        """
        if isinstance(images, torch.Tensor):
            images = images.cpu().permute(0, 2, 3, 1).numpy()
        
        num_images = len(images)
        rows = (num_images + cols - 1) // cols
        
        fig, axes = plt.subplots(rows, cols, figsize=figsize)
        if rows == 1 and cols == 1:
            axes = [axes]
        else:
            axes = axes.flatten()
        
        for i, (img, ax) in enumerate(zip(images, axes)):
            if i < num_images:
                # 归一化到0-1
                img = (img - img.min()) / (img.max() - img.min() + 1e-8)
                ax.imshow(img)
                if titles:
                    ax.set_title(titles[i])
                ax.axis('off')
            else:
                ax.axis('off')
        
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def show_batch(images, nrow=8, normalize=True):
        """显示一个batch的图像网格"""
        if isinstance(images, torch.Tensor):
            grid = make_grid(images, nrow=nrow, normalize=normalize)
            grid = grid.cpu().permute(1, 2, 0).numpy()
        
        plt.figure(figsize=(12, 8))
        plt.imshow(grid)
        plt.axis('off')
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def show_segmentation(image, mask, pred_mask=None):
        """显示分割结果"""
        fig, axes = plt.subplots(1, 3 if pred_mask is not None else 2, figsize=(12, 4))
        
        # 原始图像
        if isinstance(image, torch.Tensor):
            image = image.cpu().permute(1, 2, 0).numpy()
        image = (image - image.min()) / (image.max() - image.min() + 1e-8)
        axes[0].imshow(image)
        axes[0].set_title('原始图像')
        axes[0].axis('off')
        
        # 真实掩码
        if isinstance(mask, torch.Tensor):
            mask = mask.cpu().numpy()
        if len(mask.shape) == 3:
            mask = mask[0]
        axes[1].imshow(mask, cmap='jet')
        axes[1].set_title('真实掩码')
        axes[1].axis('off')
        
        # 预测掩码
        if pred_mask is not None:
            if isinstance(pred_mask, torch.Tensor):
                pred_mask = pred_mask.cpu().numpy()
            if len(pred_mask.shape) == 3:
                pred_mask = pred_mask[0]
            axes[2].imshow(pred_mask, cmap='jet')
            axes[2].set_title('预测掩码')
            axes[2].axis('off')
        
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def show_detection(image, boxes, labels=None, scores=None, class_names=None):
        """显示检测结果"""
        if isinstance(image, torch.Tensor):
            image = image.cpu().permute(1, 2, 0).numpy()
        image = (image - image.min()) / (image.max() - image.min() + 1e-8)
        
        fig, ax = plt.subplots(1, 1, figsize=(10, 10))
        ax.imshow(image)
        
        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = box
            
            # 绘制框
            rect = plt.Rectangle((x1, y1), x2-x1, y2-y1, 
                               fill=False, edgecolor='red', linewidth=2)
            ax.add_patch(rect)
            
            # 添加标签
            label_text = ""
            if labels is not None:
                class_id = labels[i]
                if class_names:
                    label_text += class_names[class_id]
                else:
                    label_text += f"Class {class_id}"
            
            if scores is not None:
                label_text += f": {scores[i]:.2f}"
            
            ax.text(x1, y1-5, label_text, color='red', fontsize=12,
                   bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
        
        ax.axis('off')
        plt.tight_layout()
        plt.show()

class TrainingVisualizer:
    """训练过程可视化"""
    
    @staticmethod
    def plot_training_history(history, metrics=['loss', 'acc']):
        """
        绘制训练历史
        history: dict with keys like 'train_loss', 'val_loss', etc.
        """
        fig, axes = plt.subplots(1, len(metrics), figsize=(6*len(metrics), 4))
        if len(metrics) == 1:
            axes = [axes]
        
        for idx, metric in enumerate(metrics):
            train_key = f'train_{metric}'
            val_key = f'val_{metric}'
            
            if train_key in history:
                axes[idx].plot(history[train_key], label=f'Train {metric}', linewidth=2)
            if val_key in history:
                axes[idx].plot(history[val_key], label=f'Val {metric}', linewidth=2)
            
            axes[idx].set_xlabel('Epoch')
            axes[idx].set_ylabel(metric.capitalize())
            axes[idx].set_title(f'{metric.capitalize()} over Epochs')
            axes[idx].legend()
            axes[idx].grid(True)
        
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def plot_lr_scheduler(lr_history):
        """绘制学习率调度"""
        plt.figure(figsize=(8, 4))
        plt.plot(lr_history, linewidth=2)
        plt.xlabel('Iteration/Epoch')
        plt.ylabel('Learning Rate')
        plt.title('Learning Rate Schedule')
        plt.grid(True)
        plt.show()

class MetricsVisualizer:
    """指标可视化"""
    
    @staticmethod
    def plot_confusion_matrix(y_true, y_pred, class_names=None):
        """绘制混淆矩阵"""
        cm = confusion_matrix(y_true, y_pred)
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                   xticklabels=class_names, yticklabels=class_names)
        plt.xlabel('Predicted')
        plt.ylabel('True')
        plt.title('Confusion Matrix')
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def plot_roc_curve(y_true, y_scores, class_names=None):
        """绘制ROC曲线"""
        plt.figure(figsize=(8, 6))
        
        if len(y_scores.shape) == 1:  # 二分类
            fpr, tpr, _ = roc_curve(y_true, y_scores)
            roc_auc = auc(fpr, tpr)
            plt.plot(fpr, tpr, label=f'ROC (AUC = {roc_auc:.3f})')
        else:  # 多分类
            for i in range(y_scores.shape[1]):
                fpr, tpr, _ = roc_curve((y_true == i).astype(int), y_scores[:, i])
                roc_auc = auc(fpr, tpr)
                label = class_names[i] if class_names else f'Class {i}'
                plt.plot(fpr, tpr, label=f'{label} (AUC = {roc_auc:.3f})')
        
        plt.plot([0, 1], [0, 1], 'k--', label='Random')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curve')
        plt.legend()
        plt.grid(True)
        plt.show()
    
    @staticmethod
    def plot_pr_curve(precision, recall, class_names=None):
        """绘制PR曲线"""
        plt.figure(figsize=(8, 6))
        
        if isinstance(precision, list):  # 多类
            for i, (p, r) in enumerate(zip(precision, recall)):
                label = class_names[i] if class_names else f'Class {i}'
                plt.plot(r, p, label=label)
        else:
            plt.plot(recall, precision, label='PR Curve')
        
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title('Precision-Recall Curve')
        plt.legend()
        plt.grid(True)
        plt.show()

# 使用示例

if __name__ == '__main__':
    # 示例数据
    images = torch.randn(8, 3, 224, 224)
    
    # 显示batch
    ImageVisualizer.show_batch(images, nrow=4)
    
    # 显示训练历史
    history = {
        'train_loss': [0.5, 0.3, 0.2, 0.15],
        'val_loss': [0.6, 0.4, 0.3, 0.25],
        'train_acc': [0.7, 0.8, 0.85, 0.9],
        'val_acc': [0.65, 0.75, 0.8, 0.85]
    }
    TrainingVisualizer.plot_training_history(history, metrics=['loss', 'acc'])
```

---

## 🚀 性能分析工具

### 1. 性能分析器

```bash
# profiler.py

"""
性能分析器
"""

import time
import torch
import psutil
import GPUtil
from contextlib import contextmanager
import numpy as np

class TrainingProfiler:
    """训练性能分析器"""
    
    def __init__(self):
        self.metrics = {
            'forward_time': [],
            'backward_time': [],
            'batch_time': [],
            'memory_usage': [],
            'gpu_memory': [],
        }
        self.start_time = None
    
    @contextmanager
    def timer(self, name):
        """计时器上下文管理器"""
        start = time.time()
        yield
        elapsed = time.time() - start
        
        if name in self.metrics:
            self.metrics[name].append(elapsed)
    
    def start_epoch(self):
        """开始一个epoch"""
        self.epoch_start = time.time()
    
    def end_epoch(self):
        """结束一个epoch"""
        epoch_time = time.time() - self.epoch_start
        self.metrics['epoch_time'] = self.metrics.get('epoch_time', []) + [epoch_time]
    
    def record_memory(self):
        """记录内存使用"""
        # CPU内存
        process = psutil.Process()
        memory_mb = process.memory_info().rss / 1024 / 1024
        self.metrics['memory_usage'].append(memory_mb)
        
        # GPU内存
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu_memory = gpus[0].memoryUsed
                self.metrics['gpu_memory'].append(gpu_memory)
        except:
            pass
    
    def get_stats(self):
        """获取统计信息"""
        stats = {}
        for key, values in self.metrics.items():
            if values:
                stats[key] = {
                    'mean': np.mean(values),
                    'std': np.std(values),
                    'min': np.min(values),
                    'max': np.max(values),
                }
        return stats
    
    def print_stats(self):
        """打印统计信息"""
        stats = self.get_stats()
        print("\n性能分析统计:")
        print("-" * 40)
        for key, stat in stats.items():
            print(f"{key:<20} Mean: {stat['mean']:.4f} ± {stat['std']:.4f}")
    
    def plot_metrics(self):
        """绘制性能指标"""
        import matplotlib.pyplot as plt
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        
        # 训练时间
        if 'batch_time' in self.metrics:
            axes[0, 0].plot(self.metrics['batch_time'])
            axes[0, 0].set_title('Batch Time')
            axes[0, 0].set_xlabel('Batch')
            axes[0, 0].set_ylabel('Time (s)')
        
        # 内存使用
        if 'memory_usage' in self.metrics:
            axes[0, 1].plot(self.metrics['memory_usage'])
            axes[0, 1].set_title('CPU Memory')
            axes[0, 1].set_xlabel('Step')
            axes[0, 1].set_ylabel('Memory (MB)')
        
        # GPU内存
        if 'gpu_memory' in self.metrics:
            axes[1, 0].plot(self.metrics['gpu_memory'])
            axes[1, 0].set_title('GPU Memory')
            axes[1, 0].set_xlabel('Step')
            axes[1, 0].set_ylabel('Memory (MB)')
        
        # 前向/反向时间
        if 'forward_time' in self.metrics and 'backward_time' in self.metrics:
            axes[1, 1].plot(self.metrics['forward_time'], label='Forward')
            axes[1, 1].plot(self.metrics['backward_time'], label='Backward')
            axes[1, 1].set_title('Forward/Backward Time')
            axes[1, 1].set_xlabel('Batch')
            axes[1, 1].set_ylabel('Time (s)')
            axes[1, 1].legend()
        
        plt.tight_layout()
        plt.show()

class ModelProfiler:
    """模型性能分析器"""
    
    @staticmethod
    def profile_forward(model, input_size, device='cuda', num_runs=100):
        """分析前向传播性能"""
        model.eval()
        dummy_input = torch.randn(input_size).to(device)
        
        # 预热
        with torch.no_grad():
            for _ in range(10):
                _ = model(dummy_input)
        
        # 计时
        torch.cuda.synchronize() if device == 'cuda' else None
        start = time.time()
        
        with torch.no_grad():
            for _ in range(num_runs):
                _ = model(dummy_input)
        
        torch.cuda.synchronize() if device == 'cuda' else None
        elapsed = time.time() - start
        
        avg_time = elapsed / num_runs
        fps = 1 / avg_time
        
        print(f"前向传播性能:")
        print(f"  平均时间: {avg_time*1000:.2f} ms")
        print(f"  FPS: {fps:.2f}")
        
        return avg_time, fps
    
    @staticmethod
    def profile_memory(model, input_size, device='cuda'):
        """分析内存使用"""
        if device == 'cuda':
            torch.cuda.reset_peak_memory_stats()
        
        dummy_input = torch.randn(input_size).to(device)
        
        with torch.no_grad():
            output = model(dummy_input)
        
        if device == 'cuda':
            peak_memory = torch.cuda.max_memory_allocated() / 1024**2  # MB
            print(f"峰值GPU内存: {peak_memory:.2f} MB")
            return peak_memory
        else:
            process = psutil.Process()
            memory = process.memory_info().rss / 1024**2
            print(f"CPU内存使用: {memory:.2f} MB")
            return memory
    
    @staticmethod
    def compare_models(models, input_size, device='cuda'):
        """比较多个模型的性能"""
        results = {}
        
        for name, model in models.items():
            model = model.to(device)
            print(f"\n分析模型: {name}")
            
            # 参数量
            params = sum(p.numel() for p in model.parameters())
            
            # 前向性能
            avg_time, fps = ModelProfiler.profile_forward(model, input_size, device, num_runs=50)
            
            # 内存
            memory = ModelProfiler.profile_memory(model, input_size, device)
            
            results[name] = {
                'params': params,
                'avg_time': avg_time,
                'fps': fps,
                'memory': memory,
            }
        
        # 打印对比表
        print("\n模型性能对比:")
        print("-" * 80)
        print(f"{'模型':<20} {'参数(M)':<10} {'时间(ms)':<10} {'FPS':<10} {'内存(MB)':<10}")
        print("-" * 80)
        for name, r in results.items():
            print(f"{name:<20} {r['params']/1e6:<10.2f} {r['avg_time']*1000:<10.2f} {r['fps']:<10.2f} {r['memory']:<10.2f}")
        
        return results

# 使用示例

if __name__ == '__main__':
    # 创建示例模型
    model = nn.Sequential(
        nn.Conv2d(3, 64, 3, padding=1),
        nn.ReLU(),
        nn.MaxPool2d(2),
        nn.Conv2d(64, 128, 3, padding=1),
        nn.ReLU(),
        nn.MaxPool2d(2),
        nn.AdaptiveAvgPool2d(1),
        nn.Flatten(),
        nn.Linear(128, 10)
    )
    
    # 性能分析
    ModelProfiler.profile_forward(model, (1, 3, 224, 224))
    ModelProfiler.profile_memory(model, (1, 3, 224, 224))
```

---

## 🤖 自动化脚本

### 1. 训练自动化

```python
#!/bin/bash
# train.sh - 自动化训练脚本

set -e  # 遇到错误立即退出

# 配置

PROJECT_NAME="cv_project"
DATA_DIR="./data"
MODEL_NAME="resnet50"
EPOCHS=100
BATCH_SIZE=32
LR=1e-3
DEVICE="cuda"

# 创建目录

mkdir -p checkpoints logs

echo "🚀 开始训练: $PROJECT_NAME"
echo "模型: $MODEL_NAME"
echo "数据: $DATA_DIR"
echo "设备: $DEVICE"

# 激活环境（可选）
# conda activate cv

# 运行训练

python train_template.py \
    --data_dir $DATA_DIR \
    --model_name $MODEL_NAME \
    --epochs $EPOCHS \
    --batch_size $BATCH_SIZE \
    --lr $LR \
    --device $DEVICE \
    --save_dir ./checkpoints \
    --log_dir ./logs

# 训练完成通知

echo "✅ 训练完成！"
echo "检查点: ./checkpoints"
echo "日志: ./logs"

# 可选：发送通知
# notify-send "训练完成" "项目: $PROJECT_NAME"

```

---

### 2. 评估自动化

```python
#!/bin/bash
# evaluate.sh - 自动化评估脚本

MODEL_PATH=$1
DATA_DIR=$2
DEVICE=${3:-"cuda"}

if [ -z "$MODEL_PATH" ] || [ -z "$DATA_DIR" ]; then
    echo "用法: ./evaluate.sh <model_path> <data_dir> [device]"
    exit 1
fi

echo "🔍 开始评估"
echo "模型: $MODEL_PATH"
echo "数据: $DATA_DIR"
echo "设备: $DEVICE"

python evaluate.py \
    --model_path $MODEL_PATH \
    --data_dir $DATA_DIR \
    --device $DEVICE \
    --output_dir ./results

echo "✅ 评估完成！"
echo "结果: ./results"
```

---

### 3. 部署脚本

```python
#!/bin/bash
# deploy.sh - 模型部署脚本

MODEL_PATH=$1
OUTPUT_DIR=${2:-"./deploy"}

echo "🚀 开始部署"
echo "模型: $MODEL_PATH"
echo "输出: $OUTPUT_DIR"

mkdir -p $OUTPUT_DIR

# 1. 导出ONNX

echo "步骤1: 导出ONNX"
python export_onnx.py \
    --model_path $MODEL_PATH \
    --output $OUTPUT_DIR/model.onnx

# 2. 导出TensorRT

echo "步骤2: 导出TensorRT"
trtexec --onnx=$OUTPUT_DIR/model.onnx \
        --saveEngine=$OUTPUT_DIR/model.trt \
        --fp16

# 3. 测试推理

echo "步骤3: 测试推理"
python test_inference.py \
    --model $OUTPUT_DIR/model.trt \
    --input ./test_image.jpg

echo "✅ 部署完成！"
echo "模型文件:"
echo "  - ONNX: $OUTPUT_DIR/model.onnx"
echo "  - TensorRT: $OUTPUT_DIR/model.trt"
```

---

## 📊 使用指南

### 快速开始

1. **环境配置**：
```python
   chmod +x setup_env.sh
   ./setup_env.sh
```

2. **训练模型**：
```python
   python train_template.py --data_dir ./data --model_name resnet50 --epochs 100
```

3. **分析性能**：
```python
   from model_utils import ModelAnalyzer
   ModelAnalyzer.model_info(model)
```

4. **可视化结果**：
```python
   from vis_utils import ImageVisualizer
   ImageVisualizer.show_batch(images)
```

### 最佳实践

1. **模板使用**：
   - 复制模板文件
   - 根据需求修改
   - 保持代码结构一致

2. **工具组合**：
   - 训练用 `train_template.py`
   - 分析用 `ModelAnalyzer`
   - 可视化用 `ImageVisualizer`

3. **自动化**：
   - 使用shell脚本自动化流程
   - 记录实验配置
   - 定期保存检查点

---

## 🔄 持续更新

本工具库会持续更新，添加：
- 更多模型模板
- 高级数据增强
- 分布式训练支持
- 模型压缩工具
- 部署优化脚本

---

**祝你开发顺利！** 🚀

*最后更新：2025年12月*
