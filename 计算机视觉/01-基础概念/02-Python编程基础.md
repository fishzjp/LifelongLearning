# Python编程基础 - 计算机视觉必备

> 本章从零开始详细介绍计算机视觉中必需的Python编程技能，包括NumPy、Pandas、Matplotlib等核心库。每个概念都有详细解释和代码示例。

## 📚 目录

- [为什么要学Python？](#为什么要学python)
- [Python基础语法](#python基础语法)
- [NumPy数组操作](#numpy数组操作)
- [Pandas数据处理](#pandas数据处理)
- [Matplotlib数据可视化](#matplotlib数据可视化)
- [OpenCV基础](#opencv基础)
- [实践练习](#实践练习)

---

## 为什么要学Python？

### Python是计算机视觉的首选语言

**为什么选择Python？**
- ✅ **简单易学**：语法接近自然语言，新手友好
- ✅ **生态丰富**：NumPy、OpenCV、PyTorch等强大库
- ✅ **开发快速**：代码简洁，调试方便
- ✅ **社区活跃**：海量教程和解决方案

### 本章学习目标

- ✅ 掌握Python基础，能写简单脚本
- ✅ 熟练使用NumPy处理图像数据
- ✅ 会用Pandas管理实验结果
- ✅ 能用Matplotlib展示图像和图表
- ✅ 了解OpenCV的基本图像操作

---

## Python基础语法

### 1.1 变量和数据类型

#### 什么是变量？

变量就像一个**盒子**，用来存放数据。

```bash
# 创建变量

age = 25                    # 整数（int）
height = 1.75               # 浮点数（float）
name = "小明"               # 字符串（str）
is_student = True           # 布尔值（bool）

print("变量示例：")
print(f"姓名: {name}, 类型: {type(name)}")
print(f"年龄: {age}, 类型: {type(age)}")
print(f"身高: {height}, 类型: {type(height)}")
print(f"是否学生: {is_student}, 类型: {type(is_student)}")

# 在计算机视觉中的应用

image_width = 1920          # 图像宽度
image_height = 1080         # 图像高度
fps = 30.0                  # 视频帧率
model_name = "ResNet50"     # 模型名称
is彩色 = True              # 是否彩色图像
```

#### 数据类型转换

```bash
# 类型转换示例

num_str = "123"             # 字符串
num_int = int(num_str)      # 转为整数
num_float = float(num_int)  # 转为浮点数

print(f"字符串 '{num_str}' -> 整数 {num_int} -> 浮点数 {num_float}")

# 计算机视觉中的应用

pixel_value = "255"         # 从文件读取的像素值（字符串）
pixel_int = int(pixel_value) # 转为整数进行计算
normalized = pixel_int / 255.0  # 归一化到0-1

print(f"像素值: {pixel_value} -> 归一化: {normalized}")
```

### 1.2 数据结构

#### 列表（List）- 可变的有序集合

```bash
# 创建列表

models = ["LeNet", "AlexNet", "VGG", "ResNet"]
print(f"模型列表: {models}")

# 访问元素（从0开始计数）

print(f"第一个模型: {models[0]}")      # LeNet
print(f"最后一个模型: {models[-1]}")    # ResNet

# 添加元素

models.append("EfficientNet")
print(f"添加后: {models}")

# 切片操作

print(f"前两个模型: {models[0:2]}")     # ['LeNet', 'AlexNet']
print(f"第2到第4个: {models[1:4]}")     # ['AlexNet', 'VGG', 'ResNet']

# 在计算机视觉中的应用

image_files = ["cat.jpg", "dog.jpg", "bird.jpg"]
accuracies = [0.92, 0.88, 0.95]  # 每张图片的准确率
```

#### 元组（Tuple）- 不可变的有序集合

```bash
# 创建元组

image_size = (1920, 1080)  # (宽度, 高度)
print(f"图像尺寸: {image_size}")

# 解包元组

width, height = image_size
print(f"宽度: {width}, 高度: {height}")

# 为什么用元组？
# - 保护数据不被意外修改
# - 作为字典的键
# - 函数返回多个值

# 在计算机视觉中的应用

bbox = (x1, y1, x2, y2) = (100, 150, 300, 400)  # 边界框
color = (255, 0, 0)  # RGB颜色，不可变
```

#### 字典（Dictionary）- 键值对

```bash
# 创建字典

model_info = {
    "name": "ResNet50",
    "accuracy": 0.95,
    "parameters": 25.6,
    "layers": 50
}

print("模型信息字典:")
for key, value in model_info.items():
    print(f"  {key}: {value}")

# 访问和修改

print(f"\n准确率: {model_info['accuracy']}")
model_info["accuracy"] = 0.96  # 更新
print(f"更新后准确率: {model_info['accuracy']}")

# 添加新键

model_info["训练时间"] = "12小时"
print(f"添加训练时间: {model_info}")

# 在计算机视觉中的应用

config = {
    "batch_size": 32,
    "learning_rate": 0.001,
    "epochs": 100,
    "optimizer": "Adam"
}
```

#### 集合（Set）- 去重的无序集合

```bash
# 创建集合

unique_labels = {"cat", "dog", "bird", "cat", "dog"}
print(f"原始: ['cat', 'dog', 'bird', 'cat', 'dog']")
print(f"去重后: {unique_labels}")

# 集合运算

animals1 = {"cat", "dog", "bird"}
animals2 = {"dog", "fish", "rabbit"}

print(f"交集: {animals1 & animals2}")      # 共同元素
print(f"并集: {animals1 | animals2}")      # 所有元素
print(f"差集: {animals1 - animals2}")      # 在1中但不在2中

# 在计算机视觉中的应用

all_classes = {"cat", "dog", "bird", "car", "person"}
detected_classes = {"cat", "bird", "car"}
missing_classes = all_classes - detected_classes  # 未检测到的类别
```

### 1.3 控制流

#### if条件语句

```bash
# 根据准确率给出评价

def evaluate_model(accuracy):
    if accuracy >= 0.95:
        return "优秀"
    elif accuracy >= 0.85:
        return "良好"
    elif accuracy >= 0.70:
        return "及格"
    else:
        return "需要改进"

# 测试

acc = 0.92
evaluation = evaluate_model(acc)
print(f"准确率 {acc} 的评价: {evaluation}")

# 计算机视觉中的应用

def check_image_quality(image):
    brightness = image.mean()
    contrast = image.std()

    if brightness < 50:
        return "太暗"
    elif brightness > 200:
        return "太亮"
    elif contrast < 20:
        return "对比度低"
    else:
        return "质量良好"
```

#### for循环

```bash
# 遍历列表

models = ["LeNet", "AlexNet", "VGG", "ResNet"]
print("模型列表：")
for i, model in enumerate(models):
    print(f"  {i+1}. {model}")

# 遍历字典

model_acc = {"LeNet": 0.98, "AlexNet": 0.95, "VGG": 0.96}
print("\n模型准确率：")
for model, acc in model_acc.items():
    print(f"  {model}: {acc:.1%}")

# range函数

print("\n训练进度：")
for epoch in range(5):  # 0, 1, 2, 3, 4
    print(f"  Epoch {epoch+1}/5")

# 列表推导式（简洁的循环）

accuracies = [0.85, 0.92, 0.78, 0.96]
high_acc_models = [models[i] for i, acc in enumerate(accuracies) if acc >= 0.90]
print(f"\n高准确率模型: {high_acc_models}")

# 计算机视觉中的应用
# 批量处理图像

processed_images = []
for img_path in ["img1.jpg", "img2.jpg", "img3.jpg"]:
    # img = cv2.imread(img_path)
    # processed = process_image(img)
    # processed_images.append(processed)
    print(f"  处理: {img_path}")
```

#### while循环

```bash
# 训练直到达到目标准确率

current_acc = 0.70
target_acc = 0.90
epoch = 0

print("训练过程：")
while current_acc < target_acc and epoch < 20:
    epoch += 1
    current_acc += 0.01  # 模拟准确率提升
    print(f"  Epoch {epoch}: 准确率 = {current_acc:.2f}")

print(f"训练完成！最终准确率: {current_acc:.2f}")

# 计算机视觉中的应用
# 等待模型收敛

loss = 1.0
threshold = 0.01
iteration = 0

while loss > threshold and iteration < 1000:
    # loss = train_step()
    loss *= 0.95  # 模拟损失下降
    iteration += 1
    if iteration % 100 == 0:
        print(f"迭代 {iteration}: 损失 = {loss:.4f}")
```

### 1.4 函数

#### 基础函数

```bash
# 定义函数

def calculate_iou(box1, box2):
    """
    计算两个边界框的交并比(IoU)

    参数:
        box1: [x1, y1, x2, y2] 第一个框
        box2: [x1, y1, x2, y2] 第二个框

    返回:
        iou: 交并比，范围[0, 1]
    """
    # 计算交集区域的坐标
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    # 计算交集面积
    intersection = max(0, x2 - x1) * max(0, y2 - y1)

    # 计算各自面积
    area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])

    # 计算并集面积
    union = area1 + area2 - intersection

    # 返回IoU
    return intersection / union if union > 0 else 0

# 使用函数

box_a = [50, 50, 150, 150]  # 左上角(50,50)，右下角(150,150)
box_b = [100, 100, 200, 200]
iou = calculate_iou(box_a, box_b)

print("IoU计算示例：")
print(f"框A: {box_a}")
print(f"框B: {box_b}")
print(f"IoU: {iou:.3f}")
```

#### 函数参数

```bash
# 默认参数

def train_model(name, lr=0.001, batch_size=32, epochs=100):
    print(f"训练模型: {name}")
    print(f"  学习率: {lr}")
    print(f"  批次大小: {batch_size}")
    print(f"  训练轮数: {epochs}")

# 使用默认参数

train_model("ResNet")
# 使用自定义参数

train_model("VGG", lr=0.01, epochs=50)

# 可变参数（*args）

def calculate_metrics(*values):
    """计算多个指标的平均值"""
    return sum(values) / len(values)

acc1, acc2, acc3 = 0.92, 0.88, 0.95
avg_acc = calculate_metrics(acc1, acc2, acc3)
print(f"\n平均准确率: {avg_acc:.3f}")

# 关键字参数（**kwargs）

def configure_model(name, **config):
    """配置模型参数"""
    print(f"\n模型: {name}")
    print("配置参数:")
    for key, value in config.items():
        print(f"  {key}: {value}")

configure_model("ResNet", lr=0.001, optimizer="Adam", weight_decay=1e-4)
```

#### Lambda函数（匿名函数）

```bash
# 简单的一次性函数

iou_func = lambda box1, box2: calculate_iou(box1, box2)

# 使用

box1 = [0, 0, 100, 100]
box2 = [50, 50, 150, 150]
print(f"\nLambda计算IoU: {iou_func(box1, box2):.3f}")

# 在排序中使用

models = [
    {"name": "A", "acc": 0.92},
    {"name": "B", "acc": 0.95},
    {"name": "C", "acc": 0.88}
]

# 按准确率排序

sorted_models = sorted(models, key=lambda x: x["acc"], reverse=True)
print("\n按准确率排序:")
for m in sorted_models:
    print(f"  {m['name']}: {m['acc']}")
```

---

## NumPy数组操作

### 2.1 为什么需要NumPy？

#### NumPy的优势

```python
import numpy as np
import time

# 普通Python列表

python_list = list(range(1000000))
start = time.time()
result = [x**2 for x in python_list]
end = time.time()
print(f"Python列表计算时间: {end-start:.4f}秒")

# NumPy数组

numpy_array = np.arange(1000000)
start = time.time()
result = numpy_array**2
end = time.time()
print(f"NumPy数组计算时间: {end-start:.4f}秒")

print("\nNumPy的优势：")
print("- 速度快：底层用C语言实现")
print("- 功能强大：支持各种数学运算")
print("- 内存高效：连续存储，节省空间")
print("- 语法简洁：向量化操作")
```

### 2.2 数组创建

#### 基础创建方法

```bash
# 从列表创建

arr1 = np.array([1, 2, 3, 4, 5])
print(f"从列表创建: {arr1}")

# 创建特殊数组

zeros = np.zeros(5)  # 全0数组
ones = np.ones((2, 3))  # 全1数组
eye = np.eye(3)  # 单位矩阵

print(f"\n全0数组: {zeros}")
print(f"全1数组:\n{ones}")
print(f"单位矩阵:\n{eye}")

# 创建范围数组

range1 = np.arange(0, 10, 2)  # 0到10，步长2
range2 = np.linspace(0, 1, 5)  # 0到1，分成5份

print(f"\narange(0,10,2): {range1}")
print(f"linspace(0,1,5): {range2}")

# 随机数组

random1 = np.random.rand(3, 3)  # [0,1)均匀分布
random2 = np.random.randn(3, 3)  # 标准正态分布
random3 = np.random.randint(0, 256, (100, 100, 3))  # 随机图像

print(f"\n随机数组 [0,1):\n{random1}")
print(f"随机图像形状: {random3.shape}")
```

### 2.3 数组索引和切片

#### 一维数组索引

```python
arr = np.array([10, 20, 30, 40, 50, 60])

print("一维数组索引：")
print(f"arr[0]: {arr[0]}")      # 第一个元素: 10
print(f"arr[2]: {arr[2]}")      # 第三个元素: 30
print(f"arr[-1]: {arr[-1]}")    # 最后一个: 60
print(f"arr[-2]: {arr[-2]}")    # 倒数第二个: 50

print("\n一维数组切片：")
print(f"arr[1:4]: {arr[1:4]}")      # 第2到第4个: [20 30 40]
print(f"arr[:3]: {arr[:3]}")        # 前3个: [10 20 30]
print(f"arr[3:]: {arr[3:]}")        # 第4个到最后: [40 50 60]
print(f"arr[::2]: {arr[::2]}")      # 步长为2: [10 30 50]
print(f"arr[::-1]: {arr[::-1]}")    # 反转: [60 50 40 30 20 10]
```

#### 二维数组索引（图像处理基础）

```bash
# 创建一个5x5的矩阵（模拟小图像）

matrix = np.array([
    [1, 2, 3, 4, 5],
    [6, 7, 8, 9, 10],
    [11, 12, 13, 14, 15],
    [16, 17, 18, 19, 20],
    [21, 22, 23, 24, 25]
])

print("二维数组索引：")
print(f"matrix[0, 0]: {matrix[0, 0]}")    # 第1行第1列: 1
print(f"matrix[2, 3]: {matrix[2, 3]}")    # 第3行第4列: 14
print(f"matrix[-1, -1]: {matrix[-1, -1]}") # 最后一行最后一列: 25

print("\n二维数组切片：")
print(f"matrix[0, :]: {matrix[0, :]}")        # 第1行: [1 2 3 4 5]
print(f"matrix[:, 0]: {matrix[:, 0]}")        # 第1列: [1 6 11 16 21]
print(f"matrix[1:3, 2:4]:\n{matrix[1:3, 2:4]}")  # 第2-3行，第3-4列
# 结果: [[8 9] [13 14]]

print("\n条件索引：")
even_numbers = matrix[matrix % 2 == 0]  # 所有偶数
print(f"偶数: {even_numbers}")

greater_than_15 = matrix[matrix > 15]   # 大于15的数
print(f"大于15: {greater_than_15}")
```

#### 三维数组索引（彩色图像）

```bash
# 创建一个3x4x3的数组（模拟彩色图像）
# 高度=3，宽度=4，通道=3（RGB）

image = np.random.randint(0, 256, (3, 4, 3), dtype=np.uint8)

print("彩色图像数组：")
print(f"形状: {image.shape}")
print(f"数据类型: {image.dtype}")

# 索引示例

print(f"\n左上角像素: {image[0, 0, :]}")  # [R, G, B]
print(f"中心像素: {image[1, 2, :]}")

# 切片示例

print(f"\n第一行: {image[0, :, :]}")  # 形状: (4, 3)
print(f"红色通道:\n{image[:, :, 0]}")  # 形状: (3, 4)

# 区域提取

region = image[0:2, 1:3, :]  # 提取左上角2x2区域
print(f"\n2x2区域形状: {region.shape}")
```

### 2.4 数组运算

#### 元素级运算

```python
a = np.array([1, 2, 3, 4])
b = np.array([5, 6, 7, 8])

print("元素级运算：")
print(f"a = {a}")
print(f"b = {b}")
print(f"a + b = {a + b}")      # [6 8 10 12]
print(f"a - b = {a - b}")      # [-4 -4 -4 -4]
print(f"a * b = {a * b}")      # [5 12 21 32]
print(f"a / b = {a / b}")      # [0.2 0.333... 0.428... 0.5]
print(f"a ** 2 = {a ** 2}")    # [1 4 9 16]

# 比较运算

print(f"a > 2: {a > 2}")       # [False False True True]
print(f"a == b: {a == b}")     # [False False False False]
```

#### 矩阵运算

```python
A = np.array([[1, 2],
              [3, 4]])
B = np.array([[5, 6],
              [7, 8]])

print("矩阵A:")
print(A)
print("\n矩阵B:")
print(B)

# 矩阵乘法（重要！）

print("\n矩阵乘法 A @ B:")
print(A @ B)
# 计算过程：
# 第1行: [1,2] @ [5,7] = 1*5 + 2*7 = 19
#         [1,2] @ [6,8] = 1*6 + 2*8 = 22
# 第2行: [3,4] @ [5,7] = 3*5 + 4*7 = 43
#         [3,4] @ [6,8] = 3*6 + 4*8 = 50

# 元素级乘法

print("\n元素级乘法 A * B:")
print(A * B)

# 转置

print("\nA的转置:")
print(A.T)

# 求逆（如果存在）

try:
    A_inv = np.linalg.inv(A)
    print("\nA的逆矩阵:")
    print(A_inv)
    print("\n验证 A @ A⁻¹:")
    print(A @ A_inv)  # 应该接近单位矩阵
except:
    print("\nA不可逆")
```

#### 聚合运算

```python
data = np.random.randint(0, 256, (100, 100, 3))
print(f"随机图像数据形状: {data.shape}")

# 基本统计

print(f"\n基本统计：")
print(f"均值: {data.mean():.2f}")
print(f"标准差: {data.std():.2f}")
print(f"最小值: {data.min()}")
print(f"最大值: {data.max()}")
print(f"求和: {data.sum()}")

# 沿指定轴聚合

print(f"\n各通道均值: {data.mean(axis=(0, 1))}")  # 对高度和宽度求均值
print(f"每行均值: {data.mean(axis=1).shape}")     # 对宽度求均值

# 百分位数

print(f"\n25%分位数: {np.percentile(data, 25):.2f}")
print(f"50%分位数（中位数）: {np.percentile(data, 50):.2f}")
print(f"75%分位数: {np.percentile(data, 75):.2f}")
```

### 2.5 数组变形和操作

#### 改变形状

```bash
# 创建数组

arr = np.arange(12)  # [0, 1, 2, ..., 11]
print(f"原始数组: {arr}")

# 改变形状

matrix1 = arr.reshape(3, 4)  # 3行4列
print(f"\nreshape(3, 4):\n{matrix1}")

matrix2 = arr.reshape(4, 3)  # 4行3列
print(f"\nreshape(4, 3):\n{matrix2}")

# -1表示自动计算

matrix3 = arr.reshape(2, -1)  # 2行，列数自动
print(f"\nreshape(2, -1):\n{matrix3}")

# 展平

matrix = np.array([[1, 2, 3], [4, 5, 6]])
print(f"\n原始矩阵:\n{matrix}")
print(f"展平: {matrix.flatten()}")

# 增加/减少维度

print(f"\n原始形状: {arr.shape}")
print(f"增加批次维度: {arr[np.newaxis, :].shape}")  # (1, 12)
print(f"增加通道维度: {arr[:, np.newaxis].shape}")  # (12, 1)
```

#### 数组拼接

```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print("拼接操作：")
print(f"a = {a}")
print(f"b = {b}")

# 水平拼接

print(f"\n水平拼接: {np.hstack((a, b))}")  # [1 2 3 4 5 6]

# 垂直拼接

print(f"垂直拼接:\n{np.vstack((a, b))}")
# [[1 2 3]
#  [4 5 6]]

# 沿指定轴拼接

c = np.array([[1, 2], [3, 4]])
d = np.array([[5, 6], [7, 8]])

print(f"\nc = \n{c}")
print(f"d = \n{d}")
print(f"\n沿轴0拼接（垂直）:\n{np.concatenate((c, d), axis=0)}")
print(f"\n沿轴1拼接（水平）:\n{np.concatenate((c, d), axis=1)}")
```

#### 数组分割

```python
arr = np.arange(10)
print(f"原始数组: {arr}")

# 分割

parts = np.split(arr, 5)  # 分成5份
print(f"\n分成5份: {parts}")

# 不等分割

parts2 = np.split(arr, [3, 7])  # 在索引3和7处分割
print(f"在索引[3,7]处分割: {parts2}")

# 垂直和水平分割

matrix = np.arange(12).reshape(3, 4)
print(f"\n矩阵:\n{matrix}")
print(f"\n垂直分割:\n{np.vsplit(matrix, 3)}")
print(f"\n水平分割:\n{np.hsplit(matrix, 2)}")
```

---

## Pandas数据处理

### 3.1 为什么需要Pandas？

#### 数据处理需求

在计算机视觉项目中，我们需要：
- 记录每个epoch的训练损失和准确率
- 管理数据集的信息（文件路径、标签、尺寸）
- 分析不同模型的性能对比
- 处理实验结果和统计信息

Pandas提供了类似Excel的表格数据结构，让这些操作变得简单。

### 3.2 DataFrame基础

#### 创建DataFrame

```python
import pandas as pd

# 从字典创建

data = {
    '模型': ['LeNet', 'AlexNet', 'VGG16', 'ResNet50', 'EfficientNet'],
    '准确率': [0.98, 0.95, 0.96, 0.97, 0.98],
    '参数量(M)': [0.6, 60, 138, 25.6, 5.3],
    '训练时间(小时)': [2, 8, 16, 12, 10]
}

df = pd.DataFrame(data)
print("模型性能表格：")
print(df)

print(f"\n表格形状: {df.shape}")  # (5, 4) 表示5行4列
print(f"列名: {df.columns.tolist()}")
```

#### 查看数据

```bash
# 基本信息

print("数据类型：")
print(df.dtypes)

print("\n统计摘要：")
print(df.describe())  # 数值列的统计信息

print("\n前3行：")
print(df.head(3))

print("\n后2行：")
print(df.tail(2))

print("\n指定列：")
print(df['模型'])

print("\n多列：")
print(df[['模型', '准确率']])
```

### 3.3 数据筛选和排序

#### 条件筛选

```bash
# 单条件筛选

high_acc = df[df['准确率'] >= 0.96]
print("准确率≥0.96的模型：")
print(high_acc)

# 多条件筛选

efficient = df[(df['准确率'] >= 0.96) & (df['参数量(M)'] < 30)]
print("\n准确率≥0.96且参数量<30M的模型：")
print(efficient)

# 或条件

slow_or_large = df[(df['训练时间(小时)'] > 10) | (df['参数量(M)'] > 100)]
print("\n训练时间>10小时或参数量>100M的模型：")
print(slow_or_large)

# 字符串筛选

resnet_models = df[df['模型'].str.contains('ResNet')]
print("\n包含'ResNet'的模型：")
print(resnet_models)
```

#### 排序

```bash
# 按准确率降序

sorted_by_acc = df.sort_values('准确率', ascending=False)
print("按准确率降序：")
print(sorted_by_acc)

# 按多列排序

sorted_multi = df.sort_values(['准确率', '训练时间(小时)'], ascending=[False, True])
print("\n按准确率降序，训练时间升序：")
print(sorted_multi)

# 获取前N个

top3 = df.nlargest(3, '准确率')
print("\n准确率最高的3个模型：")
print(top3)

bottom2 = df.nsmallest(2, '训练时间(小时)')
print("\n训练时间最短的2个模型：")
print(bottom2)
```

### 3.4 数据处理

#### 缺失值处理

```bash
# 创建包含缺失值的数据

df_with_nan = df.copy()
df_with_nan.loc[2, '训练时间(小时)'] = np.nan
df_with_nan.loc[3, '参数量(M)'] = np.nan

print("原始数据（含缺失值）：")
print(df_with_nan)

# 检查缺失值

print(f"\n缺失值统计：")
print(df_with_nan.isnull().sum())

# 填充缺失值

filled_mean = df_with_nan.fillna(df_with_nan.mean())
print("\n用均值填充缺失值：")
print(filled_mean)

# 删除缺失值

dropped = df_with_nan.dropna()
print("\n删除含缺失值的行：")
print(dropped)
```

#### 数据标准化和变换

```bash
# 标准化（Z-score）

df['准确率_标准化'] = (df['准确率'] - df['准确率'].mean()) / df['准确率'].std()
print("添加标准化列：")
print(df[['模型', '准确率', '准确率_标准化']])

# 归一化（Min-Max）

df['参数量_归一化'] = (df['参数量(M)'] - df['参数量(M)'].min()) / (df['参数量(M)'].max() - df['参数量(M)'].min())
print("\n添加归一化列：")
print(df[['模型', '参数量(M)', '参数量_归一化']])

# 应用函数

def efficiency_score(row):
    """效率评分 = 准确率 / 参数量"""
    return row['准确率'] / row['参数量(M)']

df['效率评分'] = df.apply(efficiency_score, axis=1)
print("\n添加效率评分：")
print(df[['模型', '效率评分']].sort_values('效率评分', ascending=False))
```

#### 分组统计

```bash
# 添加分类列

df['类型'] = ['小型', '大型', '大型', '中型', '中型']

# 分组统计

grouped = df.groupby('类型').mean()
print("按类型分组统计：")
print(grouped)

# 多个统计量

grouped_multi = df.groupby('类型').agg({
    '准确率': ['mean', 'std', 'max'],
    '训练时间(小时)': ['mean', 'sum']
})
print("\n多个统计量：")
print(grouped_multi)

# 分组计数

counts = df['类型'].value_counts()
print("\n各类型数量：")
print(counts)
```

---

## Matplotlib数据可视化

### 4.1 为什么需要可视化？

#### 可视化的重要性

- **理解数据**：直观看到数据分布和趋势
- **调试模型**：观察训练过程中的损失和准确率变化
- **展示结果**：向他人展示实验结果
- **发现问题**：发现异常值或数据问题

### 4.2 基础绘图

#### 折线图（训练过程）

```python
import matplotlib.pyplot as plt

# 设置中文字体（解决中文显示问题）

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 模拟训练过程

epochs = list(range(1, 21))
train_loss = [1.0 - 0.05 * i + np.random.randn() * 0.02 for i in epochs]
val_loss = [1.2 - 0.04 * i + np.random.randn() * 0.03 for i in epochs]

plt.figure(figsize=(10, 6))
plt.plot(epochs, train_loss, label='训练损失', linewidth=2, marker='o')
plt.plot(epochs, val_loss, label='验证损失', linewidth=2, marker='s')

plt.xlabel('训练轮数')
plt.ylabel('损失值')
plt.title('训练过程中的损失变化')
plt.legend()
plt.grid(True, alpha=0.3)

# 添加标注

min_val_idx = np.argmin(val_loss)
plt.annotate(f'最小值: {val_loss[min_val_idx]:.3f}',
             xy=(epochs[min_val_idx], val_loss[min_val_idx]),
             xytext=(10, 10), textcoords='offset points',
             bbox=dict(boxstyle='round', fc='yellow', alpha=0.7))

plt.show()
```

#### 散点图（参数vs性能）

```bash
# 模型参数和准确率

models = ['LeNet', 'AlexNet', 'VGG16', 'ResNet50', 'EfficientNet']
params = [0.6, 60, 138, 25.6, 5.3]
accs = [0.98, 0.95, 0.96, 0.97, 0.98]

plt.figure(figsize=(10, 6))
plt.scatter(params, accs, s=200, alpha=0.6, c=range(len(models)), cmap='viridis')

# 添加标签

for i, model in enumerate(models):
    plt.annotate(model, (params[i], accs[i]),
                xytext=(5, 5), textcoords='offset points',
                fontsize=10, ha='left')

plt.xlabel('参数量 (M)')
plt.ylabel('准确率')
plt.title('模型参数量 vs 准确率')
plt.grid(True, alpha=0.3)

# 添加趋势线

z = np.polyfit(params, accs, 1)
p = np.poly1d(z)
plt.plot(params, p(params), "r--", alpha=0.8, label='趋势线')
plt.legend()

plt.show()
```

#### 柱状图（性能对比）

```bash
# 模型准确率对比

plt.figure(figsize=(12, 5))

# 单柱状图

plt.subplot(1, 2, 1)
plt.bar(models, accs, color=['skyblue', 'lightgreen', 'orange', 'pink', 'yellow'])
plt.xlabel('模型')
plt.ylabel('准确率')
plt.title('各模型准确率对比')
plt.ylim(0.9, 1.0)
plt.xticks(rotation=45)

# 在柱子上标注数值

for i, v in enumerate(accs):
    plt.text(i, v + 0.001, f'{v:.3f}', ha='center', va='bottom')

# 分组柱状图

plt.subplot(1, 2, 2)
train_time = [2, 8, 16, 12, 10]
x = np.arange(len(models))
width = 0.35

plt.bar(x - width/2, accs, width, label='准确率', alpha=0.8)
plt.bar(x + width/2, [t/20 for t in train_time], width, label='训练时间/20', alpha=0.8)

plt.xlabel('模型')
plt.ylabel('数值')
plt.title('准确率和训练时间对比')
plt.xticks(x, models, rotation=45)
plt.legend()

plt.tight_layout()
plt.show()
```

### 4.3 子图布局

```bash
# 创建2x2的子图

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# 1. 折线图

axes[0, 0].plot(epochs, train_loss, 'b-', label='训练损失')
axes[0, 0].set_title('训练损失')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# 2. 散点图

axes[0, 1].scatter(params, accs, s=100, alpha=0.6)
axes[0, 1].set_title('参数 vs 准确率')
axes[0, 1].set_xlabel('参数量')
axes[0, 1].set_ylabel('准确率')

# 3. 柱状图

axes[1, 0].bar(models, accs, alpha=0.7)
axes[1, 0].set_title('模型准确率')
axes[1, 0].tick_params(axis='x', rotation=45)

# 4. 直方图（数据分布）

data = np.random.randn(1000)
axes[1, 1].hist(data, bins=30, alpha=0.7, color='purple')
axes[1, 1].set_title('数据分布')
axes[1, 1].set_xlabel('值')
axes[1, 1].set_ylabel('频次')

plt.tight_layout()
plt.show()
```

### 4.4 图像显示

#### 显示单张图像

```bash
# 创建测试图像

test_image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
# 添加一些结构

test_image[20:80, 20:80, :] = [255, 100, 50]  # 橙色方块

plt.figure(figsize=(6, 6))
plt.imshow(test_image)
plt.title('测试图像')
plt.axis('off')  # 不显示坐标轴
plt.show()
```

#### 显示多张图像

```bash
# 创建多张测试图像

images = []
for i in range(6):
    img = np.zeros((50, 50, 3), dtype=np.uint8)
    color = [0, 0, 0]
    color[i % 3] = 255  # 红、绿、蓝循环
    img[:, :] = color
    images.append(img)

# 2x3布局

fig, axes = plt.subplots(2, 3, figsize=(12, 8))
axes = axes.flatten()

for i, (img, ax) in enumerate(zip(images, axes)):
    ax.imshow(img)
    ax.set_title(f'图像 {i+1}')
    ax.axis('off')

plt.suptitle('多图像显示示例')
plt.tight_layout()
plt.show()
```

#### 灰度图像和颜色映射

```bash
# 灰度图像

gray_image = np.random.randint(0, 256, (100, 100), dtype=np.uint8)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# 灰度显示

axes[0].imshow(gray_image, cmap='gray')
axes[0].set_title('灰度图像')
axes[0].axis('off')

# 热力图

axes[1].imshow(gray_image, cmap='hot')
axes[1].set_title('热力图')
axes[1].axis('off')

# 添加颜色条

im = axes[2].imshow(gray_image, cmap='viridis')
axes[2].set_title('Viridis色图')
axes[2].axis('off')
plt.colorbar(im, ax=axes[2], label='像素强度')

plt.show()
```

---

## OpenCV基础

### 5.1 OpenCV简介

#### 为什么用OpenCV？

OpenCV（Open Source Computer Vision Library）是计算机视觉的**标准库**，提供：
- ✅ **图像读写**：支持多种格式
- ✅ **基础处理**：滤波、变换、边缘检测
- ✅ **特征提取**：SIFT、ORB等
- ✅ **目标检测**：人脸、物体检测
- ✅ **视频处理**：读取、处理、保存

### 5.2 图像读取与显示

#### 基础操作

```python
import cv2

# 创建测试图像并保存

test_img = np.zeros((200, 300, 3), dtype=np.uint8)
test_img[50:150, 50:250] = [100, 150, 200]  # 蓝绿色
cv2.imwrite('/tmp/test_image_cv.jpg', test_img)

# 读取图像

img_bgr = cv2.imread('/tmp/test_image_cv.jpg')  # OpenCV默认BGR
print(f"图像形状: {img_bgr.shape}")
print(f"数据类型: {img_bgr.dtype}")

# 转换为RGB用于显示

img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

# 显示对比

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].imshow(img_bgr)
axes[0].set_title('OpenCV BGR')
axes[0].axis('off')

axes[1].imshow(img_rgb)
axes[1].set_title('RGB')
axes[1].axis('off')

plt.show()

# 注意：OpenCV的BGR顺序 vs Matplotlib的RGB顺序

print(f"\nBGR像素值: {img_bgr[100, 150]}")
print(f"RGB像素值: {img_rgb[100, 150]}")
```

### 5.3 基础图像处理

#### 几何变换

```bash
# 缩放

h, w = img_bgr.shape[:2]
img_small = cv2.resize(img_bgr, (w//2, h//2))  # 缩小一半
img_large = cv2.resize(img_bgr, (w*2, h*2))    # 放大两倍

# 旋转

center = (w // 2, h // 2)
angle = 45
scale = 1.0
rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)
img_rotated = cv2.warpAffine(img_bgr, rotation_matrix, (w, h))

# 平移

translation_matrix = np.float32([[1, 0, 50], [0, 1, 30]])  # 右移50，下移30
img_translated = cv2.warpAffine(img_bgr, translation_matrix, (w, h))

# 可视化

fig, axes = plt.subplots(2, 2, figsize=(12, 10))
images = [img_bgr, img_small, img_rotated, img_translated]
titles = ['原图', '缩小', '旋转45°', '平移']

for ax, img, title in zip(axes.flat, images, titles):
    ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    ax.set_title(title)
    ax.axis('off')

plt.tight_layout()
plt.show()
```

#### 颜色空间转换

```bash
# BGR -> 灰度

gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

# BGR -> HSV

hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

# BGR -> LAB

lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)

# 可视化

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

axes[0, 0].imshow(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB))
axes[0, 0].set_title('BGR')
axes[0, 0].axis('off')

axes[0, 1].imshow(gray, cmap='gray')
axes[0, 1].set_title('灰度')
axes[0, 1].axis('off')

axes[1, 0].imshow(hsv)
axes[1, 0].set_title('HSV')
axes[1, 0].axis('off')

axes[1, 1].imshow(lab)
axes[1, 1].set_title('LAB')
axes[1, 1].axis('off')

plt.show()
```

#### 滤波和边缘检测

```bash
# 创建含噪声的图像

noisy = img_bgr.copy()
noise = np.random.randint(-30, 30, img_bgr.shape, dtype=np.int16)
noisy = np.clip(noisy.astype(np.int16) + noise, 0, 255).astype(np.uint8)

# 各种滤波

blur_mean = cv2.blur(noisy, (5, 5))      # 均值滤波
blur_gaussian = cv2.GaussianBlur(noisy, (5, 5), 0)  # 高斯滤波
blur_median = cv2.medianBlur(noisy, 5)   # 中值滤波

# 边缘检测

edges = cv2.Canny(gray, 50, 150)

# 可视化

fig, axes = plt.subplots(2, 3, figsize=(15, 10))

images = [noisy, blur_mean, blur_gaussian, blur_median, gray, edges]
titles = ['含噪声', '均值滤波', '高斯滤波', '中值滤波', '原图灰度', '边缘检测']

for ax, img, title in zip(axes.flat, images, titles):
    if len(img.shape) == 2:
        ax.imshow(img, cmap='gray')
    else:
        ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    ax.set_title(title)
    ax.axis('off')

plt.tight_layout()
plt.show()
```

---

## 实践练习

### 练习1：NumPy数组操作

```python
"""
练习1：NumPy数组操作

目标：掌握NumPy基础操作

任务：
1. 创建一个10x10的随机矩阵（0-255）
2. 提取中心5x5区域
3. 将该区域所有值加100
4. 计算整个矩阵的均值和标准差
5. 将矩阵展平并排序

提示：
- 使用 np.random.randint()
- 使用切片操作
- 使用 .flatten() 和 np.sort()
"""

def numpy_practice():
    # 你的代码
    pass

# 运行
# numpy_practice()

```

### 练习2：图像处理函数

```python
"""
练习2：图像处理函数

目标：编写实用的图像处理函数

任务：
1. 编写函数：调整图像亮度和对比度
2. 编写函数：图像灰度化
3. 编写函数：图像归一化（0-1范围）
4. 编写函数：添加高斯噪声

函数签名：
def adjust_brightness_contrast(image, brightness=0, contrast=1):
    # brightness: 亮度调整 (-100~100)
    # contrast: 对比度因子 (0.5~2.0)
    pass

def rgb_to_grayscale(image):
    # RGB转灰度
    pass

def normalize_image(image):
    # 归一化到[0,1]
    pass

def add_gaussian_noise(image, mean=0, sigma=25):
    # 添加高斯噪声
    pass
"""

def image_processing_practice():
    # 你的代码
    pass

# 运行
# image_processing_practice()

```

### 练习3：数据分析

```python
"""
练习3：数据分析

目标：使用Pandas分析模型性能

任务：
创建一个包含以下信息的DataFrame：
- 模型名称
- 准确率
- 参数量
- 训练时间
- 推理时间

然后：
1. 找出准确率最高的模型
2. 计算参数量的中位数
3. 筛选训练时间<10小时的模型
4. 按准确率排序并保存到CSV

提示：
- 使用 pd.DataFrame()
- 使用 .sort_values(), .describe()
- 使用 .to_csv()
"""

def data_analysis_practice():
    # 你的代码
    pass

# 运行
# data_analysis_practice()

```

### 练习4：可视化

```python
"""
练习4：可视化

目标：创建专业的可视化图表

任务：
1. 绘制训练损失和验证损失的折线图
2. 绘制不同模型的准确率对比柱状图
3. 绘制参数量 vs 准确率的散点图
4. 创建一个包含4个子图的综合图表

要求：
- 添加标题、标签、图例
- 使用不同颜色和样式
- 添加网格和标注
"""

def visualization_practice():
    # 你的代码
    pass

# 运行
# visualization_practice()

```

---

## 本章总结

### 核心知识点

#### Python基础

- ✅ **变量和类型**：理解不同数据类型
- ✅ **数据结构**：列表、元组、字典、集合
- ✅ **控制流**：if、for、while
- ✅ **函数**：定义、参数、lambda

#### NumPy

- ✅ **数组创建**：zeros, ones, arange, random
- ✅ **索引切片**：一维、二维、三维数组操作
- ✅ **数组运算**：元素级、矩阵级、聚合
- ✅ **数组变形**：reshape、拼接、分割

#### Pandas

- ✅ **DataFrame**：创建和查看数据
- ✅ **数据筛选**：条件查询和排序
- ✅ **数据处理**：缺失值、标准化、分组

#### Matplotlib

- ✅ **基础绘图**：折线图、散点图、柱状图
- ✅ **子图布局**：多图表组合
- ✅ **图像显示**：imshow、颜色映射

#### OpenCV

- ✅ **图像读写**：imread、imwrite
- ✅ **几何变换**：缩放、旋转、平移
- ✅ **颜色转换**：BGR、RGB、灰度、HSV
- ✅ **图像处理**：滤波、边缘检测

### 学习建议

1. **多写代码**：每个概念都要亲手实践
2. **查阅文档**：遇到不懂的函数，查看官方文档
3. **小项目驱动**：用实际问题练习
4. **调试技巧**：使用print和断点理解代码运行过程

### 下一步

- 完成所有练习题
- 尝试用本章知识处理真实图像
- 进入下一章：图像基础概念

---

*本章结束，建议练习时间：3-4小时*
