# 计算机视觉练习题系统

> 系统化的练习题体系，从基础概念到高级应用，帮助你巩固知识、提升实战能力。

## 📚 练习题分类

### 🎯 基础练习（概念理解）

- 数学基础练习
- Python编程练习
- 图像基础操作练习

### 💻 编程练习（代码实现）

- 算法实现练习
- 框架使用练习
- 性能优化练习

### 🚀 项目练习（综合应用）

- 小型项目实战
- 算法复现
- 竞赛题目

### 🔥 挑战题（算法改进）

- 论文复现
- 算法创新
- 性能优化

---

## 📖 基础练习

### 1. 数学基础练习

#### 练习1.1：矩阵运算

```python
"""
题目：使用NumPy实现图像的矩阵运算
目标：理解图像作为矩阵的数学操作

任务：
1. 创建一个100x100的灰度图像（随机噪声）
2. 实现图像的加法、减法、乘法
3. 计算图像的均值、方差、标准差
4. 实现图像的归一化（0-1范围）
5. 可视化处理前后的图像

提示：
- 使用np.random创建随机图像
- 使用plt.imshow可视化
- 注意数据类型（uint8 vs float）
"""

# 你的代码

import numpy as np
import matplotlib.pyplot as plt

def matrix_operations():
    # 1. 创建随机图像
    img = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
    
    # 2. 矩阵运算
    img_add = img + 50  # 增加亮度
    img_sub = img - 30  # 减少亮度
    img_mul = img * 1.5  # 增加对比度
    
    # 3. 统计计算
    mean_val = np.mean(img)
    std_val = np.std(img)
    
    # 4. 归一化
    img_normalized = (img - mean_val) / std_val
    
    # 5. 可视化
    fig, axes = plt.subplots(1, 5, figsize=(15, 3))
    axes[0].imshow(img, cmap='gray')
    axes[0].set_title('原始')
    axes[1].imshow(img_add, cmap='gray')
    axes[1].set_title('加法')
    axes[2].imshow(img_sub, cmap='gray')
    axes[2].set_title('减法')
    axes[3].imshow(img_mul, cmap='gray')
    axes[3].set_title('乘法')
    axes[4].imshow(img_normalized, cmap='gray')
    axes[4].set_title('归一化')
    
    plt.tight_layout()
    plt.show()
    
    print(f"均值: {mean_val:.2f}, 标准差: {std_val:.2f}")

# 运行测试
# matrix_operations()

```

#### 练习1.2：梯度计算

```python
"""
题目：手动计算图像梯度
目标：理解卷积和梯度概念

任务：
1. 创建一个简单的图像（如渐变）
2. 实现Sobel算子（手动计算卷积）
3. 计算水平和垂直梯度
4. 合成梯度幅值和方向
5. 与OpenCV结果对比

提示：
- Sobel_x = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
- Sobel_y = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
- 梯度幅值 = sqrt(Gx^2 + Gy^2)
- 梯度方向 = arctan(Gy/Gx)
"""

# 你的代码

import numpy as np
import matplotlib.pyplot as plt

def manual_sobel(image):
    # 实现手动Sobel卷积
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    
    h, w = image.shape
    gx = np.zeros_like(image, dtype=np.float32)
    gy = np.zeros_like(image, dtype=np.float32)
    
    # 手动卷积（忽略边界）
    for i in range(1, h-1):
        for j in range(1, w-1):
            patch = image[i-1:i+2, j-1:j+2]
            gx[i, j] = np.sum(patch * sobel_x)
            gy[i, j] = np.sum(patch * sobel_y)
    
    # 计算梯度幅值和方向
    magnitude = np.sqrt(gx**2 + gy**2)
    direction = np.arctan2(gy, gx)
    
    return gx, gy, magnitude, direction

# 测试
# img = np.random.rand(100, 100)
# gx, gy, mag, dir = manual_sobel(img)

```

---

### 2. Python编程练习

#### 练习2.1：NumPy高效操作

```python
"""
题目：NumPy vs Python性能对比
目标：理解向量化操作的优势

任务：
1. 创建1000x1000的随机矩阵
2. 用Python循环实现矩阵加法
3. 用NumPy实现相同操作
4. 对比运行时间
5. 实现矩阵乘法的两种方式

提示：
- 使用time.time()计时
- 避免Python循环
- 理解广播机制
"""

# 你的代码

import numpy as np
import time

def performance_comparison():
    size = 1000
    a = np.random.rand(size, size)
    b = np.random.rand(size, size)
    
    # Python循环
    start = time.time()
    result_python = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            result_python[i, j] = a[i, j] + b[i, j]
    time_python = time.time() - start
    
    # NumPy向量化
    start = time.time()
    result_numpy = a + b
    time_numpy = time.time() - start
    
    print(f"Python循环: {time_python:.4f}s")
    print(f"NumPy向量化: {time_numpy:.4f}s")
    print(f"加速比: {time_python/time_numpy:.2f}x")
    
    # 验证结果一致性
    print(f"结果一致: {np.allclose(result_python, result_numpy)}")

# 运行测试
# performance_comparison()

```

#### 练习2.2：OpenCV基础操作

```python
"""
题目：OpenCV图像处理流水线
目标：掌握OpenCV核心功能

任务：
1. 读取彩色图像
2. 转换为灰度图
3. 高斯模糊去噪
4. Canny边缘检测
5. 保存处理结果
6. 创建函数封装整个流程

提示：
- cv2.imread()注意BGR格式
- cv2.GaussianBlur()参数调节
- cv2.Canny()阈值选择
"""

# 你的代码

import cv2
import numpy as np

def opencv_pipeline(image_path, output_path):
    # 读取图像
    img = cv2.imread(image_path)
    if img is None:
        print("图像读取失败")
        return
    
    # 转换为灰度
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 高斯模糊
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Canny边缘检测
    edges = cv2.Canny(blurred, 50, 150)
    
    # 保存结果
    cv2.imwrite(output_path, edges)
    
    print(f"处理完成: {output_path}")
    
    return edges

# 测试
# result = opencv_pipeline('input.jpg', 'edges.jpg')

```

---

### 3. 图像基础练习

#### 练习3.1：色彩空间转换

```python
"""
题目：多色彩空间转换与可视化
目标：理解不同色彩空间的特点

任务：
1. 读取彩色图像
2. 转换RGB → HSV
3. 转换RGB → Lab
4. 分离HSV通道并可视化
5. 在HSV空间调整饱和度
6. 转换回RGB并对比

提示：
- OpenCV: cv2.cvtColor()
- HSV: Hue(0-180), Saturation(0-255), Value(0-255)
- Lab: L(0-100), a(-128-127), b(-128-127)
"""

# 你的代码

import cv2
import matplotlib.pyplot as plt
import numpy as np

def color_space_conversion(image_path):
    # 读取图像
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # 转换色彩空间
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    
    # 分离HSV通道
    h, s, v = cv2.split(hsv)
    
    # 调整饱和度
    s_adjusted = np.clip(s * 1.5, 0, 255).astype(np.uint8)
    hsv_adjusted = cv2.merge([h, s_adjusted, v])
    img_saturated = cv2.cvtColor(hsv_adjusted, cv2.COLOR_HSV2RGB)
    
    # 可视化
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    axes[0, 0].imshow(img_rgb)
    axes[0, 0].set_title('RGB')
    
    axes[0, 1].imshow(h, cmap='hsv')
    axes[0, 1].set_title('Hue')
    
    axes[0, 2].imshow(s, cmap='gray')
    axes[0, 2].set_title('Saturation')
    
    axes[1, 0].imshow(v, cmap='gray')
    axes[1, 0].set_title('Value')
    
    axes[1, 1].imshow(lab[:, :, 0], cmap='gray')
    axes[1, 1].set_title('Lab - L')
    
    axes[1, 2].imshow(img_saturated)
    axes[1, 2].set_title('增强饱和度')
    
    for ax in axes.flat:
        ax.axis('off')
    
    plt.tight_layout()
    plt.show()

# 测试
# color_space_conversion('test.jpg')

```

---

## 💻 编程练习

### 4. 算法实现练习

#### 练习4.1：实现高斯滤波

```python
"""
题目：手动实现高斯滤波器
目标：理解滤波原理和高斯核

任务：
1. 生成高斯核（5x5, sigma=1.0）
2. 实现卷积函数
3. 对图像应用高斯滤波
4. 与OpenCV结果对比
5. 测试不同sigma的效果

提示：
- 高斯公式: G(x,y) = exp(-(x²+y²)/(2σ²))
- 归一化: 核元素和为1
- 边界处理: zero-padding
"""

# 你的代码

import numpy as np
import matplotlib.pyplot as plt

def create_gaussian_kernel(size=5, sigma=1.0):
    """生成高斯核"""
    center = size // 2
    kernel = np.zeros((size, size))
    
    for i in range(size):
        for j in range(size):
            x = i - center
            y = j - center
            kernel[i, j] = np.exp(-(x**2 + y**2) / (2 * sigma**2))
    
    # 归一化
    kernel = kernel / np.sum(kernel)
    return kernel

def manual_convolution(image, kernel):
    """手动卷积"""
    h, w = image.shape
    kh, kw = kernel.shape
    pad_h, pad_w = kh // 2, kw // 2
    
    # 边界填充
    padded = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant')
    result = np.zeros_like(image, dtype=np.float32)
    
    # 卷积
    for i in range(h):
        for j in range(w):
            patch = padded[i:i+kh, j:j+kw]
            result[i, j] = np.sum(patch * kernel)
    
    return result

def gaussian_filter_demo(image_path):
    # 读取图像
    img = plt.imread(image_path)
    if len(img.shape) == 3:
        img = img.mean(axis=2)
    
    # 手动实现
    kernel = create_gaussian_kernel(5, 1.0)
    manual_result = manual_convolution(img, kernel)
    
    # OpenCV对比
    import cv2
    cv_result = cv2.GaussianBlur(img, (5, 5), 1.0)
    
    # 可视化
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    axes[0].imshow(img, cmap='gray')
    axes[0].set_title('原始')
    axes[1].imshow(manual_result, cmap='gray')
    axes[1].set_title('手动实现')
    axes[2].imshow(cv_result, cmap='gray')
    axes[2].set_title('OpenCV')
    
    for ax in axes:
        ax.axis('off')
    
    plt.tight_layout()
    plt.show()
    
    print(f"差异: {np.abs(manual_result - cv_result).max():.6f}")

# 测试
# gaussian_filter_demo('test.jpg')

```

#### 练习4.2：实现边缘检测

```python
"""
题目：实现Canny边缘检测器
目标：理解边缘检测完整流程

任务：
1. 高斯滤波去噪
2. 计算梯度（Sobel）
3. 非极大值抑制
4. 双阈值检测
5. 滞后边缘跟踪

提示：
- 步骤1-2: 使用之前实现的函数
- 步骤3: 保留局部最大值
- 步骤4-5: 强边缘、弱边缘、伪边缘
"""

# 你的代码

import numpy as np
import matplotlib.pyplot as plt

def canny_edge_detector(image, low_threshold=50, high_threshold=150):
    """手动实现Canny边缘检测"""
    
    # 1. 高斯滤波
    kernel = create_gaussian_kernel(5, 1.0)
    smoothed = manual_convolution(image, kernel)
    
    # 2. 计算梯度
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    
    gx = manual_convolution(smoothed, sobel_x)
    gy = manual_convolution(smoothed, sobel_y)
    
    magnitude = np.sqrt(gx**2 + gy**2)
    direction = np.arctan2(gy, gx) * 180 / np.pi
    
    # 3. 非极大值抑制
    suppressed = np.zeros_like(magnitude)
    for i in range(1, magnitude.shape[0]-1):
        for j in range(1, magnitude.shape[1]-1):
            angle = direction[i, j]
            mag = magnitude[i, j]
            
            # 确定方向
            if (angle < 22.5 or angle >= 157.5) or (angle < -157.5 or angle >= -22.5):
                neighbors = [magnitude[i, j-1], magnitude[i, j+1]]
            elif (angle >= 22.5 and angle < 67.5) or (angle < -112.5 and angle >= -157.5):
                neighbors = [magnitude[i-1, j+1], magnitude[i+1, j-1]]
            elif (angle >= 67.5 and angle < 112.5) or (angle < -67.5 and angle >= -112.5):
                neighbors = [magnitude[i-1, j], magnitude[i+1, j]]
            else:
                neighbors = [magnitude[i-1, j-1], magnitude[i+1, j+1]]
            
            if mag >= max(neighbors):
                suppressed[i, j] = mag
    
    # 4. 双阈值和滞后
    edges = np.zeros_like(suppressed)
    strong = (suppressed >= high_threshold)
    weak = ((suppressed >= low_threshold) & (suppressed < high_threshold))
    
    edges[strong] = 255
    
    # 滞后连接
    for i in range(1, edges.shape[0]-1):
        for j in range(1, edges.shape[1]-1):
            if weak[i, j]:
                # 检查8邻域是否有强边缘
                if np.any(edges[i-1:i+2, j-1:j+2] == 255):
                    edges[i, j] = 255
    
    return edges

# 测试
# edges = canny_edge_detector(img, 50, 150)

```

---

### 5. 框架使用练习

#### 练习5.1：PyTorch神经网络

```python
"""
题目：用PyTorch实现MNIST分类器
目标：掌握PyTorch基本使用

任务：
1. 加载MNIST数据集
2. 定义简单CNN网络
3. 实现训练循环
4. 记录训练过程
5. 可视化结果

提示：
- 使用torchvision.datasets
- 网络结构: Conv2d → ReLU → MaxPool → Linear
- 损失函数: CrossEntropyLoss
- 优化器: Adam
"""

# 你的代码

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt

class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = x.view(-1, 64 * 7 * 7)
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x

def train_mnist():
    # 数据加载
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    
    train_dataset = datasets.MNIST('./data', train=True, download=True, transform=transform)
    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
    
    test_dataset = datasets.MNIST('./data', train=False, transform=transform)
    test_loader = DataLoader(test_dataset, batch_size=1000)
    
    # 模型、损失、优化器
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = SimpleCNN().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # 训练
    losses = []
    accuracies = []
    
    for epoch in range(10):
        model.train()
        running_loss = 0
        
        for batch_idx, (data, target) in enumerate(train_loader):
            data, target = data.to(device), target.to(device)
            
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
        
        # 测试
        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for data, target in test_loader:
                data, target = data.to(device), target.to(device)
                output = model(data)
                _, predicted = torch.max(output.data, 1)
                total += target.size(0)
                correct += (predicted == target).sum().item()
        
        epoch_loss = running_loss / len(train_loader)
        epoch_acc = 100 * correct / total
        
        losses.append(epoch_loss)
        accuracies.append(epoch_acc)
        
        print(f'Epoch {epoch+1}: Loss={epoch_loss:.4f}, Acc={epoch_acc:.2f}%')
    
    # 可视化
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    ax1.plot(losses, 'r-', linewidth=2)
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.set_title('Training Loss')
    ax1.grid(True)
    
    ax2.plot(accuracies, 'b-', linewidth=2)
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy (%)')
    ax2.set_title('Test Accuracy')
    ax2.grid(True)
    
    plt.tight_layout()
    plt.show()
    
    return model

# 运行
# model = train_mnist()

```

---

## 🚀 项目练习

### 6. 小型项目实战

#### 练习6.1：文档扫描与OCR预处理

```python
"""
项目：智能文档扫描系统
目标：综合应用图像处理技术

需求：
1. 检测文档边缘（角点检测）
2. 透视变换校正文档
3. 图像增强（对比度、锐化）
4. 二值化处理
5. 输出扫描结果

步骤：
1. 读取文档照片
2. 边缘检测 + 霍夫变换找直线
3. 找到四个角点
4. 透视变换
5. 图像增强
6. 二值化
7. 保存结果

扩展：集成Tesseract OCR
"""

# 你的代码

import cv2
import numpy as np
import matplotlib.pyplot as plt

def document_scanner(image_path):
    """文档扫描器"""
    
    # 1. 读取图像
    img = cv2.imread(image_path)
    original = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 2. 高斯模糊
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # 3. Canny边缘检测
    edges = cv2.Canny(blurred, 50, 150)
    
    # 4. 轮廓检测
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 5. 找到最大的轮廓（文档）
    if contours:
        doc_contour = max(contours, key=cv2.contourArea)
        
        # 近似多边形
        epsilon = 0.02 * cv2.arcLength(doc_contour, True)
        approx = cv2.approxPolyDP(doc_contour, epsilon, True)
        
        if len(approx) == 4:
            # 6. 透视变换
            pts = approx.reshape(4, 2).astype(np.float32)
            
            # 目标尺寸（A4纸）
            width, height = 210 * 4, 297 * 4
            dst = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype=np.float32)
            
            M = cv2.getPerspectiveTransform(pts, dst)
            warped = cv2.warpPerspective(original, M, (width, height))
            
            # 7. 图像增强
            # 转换为灰度
            warped_gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
            
            # 对比度增强
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            enhanced = clahe.apply(warped_gray)
            
            # 锐化
            kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
            sharpened = cv2.filter2D(enhanced, -1, kernel)
            
            # 二值化
            _, binary = cv2.threshold(sharpened, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            return warped, enhanced, binary
    
    return None, None, None

# 测试
# warped, enhanced, binary = document_scanner('document.jpg')

```

#### 练习6.2：人脸检测与美化

```python
"""
项目：人脸检测与美化系统
目标：综合应用人脸相关技术

需求：
1. 人脸检测（Haar或DNN）
2. 人脸关键点检测
3. 美白磨皮
4. 瘦脸大眼
5. 实时处理

步骤：
1. 检测人脸位置
2. 提取人脸区域
3. 磨皮处理（双边滤波）
4. 美白（亮度调整）
5. 瘦脸（局部变形）
6. 大眼（局部放大）
7. 实时摄像头处理

扩展：添加滤镜效果
"""

# 你的代码

import cv2
import numpy as np

class FaceBeautifier:
    def __init__(self):
        # 加载人脸检测器
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
    
    def detect_faces(self, image):
        """检测人脸"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )
        return faces
    
    def smooth_skin(self, face_roi):
        """磨皮"""
        # 双边滤波保边去噪
        smoothed = cv2.bilateralFilter(face_roi, 9, 75, 75)
        return smoothed
    
    def whiten_skin(self, face_roi, factor=1.2):
        """美白"""
        # 转换到HSV空间，调整V通道
        hsv = cv2.cvtColor(face_roi, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        
        # 限制范围避免过曝
        v = np.clip(v.astype(np.float32) * factor, 0, 255).astype(np.uint8)
        
        hsv = cv2.merge([h, s, v])
        whitened = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return whitened
    
    def process_image(self, image_path, output_path):
        """处理单张图片"""
        img = cv2.imread(image_path)
        faces = self.detect_faces(img)
        
        for (x, y, w, h) in faces:
            # 扩大ROI
            padding = int(min(w, h) * 0.1)
            x = max(0, x - padding)
            y = max(0, y - padding)
            w = min(img.shape[1] - x, w + 2 * padding)
            h = min(img.shape[0] - y, h + 2 * padding)
            
            face_roi = img[y:y+h, x:x+w].copy()
            
            # 美化
            smoothed = self.smooth_skin(face_roi)
            whitened = self.whiten_skin(smoothed)
            
            img[y:y+h, x:x+w] = whitened
            
            # 绘制人脸框
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        cv2.imwrite(output_path, img)
        return img
    
    def process_video(self, camera_id=0):
        """实时摄像头处理"""
        cap = cv2.VideoCapture(camera_id)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            faces = self.detect_faces(frame)
            
            for (x, y, w, h) in faces:
                padding = int(min(w, h) * 0.1)
                x = max(0, x - padding)
                y = max(0, y - padding)
                w = min(frame.shape[1] - x, w + 2 * padding)
                h = min(frame.shape[0] - y, h + 2 * padding)
                
                face_roi = frame[y:y+h, x:x+w].copy()
                
                if face_roi.size > 0:
                    smoothed = self.smooth_skin(face_roi)
                    whitened = self.whiten_skin(smoothed)
                    frame[y:y+h, x:x+w] = whitened
                
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            cv2.imshow('Face Beautifier', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

# 测试
# beautifier = FaceBeautifier()
# beautifier.process_image('portrait.jpg', 'beautiful.jpg')
# beautifier.process_video()  # 实时处理

```

---

### 7. 算法复现练习

#### 练习7.1：复现LeNet-5

```python
"""
题目：从零实现LeNet-5
目标：理解经典CNN架构

要求：
1. 手动实现卷积层（不使用框架）
2. 手动实现池化层
3. 实现前向传播
4. 在MNIST上测试
5. 与PyTorch版本对比

扩展：实现反向传播
"""

# 你的代码

import numpy as np

class ManualConv2D:
    """手动卷积层"""
    def __init__(self, in_channels, out_channels, kernel_size):
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        
        # 初始化权重
        self.weights = np.random.randn(out_channels, in_channels, kernel_size, kernel_size) * 0.1
        self.bias = np.zeros(out_channels)
    
    def forward(self, x):
        """前向传播"""
        batch_size, in_channels, h, w = x.shape
        out_h = h - self.kernel_size + 1
        out_w = w - self.kernel_size + 1
        
        output = np.zeros((batch_size, self.out_channels, out_h, out_w))
        
        for b in range(batch_size):
            for oc in range(self.out_channels):
                for ic in range(self.in_channels):
                    for i in range(out_h):
                        for j in range(out_w):
                            patch = x[b, ic, i:i+self.kernel_size, j:j+self.kernel_size]
                            output[b, oc, i, j] += np.sum(patch * self.weights[oc, ic]) + self.bias[oc]
        
        return output

class ManualMaxPool2D:
    """手动最大池化层"""
    def __init__(self, kernel_size, stride):
        self.kernel_size = kernel_size
        self.stride = stride
    
    def forward(self, x):
        batch_size, channels, h, w = x.shape
        out_h = (h - self.kernel_size) // self.stride + 1
        out_w = (w - self.kernel_size) // self.stride + 1
        
        output = np.zeros((batch_size, channels, out_h, out_w))
        
        for b in range(batch_size):
            for c in range(channels):
                for i in range(out_h):
                    for j in range(out_w):
                        i_start = i * self.stride
                        j_start = j * self.stride
                        patch = x[b, c, i_start:i_start+self.kernel_size, j_start:j_start+self.kernel_size]
                        output[b, c, i, j] = np.max(patch)
        
        return output

class ManualLinear:
    """手动全连接层"""
    def __init__(self, in_features, out_features):
        self.in_features = in_features
        self.out_features = out_features
        
        self.weights = np.random.randn(in_features, out_features) * 0.1
        self.bias = np.zeros(out_features)
    
    def forward(self, x):
        return np.dot(x, self.weights) + self.bias

class ManualLeNet5:
    """手动实现LeNet-5"""
    def __init__(self):
        self.conv1 = ManualConv2D(1, 6, 5)
        self.pool1 = ManualMaxPool2D(2, 2)
        self.conv2 = ManualConv2D(6, 16, 5)
        self.pool2 = ManualMaxPool2D(2, 2)
        self.fc1 = ManualLinear(16 * 5 * 5, 120)
        self.fc2 = ManualLinear(120, 84)
        self.fc3 = ManualLinear(84, 10)
    
    def forward(self, x):
        # Conv1
        x = self.conv1.forward(x)
        x = np.maximum(0, x)  # ReLU
        
        # Pool1
        x = self.pool1.forward(x)
        
        # Conv2
        x = self.conv2.forward(x)
        x = np.maximum(0, x)
        
        # Pool2
        x = self.pool2.forward(x)
        
        # Flatten
        batch_size = x.shape[0]
        x = x.reshape(batch_size, -1)
        
        # FC layers
        x = self.fc1.forward(x)
        x = np.maximum(0, x)
        
        x = self.fc2.forward(x)
        x = np.maximum(0, x)
        
        x = self.fc3.forward(x)
        
        # Softmax
        x = np.exp(x - np.max(x, axis=1, keepdims=True))
        x = x / np.sum(x, axis=1, keepdims=True)
        
        return x

# 测试

def test_manual_lenet():
    # 加载MNIST（简化）
    from torchvision import datasets, transforms
    import torch
    
    transform = transforms.Compose([transforms.ToTensor()])
    test_dataset = datasets.MNIST('./data', train=False, download=True, transform=transform)
    
    # 取前10个样本
    images = []
    labels = []
    for i in range(10):
        img, lbl = test_dataset[i]
        images.append(img.numpy())
        labels.append(lbl)
    
    images = np.array(images)  # (10, 1, 28, 28)
    
    # 调整尺寸到32x32
    from scipy.ndimage import zoom
    images_32 = np.zeros((10, 1, 32, 32))
    for i in range(10):
        images_32[i, 0] = zoom(images[i, 0], (32/28, 32/28))
    
    # 前向传播
    model = ManualLeNet5()
    outputs = model.forward(images_32)
    predictions = np.argmax(outputs, axis=1)
    
    accuracy = np.mean(predictions == labels)
    print(f"手动LeNet-5准确率: {accuracy:.2%}")
    
    return accuracy

# 运行测试
# test_manual_lenet()

```

---

## 🔥 挑战题

### 8. 算法改进挑战

#### 挑战8.1：优化YOLO检测器

```python
"""
挑战：改进YOLOv5检测器
目标：提升mAP或推理速度

任务：
1. 数据增强策略设计
2. 网络结构微调
3. 损失函数改进
4. 训练策略优化
5. 模型压缩

评估标准：
- mAP@0.5提升 > 5%
- 推理速度提升 > 20%
- 模型大小减少 > 30%

提交：代码 + 实验报告
"""

# 你的实现

"""
思路：
1. 数据增强：Mosaic + Mixup + AutoAugment
2. 网络：CSPDarknet + SE注意力
3. 损失：CIoU + Focal Loss
4. 训练：余弦退火 + warmup
5. 压缩：知识蒸馏 + 量化
"""

# 代码实现...

```

#### 挑战8.2：医学图像分割优化

```python
"""
挑战：提升U-Net在医学图像上的性能
目标：Dice系数 > 0.90

任务：
1. 设计新的损失函数
2. 改进网络结构
3. 数据增强策略
4. 后处理优化
5. 集成学习

数据集：Kvasir-SEG或自定义医学数据

提交：训练脚本 + 测试结果 + 分析报告
"""

# 你的实现

"""
思路：
1. 损失：Dice + BCE + 边界损失
2. 网络：U-Net++ + 注意力门控
3. 增强：弹性变形 + 旋转 + 亮度调整
4. 后处理：CRF优化
5. 集成：5-fold交叉验证
"""

# 代码实现...

```

---

## 📊 练习题完成标准

### 基础练习

- ✅ 代码能正确运行
- ✅ 理解每个步骤的原理
- ✅ 能解释关键参数的作用
- ✅ 完成所有任务要求

### 编程练习

- ✅ 代码结构清晰
- ✅ 有必要的注释
- ✅ 处理边界情况
- ✅ 与标准库结果对比

### 项目练习

- ✅ 完整的解决方案
- ✅ 代码模块化
- ✅ 有测试和验证
- ✅ 输出可视化结果

### 挑战题

- ✅ 创新性改进
- ✅ 实验数据支持
- ✅ 性能提升证明
- ✅ 详细分析报告

---

## 🎯 学习建议

### 每日练习计划

- **基础练习**：1-2小时，每天1-2题
- **编程练习**：2-3小时，每天1题
- **项目练习**：周末完成，3-4小时
- **挑战题**：每月1-2题，深度研究

### 练习方法

1. **先理解后实现**：看懂原理再写代码
2. **从简单开始**：先用小数据集测试
3. **逐步优化**：先实现功能，再优化性能
4. **记录问题**：遇到bug记录解决方案
5. **总结经验**：每个练习写总结

### 评估标准

- **初级**：能完成基础练习
- **中级**：能独立完成项目
- **高级**：能解决挑战题
- **专家**：能提出创新方案

---

## 📝 练习记录模板

```bash
# 练习记录

## 基本信息

- 练习名称：
- 完成日期：
- 用时：

## 练习内容

- 任务描述：
- 实现思路：
- 关键代码：

## 遇到问题

- 问题1：
- 解决方案：
- 学到经验：

## 总结

- 掌握知识点：
- 需要改进：
- 下一步计划：
```

---

**开始练习吧！每个练习都是通向专家的阶梯！** 🚀

*练习题系统持续更新中...*

*最后更新：2026年12月*
