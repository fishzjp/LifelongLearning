# 实践项目：完整训练一个 CNN

> 从零跑通完整流程：数据准备 → 模型定义 → 训练循环 → 评估 → 保存加载，在 CIFAR-10 上从基线一路调到 90%+。这是本章的毕业设计，也是后续目标检测、分割项目的模板代码。

**前置知识**：本里程碑 L01-L04 + [M2 训练与调参](../M2/L04-训练与调参.md)。
**预计投入**：跟着敲 2-3 小时（含训练等待）。

---


> 从入门到精通的完整实战项目

## 目录
- [项目1: 架构对比实验](#项目1-架构对比实验)
- [项目2: 自定义架构设计](#项目2-自定义架构设计)
- [项目3: 迁移学习对比](#项目3-迁移学习对比)
- [项目4: 模型压缩实验](#项目4-模型压缩实验)
- [完整训练Pipeline](#完整训练pipeline)

---

## 项目1: 架构对比实验
**目标**：在同一数据集上对比不同CNN架构  
**数据集**：CIFAR-10  
**对比指标**：准确率、参数量、推理速度

```python

# 依赖: time, torch, torchvision
# 安装: pip install time torch torchvision
import time
import torch
import torchvision
from torchvision import transforms

def compare_architectures():
    # 定义模型
    models = {
        'ResNet18': ResNet18(num_classes=10),
        'MobileNetV2': MobileNetV2(num_classes=10),
        'EfficientNet': create_efficientnet_b0(),
    }
    
    # 数据预处理
    transform = transforms.Compose([
        transforms.Resize(224),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    
    # 加载数据
    testset = torchvision.datasets.CIFAR10(root='./data', train=False,
                                          download=True, transform=transform)
    testloader = torch.utils.data.DataLoader(testset, batch_size=32, shuffle=False)
    
    results = {}
    
    for name, model in models.items():
        model.eval()
        
        # 计算参数量
        params = sum(p.numel() for p in model.parameters())
        
        # 测试推理速度
        start_time = time.time()
        with torch.no_grad():
            for i, (images, _) in enumerate(testloader):
                if i >= 10:  # 只测试10个batch
                    break
                _ = model(images)
        inference_time = time.time() - start_time
        
        results[name] = {
            'parameters': params / 1e6,
            'inference_time': inference_time,
            'memory_usage': torch.cuda.memory_allocated() / 1024**2 if torch.cuda.is_available() else 0
        }
        
        print(f"{name}: {params/1e6:.2f}M params, {inference_time:.2f}s")
    
    return results
```

---

## 项目2: 自定义架构设计
**目标**：设计一个轻量级CNN架构  
**约束**：参数量 < 5M，CIFAR-10准确率 > 85%

```python

# 依赖: torch
# 安装: pip install torch
import torch.nn.functional as F

class CustomCNN(nn.Module):
    def __init__(self, num_classes=10):
        super(CustomCNN, self).__init__()
        
        # 设计思路：深度可分离 + 瓶颈结构 + 注意力
        self.features = nn.Sequential(
            # 初始卷积
            nn.Conv2d(3, 32, 3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            
            # 瓶颈块1
            nn.Conv2d(32, 64, 1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, 3, padding=1, groups=64),
            nn.Conv2d(64, 32, 1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            
            # SE注意力
            nn.AdaptiveAvgPool2d(1),
        )
        
        self.classifier = nn.Sequential(
            nn.Linear(32, 128),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3),
            nn.Linear(128, num_classes)
        )
    
    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x

# 验证设计
def validate_design():
    model = CustomCNN()
    params = sum(p.numel() for p in model.parameters())
    print(f"自定义模型参数量: {params/1e6:.2f}M")
    
    # 测试前向传播
    x = torch.randn(1, 3, 32, 32)
    out = model(x)
    print(f"输出形状: {out.shape}")
    
    return model

# 训练循环示例
def train_custom_model(model, train_loader, val_loader, epochs=20):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
    criterion = nn.CrossEntropyLoss()
    
    best_acc = 0
    for epoch in range(epochs):
        model.train()
        train_loss = 0
        correct = 0
        total = 0
        
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
        
        # 验证
        model.eval()
        val_correct = 0
        val_total = 0
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                _, predicted = outputs.max(1)
                val_total += labels.size(0)
                val_correct += (predicted == labels).sum().item()
        
        train_acc = 100. * correct / total
        val_acc = 100. * val_correct / val_total
        
        print(f'Epoch {epoch+1}/{epochs}: Train Loss: {train_loss/len(train_loader):.3f} | '
              f'Train Acc: {train_acc:.2f}% | Val Acc: {val_acc:.2f}%')
        
        if val_acc > best_acc:
            best_acc = val_acc
            torch.save(model.state_dict(), 'best_model.pth')
        
        scheduler.step()
    
    print(f'Best Validation Accuracy: {best_acc:.2f}%')
    return best_acc
```

---

## 项目3: 迁移学习对比
**目标**：对比不同预训练架构在迁移学习任务上的表现  
**数据集**：自定义小数据集（如花卉分类）  
**对比指标**：微调准确率、收敛速度、训练时间

```python
def compare_transfer_learning():
    from torchvision.models import resnet18, mobilenet_v2, efficientnet_b0
    from torchvision.models import ResNet18_Weights, MobileNet_V2_Weights, EfficientNet_B0_Weights
    
    # 加载预训练模型
    models = {
        'ResNet18': resnet18(weights=ResNet18_Weights.IMAGENET1K_V1),
        'MobileNetV2': mobilenet_v2(weights=MobileNet_V2_Weights.IMAGENET1K_V1),
        'EfficientNet-B0': efficientnet_b0(weights=EfficientNet_B0_Weights.IMAGENET1K_V1),
    }
    
    # 修改分类头
    for name, model in models.items():
        num_ftrs = model.fc.in_features if hasattr(model, 'fc') else model.classifier[1].in_features
        if hasattr(model, 'fc'):
            model.fc = nn.Linear(num_ftrs, 5)  # 假设5类
        else:
            model.classifier[1] = nn.Linear(num_ftrs, 5)
    
    # 冻结特征提取层
    for name, model in models.items():
        for param in model.parameters():
            param.requires_grad = False
        
        # 只训练分类头
        if hasattr(model, 'fc'):
            for param in model.fc.parameters():
                param.requires_grad = True
        else:
            for param in model.classifier.parameters():
                param.requires_grad = True
    
    return models
```

---

## 项目4: 模型压缩实验
**目标**：对比不同压缩技术的效果  
**技术**：量化、剪枝、知识蒸馏  
**指标**：模型大小、推理速度、准确率

```python
def compression_pipeline(model, train_loader, val_loader):
    """完整的模型压缩流程"""
    
    # 1. 基准性能
    baseline_metrics = evaluate_model(model, val_loader)
    print(f"基准: {baseline_metrics}")
    
    # 2. 量化
    quantized_model = quantize_model(model, train_loader)
    quantized_metrics = evaluate_model(quantized_model, val_loader)
    print(f"量化后: {quantized_metrics}")
    
    # 3. 剪枝
    pruned_model = prune_model(model, pruning_ratio=0.3)
    # 重新训练
    train_model(pruned_model, train_loader, epochs=5)
    pruned_metrics = evaluate_model(pruned_model, val_loader)
    print(f"剪枝后: {pruned_metrics}")
    
    # 4. 知识蒸馏（使用原始模型作为教师）
    student = CustomCNN()  # 轻量级学生模型
    distill_model(model, student, train_loader, epochs=10)
    distilled_metrics = evaluate_model(student, val_loader)
    print(f"蒸馏后: {distilled_metrics}")
    
    return {
        'baseline': baseline_metrics,
        'quantized': quantized_metrics,
        'pruned': pruned_metrics,
        'distilled': distilled_metrics
    }

# 量化函数
def quantize_model(model, calibration_loader):
    """模型量化示例"""
    import torch.quantization as quantization
    
    model.eval()
    model.qconfig = quantization.get_default_qconfig('fbgemm')
    
    # 准备量化
    model_prepared = quantization.prepare(model)
    
    # 校准
    with torch.no_grad():
        for data, _ in calibration_loader:
            model_prepared(data)
    
    # 转换为量化模型
    quantized_model = quantization.convert(model_prepared)
    
    return quantized_model

# 剪枝函数
def prune_model(model, pruning_ratio=0.3):
    """结构化剪枝"""
    import torch.nn.utils.prune as prune
    
    for name, module in model.named_modules():
        if isinstance(module, torch.nn.Conv2d):
            prune.l1_unstructured(module, name='weight', amount=pruning_ratio)
            prune.remove(module, 'weight')
    
    return model

# 知识蒸馏损失
class DistillationLoss(nn.Module):
    """知识蒸馏损失"""
    def __init__(self, temperature=3.0, alpha=0.7):
        super().__init__()
        self.temperature = temperature
        self.alpha = alpha
        self.kl_div = nn.KLDivLoss(reduction='batchmean')
        self.ce_loss = nn.CrossEntropyLoss()
    
    def forward(self, student_logits, teacher_logits, labels):
        # 软标签损失
        soft_loss = self.kl_div(
            F.log_softmax(student_logits / self.temperature, dim=1),
            F.softmax(teacher_logits / self.temperature, dim=1)
        ) * (self.temperature ** 2)
        
        # 硬标签损失
        hard_loss = self.ce_loss(student_logits, labels)
        
        return self.alpha * soft_loss + (1 - self.alpha) * hard_loss

def distill_model(teacher_model, student_model, train_loader, epochs=10):
    """知识蒸馏训练"""
    teacher_model.eval()
    optimizer = torch.optim.Adam(student_model.parameters())
    criterion = DistillationLoss()
    
    for epoch in range(epochs):
        for images, labels in train_loader:
            with torch.no_grad():
                teacher_logits = teacher_model(images)
            
            student_logits = student_model(images)
            loss = criterion(student_logits, teacher_logits, labels)
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
```

---

## 完整训练Pipeline
```python

# 依赖: matplotlib, time
# 安装: pip install matplotlib time
import time
import matplotlib.pyplot as plt

class TrainingPipeline:
    """完整的训练流程"""
    
    def __init__(self, model, train_loader, val_loader, config=None):
        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.config = config or {
            'lr': 1e-3,
            'epochs': 50,
            'weight_decay': 1e-4,
            'patience': 10,
            'device': 'cuda' if torch.cuda.is_available() else 'cpu'
        }
        
        self.history = {
            'train_loss': [],
            'val_loss': [],
            'train_acc': [],
            'val_acc': [],
            'learning_rate': []
        }
        
        self.best_val_acc = 0
        self.patience_counter = 0
        
    def setup_optimizer(self):
        """设置优化器和调度器"""
        optimizer = torch.optim.AdamW(
            self.model.parameters(),
            lr=self.config['lr'],
            weight_decay=self.config['weight_decay']
        )
        
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizer, 
            T_max=self.config['epochs']
        )
        
        return optimizer, scheduler
    
    def train_epoch(self, epoch, optimizer, criterion):
        """单轮训练"""
        self.model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        for batch_idx, (images, labels) in enumerate(self.train_loader):
            images, labels = images.to(self.config['device']), labels.to(self.config['device'])
            
            optimizer.zero_grad()
            outputs = self.model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            
            # 梯度裁剪
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
            
            optimizer.step()
            
            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            
            if batch_idx % 100 == 0:
                print(f'Epoch: {epoch} [{batch_idx * len(images)}/{len(self.train_loader.dataset)} '
                      f'({100. * batch_idx / len(self.train_loader):.0f}%)]\tLoss: {loss.item():.6f}')
        
        epoch_loss = running_loss / len(self.train_loader)
        epoch_acc = 100. * correct / total
        
        return epoch_loss, epoch_acc
    
    def validate(self, criterion):
        """验证"""
        self.model.eval()
        val_loss = 0.0
        correct = 0
        total = 0
        
        with torch.no_grad():
            for images, labels in self.val_loader:
                images, labels = images.to(self.config['device']), labels.to(self.config['device'])
                outputs = self.model(images)
                loss = criterion(outputs, labels)
                
                val_loss += loss.item()
                _, predicted = outputs.max(1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        
        val_loss /= len(self.val_loader)
        val_acc = 100. * correct / total
        
        return val_loss, val_acc
    
    def train(self):
        """完整训练流程"""
        self.model = self.model.to(self.config['device'])
        optimizer, scheduler = self.setup_optimizer()
        criterion = nn.CrossEntropyLoss()
        
        print(f"开始训练，设备: {self.config['device']}")
        print(f"模型参数量: {sum(p.numel() for p in self.model.parameters())/1e6:.2f}M")
        
        start_time = time.time()
        
        for epoch in range(1, self.config['epochs'] + 1):
            # 训练
            train_loss, train_acc = self.train_epoch(epoch, optimizer, criterion)
            
            # 验证
            val_loss, val_acc = self.validate(criterion)
            
            # 记录历史
            self.history['train_loss'].append(train_loss)
            self.history['val_loss'].append(val_loss)
            self.history['train_acc'].append(train_acc)
            self.history['val_acc'].append(val_acc)
            self.history['learning_rate'].append(optimizer.param_groups[0]['lr'])
            
            # 打印进度
            print(f'Epoch {epoch:03d}: '
                  f'Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.2f}% | '
                  f'Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.2f}% | '
                  f'LR: {optimizer.param_groups[0]["lr"]:.6f}')
            
            # 早停检查
            if val_acc > self.best_val_acc:
                self.best_val_acc = val_acc
                self.patience_counter = 0
                torch.save({
                    'epoch': epoch,
                    'model_state_dict': self.model.state_dict(),
                    'optimizer_state_dict': optimizer.state_dict(),
                    'val_acc': val_acc,
                    'train_acc': train_acc
                }, 'best_model.pth')
                print(f"✨ 模型已保存，最佳验证准确率: {val_acc:.2f}%")
            else:
                self.patience_counter += 1
                if self.patience_counter >= self.config['patience']:
                    print(f"🛑 早停触发，最佳验证准确率: {self.best_val_acc:.2f}%")
                    break
            
            # 学习率调度
            scheduler.step()
        
        total_time = time.time() - start_time
        print(f"\n训练完成！总耗时: {total_time:.2f}秒")
        print(f"最佳验证准确率: {self.best_val_acc:.2f}%")
        
        return self.best_val_acc
    
    def plot_history(self, save_path='training_history.png'):
        """绘制训练历史"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Loss曲线
        axes[0, 0].plot(self.history['train_loss'], label='Train Loss', marker='o')
        axes[0, 0].plot(self.history['val_loss'], label='Val Loss', marker='s')
        axes[0, 0].set_title('Loss Curves')
        axes[0, 0].set_xlabel('Epoch')
        axes[0, 0].set_ylabel('Loss')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Accuracy曲线
        axes[0, 1].plot(self.history['train_acc'], label='Train Acc', marker='o')
        axes[0, 1].plot(self.history['val_acc'], label='Val Acc', marker='s')
        axes[0, 1].set_title('Accuracy Curves')
        axes[0, 1].set_xlabel('Epoch')
        axes[0, 1].set_ylabel('Accuracy (%)')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # 学习率曲线
        axes[1, 0].plot(self.history['learning_rate'], marker='o', color='green')
        axes[1, 0].set_title('Learning Rate Schedule')
        axes[1, 0].set_xlabel('Epoch')
        axes[1, 0].set_ylabel('LR')
        axes[1, 0].grid(True, alpha=0.3)
        
        # 过拟合指示
        if len(self.history['train_acc']) > 1:
            gap = [t - v for t, v in zip(self.history['train_acc'], self.history['val_acc'])]
            axes[1, 1].plot(gap, marker='s', color='red')
            axes[1, 1].axhline(y=0, color='black', linestyle='--')
            axes[1, 1].set_title('Train-Val Gap (Overfitting Indicator)')
            axes[1, 1].set_xlabel('Epoch')
            axes[1, 1].set_ylabel('Gap (%)')
            axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"📊 训练曲线已保存到: {save_path}")
        
        return fig

# 使用示例
def run_complete_pipeline():
    """运行完整训练流程"""
    # 1. 准备数据
    transform = transforms.Compose([
        transforms.Resize(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    
    trainset = torchvision.datasets.CIFAR10(root='./data', train=True, 
                                           download=True, transform=transform)
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=32, shuffle=True, num_workers=2)
    
    testset = torchvision.datasets.CIFAR10(root='./data', train=False, 
                                          download=True, transform=transform)
    valloader = torch.utils.data.DataLoader(testset, batch_size=32, shuffle=False, num_workers=2)
    
    # 2. 创建模型
    model = CustomCNN(num_classes=10)
    
    # 3. 训练
    pipeline = TrainingPipeline(model, trainloader, valloader, config={
        'lr': 1e-3,
        'epochs': 30,
        'weight_decay': 1e-4,
        'patience': 7
    })
    
    best_acc = pipeline.train()
    
    # 4. 绘制结果
    pipeline.plot_history()
    
    return best_acc
```

---

## 快速测试函数
```python
def quick_test():
    """快速测试模型"""
    print("🔍 快速测试...")
    
    # 测试数据
    x = torch.randn(1, 3, 32, 32)
    
    # 测试不同模型
    models = {
        'CustomCNN': CustomCNN(),
        'ResNet18': ResNet18(num_classes=10),
        'MobileNetV2': MobileNetV2(num_classes=10),
    }
    
    for name, model in models.items():
        params = sum(p.numel() for p in model.parameters())
        with torch.no_grad():
            out = model(x)
        
        print(f"{name:15} | 参数: {params/1e6:6.2f}M | 输出: {out.shape}")

# 参数量统计
def count_parameters(model):
    """统计模型参数"""
    total = sum(p.numel() for p in model.parameters())
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    
    print(f"总参数量: {total/1e6:.2f}M")
    print(f"可训练参数: {trainable/1e6:.2f}M")
    print(f"冻结参数: {(total-trainable)/1e6:.2f}M")
    
    return total, trainable
```

---

## 项目总结
### 必做实践项目
1. **基础项目**: 在MNIST上训练并对比LeNet、ResNet18、MobileNetV2
2. **进阶项目**: 在CIFAR-10上进行架构对比，绘制性能曲线
3. **高级项目**: 设计自定义架构，目标参数量<5M，准确率>85%
4. **部署项目**: 将训练好的模型量化并部署到移动端

### 学习要点
- 掌握完整的训练流程
- 理解不同架构的性能差异
- 学会模型压缩和优化技术
- 能够进行系统化的实验对比

---

**上一章：[L04-选型指南](L04-%E9%80%89%E5%9E%8B%E6%8C%87%E5%8D%97.md)**  
**下一章：[debug-cv](../../../references/debug-cv.md)**

