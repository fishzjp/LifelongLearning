# 目标检测项目：YOLOv5 口罩检测

> 第一个"真数据"项目：从公开图片开始，亲手标注数据集、转换格式、训练 YOLOv5、评估 mAP、导出部署。做完这个，任何自定义检测需求你都有完整路径可循。

**前置知识**：[06-目标检测](L05-%E7%9B%AE%E6%A0%87%E6%A3%80%E6%B5%8B.md)。
**预计投入**：3-4 天（大头在数据标注）。

---

## 项目概述
本项目将指导您从零开始使用YOLOv5构建一个自定义目标检测系统。我们将以口罩检测为例，完整演示数据集准备、模型训练、推理和部署的全流程。

### 项目目标
- 掌握目标检测的基本概念
- 学习YOLO系列算法的原理和使用
- 掌握自定义数据集的准备和标注方法
- 学会训练和评估目标检测模型
- 实现模型部署和优化

### 预期效果
- 训练一个能够在自定义数据集上达到良好性能的检测模型
- 实现实时目标检测（>30 FPS）
- 部署到实际应用场景

## 环境准备
### 1. 硬件要求
**推荐配置**：
- GPU: NVIDIA RTX 3060或更高（显存≥6GB）
- CPU: 4核心以上
- RAM: 16GB以上
- 存储: 至少20GB可用空间

**最低配置**：
- GPU: GTX 1650或更高
- RAM: 8GB
- 也可以使用Google Colab免费GPU

### 2. 软件安装
```bash
# 创建虚拟环境
python -m venv yolov5_env
source yolov5_env/bin/activate  # Linux/Mac
# 或 yolov5_env\Scripts\activate  # Windows
# 安装PyTorch（根据您的CUDA版本选择）
# CUDA 11.8
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# CUDA 12.1
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# CPU版本
pip install torch torchvision torchaudio

# 安装YOLOv5依赖
cd /path/to/your/project
git clone https://github.com/ultralytics/yolov5
cd yolov5
pip install -r requirements.txt

# 验证安装
python detect.py --weights yolov5s.pt --source data/images/bus.jpg
```

### 3. 验证环境
```python

# 依赖: cv2, numpy, torch
# 安装: pip install cv2 numpy torch
import torch
import cv2
import numpy as np

print(f"PyTorch版本: {torch.__version__}")
print(f"CUDA可用: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"CUDA版本: {torch.version.cuda}")
    print(f"GPU数量: {torch.cuda.device_count()}")
    print(f"GPU名称: {torch.cuda.get_device_name(0)}")
print(f"OpenCV版本: {cv2.__version__}")
print(f"NumPy版本: {np.__version__}")
```

## 数据准备和标注
### 1. 数据集组织结构
```
dataset/
├── images/
│   ├── train/          # 训练图像（约80%）
│   │   ├── img001.jpg
│   │   ├── img002.jpg
│   │   └── ...
│   ├── val/            # 验证图像（约10%）
│   │   ├── img101.jpg
│   │   └── ...
│   └── test/           # 测试图像（约10%）
│       └── ...
└── labels/
    ├── train/          # 训练标签
    │   ├── img001.txt
    │   ├── img002.txt
    │   └── ...
    ├── val/            # 验证标签
    │   └── ...
    └── test/           # 测试标签
        └── ...
```

### 2. 数据收集
**数据收集策略**：

```python

# 依赖: shutil
# 安装: pip install shutil
import os
import shutil
from pathlib import Path


def collect_dataset(source_dirs, target_dir, max_samples=None):
    """
    从多个源目录收集数据

    Args:
        source_dirs: 源目录列表
        target_dir: 目标目录
        max_samples: 最大样本数
    """
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    collected = 0
    for source_dir in source_dirs:
        source_path = Path(source_dir)
        if not source_path.exists():
            print(f"警告: {source_dir} 不存在")
            continue

        # 支持的图像格式
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}

        for img_path in source_path.rglob('*'):
            if img_path.suffix.lower() in image_extensions:
                if max_samples and collected >= max_samples:
                    return

                # 复制图像
                dest_path = target_dir / img_path.name
                shutil.copy2(img_path, dest_path)
                collected += 1

                if collected % 100 == 0:
                    print(f"已收集 {collected} 张图像")

    print(f"总共收集 {collected} 张图像")


# 使用示例
if __name__ == "__main__":
    sources = [
        '/path/to/source1',
        '/path/to/source2'
    ]
    collect_dataset(sources, 'dataset/raw_images')
```

**从网络爬取数据**：

```python

# 依赖: bs4, requests, time, urllib
# 安装: pip install bs4 requests time urllib
import requests
from bs4 import BeautifulSoup
import urllib.request
import time


def download_images(query, num_images, save_dir):
    """
    使用Google Images下载图像（简化版）

    注意：实际项目中建议使用专门的爬虫工具如scrapy、selenium
    或使用API服务如Google Images API、Bing Images API
    """
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys

    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)

    # 配置Chrome无头模式
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)

    # 搜索图像
    search_url = f"https://www.google.com/search?tbm=isch&q={query}"
    driver.get(search_url)
    time.sleep(2)

    # 滚动加载更多图像
    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    # 获取图像URL
    image_elements = driver.find_elements(By.TAG_NAME, 'img')

    downloaded = 0
    for i, img in enumerate(image_elements[:num_images]):
        try:
            src = img.get_attribute('src')
            if src and src.startswith('http'):
                # 下载图像
                urllib.request.urlretrieve(
                    src,
                    save_dir / f"{query}_{i}.jpg"
                )
                downloaded += 1
                print(f"下载: {downloaded}/{num_images}")
        except Exception as e:
            print(f"下载失败: {e}")

    driver.quit()
    print(f"完成! 下载了 {downloaded} 张图像")
```

### 3. 数据标注
**方法1: 使用LabelImg（推荐）**

```bash
# 安装LabelImg
pip install labelImg

# 启动LabelImg
labelImg

# 使用说明：
# 1. 点击 'Open Dir' 选择图像目录
# 2. 点击 'Change Save Dir' 选择标签保存目录
# 3. 设置标注格式为 YOLO (在View中勾选)
# 4. 使用 'Create RectBox' 绘制边界框
# 5. 选择类别标签
# 6. 按 'w' 快捷键创建新框
# 7. 按 'd' 下一张，'a' 上一张
# 8. 完成后标签会自动保存为.txt文件
```

**方法2: 使用CVAT（专业标注工具）**

```bash
# 使用Docker运行CVAT
docker pull cvat/server
docker run -it -p 8080:8080 cvat/server

# 访问 http://localhost:8080
# 功能更强大，支持多人协作、视频标注等
```

**YOLO标注格式说明**：

每个图像对应一个.txt文件，每行格式：
```
<class_id> <x_center> <y_center> <width> <height>
```

其中坐标都是归一化的（0-1之间）。

示例：
```
# 对于 640x480 的图像
# 边界框 (100, 150, 200, 250) 的标注：
0 0.234 0.417 0.156 0.208

# 计算方式：
# class_id = 0
# x_center = (100 + 200) / 2 / 640 = 0.234
# y_center = (150 + 250) / 2 / 480 = 0.417
# width = (200 - 100) / 640 = 0.156
# height = (250 - 150) / 480 = 0.208
```

### 4. 数据集划分脚本
```python

# 依赖: shutil
# 安装: pip install shutil
import os
import shutil
from pathlib import Path
import random
from sklearn.model_selection import train_test_split


def split_dataset(images_dir, labels_dir, output_dir,
                  train_ratio=0.8, val_ratio=0.1, test_ratio=0.1,
                  seed=42):
    """
    划分数据集为训练集、验证集和测试集

    Args:
        images_dir: 图像目录
        labels_dir: 标签目录
        output_dir: 输出目录
        train_ratio: 训练集比例
        val_ratio: 验证集比例
        test_ratio: 测试集比例
        seed: 随机种子
    """
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-6

    random.seed(seed)

    images_dir = Path(images_dir)
    labels_dir = Path(labels_dir)
    output_dir = Path(output_dir)

    # 获取所有图像文件
    image_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp']:
        image_files.extend(images_dir.glob(ext))

    print(f"找到 {len(image_files)} 张图像")

    # 提取文件名（不含扩展名）
    file_names = [f.stem for f in image_files]

    # 划分数据集
    # 先划分出训练集和临时集（验证集+测试集）
    train_names, temp_names = train_test_split(
        file_names,
        test_size=(1 - train_ratio),
        random_state=seed
    )

    # 再将临时集划分为验证集和测试集
    val_ratio_adjusted = val_ratio / (val_ratio + test_ratio)
    val_names, test_names = train_test_split(
        temp_names,
        test_size=(1 - val_ratio_adjusted),
        random_state=seed
    )

    print(f"训练集: {len(train_names)} 张")
    print(f"验证集: {len(val_names)} 张")
    print(f"测试集: {len(test_names)} 张")

    # 创建目录结构
    splits = {
        'train': train_names,
        'val': val_names,
        'test': test_names
    }

    for split_name, file_list in splits.items():
        # 创建目录
        split_img_dir = output_dir / 'images' / split_name
        split_label_dir = output_dir / 'labels' / split_name
        split_img_dir.mkdir(parents=True, exist_ok=True)
        split_label_dir.mkdir(parents=True, exist_ok=True)

        # 复制文件
        for file_name in file_list:
            # 查找对应的图像文件
            img_file = None
            for ext in ['.jpg', '.jpeg', '.png', '.bmp']:
                potential_path = images_dir / f"{file_name}{ext}"
                if potential_path.exists():
                    img_file = potential_path
                    break

            if img_file is None:
                print(f"警告: 找不到图像 {file_name}")
                continue

            # 复制图像
            shutil.copy2(img_file, split_img_dir / img_file.name)

            # 复制标签（如果存在）
            label_file = labels_dir / f"{file_name}.txt"
            if label_file.exists():
                shutil.copy2(label_file, split_label_dir / label_file.name)
            else:
                print(f"警告: 找不到标签 {file_name}.txt")

    print(f"\n数据集划分完成! 保存至: {output_dir}")

    # 创建数据集配置文件
    create_data_yaml(output_dir)


def create_data_yaml(dataset_dir, class_names=None):
    """
    创建数据集配置文件

    Args:
        dataset_dir: 数据集目录
        class_names: 类别名称列表
    """
    dataset_dir = Path(dataset_dir)

    # 自动检测类别
    if class_names is None:
        label_dir = dataset_dir / 'labels' / 'train'
        class_ids = set()

        if label_dir.exists():
            for label_file in label_dir.glob('*.txt'):
                with open(label_file, 'r') as f:
                    for line in f:
                        if line.strip():
                            class_id = int(line.split()[0])
                            class_ids.add(class_id)

        class_names = [f"class_{i}" for i in sorted(class_ids)]

    # 创建YAML配置文件
    yaml_content = f"""# 数据集配置文件
path: {dataset_dir.absolute()}  # 数据集根目录
train: images/train  # 训练图像目录（相对于path）
val: images/val      # 验证图像目录
test: images/test    # 测试图像目录

# 类别数量
nc: {len(class_names)}

# 类别名称
names:
"""

    for i, name in enumerate(class_names):
        yaml_content += f"  {i}: {name}\n"

    # 保存配置文件
    config_path = dataset_dir / 'data.yaml'
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(yaml_content)

    print(f"\n配置文件已创建: {config_path}")
    print(f"类别: {class_names}")

    return config_path


# 使用示例
if __name__ == "__main__":
    # 划分数据集
    split_dataset(
        images_dir='dataset/raw_images',
        labels_dir='dataset/raw_labels',
        output_dir='dataset/organized',
        train_ratio=0.8,
        val_ratio=0.1,
        test_ratio=0.1
    )
```

### 5. 数据分析和可视化
```python

# 依赖: cv2, matplotlib, numpy, yaml
# 安装: pip install cv2 matplotlib numpy yaml
import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import yaml


class DatasetAnalyzer:
    """数据集分析工具"""

    def __init__(self, dataset_dir):
        self.dataset_dir = Path(dataset_dir)

        # 加载配置文件
        config_path = self.dataset_dir / 'data.yaml'
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

        self.class_names = self.config['names']

    def analyze_dataset(self):
        """分析数据集统计信息"""
        stats = {
            'split': {},
            'total': 0,
            'class_distribution': {name: 0 for name in self.class_names},
            'bbox_sizes': []
        }

        for split in ['train', 'val', 'test']:
            img_dir = self.dataset_dir / 'images' / split
            label_dir = self.dataset_dir / 'labels' / split

            if not img_dir.exists():
                continue

            images = list(img_dir.glob('*.*'))
            stats['split'][split] = len(images)
            stats['total'] += len(images)

            # 统计类别和边界框
            for img_path in images:
                label_path = label_dir / f"{img_path.stem}.txt"

                if label_path.exists():
                    with open(label_path, 'r') as f:
                        for line in f:
                            if line.strip():
                                parts = line.strip().split()
                                class_id = int(parts[0])
                                class_name = self.class_names[class_id]

                                # 统计类别
                                stats['class_distribution'][class_name] += 1

                                # 记录边界框大小
                                w, h = float(parts[3]), float(parts[4])
                                stats['bbox_sizes'].append((w, h))

        return stats

    def plot_statistics(self, stats):
        """绘制统计图表"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))

        # 1. 数据集划分
        splits = list(stats['split'].keys())
        counts = list(stats['split'].values())

        axes[0, 0].pie(counts, labels=splits, autopct='%1.1f%%',
                       colors=['#66b3ff', '#99ff99', '#ffcc99'])
        axes[0, 0].set_title('数据集划分', fontsize=14)

        # 2. 类别分布
        class_names = list(stats['class_distribution'].keys())
        class_counts = list(stats['class_distribution'].values())

        axes[0, 1].bar(range(len(class_names)), class_counts,
                      color='steelblue')
        axes[0, 1].set_xticks(range(len(class_names)))
        axes[0, 1].set_xticklabels(class_names, rotation=45, ha='right')
        axes[0, 1].set_xlabel('类别')
        axes[0, 1].set_ylabel('实例数量')
        axes[0, 1].set_title('类别分布', fontsize=14)
        axes[0, 1].grid(True, alpha=0.3)

        # 3. 边界框宽度分布
        widths = [s[0] for s in stats['bbox_sizes']]
        axes[1, 0].hist(widths, bins=50, color='coral', edgecolor='black')
        axes[1, 0].set_xlabel('归一化宽度')
        axes[1, 0].set_ylabel('频次')
        axes[1, 0].set_title('边界框宽度分布', fontsize=14)
        axes[1, 0].grid(True, alpha=0.3)

        # 4. 边界框高度分布
        heights = [s[1] for s in stats['bbox_sizes']]
        axes[1, 1].hist(heights, bins=50, color='lightgreen',
                       edgecolor='black')
        axes[1, 1].set_xlabel('归一化高度')
        axes[1, 1].set_ylabel('频次')
        axes[1, 1].set_title('边界框高度分布', fontsize=14)
        axes[1, 1].grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig('dataset_statistics.png', dpi=150, bbox_inches='tight')
        plt.show()

        # 打印统计信息
        print("\n=== 数据集统计 ===")
        print(f"总图像数: {stats['total']}")
        print(f"\n划分:")
        for split, count in stats['split'].items():
            print(f"  {split}: {count} ({count/stats['total']*100:.1f}%)")

        print(f"\n类别分布:")
        for name, count in stats['class_distribution'].items():
            print(f"  {name}: {count}")

    def visualize_samples(self, split='train', num_samples=9):
        """可视化样本"""
        img_dir = self.dataset_dir / 'images' / split
        label_dir = self.dataset_dir / 'labels' / split

        images = list(img_dir.glob('*.*'))
        random.shuffle(images)

        num_samples = min(num_samples, len(images))
        n_cols = 3
        n_rows = (num_samples + n_cols - 1) // n_cols

        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
        fig.suptitle(f'{split.capitalize()} 样本可视化', fontsize=16)

        for idx, ax in enumerate(axes.flat):
            if idx < num_samples:
                img_path = images[idx]
                img = cv2.imread(str(img_path))
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                # 读取标签
                label_path = label_dir / f"{img_path.stem}.txt"
                if label_path.exists():
                    h, w = img.shape[:2]

                    with open(label_path, 'r') as f:
                        for line in f:
                            if line.strip():
                                parts = line.strip().split()
                                class_id = int(parts[0])
                                x_center, y_center, bw, bh = map(float, parts[1:])

                                # 转换为像素坐标
                                x = int((x_center - bw / 2) * w)
                                y = int((y_center - bh / 2) * h)
                                bw_px = int(bw * w)
                                bh_px = int(bh * h)

                                # 绘制边界框
                                color = plt.cm.tab10(class_id)
                                color = tuple([int(c * 255) for c in color[:3]])
                                cv2.rectangle(img, (x, y),
                                             (x + bw_px, y + bh_px),
                                             color, 2)

                                # 绘制标签
                                label = self.class_names[class_id]
                                cv2.putText(img, label, (x, y - 10),
                                           cv2.FONT_HERSHEY_SIMPLEX,
                                           0.5, color, 2)

                ax.imshow(img)
                ax.axis('off')
            else:
                ax.axis('off')

        plt.tight_layout()
        plt.savefig(f'{split}_samples.png', dpi=150, bbox_inches='tight')
        plt.show()


# 使用示例
if __name__ == "__main__":
    analyzer = DatasetAnalyzer('dataset/organized')

    # 分析数据集
    stats = analyzer.analyze_dataset()
    analyzer.plot_statistics(stats)

    # 可视化样本
    analyzer.visualize_samples('train', num_samples=9)
```

## 模型训练
### 1. YOLOv5架构简介
YOLOv5系列包含5个模型，从轻量到重型：

| 模型 | mAP@0.5 | 速度(FPS) | 参数量 | 权重大小 |
|------|---------|-----------|--------|----------|
| YOLOv5n | 28.4 | 155 | 1.9M | 3.9MB |
| YOLOv5s | 37.4 | 98 | 7.2M | 14.4MB |
| YOLOv5m | 45.4 | 62 | 21.2M | 41.6MB |
| YOLOv5l | 49.0 | 45 | 46.5M | 90.8MB |
| YOLOv5x | 50.7 | 34 | 86.7M | 167.3MB**

**选择建议**：
- 边缘设备/移动端: YOLOv5n或YOLOv5s
- 一般应用: YOLOv5s或YOLOv5m
- 高精度要求: YOLOv5l或YOLOv5x

### 2. 训练脚本
```bash
# 基本训练命令
python train.py \
  --data dataset/organized/data.yaml \
  --cfg models/yolov5s.yaml \
  --weights yolov5s.pt \
  --batch-size 16 \
  --epochs 100 \
  --img 640 \
  --device 0 \
  --workers 8 \
  --name my_custom_model

# 参数说明：
# --data: 数据集配置文件
# --cfg: 模型配置文件
# --weights: 预训练权重 (yolov5s.pt, yolov5m.pt等，或空表示从头训练)
# --batch-size: 批次大小 (根据显存调整)
# --epochs: 训练轮数
# --img: 输入图像大小
# --device: 设备 (0表示GPU 0, cpu表示CPU)
# --workers: 数据加载线程数
# --name: 实验名称
```

### 3. 自定义训练脚本
```python

# 依赖: subprocess, yaml
# 安装: pip install subprocess yaml
import os
import subprocess
import yaml
from pathlib import Path


class YOLOv5Trainer:
    """YOLOv5训练器"""

    def __init__(self, yolov5_path, data_yaml, weights='yolov5s.pt'):
        """
        初始化训练器

        Args:
            yolov5_path: YOLOv5代码路径
            data_yaml: 数据集配置文件
            weights: 预训练权重
        """
        self.yolov5_path = Path(yolov5_path)
        self.data_yaml = data_yaml
        self.weights = weights

        # 读取数据集配置
        with open(data_yaml, 'r') as f:
            self.config = yaml.safe_load(f)

        self.num_classes = self.config['nc']

    def create_custom_model(self, model_size='s'):
        """
        创建自定义模型配置文件

        Args:
            model_size: 模型大小 (n, s, m, l, x)
        """
        # 加载基础模型配置
        base_config = f'models/yolov5{model_size}.yaml'
        config_path = self.yolov5_path / base_config

        with open(config_path, 'r') as f:
            model_config = yaml.safe_load(f)

        # 修改类别数量
        model_config['nc'] = self.num_classes

        # 保存自定义配置
        custom_config_path = self.yolov5_path / f'models/custom_{model_size}.yaml'
        with open(custom_config_path, 'w') as f:
            yaml.dump(model_config, f)

        print(f"自定义模型配置已创建: {custom_config_path}")
        return custom_config_path

    def train(self, epochs=100, batch_size=16, img_size=640,
              device=0, name='custom_model', **kwargs):
        """
        训练模型

        Args:
            epochs: 训练轮数
            batch_size: 批次大小
            img_size: 输入图像大小
            device: 设备ID
            name: 实验名称
            **kwargs: 其他参数
        """
        # 创建自定义模型配置
        model_size = self.weights.replace('yolov5', '').replace('.pt', '')
        custom_model = self.create_custom_model(model_size)

        # 构建训练命令
        cmd = [
            'python', 'train.py',
            '--data', str(self.data_yaml),
            '--cfg', str(custom_model),
            '--weights', self.weights,
            '--batch-size', str(batch_size),
            '--epochs', str(epochs),
            '--img', str(img_size),
            '--device', str(device),
            '--name', name,
            '--project', 'runs/train',
            '--exist-ok',
            '--patience', '50',  # 早停耐心值
            '--save-period', '10',  # 每10个epoch保存一次
        ]

        # 添加其他参数
        for key, value in kwargs.items():
            cmd.extend([f'--{key}', str(value)])

        print("\n=== 开始训练 ===")
        print(f"命令: {' '.join(cmd)}\n")

        # 切换到YOLOv5目录
        os.chdir(self.yolov5_path)

        # 运行训练
        try:
            subprocess.run(cmd, check=True)
            print("\n训练完成!")
        except subprocess.CalledProcessError as e:
            print(f"\n训练失败: {e}")

    def resume_training(self, checkpoint_path):
        """
        恢复训练

        Args:
            checkpoint_path: 检查点路径 (如 runs/train/exp/weights/last.pt)
        """
        cmd = [
            'python', 'train.py',
            '--resume', str(checkpoint_path)
        ]

        os.chdir(self.yolov5_path)
        subprocess.run(cmd, check=True)


# 使用示例
if __name__ == "__main__":
    # 创建训练器
    trainer = YOLOv5Trainer(
        yolov5_path='./yolov5',
        data_yaml='dataset/organized/data.yaml',
        weights='yolov5s.pt'
    )

    # 训练模型
    trainer.train(
        epochs=150,
        batch_size=16,
        img_size=640,
        device=0,
        name='mask_detection',
        # 可选参数
        # lr0=0.01,           # 初始学习率
        # lrf=0.01,           # 最终学习率 (与lr0的比率)
        # momentum=0.937,     # SGD动量
        # weight_decay=0.0005,# 权重衰减
        # warmup_epochs=3.0,  # 预热epoch数
        # warmup_momentum=0.8,# 预热动量
        # warmup_bias_lr=0.1, # 预热偏置学习率
        # box=0.05,           # box损失增益
        # cls=0.5,            # cls损失增益
        # cls_pw=1.0,         # cls BCELoss positive_weight
        # obj=1.0,            # obj损失增益
        # obj_pw=1.0,         # obj BCELoss positive_weight
        # iou_t=0.20,         # IoU训练阈值
        # anchor_t=4.0,       # anchor-multiple阈值
        # fl_gamma=0.0,       # focal loss gamma
        # hsv_h=0.015,        # image HSV-Hue增强
        # hsv_s=0.7,          # image HSV-Saturation增强
        # hsv_v=0.4,          # image HSV-Value增强
        # degrees=0.0,        # image rotation (+/- deg)
        # translate=0.1,      # image translation (+/- fraction)
        # scale=0.5,          # image scale (+/- gain)
        # shear=0.0,          # image shear (+/- deg)
        # perspective=0.0,    # image perspective (+/- fraction)
        # flipud=0.0,         # image flip up-down
        # fliplr=0.5,         # image flip left-right
        # mosaic=1.0,         # image mosaic概率
        # mixup=0.0,          # image mixup概率
    )
```

### 4. 超参数调优
```python

# 依赖: itertools, yaml
# 安装: pip install itertools yaml
import itertools
import yaml


class HyperparameterTuner:
    """超参数调优器"""

    def __init__(self, trainer):
        self.trainer = trainer
        self.results = []

    def grid_search(self, param_grid, max_runs=10):
        """
        网格搜索

        Args:
            param_grid: 参数字典
            max_runs: 最大运行次数

        示例:
            param_grid = {
                'lr0': [0.001, 0.01, 0.1],
                'batch_size': [8, 16, 32],
                'weight_decay': [0.0005, 0.0001]
            }
        """
        # 生成所有参数组合
        keys = param_grid.keys()
        values = param_grid.values()
        combinations = list(itertools.product(*values))

        # 限制运行次数
        if len(combinations) > max_runs:
            print(f"警告: 总共{len(combinations)}种组合，只运行前{max_runs}种")
            combinations = combinations[:max_runs]

        print(f"开始网格搜索，共{len(combinations)}种组合\n")

        for i, combination in enumerate(combinations, 1):
            params = dict(zip(keys, combination))

            print(f"\n=== 运行 {i}/{len(combinations)} ===")
            print(f"参数: {params}\n")

            # 训练模型
            exp_name = f"tune_run_{i}"
            self.trainer.train(
                epochs=50,  # 用较少的epoch快速评估
                name=exp_name,
                **params
            )

            # 评估结果（简化版）
            # 实际应该从训练日志中提取最佳mAP
            self.results.append({
                'run': i,
                'params': params,
                'metrics': self._evaluate_exp(exp_name)
            })

        # 打印最佳结果
        self._print_best_results()

    def _evaluate_exp(self, exp_name):
        """评估实验结果"""
        # 这里应该从训练日志中读取mAP等指标
        # 简化版，返回随机值
        import random
        return {'mAP@0.5': random.uniform(0.7, 0.95)}

    def _print_best_results(self):
        """打印最佳结果"""
        sorted_results = sorted(
            self.results,
            key=lambda x: x['metrics']['mAP@0.5'],
            reverse=True
        )

        print("\n=== 最佳5个配置 ===")
        for result in sorted_results[:5]:
            print(f"\n运行 {result['run']}:")
            print(f"  参数: {result['params']}")
            print(f"  mAP@0.5: {result['metrics']['mAP@0.5']:.4f}")


# 使用示例
if __name__ == "__main__":
    trainer = YOLOv5Trainer(
        yolov5_path='./yolov5',
        data_yaml='dataset/organized/data.yaml',
        weights='yolov5s.pt'
    )

    tuner = HyperparameterTuner(trainer)

    # 定义搜索空间
    param_grid = {
        'lr0': [0.001, 0.01],
        'batch_size': [16, 32],
        'weight_decay': [0.0005, 0.0001]
    }

    # 执行网格搜索
    tuner.grid_search(param_grid, max_runs=8)
```

## 推理和可视化
### 1. 基本推理
```bash
# 使用训练好的模型进行推理
python detect.py \
  --weights runs/train/custom_model/weights/best.pt \
  --source dataset/organized/images/test \
  --conf 0.25 \
  --iou 0.45 \
  --img 640 \
  --device 0 \
  --name inference_results

# 参数说明：
# --weights: 模型权重路径
# --source: 输入源 (图像目录、视频、摄像头等)
# --conf: 置信度阈值
# --iou: NMS IOU阈值
# --img: 推理图像大小
# --device: 设备
# --name: 保存目录名称
```

### 2. Python推理脚本
```python

# 依赖: cv2, matplotlib, numpy, torch
# 安装: pip install cv2 matplotlib numpy torch
import torch
import cv2
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt


class YOLOv5Detector:
    """YOLOv5检测器"""

    def __init__(self, weights_path, device='cuda',
                 conf_threshold=0.25, iou_threshold=0.45):
        """
        初始化检测器

        Args:
            weights_path: 模型权重路径
            device: 设备 ('cuda' 或 'cpu')
            conf_threshold: 置信度阈值
            iou_threshold: IOU阈值
        """
        self.device = torch.device(device if torch.cuda.is_available() else 'cpu')
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold

        # 加载模型
        print(f"加载模型: {weights_path}")
        self.model = torch.hub.load(
            'ultralytics/yolov5', 'custom',
            path=weights_path,
            device=self.device
        )

        # 设置模型参数
        self.model.conf = conf_threshold
        self.model.iou = iou_threshold

        # 获取类别名称
        self.class_names = self.model.names

        print(f"模型已加载到 {self.device}")
        print(f"类别数量: {len(self.class_names)}")

    def detect(self, image_source):
        """
        检测图像

        Args:
            image_source: 图像路径、numpy数组或PIL Image

        Returns:
            results: 检测结果
        """
        # 推理
        results = self.model(image_source)

        return results

    def detect_and_draw(self, image_path, save_path=None):
        """
        检测并绘制结果

        Args:
            image_path: 图像路径
            save_path: 保存路径

        Returns:
            image: 绘制后的图像
        """
        # 读取图像
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError(f"无法读取图像: {image_path}")

        # 检测
        results = self.detect(image_path)

        # 解析结果
        df = results.pandas().xyxy[0]

        # 绘制边界框
        for _, row in df.iterrows():
            x1, y1, x2, y2 = int(row['xmin']), int(row['ymin']), \
                            int(row['xmax']), int(row['ymax'])
            conf = row['confidence']
            class_id = int(row['class'])
            class_name = row['name']

            # 选择颜色
            color = self._get_color(class_id)

            # 绘制边界框
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

            # 绘制标签
            label = f"{class_name}: {conf:.2f}"
            label_size, _ = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2
            )

            # 绘制标签背景
            cv2.rectangle(
                image,
                (x1, y1 - label_size[1] - 10),
                (x1 + label_size[0], y1),
                color, -1
            )

            # 绘制标签文字
            cv2.putText(
                image, label,
                (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 255, 255), 2
            )

        # 转换为RGB用于显示
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # 保存
        if save_path:
            cv2.imwrite(str(save_path), image)
            print(f"结果已保存至: {save_path}")

        return image_rgb

    def detect_video(self, video_path, output_path=None,
                    display=False, fps=30):
        """
        检测视频

        Args:
            video_path: 视频路径
            output_path: 输出视频路径
            display: 是否显示
            fps: 输出视频帧率
        """
        # 打开视频
        cap = cv2.VideoCapture(str(video_path))

        if not cap.isOpened():
            raise ValueError(f"无法打开视频: {video_path}")

        # 获取视频属性
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # 创建视频写入器
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(
                str(output_path), fourcc, fps,
                (width, height)
            )

        # 处理每一帧
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1

            # 检测
            results = self.detect(frame)

            # 解析并绘制
            df = results.pandas().xyxy[0]
            for _, row in df.iterrows():
                x1, y1, x2, y2 = int(row['xmin']), int(row['ymin']), \
                                int(row['xmax']), int(row['ymax'])
                conf = row['confidence']
                class_name = row['name']
                class_id = int(row['class'])

                color = self._get_color(class_id)

                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

                label = f"{class_name}: {conf:.2f}"
                cv2.putText(frame, label, (x1, y1 - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                           color, 2)

            # 写入视频
            if output_path:
                out.write(frame)

            # 显示
            if display:
                cv2.imshow('Detection', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            # 打印进度
            if frame_count % 30 == 0:
                print(f"处理进度: {frame_count}/{total_frames} "
                      f"({frame_count/total_frames*100:.1f}%)")

        # 释放资源
        cap.release()
        if output_path:
            out.release()
        cv2.destroyAllWindows()

        print(f"\n视频处理完成! 共处理 {frame_count} 帧")

    def detect_webcam(self, camera_id=0):
        """实时检测摄像头输入"""
        # 打开摄像头
        cap = cv2.VideoCapture(camera_id)

        if not cap.isOpened():
            raise ValueError(f"无法打开摄像头: {camera_id}")

        print("按 'q' 退出")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # 检测
            results = self.detect(frame)

            # 绘制
            df = results.pandas().xyxy[0]
            for _, row in df.iterrows():
                x1, y1, x2, y2 = int(row['xmin']), int(row['ymin']), \
                                int(row['xmax']), int(row['ymax'])
                conf = row['confidence']
                class_name = row['name']
                class_id = int(row['class'])

                color = self._get_color(class_id)

                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

                label = f"{class_name}: {conf:.2f}"
                cv2.putText(frame, label, (x1, y1 - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                           color, 2)

            # 显示FPS
            # fps = self.model.fps  # 如果可用

            # 显示
            cv2.imshow('YOLOv5 Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def batch_detect(self, image_dir, output_dir):
        """
        批量检测图像

        Args:
            image_dir: 图像目录
            output_dir: 输出目录
        """
        image_dir = Path(image_dir)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # 支持的图像格式
        extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
        image_files = [f for f in image_dir.glob('*')
                      if f.suffix.lower() in extensions]

        print(f"找到 {len(image_files)} 张图像")

        for i, img_path in enumerate(image_files, 1):
            print(f"[{i}/{len(image_files)}] 处理: {img_path.name}")

            # 检测并保存
            output_path = output_dir / img_path.name
            self.detect_and_draw(img_path, output_path)

        print(f"\n批量检测完成! 结果保存至: {output_dir}")

    def evaluate(self, data_dir):
        """
        评估模型性能

        Args:
            data_dir: 数据集目录 (包含images和labels子目录)
        """
        # 这里可以实现完整的评估指标计算
        # 如mAP, precision, recall等
        print("评估功能 - 可以使用val.py实现")
        print("命令示例:")
        print(f"python val.py --weights {self.model.weights_path} "
              f"--data {data_dir} --device {self.device}")

    def _get_color(self, class_id):
        """根据类别ID获取颜色"""
        # 使用预定义颜色集
        colors = [
            (255, 0, 0), (0, 255, 0), (0, 0, 255),
            (255, 255, 0), (255, 0, 255), (0, 255, 255),
            (128, 0, 128), (255, 165, 0), (255, 192, 203),
            (0, 128, 128)
        ]
        return colors[class_id % len(colors)]


# 使用示例
if __name__ == "__main__":
    # 创建检测器
    detector = YOLOv5Detector(
        weights_path='runs/train/mask_detection/weights/best.pt',
        device='cuda',
        conf_threshold=0.25,
        iou_threshold=0.45
    )

    # 1. 单张图像检测
    print("\n=== 单张图像检测 ===")
    image = detector.detect_and_draw(
        'test_image.jpg',
        'output.jpg'
    )
    plt.imshow(image)
    plt.axis('off')
    plt.show()

    # 2. 批量检测
    print("\n=== 批量检测 ===")
    detector.batch_detect(
        image_dir='dataset/organized/images/test',
        output_dir='results/inference'
    )

    # 3. 视频检测
    print("\n=== 视频检测 ===")
    detector.detect_video(
        video_path='test_video.mp4',
        output_path='output_video.mp4',
        fps=30
    )

    # 4. 摄像头检测
    # print("\n=== 摄像头检测 ===")
    # detector.detect_webcam(camera_id=0)
```

### 3. 结果可视化
```python

# 依赖: matplotlib, numpy
# 安装: pip install matplotlib numpy
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict


def visualize_detection_results(image_dir, label_dir, detector,
                                num_samples=12):
    """
    可视化检测结果

    Args:
        image_dir: 图像目录
        label_dir: 标签目录
        detector: 检测器
        num_samples: 样本数量
    """
    image_dir = Path(image_dir)
    label_dir = Path(label_dir)

    # 获取图像文件
    image_files = list(image_dir.glob('*.jpg'))[:num_samples]

    n_cols = 4
    n_rows = (num_samples + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(20, 5*n_rows))
    fig.suptitle('检测结果可视化', fontsize=16)

    for idx, ax in enumerate(axes.flat):
        if idx < len(image_files):
            img_path = image_files[idx]

            # 检测
            result_img = detector.detect_and_draw(img_path)

            # 显示
            ax.imshow(result_img)
            ax.set_title(img_path.name, fontsize=10)
            ax.axis('off')
        else:
            ax.axis('off')

    plt.tight_layout()
    plt.savefig('detection_results.png', dpi=150, bbox_inches='tight')
    plt.show()


def analyze_predictions(detector, image_dir, label_dir):
    """
    分析预测结果

    Args:
        detector: 检测器
        image_dir: 图像目录
        label_dir: 标签目录
    """
    image_dir = Path(image_dir)
    label_dir = Path(label_dir)

    # 统计信息
    stats = defaultdict(int)
    confidences = []

    for img_path in image_dir.glob('*.jpg'):
        # 检测
        results = detector.detect(img_path)
        df = results.pandas().xyxy[0]

        # 统计
        for _, row in df.iterrows():
            class_name = row['name']
            conf = row['confidence']

            stats[class_name] += 1
            confidences.append(conf)

    # 绘制统计图
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))

    # 1. 类别分布
    if stats:
        classes = list(stats.keys())
        counts = list(stats.values())

        axes[0].bar(classes, counts, color='steelblue')
        axes[0].set_xlabel('类别')
        axes[0].set_ylabel('检测数量')
        axes[0].set_title('检测类别分布')
        axes[0].tick_params(axis='x', rotation=45)
        axes[0].grid(True, alpha=0.3)

    # 2. 置信度分布
    if confidences:
        axes[1].hist(confidences, bins=50, color='coral',
                    edgecolor='black')
        axes[1].set_xlabel('置信度')
        axes[1].set_ylabel('频次')
        axes[1].set_title('置信度分布')
        axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('prediction_analysis.png', dpi=150, bbox_inches='tight')
    plt.show()

    # 打印统计
    print("\n=== 检测统计 ===")
    for class_name, count in sorted(stats.items(),
                                    key=lambda x: x[1],
                                    reverse=True):
        print(f"{class_name}: {count}")

    if confidences:
        print(f"\n平均置信度: {np.mean(confidences):.4f}")
        print(f"最小置信度: {np.min(confidences):.4f}")
        print(f"最大置信度: {np.max(confidences):.4f}")
```

## 性能优化
### 1. 模型优化
```python

# 依赖: torch
# 安装: pip install torch
import torch


class ModelOptimizer:
    """模型优化工具"""

    @staticmethod
    def prune_model(model_path, output_path, pruning_ratio=0.3):
        """
        模型剪枝

        Args:
            model_path: 原始模型路径
            output_path: 剪枝后模型保存路径
            pruning_ratio: 剪枝比例
        """
        # 加载模型
        model = torch.hub.load('ultralytics/yolov5', 'custom',
                              path=model_path)

        # 这里需要实现剪枝逻辑
        # 可以使用torch.nn.utils.prune
        print("模型剪枝 - 需要进一步实现")

    @staticmethod
    def quantize_model(model_path, output_path):
        """
        模型量化 (INT8)

        Args:
            model_path: 原始模型路径
            output_path: 量化后模型保存路径
        """
        # 动态量化
        model = torch.hub.load('ultralytics/yolov5', 'custom',
                              path=model_path)
        model.model = torch.quantization.quantize_dynamic(
            model.model, {torch.nn.Linear}, dtype=torch.qint8
        )

        # 保存
        torch.save(model.model.state_dict(), output_path)
        print(f"量化模型已保存至: {output_path}")

    @staticmethod
    def export_to_onnx(model_path, output_path, img_size=640):
        """
        导出为ONNX格式

        Args:
            model_path: PyTorch模型路径
            output_path: ONNX输出路径
            img_size: 输入图像大小
        """
        # 导出命令
        import subprocess

        cmd = [
            'python', 'export.py',
            '--weights', model_path,
            '--img-size', str(img_size),
            '--batch-size', '1',
            '--device', 'cpu',
            '--include', 'onnx'
        ]

        subprocess.run(cmd, check=True)
        print(f"ONNX模型已导出")

    @staticmethod
    def export_to_tensorrt(model_path, engine_path, img_size=640):
        """
        导出为TensorRT引擎 (需要GPU)

        Args:
            model_path: ONNX模型路径
            engine_path: TensorRT引擎输出路径
            img_size: 输入图像大小
        """
        import tensorrt as trt
        import pycuda.driver as cuda
        import pycuda.autoinit

        print("TensorRT导出 - 需要安装TensorRT和CUDA工具包")
        # 这里需要实现TensorRT转换逻辑
```

### 2. 推理加速
```python

# 依赖: time
# 安装: pip install time
import time


class InferenceOptimizer:
    """推理优化"""

    def __init__(self, detector):
        self.detector = detector

    def benchmark(self, test_images, warmup_runs=10,
                 timed_runs=100):
        """
        性能测试

        Args:
            test_images: 测试图像列表
            warmup_runs: 预热运行次数
            timed_runs: 计时运行次数
        """
        print("\n=== 性能测试 ===")

        # 预热
        print(f"预热 ({warmup_runs} 次)...")
        for i in range(warmup_runs):
            img_path = test_images[i % len(test_images)]
            self.detector.detect(img_path)

        # 计时
        print(f"计时 ({timed_runs} 次)...")
        times = []
        for i in range(timed_runs):
            img_path = test_images[i % len(test_images)]

            start = time.time()
            self.detector.detect(img_path)
            end = time.time()

            times.append(end - start)

            if (i + 1) % 20 == 0:
                print(f"  进度: {i+1}/{timed_runs}")

        # 统计
        times = np.array(times)
        avg_time = np.mean(times)
        std_time = np.std(times)
        fps = 1.0 / avg_time

        print(f"\n结果:")
        print(f"  平均推理时间: {avg_time*1000:.2f} ms")
        print(f"  标准差: {std_time*1000:.2f} ms")
        print(f"  FPS: {fps:.2f}")

        return {
            'avg_time': avg_time,
            'std_time': std_time,
            'fps': fps
        }

    def optimize_batch_size(self, test_images, batch_sizes=[1, 2, 4, 8]):
        """
        优化批次大小

        Args:
            test_images: 测试图像列表
            batch_sizes: 要测试的批次大小列表
        """
        print("\n=== 批次大小优化 ===")

        results = {}
        for batch_size in batch_sizes:
            print(f"\n测试批次大小: {batch_size}")

            # 准备批次
            batch = test_images[:batch_size]
            if len(batch) < batch_size:
                batch = batch * (batch_size // len(batch) + 1)
                batch = batch[:batch_size]

            # 测试
            times = []
            for _ in range(50):
                start = time.time()

                # 批量推理
                for img_path in batch:
                    self.detector.detect(img_path)

                end = time.time()
                times.append(end - start)

            avg_time = np.mean(times)
            throughput = batch_size / avg_time

            results[batch_size] = {
                'avg_time': avg_time,
                'throughput': throughput
            }

            print(f"  平均时间: {avg_time*1000:.2f} ms")
            print(f"  吞吐量: {throughput:.2f} FPS")

        # 找出最佳批次大小
        best_batch_size = max(results.keys(),
                             key=lambda k: results[k]['throughput'])
        print(f"\n最佳批次大小: {best_batch_size}")
        print(f"最大吞吐量: {results[best_batch_size]['throughput']:.2f} FPS")

        return results
```

### 3. 部署优化
```python

# 依赖: detector, fastapi, io
# 安装: pip install detector fastapi io
class DeploymentOptimizer:
    """部署优化"""

    @staticmethod
    def create_dockerfile():
        """创建Docker部署文件"""
        dockerfile = """
FROM python:3.8-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制模型和代码
COPY models/ /app/models/
COPY src/ /app/src/

# 暴露端口
EXPOSE 8000

# 运行服务
CMD ["python", "/app/src/app.py"]
"""
        with open('Dockerfile', 'w') as f:
            f.write(dockerfile)
        print("Dockerfile已创建")

    @staticmethod
    def create_fastapi_app():
        """创建FastAPI应用"""
        app_code = """
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import io
from detector import YOLOv5Detector

app = FastAPI(title="YOLOv5 Detection API")

# 加载模型
detector = YOLOv5Detector(
    weights_path="models/best.pt",
    device="cpu"
)

@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    \"\"\"检测接口\"\"\"
    # 读取图像
    contents = await file.read()
    image_bytes = io.BytesIO(contents)

    # 保存临时文件
    with open("temp.jpg", "wb") as f:
        f.write(contents)

    # 检测
    results = detector.detect("temp.jpg")
    df = results.pandas().xyxy[0]

    # 转换为JSON
    detections = []
    for _, row in df.iterrows():
        detections.append({
            "class": row['name'],
            "confidence": float(row['confidence']),
            "bbox": {
                "xmin": float(row['xmin']),
                "ymin": float(row['ymin']),
                "xmax": float(row['xmax']),
                "ymax": float(row['ymax'])
            }
        })

    return JSONResponse(content={"detections": detections})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""
        with open('app.py', 'w') as f:
            f.write(app_code)
        print("FastAPI应用已创建")
```

## 项目总结
### 学习要点
1. **数据准备**
   - 数据收集策略
   - 标注工具的使用
   - 数据集划分和组织
   - 数据增强

2. **模型训练**
   - YOLOv5架构理解
   - 超参数调优
   - 训练技巧和最佳实践
   - 过拟合和欠拟合的处理

3. **模型评估**
   - mAP、Precision、Recall等指标
   - 混淆矩阵分析
   - 错误案例分析

4. **模型优化**
   - 模型压缩和加速
   - ONNX、TensorRT等格式转换
   - 边缘设备部署

5. **实际部署**
   - Flask/FastAPI接口开发
   - Docker容器化
   - 性能监控和日志

### 扩展方向
1. **多目标跟踪**
   - 集成DeepSORT、ByteTrack等跟踪算法
   - 实现视频中的目标跟踪

2. **实例分割**
   - 使用Mask R-CNN、YOLOACT等
   - 实现像素级分割

3. **3D目标检测**
   - 使用点云数据
   - 实现三维空间检测

4. **自动标注**
   - 使用主动学习
   - 减少标注工作量

### 参考资源
- [YOLOv5官方仓库](https://github.com/ultralytics/yolov5)
- [YOLOv5文档](https://docs.ultralytics.com/)
- [目标检测数据集](https://paperswithcode.com/datasets)
- [COCO数据集](https://cocodataset.org/)
- [Roboflow数据集工具](https://roboflow.com/)

### 常见问题
**Q1: 训练时显存不足？**
- 减小batch_size
- 使用更小的模型（如yolov5n或yolov5s）
- 减小输入图像大小
- 使用梯度累积

**Q2: 检测精度不够？**
- 收集更多训练数据
- 使用数据增强
- 调整置信度和IOU阈值
- 尝试更大的模型
- 训练更多epoch

**Q3: 推理速度太慢？**
- 使用更小的模型
- 减小输入图像大小
- 使用TensorRT优化
- 使用模型量化
- 使用批处理

**Q4: 如何处理小目标？**
- 增大输入图像大小
- 使用P2、P3等更小尺度的特征图
- 使用专门的注意力机制
- 使用数据增强（如Mosaic）

---

