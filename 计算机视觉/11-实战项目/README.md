# 计算机视觉实战项目

> 4个完整的实战项目，从简单到复杂，涵盖目标检测、图像分割、人脸识别和视频分析。每个项目都包含完整的代码、数据准备、训练流程和部署方案。

## 📋 项目概览

| 项目 | 难度 | 核心技术 | 预计时间 | 应用场景 |
|------|------|----------|----------|----------|
| **项目1：人脸检测与识别系统** | ⭐⭐ | 目标检测 + 人脸识别 | 2-3天 | 智能门禁、考勤系统 |
| **项目2：智能目标检测器** | ⭐⭐⭐ | YOLOv8 + 数据标注 | 3-5天 | 安防监控、自动驾驶 |
| **项目3：医学图像分割** | ⭐⭐⭐ | U-Net + 医学影像 | 3-4天 | 病灶检测、辅助诊断 |
| **项目4：视频行为分析** | ⭐⭐⭐⭐ | 目标跟踪 + 动作识别 | 5-7天 | 智能监控、行为分析 |

---

## 🚀 项目1：人脸检测与识别系统

### 项目概述
构建一个完整的人脸检测与识别系统，支持实时摄像头检测和图片识别。

### 技术栈
- **人脸检测**：MTCNN / RetinaFace
- **人脸识别**：FaceNet / ArcFace
- **部署**：OpenCV + PyQt5

### 实现步骤

#### 1. 环境准备
```bash
pip install opencv-python
pip install torch torchvision
pip install facenet-pytorch  # 预训练模型
pip install mtcnn  # 人脸检测
pip install PyQt5  # GUI界面
```

#### 2. 人脸检测模块
```python
# face_detection.py
import cv2
import torch
from facenet_pytorch import MTCNN
import numpy as np

class FaceDetector:
    def __init__(self, device='cuda'):
        self.device = device
        self.mtcnn = MTCNN(keep_all=True, device=device)
    
    def detect_faces(self, image):
        """检测人脸并返回边界框"""
        boxes, _ = self.mtcnn.detect(image)
        return boxes
    
    def draw_boxes(self, image, boxes):
        """在图像上绘制人脸框"""
        if boxes is not None:
            for box in boxes:
                x1, y1, x2, y2 = box.astype(int)
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        return image
    
    def extract_faces(self, image, boxes, size=160):
        """提取人脸区域"""
        faces = []
        if boxes is not None:
            for box in boxes:
                x1, y1, x2, y2 = box.astype(int)
                face = image[y1:y2, x1:x2]
                if face.size > 0:
                    face = cv2.resize(face, (size, size))
                    faces.append(face)
        return faces

# 测试
if __name__ == '__main__':
    detector = FaceDetector()
    image = cv2.imread('test.jpg')
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    boxes = detector.detect_faces(image_rgb)
    result = detector.draw_boxes(image, boxes)
    
    cv2.imwrite('result.jpg', result)
    print(f"检测到 {len(boxes) if boxes is not None else 0} 张人脸")
```

#### 3. 人脸识别模块
```python
# face_recognition.py
import torch
from facenet_pytorch import InceptionResnetV1
import pickle
import os

class FaceRecognizer:
    def __init__(self, model_path=None, device='cuda'):
        self.device = device
        self.model = InceptionResnetV1(pretrained='vggface2').eval().to(device)
        
        # 加载已注册的人脸数据库
        self.database = {}
        if model_path and os.path.exists(model_path):
            self.load_database(model_path)
    
    def get_embedding(self, face_image):
        """提取人脸特征向量"""
        # 预处理
        face_tensor = torch.from_numpy(face_image).permute(2, 0, 1).float() / 255.0
        face_tensor = face_tensor.unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            embedding = self.model(face_tensor)
        
        return embedding.cpu().numpy()[0]
    
    def register_face(self, name, face_images):
        """注册新人脸"""
        embeddings = []
        for img in face_images:
            emb = self.get_embedding(img)
            embeddings.append(emb)
        
        # 平均嵌入
        avg_embedding = np.mean(embeddings, axis=0)
        self.database[name] = avg_embedding
        print(f"注册成功: {name}")
    
    def recognize_face(self, face_image, threshold=0.7):
        """识别人脸"""
        embedding = self.get_embedding(face_image)
        
        min_distance = float('inf')
        best_name = "Unknown"
        
        for name, db_embedding in self.database.items():
            distance = np.linalg.norm(embedding - db_embedding)
            if distance < min_distance:
                min_distance = distance
                best_name = name
        
        # 阈值判断
        if min_distance > threshold:
            return "Unknown", min_distance
        return best_name, min_distance
    
    def save_database(self, path):
        """保存人脸数据库"""
        with open(path, 'wb') as f:
            pickle.dump(self.database, f)
        print(f"数据库已保存: {path}")
    
    def load_database(self, path):
        """加载人脸数据库"""
        with open(path, 'rb') as f:
            self.database = pickle.load(f)
        print(f"数据库已加载: {path}, 包含 {len(self.database)} 人")

# 测试
if __name__ == '__main__':
    recognizer = FaceRecognizer()
    
    # 模拟注册
    # 读取多张同一个人的照片
    # face_imgs = [cv2.imread(f'person1_{i}.jpg') for i in range(5)]
    # recognizer.register_face('张三', face_imgs)
    
    # 识别
    # test_face = cv2.imread('test_face.jpg')
    # name, score = recognizer.recognize_face(test_face)
    # print(f"识别结果: {name}, 相似度: {score:.3f}")
```

#### 4. 完整系统（带GUI）
```python
# main_app.py
import sys
import cv2
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
from face_detection import FaceDetector
from face_recognition import FaceRecognizer

class FaceSystemApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
        # 初始化检测器和识别器
        self.detector = FaceDetector()
        self.recognizer = FaceRecognizer('face_db.pkl')
        
        # 摄像头
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        
        self.is_running = False
    
    def initUI(self):
        self.setWindowTitle('人脸检测与识别系统')
        self.setGeometry(100, 100, 800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 视频显示
        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setMinimumSize(640, 480)
        layout.addWidget(self.video_label)
        
        # 控制按钮
        btn_layout = QHBoxLayout()
        
        self.start_btn = QPushButton('开始检测')
        self.start_btn.clicked.connect(self.toggle_detection)
        btn_layout.addWidget(self.start_btn)
        
        self.register_btn = QPushButton('注册人脸')
        self.register_btn.clicked.connect(self.register_face)
        btn_layout.addWidget(self.register_btn)
        
        self.save_btn = QPushButton('保存数据库')
        self.save_btn.clicked.connect(self.save_database)
        btn_layout.addWidget(self.save_btn)
        
        layout.addLayout(btn_layout)
        
        # 状态显示
        self.status_label = QLabel('状态: 准备就绪')
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
    
    def toggle_detection(self):
        if not self.is_running:
            self.is_running = True
            self.timer.start(30)
            self.start_btn.setText('停止检测')
            self.status_label.setText('状态: 正在检测...')
        else:
            self.is_running = False
            self.timer.stop()
            self.start_btn.setText('开始检测')
            self.status_label.setText('状态: 已停止')
    
    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return
        
        # 转换为RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # 检测人脸
        boxes = self.detector.detect_faces(frame_rgb)
        
        # 绘制框和识别
        if boxes is not None:
            for box in boxes:
                x1, y1, x2, y2 = box.astype(int)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # 提取人脸并识别
                face = frame_rgb[y1:y2, x1:x2]
                if face.size > 0:
                    name, score = self.recognizer.recognize_face(face)
                    
                    # 显示结果
                    text = f"{name} ({score:.2f})"
                    cv2.putText(frame, text, (x1, y1-10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # 显示
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(q_img))
    
    def register_face(self):
        """注册人脸对话框"""
        from PyQt5.QtWidgets import QInputDialog
        
        name, ok = QInputDialog.getText(self, '注册人脸', '请输入姓名:')
        if ok and name:
            # 捕捉5张照片
            self.status_label.setText(f'正在注册 {name}，请保持面部对准摄像头...')
            faces = []
            
            def capture_faces():
                for i in range(5):
                    ret, frame = self.cap.read()
                    if ret:
                        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        boxes = self.detector.detect_faces(frame_rgb)
                        if boxes is not None and len(boxes) == 1:
                            face = self.detector.extract_faces(frame_rgb, boxes)[0]
                            faces.append(face)
                            self.status_label.setText(f'采集进度: {i+1}/5')
                            import time
                            time.sleep(0.5)
                
                if len(faces) == 5:
                    self.recognizer.register_face(name, faces)
                    self.status_label.setText(f'注册成功: {name}')
                else:
                    self.status_label.setText('注册失败，请重试')
            
            threading.Thread(target=capture_faces, daemon=True).start()
    
    def save_database(self):
        """保存数据库"""
        self.recognizer.save_database('face_db.pkl')
        self.status_label.setText('数据库已保存')
    
    def closeEvent(self, event):
        """关闭窗口"""
        if self.cap.isOpened():
            self.cap.release()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FaceSystemApp()
    window.show()
    sys.exit(app.exec_())
```

### 项目扩展
- [ ] 添加活体检测（防止照片攻击）
- [ ] 支持批量注册
- [ ] 添加考勤记录功能
- [ ] Web API接口
- [ ] 云端部署

---

## 🎯 项目2：智能目标检测器

### 项目概述
使用YOLOv8训练自定义目标检测器，支持数据标注、模型训练、评估和部署。

### 技术栈
- **检测框架**：YOLOv8 (Ultralytics)
- **数据标注**：LabelImg / CVAT
- **部署**：ONNX / TensorRT

### 实现步骤

#### 1. 数据准备与标注
```python
# prepare_data.py
import os
import shutil
import random
from pathlib import Path

def prepare_yolo_dataset(raw_data_dir, output_dir):
    """
    准备YOLO格式数据集
    目录结构:
    raw_data_dir/
    ├── images/
    │   ├── img1.jpg
    │   └── img2.jpg
    └── labels/
        ├── img1.txt
        └── img2.txt
    """
    
    # 创建输出目录
    for split in ['train', 'val']:
        Path(f"{output_dir}/{split}/images").mkdir(parents=True, exist_ok=True)
        Path(f"{output_dir}/{split}/labels").mkdir(parents=True, exist_ok=True)
    
    # 获取所有图像
    images = list(Path(f"{raw_data_dir}/images").glob("*.jpg"))
    random.shuffle(images)
    
    # 划分数据集
    split_idx = int(len(images) * 0.8)
    train_images = images[:split_idx]
    val_images = images[split_idx:]
    
    def copy_files(image_list, split):
        for img_path in image_list:
            # 复制图像
            shutil.copy(img_path, f"{output_dir}/{split}/images/")
            
            # 复制标注
            label_path = f"{raw_data_dir}/labels/{img_path.stem}.txt"
            if os.path.exists(label_path):
                shutil.copy(label_path, f"{output_dir}/{split}/labels/")
    
    copy_files(train_images, 'train')
    copy_files(val_images, 'val')
    
    print(f"数据集准备完成:")
    print(f"训练集: {len(train_images)} 张")
    print(f"验证集: {len(val_images)} 张")

# 创建数据集配置文件
def create_dataset_yaml(output_dir, class_names):
    """创建YOLO数据集配置"""
    yaml_content = f"""
path: {os.path.abspath(output_dir)}
train: train/images
val: val/images

nc: {len(class_names)}
names: {class_names}
"""
    
    with open(f"{output_dir}/data.yaml", 'w') as f:
        f.write(yaml_content)
    
    print(f"数据集配置已创建: {output_dir}/data.yaml")

# 使用示例
if __name__ == '__main__':
    prepare_yolo_dataset('./raw_data', './dataset')
    create_dataset_yaml('./dataset', ['person', 'car', 'dog'])
```

#### 2. 模型训练
```python
# train_detector.py
from ultralytics import YOLO
import yaml

def train_custom_model():
    """训练自定义检测器"""
    
    # 加载预训练模型
    model = YOLO('yolov8n.pt')  # nano版本，速度快
    
    # 训练配置
    results = model.train(
        data='./dataset/data.yaml',
        epochs=100,
        imgsz=640,
        batch=16,
        device='cuda' if torch.cuda.is_available() else 'cpu',
        workers=4,
        
        # 优化参数
        optimizer='SGD',
        lr0=0.01,
        lrf=0.01,
        momentum=0.937,
        weight_decay=0.0005,
        
        # 损失权重
        box=7.5,
        cls=0.5,
        dfl=1.5,
        
        # 数据增强
        hsv_h=0.015,
        hsv_s=0.7,
        hsv_v=0.4,
        degrees=15,
        translate=0.1,
        scale=0.5,
        shear=0.0,
        perspective=0.0,
        flipud=0.0,
        fliplr=0.5,
        mosaic=1.0,
        mixup=0.0,
        
        # 保存
        save=True,
        save_period=10,
        project='runs/train',
        name='custom_detector',
        
        # 验证
        val=True,
        plots=True,
    )
    
    return model, results

def evaluate_model(model_path, data_yaml):
    """评估模型性能"""
    model = YOLO(model_path)
    
    # 验证
    metrics = model.val(data=data_yaml)
    
    print(f"mAP@0.5: {metrics.box.map50:.3f}")
    print(f"mAP@0.5:0.95: {metrics.box.map:.3f}")
    print(f"精确率: {metrics.box.mp:.3f}")
    print(f"召回率: {metrics.box.mr:.3f}")
    
    return metrics

def predict_image(model_path, image_path, conf=0.5):
    """预测单张图像"""
    model = YOLO(model_path)
    results = model(image_path, conf=conf)
    
    # 保存结果
    results[0].save('prediction.jpg')
    
    # 获取检测信息
    boxes = results[0].boxes.xyxy.cpu().numpy()
    scores = results[0].boxes.conf.cpu().numpy()
    classes = results[0].boxes.cls.cpu().numpy().astype(int)
    
    return boxes, scores, classes

# 使用示例
if __name__ == '__main__':
    # 训练
    model, results = train_custom_model()
    
    # 评估
    evaluate_model('runs/train/custom_detector/weights/best.pt', './dataset/data.yaml')
    
    # 预测
    boxes, scores, classes = predict_image(
        'runs/train/custom_detector/weights/best.pt',
        'test.jpg'
    )
    
    print(f"检测到 {len(boxes)} 个物体")
```

#### 3. 模型部署
```python
# deploy.py
from ultralytics import YOLO
import torch
import onnx
import tensorrt as trt

def export_to_onnx(model_path, output_path):
    """导出为ONNX格式"""
    model = YOLO(model_path)
    model.export(format='onnx', imgsz=640, opset=12)
    
    # 验证ONNX模型
    onnx_model = onnx.load(output_path)
    onnx.checker.check_model(onnx_model)
    print(f"ONNX模型已导出: {output_path}")

def export_to_tensorrt(onnx_path, trt_path):
    """导出为TensorRT格式"""
    logger = trt.Logger(trt.Logger.WARNING)
    builder = trt.Builder(logger)
    config = builder.create_builder_config()
    config.set_memory_pool_limit(trt.MemoryPoolType.WORKSPACE, 1 << 30)  # 1GB
    
    # 启用FP16
    config.set_flag(trt.BuilderFlag.FP16)
    
    # 创建网络
    network = builder.create_network(1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH))
    parser = trt.OnnxParser(network, logger)
    
    # 解析ONNX
    with open(onnx_path, 'rb') as f:
        parser.parse(f.read())
    
    # 构建引擎
    engine = builder.build_engine(network, config)
    
    # 保存
    with open(trt_path, 'wb') as f:
        f.write(engine.serialize())
    
    print(f"TensorRT引擎已导出: {trt_path}")

class TRTDetector:
    """TensorRT推理器"""
    
    def __init__(self, engine_path):
        self.logger = trt.Logger(trt.Logger.WARNING)
        self.runtime = trt.Runtime(self.logger)
        
        with open(engine_path, 'rb') as f:
            self.engine = self.runtime.deserialize_cuda_engine(f.read())
        
        self.context = self.engine.create_execution_context()
        
        # 分配内存
        self.inputs, self.outputs, self.bindings, self.stream = self._allocate_buffers()
    
    def _allocate_buffers(self):
        inputs = []
        outputs = []
        bindings = []
        stream = torch.cuda.Stream()
        
        for binding in self.engine:
            shape = self.engine.get_binding_shape(binding)
            dtype = trt.nptype(self.engine.get_binding_dtype(binding))
            
            # 分配GPU内存
            device_mem = torch.empty(np.prod(shape), dtype=torch.from_numpy(dtype)).cuda()
            bindings.append(int(device_mem.data_ptr()))
            
            if self.engine.binding_is_input(binding):
                inputs.append({'host': None, 'device': device_mem, 'shape': shape})
            else:
                outputs.append({'host': None, 'device': device_mem, 'shape': shape})
        
        return inputs, outputs, bindings, stream
    
    def infer(self, image):
        """推理"""
        # 预处理
        input_tensor = self._preprocess(image)
        
        # 复制到GPU
        torch.cudaMemcpyAsync(
            self.inputs[0]['device'].data_ptr(),
            input_tensor.data_ptr(),
            input_tensor.numel() * input_tensor.element_size(),
            self.stream
        )
        
        # 推理
        self.context.execute_async_v2(
            bindings=self.bindings,
            stream_handle=self.stream.cuda_stream
        )
        
        # 同步
        self.stream.synchronize()
        
        # 获取结果
        output = self.outputs[0]['device'].cpu().numpy()
        
        return self._postprocess(output)
    
    def _preprocess(self, image):
        """图像预处理"""
        # 调整大小、归一化、转tensor
        pass
    
    def _postprocess(self, output):
        """结果后处理"""
        # NMS、坐标转换
        pass

# 使用示例
if __name__ == '__main__':
    # 导出ONNX
    export_to_onnx('best.pt', 'best.onnx')
    
    # 导出TensorRT
    export_to_tensorrt('best.onnx', 'best.trt')
    
    # 使用TensorRT推理
    detector = TRTDetector('best.trt')
    results = detector.infer('test.jpg')
```

#### 4. Web API接口
```python
# api_server.py
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
import io

app = FastAPI(title="目标检测API")
model = None

@app.on_event("startup")
async def load_model():
    """加载模型"""
    global model
    model = YOLO('best.pt')
    print("模型加载完成")

@app.post("/detect")
async def detect_objects(file: UploadFile = File(...)):
    """检测接口"""
    contents = await file.read()
    
    # 转换为图像
    image = Image.open(io.BytesIO(contents))
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # 检测
    results = model(image)
    
    # 解析结果
    detections = []
    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()
        scores = result.boxes.conf.cpu().numpy()
        classes = result.boxes.cls.cpu().numpy().astype(int)
        
        for box, score, cls in zip(boxes, scores, classes):
            detections.append({
                'class': model.names[int(cls)],
                'confidence': float(score),
                'bbox': box.tolist()
            })
    
    return JSONResponse(content={
        "detections": detections,
        "count": len(detections)
    })

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": model is not None}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 项目扩展
- [ ] 实时视频检测
- [ ] 多模型集成
- [ ] 异常检测
- [ ] 跟踪功能
- [ ] Web界面

---

## 🏥 项目3：医学图像分割

### 项目概述
使用U-Net进行医学图像分割，支持医学图像预处理、模型训练和结果可视化。

### 技术栈
- **网络架构**：U-Net / U-Net++
- **医学图像库**：SimpleITK, pydicom
- **数据增强**：Albumentations

### 实现步骤

#### 1. 医学图像处理
```python
# medical_utils.py
import SimpleITK as sitk
import pydicom
import numpy as np
import cv2

class MedicalImageProcessor:
    """医学图像处理器"""
    
    @staticmethod
    def load_dicom_series(dicom_dir):
        """加载DICOM序列"""
        reader = sitk.ImageSeriesReader()
        reader.SetDirectory(dicom_dir)
        dicom_names = reader.GetFileNames()
        reader.SetFileNames(dicom_names)
        image = reader.Execute()
        return image
    
    @staticmethod
    def load_nii(nii_path):
        """加载NIfTI格式"""
        image = sitk.ReadImage(nii_path)
        return image
    
    @staticmethod
    def normalize_hu(image):
        """CT值归一化（HU单位）"""
        array = sitk.GetArrayFromImage(image)
        
        # 窗宽窗位调整
        array = np.clip(array, -1000, 1000)
        array = (array + 1000) / 2000.0
        
        return array
    
    @staticmethod
    def window_image(image, window_center, window_width):
        """窗口化处理"""
        array = sitk.GetArrayFromImage(image)
        min_val = window_center - window_width / 2
        max_val = window_center + window_width / 2
        
        array = np.clip(array, min_val, max_val)
        array = (array - min_val) / (max_val - min_val) * 255
        
        return array.astype(np.uint8)
    
    @staticmethod
    def resample_image(image, new_spacing=(1.0, 1.0, 1.0)):
        """重采样到统一间距"""
        original_spacing = image.GetSpacing()
        original_size = image.GetSize()
        
        new_size = [
            int(original_size[0] * original_spacing[0] / new_spacing[0]),
            int(original_size[1] * original_spacing[1] / new_spacing[1]),
            int(original_size[2] * original_spacing[2] / new_spacing[2])
        ]
        
        resample = sitk.ResampleImageFilter()
        resample.SetOutputSpacing(new_spacing)
        resample.SetSize(new_size)
        resample.SetOutputDirection(image.GetDirection())
        resample.SetOutputOrigin(image.GetOrigin())
        resample.SetTransform(sitk.Transform())
        resample.SetInterpolator(sitk.sitkLinear)
        
        return resample.Execute(image)

# 使用示例
if __name__ == '__main__':
    processor = MedicalImageProcessor()
    
    # 加载CT图像
    ct_image = processor.load_dicom_series('./ct_scan/')
    
    # 归一化
    ct_array = processor.normalize_hu(ct_image)
    
    # 窗宽窗位
    lung_window = processor.window_image(ct_image, -600, 1500)
    
    print(f"图像形状: {ct_array.shape}")
    print(f"值范围: [{ct_array.min():.3f}, {ct_array.max():.3f}]")
```

#### 2. U-Net模型训练
```python
# train_medical.py
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import numpy as np
import os
from medical_utils import MedicalImageProcessor
import albumentations as A
from albumentations.pytorch import ToTensorV2

class MedicalSegmentationDataset(Dataset):
    """医学图像分割数据集"""
    
    def __init__(self, image_dir, mask_dir, transform=None):
        self.image_dir = image_dir
        self.mask_dir = mask_dir
        self.transform = transform
        
        self.image_files = sorted(os.listdir(image_dir))
        self.mask_files = sorted(os.listdir(mask_dir))
    
    def __len__(self):
        return len(self.image_files)
    
    def __getitem__(self, idx):
        # 加载图像和掩码
        img_path = os.path.join(self.image_dir, self.image_files[idx])
        mask_path = os.path.join(self.mask_dir, self.mask_files[idx])
        
        image = np.load(img_path)
        mask = np.load(mask_path)
        
        # 确保是单通道
        if len(image.shape) == 3:
            image = image[0]  # 取第一个slice
        
        # 扩展通道维度
        image = np.expand_dims(image, axis=0)
        mask = np.expand_dims(mask, axis=0)
        
        # 应用变换
        if self.transform:
            augmented = self.transform(image=image.transpose(1, 2, 0), mask=mask.transpose(1, 2, 0))
            image = augmented['image']
            mask = augmented['mask']
        
        return image, mask

class UNet(nn.Module):
    """U-Net实现"""
    
    def __init__(self, in_channels=1, out_channels=1, init_features=64):
        super(UNet, self).__init__()
        
        features = init_features
        
        # 编码器
        self.enc1 = self._block(in_channels, features, name='enc1')
        self.pool1 = nn.MaxPool2d(2)
        self.enc2 = self._block(features, features * 2, name='enc2')
        self.pool2 = nn.MaxPool2d(2)
        self.enc3 = self._block(features * 2, features * 4, name='enc3')
        self.pool3 = nn.MaxPool2d(2)
        self.enc4 = self._block(features * 4, features * 8, name='enc4')
        self.pool4 = nn.MaxPool2d(2)
        
        # 瓶颈
        self.bottleneck = self._block(features * 8, features * 16, name='bottleneck')
        
        # 解码器
        self.upconv4 = nn.ConvTranspose2d(features * 16, features * 8, 2, stride=2)
        self.dec4 = self._block(features * 16, features * 8, name='dec4')
        
        self.upconv3 = nn.ConvTranspose2d(features * 8, features * 4, 2, stride=2)
        self.dec3 = self._block(features * 8, features * 4, name='dec3')
        
        self.upconv2 = nn.ConvTranspose2d(features * 4, features * 2, 2, stride=2)
        self.dec2 = self._block(features * 4, features * 2, name='dec2')
        
        self.upconv1 = nn.ConvTranspose2d(features * 2, features, 2, stride=2)
        self.dec1 = self._block(features * 2, features, name='dec1')
        
        # 输出
        self.conv_out = nn.Conv2d(features, out_channels, 1)
        self.sigmoid = nn.Sigmoid()
    
    def _block(self, in_channels, out_channels, name):
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
        enc1 = self.enc1(x)
        enc2 = self.enc2(self.pool1(enc1))
        enc3 = self.enc3(self.pool2(enc2))
        enc4 = self.enc4(self.pool3(enc3))
        
        # 瓶颈
        bottleneck = self.bottleneck(self.pool4(enc4))
        
        # 解码 + 跳跃连接
        dec4 = self.upconv4(bottleneck)
        dec4 = torch.cat([enc4, dec4], dim=1)
        dec4 = self.dec4(dec4)
        
        dec3 = self.upconv3(dec4)
        dec3 = torch.cat([enc3, dec3], dim=1)
        dec3 = self.dec3(dec3)
        
        dec2 = self.upconv2(dec3)
        dec2 = torch.cat([enc2, dec2], dim=1)
        dec2 = self.dec2(dec2)
        
        dec1 = self.upconv1(dec2)
        dec1 = torch.cat([enc1, dec1], dim=1)
        dec1 = self.dec1(dec1)
        
        # 输出
        output = self.conv_out(dec1)
        output = self.sigmoid(output)
        
        return output

class DiceLoss(nn.Module):
    """Dice损失函数"""
    
    def __init__(self, smooth=1e-6):
        super(DiceLoss, self).__init__()
        self.smooth = smooth
    
    def forward(self, pred, target):
        pred = pred.contiguous().view(-1)
        target = target.contiguous().view(-1)
        
        intersection = (pred * target).sum()
        dice = (2. * intersection + self.smooth) / (pred.sum() + target.sum() + self.smooth)
        
        return 1 - dice

def train_medical_segmentation():
    """训练医学图像分割模型"""
    
    # 数据增强
    train_transform = A.Compose([
        A.Resize(256, 256),
        A.HorizontalFlip(p=0.5),
        A.VerticalFlip(p=0.3),
        A.RandomRotate90(p=0.5),
        A.ElasticTransform(p=0.3, alpha=120, sigma=120 * 0.05, alpha_affine=120 * 0.03),
        A.Normalize(mean=[0.5], std=[0.5]),
        ToTensorV2(),
    ])
    
    val_transform = A.Compose([
        A.Resize(256, 256),
        A.Normalize(mean=[0.5], std=[0.5]),
        ToTensorV2(),
    ])
    
    # 数据集
    train_dataset = MedicalSegmentationDataset(
        './data/train/images',
        './data/train/masks',
        transform=train_transform
    )
    
    val_dataset = MedicalSegmentationDataset(
        './data/val/images',
        './data/val/masks',
        transform=val_transform
    )
    
    train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True, num_workers=4)
    val_loader = DataLoader(val_dataset, batch_size=8, shuffle=False, num_workers=4)
    
    # 模型
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = UNet(in_channels=1, out_channels=1).to(device)
    
    # 损失和优化器
    criterion = DiceLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', patience=5)
    
    # 训练循环
    best_dice = 0
    
    for epoch in range(100):
        # 训练
        model.train()
        train_loss = 0
        
        for images, masks in train_loader:
            images, masks = images.to(device), masks.to(device)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, masks)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
        
        # 验证
        model.eval()
        val_dice = 0
        
        with torch.no_grad():
            for images, masks in val_loader:
                images, masks = images.to(device), masks.to(device)
                outputs = model(images)
                
                # 计算Dice
                pred = (outputs > 0.5).float()
                intersection = (pred * masks).sum()
                dice = (2. * intersection) / (pred.sum() + masks.sum() + 1e-6)
                val_dice += dice.item()
        
        avg_train_loss = train_loss / len(train_loader)
        avg_val_dice = val_dice / len(val_loader)
        
        scheduler.step(avg_train_loss)
        
        print(f'Epoch {epoch+1}: Train Loss={avg_train_loss:.4f}, Val Dice={avg_val_dice:.4f}')
        
        # 保存最佳模型
        if avg_val_dice > best_dice:
            best_dice = avg_val_dice
            torch.save(model.state_dict(), 'best_medical_unet.pth')
            print(f'保存最佳模型，Dice={best_dice:.4f}')

# 使用示例
if __name__ == '__main__':
    train_medical_segmentation()
```

#### 3. 结果可视化与评估
```python
# visualize_medical.py
import matplotlib.pyplot as plt
import numpy as np
import torch
from medical_utils import MedicalImageProcessor

def visualize_segmentation_results(image, mask_true, mask_pred, save_path=None):
    """可视化分割结果"""
    fig, axes = plt.subplots(1, 4, figsize=(16, 4))
    
    # 原始图像
    axes[0].imshow(image, cmap='gray')
    axes[0].set_title('原始图像')
    axes[0].axis('off')
    
    # 真实掩码
    axes[1].imshow(mask_true, cmap='jet')
    axes[1].set_title('真实分割')
    axes[1].axis('off')
    
    # 预测掩码
    axes[2].imshow(mask_pred, cmap='jet')
    axes[2].set_title('预测分割')
    axes[2].axis('off')
    
    # 差异
    diff = np.abs(mask_true - mask_pred)
    axes[3].imshow(diff, cmap='hot')
    axes[3].set_title('差异')
    axes[3].axis('off')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    else:
        plt.show()

def calculate_metrics(mask_true, mask_pred):
    """计算分割指标"""
    mask_true = mask_true.flatten()
    mask_pred = mask_pred.flatten()
    
    # Dice系数
    intersection = np.sum(mask_true * mask_pred)
    dice = (2. * intersection) / (np.sum(mask_true) + np.sum(mask_pred) + 1e-6)
    
    # IoU
    union = np.sum(mask_true) + np.sum(mask_pred) - intersection
    iou = intersection / (union + 1e-6)
    
    # 精确率和召回率
    tp = np.sum((mask_true == 1) & (mask_pred == 1))
    fp = np.sum((mask_true == 0) & (mask_pred == 1))
    fn = np.sum((mask_true == 1) & (mask_pred == 0))
    
    precision = tp / (tp + fp + 1e-6)
    recall = tp / (tp + fn + 1e-6)
    
    return {
        'Dice': dice,
        'IoU': iou,
        'Precision': precision,
        'Recall': recall
    }

def predict_medical_image(model_path, image_path):
    """预测单张医学图像"""
    # 加载模型
    model = UNet(in_channels=1, out_channels=1)
    model.load_state_dict(torch.load(model_path, map_location='cpu'))
    model.eval()
    
    # 加载图像
    processor = MedicalImageProcessor()
    image = processor.load_nii(image_path)
    image_array = processor.normalize_hu(image)
    
    # 预测
    with torch.no_grad():
        input_tensor = torch.from_numpy(image_array).float().unsqueeze(0).unsqueeze(0)
        output = model(input_tensor)
        pred_mask = (output > 0.5).float().numpy()[0, 0]
    
    return image_array[0], pred_mask

# 使用示例
if __name__ == '__main__':
    # 预测
    image, pred_mask = predict_medical_image('best_medical_unet.pth', 'test_scan.nii.gz')
    
    # 假设有真实掩码
    true_mask = np.load('true_mask.npy')
    
    # 计算指标
    metrics = calculate_metrics(true_mask, pred_mask)
    print("分割指标:", metrics)
    
    # 可视化
    visualize_segmentation_results(image, true_mask, pred_mask, 'result.png')
```

### 项目扩展
- [ ] 3D U-Net处理体积数据
- [ ] 多模态融合（CT + MRI）
- [ ] 主动学习减少标注
- [ ] 模型解释性（Grad-CAM）
- [ ] DICOM Web集成

---

## 🎬 项目4：视频行为分析系统

### 项目概述
构建视频分析系统，支持目标跟踪、动作识别和异常检测。

### 技术栈
- **目标跟踪**：ByteTrack / DeepSORT
- **动作识别**：SlowFast / I3D
- **视频处理**：FFmpeg, OpenCV

### 实现步骤

#### 1. 视频处理与目标跟踪
```python
# video_tracker.py
import cv2
import numpy as np
from ultralytics import YOLO
from collections import deque

class ObjectTracker:
    """目标跟踪器"""
    
    def __init__(self, model_path='yolov8n.pt', max_tracklets=50):
        self.detector = YOLO(model_path)
        self.tracklets = {}  # 跟踪轨迹
        self.max_tracklets = max_tracklets
        self.next_id = 0
    
    def update(self, frame):
        """更新跟踪"""
        # 检测
        results = self.detector(frame, verbose=False)
        
        # 提取检测框
        detections = []
        for result in results:
            boxes = result.boxes.xyxy.cpu().numpy()
            scores = result.boxes.conf.cpu().numpy()
            classes = result.boxes.cls.cpu().numpy()
            
            for box, score, cls in zip(boxes, scores, classes):
                if score > 0.5:  # 置信度阈值
                    detections.append({
                        'bbox': box,
                        'score': score,
                        'class': int(cls),
                        'center': ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)
                    })
        
        # 简单的跟踪逻辑（实际使用ByteTrack或DeepSORT）
        self._match_tracklets(detections)
        
        return self.tracklets
    
    def _match_tracklets(self, detections):
        """匹配跟踪轨迹"""
        # 计算距离矩阵
        if len(self.tracklets) == 0:
            # 新建轨迹
            for det in detections:
                self.tracklets[self.next_id] = {
                    'bbox': det['bbox'],
                    'center': det['center'],
                    'history': deque([det['center']], maxlen=20),
                    'class': det['class'],
                    'score': det['score']
                }
                self.next_id += 1
            return
        
        # 简单的最近邻匹配
        used = set()
        for track_id, track in list(self.tracklets.items()):
            if track_id in used:
                continue
            
            min_dist = float('inf')
            best_det = None
            
            for det in detections:
                if det['class'] != track['class']:
                    continue
                
                dist = np.linalg.norm(
                    np.array(track['center']) - np.array(det['center'])
                )
                
                if dist < min_dist and dist < 50:  # 距离阈值
                    min_dist = dist
                    best_det = det
            
            if best_det:
                # 更新轨迹
                track['bbox'] = best_det['bbox']
                track['center'] = best_det['center']
                track['history'].append(best_det['center'])
                track['score'] = best_det['score']
                used.add(track_id)
                detections.remove(best_det)
        
        # 删除未匹配的轨迹
        self.tracklets = {k: v for k, v in self.tracklets.items() if k in used}
        
        # 添加新轨迹
        for det in detections:
            if len(self.tracklets) < self.max_tracklets:
                self.tracklets[self.next_id] = {
                    'bbox': det['bbox'],
                    'center': det['center'],
                    'history': deque([det['center']], maxlen=20),
                    'class': det['class'],
                    'score': det['score']
                }
                self.next_id += 1
    
    def draw_tracks(self, frame):
        """绘制跟踪结果"""
        for track_id, track in self.tracklets.items():
            # 绘制轨迹
            if len(track['history']) > 1:
                points = np.array(track['history'], dtype=np.int32)
                cv2.polylines(frame, [points], False, (0, 255, 255), 2)
            
            # 绘制框
            bbox = track['bbox'].astype(int)
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
            
            # 绘制ID
            cv2.putText(frame, f"ID:{track_id}", (bbox[0], bbox[1]-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        return frame

# 使用示例
if __name__ == '__main__':
    tracker = ObjectTracker()
    cap = cv2.VideoCapture('video.mp4')
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        tracks = tracker.update(frame)
        frame = tracker.draw_tracks(frame)
        
        cv2.imshow('Tracking', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
```

#### 2. 动作识别
```python
# action_recognition.py
import torch
import torch.nn as nn
from torchvision import models
import cv2
import numpy as np

class ActionRecognizer:
    """动作识别器"""
    
    def __init__(self, num_classes=10, model_type='slowfast'):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.num_classes = num_classes
        
        if model_type == 'slowfast':
            # 使用预训练的SlowFast
            self.model = self._build_slowfast()
        else:
            # 使用3D CNN
            self.model = self._build_3dcnn()
        
        self.model.to(self.device)
        self.model.eval()
        
        # 动作类别
        self.classes = ['Walking', 'Running', 'Sitting', 'Standing', 'Jumping',
                       'Falling', 'Waving', 'Eating', 'Drinking', 'Other']
    
    def _build_slowfast(self):
        """构建SlowFast网络（简化版）"""
        # 实际使用时可以使用torchvideo或自定义实现
        # 这里使用3D ResNet作为替代
        model = models.video.r3d_18(pretrained=True)
        model.fc = nn.Linear(model.fc.in_features, self.num_classes)
        return model
    
    def _build_3dcnn(self):
        """构建简单3D CNN"""
        class Simple3DCNN(nn.Module):
            def __init__(self, num_classes):
                super().__init__()
                self.conv1 = nn.Conv3d(3, 64, kernel_size=(3, 7, 7), stride=(1, 2, 2), padding=(1, 3, 3))
                self.pool1 = nn.MaxPool3d(kernel_size=(1, 3, 3), stride=(1, 2, 2), padding=(0, 1, 1))
                
                self.conv2 = nn.Conv3d(64, 128, kernel_size=3, stride=1, padding=1)
                self.pool2 = nn.MaxPool3d(kernel_size=2, stride=2)
                
                self.global_pool = nn.AdaptiveAvgPool3d(1)
                self.fc = nn.Linear(128, num_classes)
            
            def forward(self, x):
                x = torch.relu(self.conv1(x))
                x = self.pool1(x)
                x = torch.relu(self.conv2(x))
                x = self.pool2(x)
                x = self.global_pool(x)
                x = x.view(x.size(0), -1)
                x = self.fc(x)
                return x
        
        return Simple3DCNN(num_classes)
    
    def extract_frames(self, video_path, num_frames=16):
        """从视频中提取帧"""
        cap = cv2.VideoCapture(video_path)
        frames = []
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_indices = np.linspace(0, total_frames-1, num_frames, dtype=int)
        
        for idx in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            if ret:
                frame = cv2.resize(frame, (224, 224))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(frame)
        
        cap.release()
        
        # 如果不够，重复最后一帧
        while len(frames) < num_frames:
            frames.append(frames[-1])
        
        return np.array(frames)  # (T, H, W, C)
    
    def preprocess(self, frames):
        """预处理"""
        # 转换为tensor (T, C, H, W)
        frames = frames.astype(np.float32) / 255.0
        frames = torch.from_numpy(frames).permute(0, 3, 1, 2)
        
        # 标准化
        mean = torch.tensor([0.4321, 0.4202, 0.3928]).view(1, 3, 1, 1)
        std = torch.tensor([0.2280, 0.2214, 0.2169]).view(1, 3, 1, 1)
        frames = (frames - mean) / std
        
        # 添加batch维度 (B, C, T, H, W)
        frames = frames.permute(1, 0, 2, 3).unsqueeze(0)
        
        return frames
    
    def recognize(self, video_path):
        """识别视频中的动作"""
        # 提取帧
        frames = self.extract_frames(video_path)
        
        # 预处理
        input_tensor = self.preprocess(frames).to(self.device)
        
        # 预测
        with torch.no_grad():
            output = self.model(input_tensor)
            probabilities = torch.softmax(output, dim=1)
            pred_class = torch.argmax(probabilities, dim=1).item()
            confidence = probabilities[0, pred_class].item()
        
        return self.classes[pred_class], confidence

# 使用示例
if __name__ == '__main__':
    recognizer = ActionRecognizer(num_classes=10)
    
    # 识别
    action, confidence = recognizer.recognize('action_video.mp4')
    print(f"检测到动作: {action}, 置信度: {confidence:.3f}")
```

#### 3. 异常检测
```python
# anomaly_detection.py
import numpy as np
from sklearn.ensemble import IsolationForest
import cv2

class AnomalyDetector:
    """基于统计的异常检测"""
    
    def __init__(self, contamination=0.1):
        self.contamination = contamination
        self.model = IsolationForest(contamination=contamination, random_state=42)
        self.is_fitted = False
        self.normal_features = []
    
    def extract_features(self, tracks):
        """从跟踪结果中提取特征"""
        features = []
        
        for track_id, track in tracks.items():
            # 特征1: 速度
            if len(track['history']) >= 2:
                dx = track['history'][-1][0] - track['history'][-2][0]
                dy = track['history'][-1][1] - track['history'][-2][1]
                speed = np.sqrt(dx**2 + dy**2)
            else:
                speed = 0
            
            # 特征2: 轨迹长度
            traj_len = len(track['history'])
            
            # 特征3: 置信度
            score = track['score']
            
            # 特征4: 运动方向变化（简化）
            if len(track['history']) >= 3:
                v1 = np.array(track['history'][-2]) - np.array(track['history'][-3])
                v2 = np.array(track['history'][-1]) - np.array(track['history'][-2])
                if np.linalg.norm(v1) > 0 and np.linalg.norm(v2) > 0:
                    angle = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
                else:
                    angle = 0
            else:
                angle = 0
            
            features.append([speed, traj_len, score, angle])
        
        return np.array(features)
    
    def fit(self, normal_data):
        """训练正常模型"""
        all_features = []
        
        for tracks in normal_data:
            features = self.extract_features(tracks)
            if len(features) > 0:
                all_features.extend(features)
        
        if len(all_features) > 0:
            self.model.fit(all_features)
            self.is_fitted = True
            print(f"模型训练完成，样本数: {len(all_features)}")
    
    def detect(self, tracks):
        """检测异常"""
        if not self.is_fitted:
            return []
        
        features = self.extract_features(tracks)
        if len(features) == 0:
            return []
        
        predictions = self.model.predict(features)
        anomalies = []
        
        for idx, pred in enumerate(predictions):
            if pred == -1:  # 异常
                track_id = list(tracks.keys())[idx]
                anomalies.append(track_id)
        
        return anomalies
    
    def visualize_anomalies(self, frame, tracks, anomalies):
        """可视化异常"""
        for track_id, track in tracks.items():
            bbox = track['bbox'].astype(int)
            
            if track_id in anomalies:
                # 异常：红色
                color = (0, 0, 255)
                label = f"Anomaly ID:{track_id}"
            else:
                # 正常：绿色
                color = (0, 255, 0)
                label = f"ID:{track_id}"
            
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)
            cv2.putText(frame, label, (bbox[0], bbox[1]-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        return frame

# 使用示例
if __name__ == '__main__':
    # 1. 收集正常数据
    normal_data = []
    # 在正常视频上运行跟踪器，收集tracks
    
    # 2. 训练模型
    detector = AnomalyDetector()
    detector.fit(normal_data)
    
    # 3. 检测异常
    # tracks = tracker.update(frame)
    # anomalies = detector.detect(tracks)
    # frame = detector.visualize_anomalies(frame, tracks, anomalies)
```

#### 4. 完整视频分析系统
```python
# video_analysis_system.py
import cv2
import numpy as np
from video_tracker import ObjectTracker
from action_recognition import ActionRecognizer
from anomaly_detection import AnomalyDetector

class VideoAnalysisSystem:
    """视频分析系统"""
    
    def __init__(self, config):
        self.tracker = ObjectTracker(config['detector_path'])
        self.action_recognizer = ActionRecognizer(num_classes=config['num_classes'])
        self.anomaly_detector = AnomalyDetector(contamination=config.get('contamination', 0.1))
        
        self.config = config
        self.is_training = True
        self.normal_data = []
    
    def process_video(self, video_path, output_path=None, visualize=True):
        """处理视频"""
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frame_count = 0
        action_buffer = []
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # 1. 目标跟踪
            tracks = self.tracker.update(frame)
            
            # 2. 收集正常数据或检测异常
            if self.is_training:
                self.normal_data.append(tracks.copy())
                if len(self.normal_data) > 100:  # 收集足够数据后停止
                    self.is_training = False
                    self.anomaly_detector.fit(self.normal_data)
                    print("正常数据收集完成，开始异常检测")
            else:
                anomalies = self.anomaly_detector.detect(tracks)
                frame = self.anomaly_detector.visualize_anomalies(frame, tracks, anomalies)
            
            # 3. 动作识别（每N帧）
            if frame_count % 30 == 0 and len(tracks) > 0:
                # 为每个track提取动作
                for track_id, track in tracks.items():
                    # 简化：使用当前帧作为输入
                    # 实际应该提取track的历史帧
                    action_buffer.append((track_id, frame))
            
            # 4. 绘制跟踪结果
            frame = self.tracker.draw_tracks(frame)
            
            # 5. 显示状态
            status_text = f"Training: {self.is_training} | Tracks: {len(tracks)}"
            cv2.putText(frame, status_text, (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            
            if visualize:
                cv2.imshow('Video Analysis', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            if output_path:
                out.write(frame)
            
            frame_count += 1
        
        cap.release()
        if output_path:
            out.release()
        cv2.destroyAllWindows()
        
        return frame_count

# 使用示例
if __name__ == '__main__':
    config = {
        'detector_path': 'yolov8n.pt',
        'num_classes': 10,
        'contamination': 0.05
    }
    
    system = VideoAnalysisSystem(config)
    
    # 处理视频
    total_frames = system.process_video(
        video_path='input_video.mp4',
        output_path='output_video.mp4',
        visualize=True
    )
    
    print(f"处理完成，总帧数: {total_frames}")
```

### 项目扩展
- [ ] 多摄像头同步分析
- [ ] 实时流处理
- [ ] 行为预测
- [ ] 报警系统
- [ ] Web实时监控界面

---

## 📊 项目评估标准

### 代码质量
- [ ] 代码结构清晰，模块化
- [ ] 有完整的注释和文档
- [ ] 错误处理完善
- [ ] 代码复用性高

### 功能完整性
- [ ] 数据预处理
- [ ] 模型训练
- [ ] 模型评估
- [ ] 结果可视化
- [ ] 部署方案

### 性能指标
- [ ] 准确率达到预期
- [ ] 推理速度满足需求
- [ ] 资源占用合理
- [ ] 稳定性测试通过

### 创新性
- [ ] 有独特的功能设计
- [ ] 优化现有方法
- [ ] 解决实际问题
- [ ] 提供实用价值

---

## 🎯 学习建议

### 项目选择
1. **初学者**：从项目1开始，熟悉完整流程
2. **进阶者**：选择项目2或3，深入特定领域
3. **高级者**：挑战项目4，综合应用

### 实施策略
1. **分阶段实现**：先完成核心功能，再添加高级特性
2. **数据为王**：确保数据质量和数量
3. **迭代优化**：从简单模型开始，逐步优化
4. **记录过程**：写博客记录学习心得

### 调试技巧
1. **可视化中间结果**：每步都检查输出
2. **小数据集测试**：先用少量数据验证
3. **日志记录**：详细记录训练过程
4. **单元测试**：每个模块单独测试

---

## 🚀 项目扩展方向

### 部署优化
- [ ] 模型量化（INT8）
- [ ] TensorRT加速
- [ ] 边缘设备部署（Jetson）
- [ ] Web服务化

### 功能增强
- [ ] 多模型集成
- [ ] 主动学习
- [ ] 在线学习
- [ ] 联邦学习

### 应用场景
- [ ] 工业质检
- [ ] 智慧城市
- [ ] 医疗辅助
- [ ] 自动驾驶

---

**祝你项目成功！每个项目都是通向专家的阶梯！** 🚀

*最后更新：2025年12月*
