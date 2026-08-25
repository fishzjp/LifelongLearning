# 调试与优化指南

> CNN 训练的排障手册：准确率不涨、显存爆掉、loss 变 NaN、推理太慢……按症状索引，每条给出排查步骤和修复代码。训练卡住时先来这里。

**前置知识**：本章 01-05 篇。
**用法**：不必通读，按症状查；训练前浏览一遍"预防清单"最划算。

---


> 训练诊断、性能监控、部署优化

## 目录
- [训练过程诊断](#训练过程诊断)
- [性能监控工具](#性能监控工具)
- [常见问题修复](#常见问题修复)
- [模型部署优化](#模型部署优化)
- [性能基准测试](#性能基准测试)

---

## 训练过程诊断工具包
```python
class TrainingDiagnostics:
    """训练过程诊断工具"""
    
    def __init__(self, model):
        self.model = model
        self.history = {
            'loss': [],
            'grad_norms': {},
            'activations': {},
            'weights': {}
        }
    
    def diagnose_gradients(self):
        """诊断梯度问题"""
        print("🔍 梯度诊断:")
        issues = []
        
        for name, param in self.model.named_parameters():
            if param.grad is None:
                issues.append(f"❌ {name}: 无梯度")
                continue
            
            grad_norm = param.grad.norm().item()
            param_norm = param.norm().item()
            
            if grad_norm > 1e3:
                issues.append(f"⚠️ {name}: 梯度爆炸 ({grad_norm:.2e})")
            elif grad_norm < 1e-7:
                issues.append(f"⚠️ {name}: 梯度消失 ({grad_norm:.2e})")
            elif grad_norm == 0:
                issues.append(f"❌ {name}: 梯度为零")
            
            # 记录历史
            if name not in self.history['grad_norms']:
                self.history['grad_norms'][name] = []
            self.history['grad_norms'][name].append(grad_norm)
        
        if not issues:
            print("✅ 梯度正常")
        else:
            for issue in issues:
                print(f"  {issue}")
        
        return issues
    
    def diagnose_activations(self, dataloader, device='cuda'):
        """诊断激活分布"""
        print("\n🔍 激活分布诊断:")
        issues = []
        
        def hook_fn(name):
            def hook(module, input, output):
                mean = output.mean().item()
                std = output.std().item()
                max_val = output.max().item()
                min_val = output.min().item()
                
                # 记录历史
                if name not in self.history['activations']:
                    self.history['activations'][name] = {
                        'mean': [], 'std': [], 'max': [], 'min': []
                    }
                self.history['activations'][name]['mean'].append(mean)
                self.history['activations'][name]['std'].append(std)
                self.history['activations'][name]['max'].append(max_val)
                self.history['activations'][name]['min'].append(min_val)
                
                # 诊断
                if abs(mean) > 10:
                    issues.append(f"⚠️ {name}: 均值异常 ({mean:.2f})")
                if std > 20:
                    issues.append(f"⚠️ {name}: 标准差过大 ({std:.2f})")
                if max_val > 1e6:
                    issues.append(f"❌ {name}: 激活爆炸 ({max_val:.2e})")
                if min_val < -1e6:
                    issues.append(f"❌ {name}: 激活爆炸 ({min_val:.2e})")
            return hook
        
        # 注册hooks
        hooks = []
        for name, module in self.model.named_modules():
            if isinstance(module, (nn.Conv2d, nn.Linear, nn.ReLU, nn.BatchNorm2d)):
                hooks.append(module.register_forward_hook(hook_fn(name)))
        
        # 前向传播
        self.model.eval()
        with torch.no_grad():
            for i, (images, _) in enumerate(dataloader):
                if i >= 5:  # 只测试5个batch
                    break
                images = images.to(device)
                _ = self.model(images)
        
        # 移除hooks
        for h in hooks:
            h.remove()
        
        if not issues:
            print("✅ 激活分布正常")
        else:
            for issue in issues:
                print(f"  {issue}")
        
        return issues
    
    def diagnose_weights(self):
        """诊断权重分布"""
        print("\n🔍 权重分布诊断:")
        issues = []
        
        for name, param in self.model.named_parameters():
            if 'weight' in name:
                mean = param.data.mean().item()
                std = param.data.std().item()
                max_val = param.data.max().item()
                min_val = param.data.min().item()
                
                # 记录历史
                if name not in self.history['weights']:
                    self.history['weights'][name] = {
                        'mean': [], 'std': [], 'max': [], 'min': []
                    }
                self.history['weights'][name]['mean'].append(mean)
                self.history['weights'][name]['std'].append(std)
                self.history['weights'][name]['max'].append(max_val)
                self.history['weights'][name]['min'].append(min_val)
                
                # 诊断
                if std < 1e-5:
                    issues.append(f"⚠️ {name}: 权重几乎不变 (std={std:.2e})")
                if abs(mean) > 5:
                    issues.append(f"⚠️ {name}: 均值偏大 ({mean:.2f})")
                if max_val > 10 or min_val < -10:
                    issues.append(f"⚠️ {name}: 权重值 ({max_val_val:.2f}, {min_val:.2f})")
        
        if not issues:
            print("✅ 权重分布正常")
        else:
            for issue in issues:
                print(f"  {issue}")
        
        return issues
    
    def full_diagnosis(self, dataloader, device='cuda'):
        """完整诊断"""
        print("="*60)
        print("🚀 开始完整训练诊断")
        print("="*60)
        
 # 1. 梯度诊断
        grad_issues = self.diagnose_gradients()
        
        # 2. 激活诊断
        act_issues = self.diagnose_activations(dataloader, device)
        
        # 3. 权重诊断
        weight_issues = self.diagnose_weights()
        
        # 总结
        total_issues =_grad = len(grad_issues)
        total_issues_act = len(act_issues)
        total_issues_weight = len(weight_issues)
        total_issues = total_issues_grad + total_issues_act + total_issues_weight
        
        print(f"\n📊 诊断总结: 发现 {total_issues} 个潜在问题")
        
        if total_issues == 0:
            print("🎉 模型状态良好，可以开始训练！")
        else:
            print("⚠️  发现问题，请根据上述提示修复")
        
        return {
            'gradient_issues': grad_issues,
            'activation_issues': act_issues,
            'weight_issues': weight_issues,
            'total_issues': total_issues
        }
```

---

## 训练过程监控器
```python
class TrainingMonitor:
    """训练过程监控器"""
    
    def __init__(self, model, log_dir='./logs'):
        self.model = model
        self.log_dir = log_dir
        self.metrics = {
            'train_loss': [],
            'val_loss': [],
            'train_acc': [],
            'val_acc': [],
            'learning_rate': []
        }
        self.best_val_acc = 0
        self.patience_counter = 0
        
        # 创建日志目录
        import os
        os.makedirs(log_dir, exist_ok=True)
    
    def on_epoch_end(self, epoch, train_loss, train_acc, val_loss, val_acc, lr):
        """每个epoch结束时调用"""
        self.metrics['train_loss'].append(train_loss)
        self.metrics['val_loss'].append(val_loss)
        self.metrics['train_acc'].append(train_acc)
        self.metrics['val_acc'].append(val_acc)
        self.metrics['learning_rate'].append(lr)
        
        # 早停检查
        if val_acc > self.best_val_acc:
            self.best_val_acc = val_acc
            self.patience_counter = 0
            # 保存最佳模型
            torch.save({
                'epoch': epoch,
                'model_state_dict': self.model.state_dict(),
                'val_acc': val_acc,
                'train_acc': train_acc
            }, os.path.join(self.log_dir, 'best_model.pth'))
        else:
            self.patience_counter += 1
        
        # 打印进度
        print(f"Epoch {epoch+1:03d}: "
              f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.2f}% | "
              f"Val Loss: {_loss:.4f} | Val Acc: {val_acc:.2f}% | "
              f"LR: {lr:.6f}")
        
        # 检查过拟合
        if len(self.metrics['train_acc']) > 5:
            train_accs = self.metrics['train_acc'][-5:]
            val_accs = self.metrics['val_acc'][-5:]
            if all(t > v + 10 for t, v in zip(train_accs, val_accs)):
                print("⚠️  检测到过拟合！建议增加正则化")
        
        return self.patience_counter
    
    def plot_metrics(self, save_path=None):
        """绘制训练曲线"""
        import matplotlib.pyplot as plt
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        
        # Loss曲线
        axes[0, 0].plot(self.metrics['train_loss'], label='Train Loss', marker='o')
        axes[0, 0].plot(self.metrics['val_loss'], label='Val Loss', marker='s')
        axes[0, 0].set_title('Loss Curves')
        axes[0, 0].set_xlabel('Epoch')
        axes[0, 0].set_ylabel('Loss')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Accuracy曲线
        axes[0, 1].plot(self.metrics['train_acc'], label='Train Acc', marker='o')
        axes[0, 1].plot(self.metrics['val_acc'], label='Val Acc', marker='s')
        axes[0, 1].set_title('Accuracy Curves')
        axes[0, 1].set_xlabel('Epoch')
        axes[0, 1].set_ylabel('Accuracy (%)')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # 学习率曲线
        axes[1, 0].plot(self.metrics['learning_rate'], marker='o', color='green')
        axes[1, 0].set_title('Learning Rate Schedule')
        axes[1, 0].set_xlabel('Epoch')
        axes[1, 0].set_ylabel('LR')
        axes[1, 0].grid(True, alpha=0.3)
        
        # 指标对比
        if len(self.metrics['train_acc']) > 1:
            train_gap = [t - v for t, v in zip(self.metrics['train_acc'], self.metrics['val_acc'])]
            axes[1, 1].plot(train_gap, marker='s', color='red')
            axes[1, 1].axhline(y=0, color='black', linestyle='--')
            axes[1, 1].set_title('Train-Val Gap (Overfitting Indicator)')
            axes[1, 1].set_xlabel('Epoch')
            axes[1, 1].set_ylabel('Gap (%)')
            axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"📊 训练曲线已保存到: {save_path}")
        
        return fig
```

---

## 常见问题快速修复
```python
def quick_fixes(model, train_loader, val_loader, device='cuda'):
    """常见问题快速修复指南"""
    
    print("\n🔧 常见问题快速修复:")
    
    # 问题1: 训练不收敛
    print("\n1️⃣ 训练不收敛:")
    print("   - 检查学习率: 尝试 1e-3, 1e-4")
    print("   - 检查损失函数: 确保与任务匹配")
    print("   - 检查数据预处理: 归一化是否正确")
    print("   - 尝试更小的模型")
    
    # 问题2: 过拟合
    print("\n2️⃣ 过拟合:")
    print("   - 增加Dropout (0.3-0.5)")
    print("   - 增加权重衰减 (1e-4)")
    print("   - 数据增强")
    print("   - 早停 (patience=10)")
    print("   - 减少模型复杂度")
    
    # 问题3: 梯度爆炸/消失
    print("\n3️⃣ 梯度问题:")
    print("   - 使用梯度裁剪 (max_norm=1.0)")
    print("   - 检查权重初始化")
    print("   - 使用BatchNorm")
    print("   - 使用残差连接")
    print("   - 尝试更小的学习率")
    
    # 问题4: 内存不足
    print("\n4️⃣ 内存不足:")
    print("   - 减小batch_size")
    print("   - 使用梯度累积")
    print("   - 使用混合精度训练")
    print("   - 使用梯度检查点")
    print("   - 清理CUDA缓存")
    
    # 问题5: 训练速度慢
    print("\n5️⃣ 训练速度慢:")
    print("   - 使用GPU加速")
    print("   - 增加num_workers")
    print("   - 使用pin_memory=True")
    print("   - 混合精度训练")
    print("   - 检查数据加载瓶颈")
    
    # 实用修复函数
    def apply_fixes():
        """应用修复"""
        fixes = {
            'gradient_clipping': lambda: torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0),
            'add_dropout': lambda: add_dropout_to_model(model, p=0.3),
            'enable_mixed_precision': lambda: enable_mixed_precision_training(),
        }
        return fixes
    
    return apply_fixes()

def add_dropout_to_model(model, p=0.3):
    """为模型添加Dropout"""
    for name, module in model.named_modules():
        if isinstance(module, nn.Linear):
            # 在Linear层后添加Dropout
            parent_name = name.rsplit('.', 1)[0] if '.' in name else ''
            parent = model
            if parent_name:
                for part in parent_name.split('.'):
                    parent = getattr(parent, part)
            
            # 创建新的Sequential
            new_modules = []
            for child in module.children():
                new_modules.append(child)
            new_modules.append(nn.Dropout(p))
            
            # 替换原模块
            setattr(parent, name.split('.')[-1], nn.Sequential(*new_modules))
    
    return model

def enable_mixed_precision_training():
    """启用混合精度训练"""
    return torch.cuda.amp.GradScaler()
```

---

## 模型结构可视化
```python
def visualize_model_structure(model, input_shape=(1, 3, 224, 224)):
    """可视化模型结构和数据流"""
    print("\n🔍 模型结构分析:")
    print("="*60)
    
    # 层次结构
    print(f"{'层类型':<20} {'输出形状':<20} {'参数量':<10}")
    print print("-"*60)
    
    def hook_fn(name):
        def hook(module, input, output):
            output_shape = list(output.shape)
            params = sum(p.numel() for p in module.parameters())
            layer_type = module.__class__.__name__
            print(f"{layer_type:<20} {str(output_shape):<20} {params:<10}")
        return hook
    
    hooks = []
    for name, module in model.named_modules():
        if len(list(module.children())) == 0:  # 叶子模块
            hooks.append(module.register_forward_hook(hook_fn(name)))
    
    # 前向传播
    with torch.no_grad():
        dummy_input = torch.randn(*input_shape)
        _ =(model(dummy(dummy(dummy
    
 hooks hooks hooks hooks hooks hooks hooks hookshooks hooks hooks hookshooks hooks hooks hooks hooks hooks hookshooks hooks hooks hooks hooks � # hooks hooks hooks hooks hooks
    
 hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks hooks     hooks hooks hooks hooks  hooks hooks
    for h in hooks:
        h.remove()
    
    # 总结
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    
    print("-"*60)
    print(f"总参数量: {total_params/1e6:.2f}M")
    print(f"可训练参数: {trainable_params/1e6:.2f}M")
    print(f"冻结参数: {(total_params - trainable_params)/1e6:.2f}M")
```

---

## 特征可视化
```python
def visualize_feature_maps(model, image, layer_names):
    """可视化指定层的特征图"""
    features = {}
    
    def hook_fn(name):
        def hook(module, input, output):
            features[name] = output.detach()
        return hook
    
    # 注册hook
    hooks = []
    for name, module in model.named_modules():
        if name in layer_names:
            hooks.append(module.register_forward_hook(hook_fn(name)))
    
    # 前向传播
    model.eval()
    with torch.no_grad():
        _ = model(image)
    
    # 移除hooks
    for h in hooks:
        h.remove()
    
    return features
```

---

## 模型量化与压缩
```python

# 依赖: torch
# 安装: pip install torch
import torch.quantization as quantization

def quantize_model(model, calibration_loader):
    """模型量化示例"""
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

def prune_model(model, pruning_ratio=0.3):
    """结构化剪枝"""
    import torch.nn.utils.prune as prune
    
    for name, module in model.named_modules():
        if isinstance(module, torch.nn.Conv2d):
            prune.l1_unstructured(module, name='weight', amount=pruning_ratio)
            prune.remove(module, 'weight')
    
    return model

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
    optimizer optimizer torch.Adam student student student student.parameters optimizer optimizer criterion criterion criterion = criterion = = criterion criterion = criterion Dist criterion = = = =    = for    criterion for for for for for for for for for for for for for for for for for for for for for for for for for for = for teacher for loss loss = = loss for loss loss = student = student optimizer optimizer for for teacher loss optimizer optimizer for for for for optimizer for for = for  =  torch蒸 _loss       蒸    蒸蒸  optimizer  optimizer蒸蒸，蒸     torch torch torch torch torch torch " torch torch torch torch 

        # 3. 剪
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
```

---

## ONNX导出与推理加速
```python

# 依赖: numpy, onnxruntime, torch
# 安装: pip install numpy onnxruntime torch
import torch.onnx
import onnxruntime as ort
import numpy as np

def export_to_onnx(model, input_shape, output_path):
    """导出为ONNX格式"""
    model.eval()
    dummy_input = torch.randn(1, *input_shape)
    
    torch.onnx.export(
        model, dummy_input, output_path,
        input_names=['input'], output_names=['output'],
        dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}},
        opset_version=11
    )
    print(f"模型已导出到: {output_path}")

def onnx_inference(model_path, input_data):
    """ONNX推理"""
    session = ort.InferenceSession(model_path)
    input_name = session.get_inputs()[0].name
    
    # 转换输入类型
    if isinstance(input_data, torch.Tensor):
        input_data = input_data.numpy()
    
    outputs = session.run(None, {input_name: input_data})
    return outputs[0]

# 性能对比
def compare_inference_speed(model, onnx_path, input_tensor):
    """对比PyTorch和ONNX推理速度"""
    import time
    
    # PyTorch推理
    start = time.time()
    with torch.no_grad():
        for _ in range(100):
            _ = model(input_tensor)
    torch_time = (time.time() - start) / 100
    
    # ONNX推理
    input_np = input_tensor.numpy()
    start = time.time()
    for _ in range(100):
        _ = onnx_inference(onnx_path, input_np)
    onnx_time = (time.time() - start) / 100
    
    print(f"PyTorch: {torch_time*1000:.2f}ms")
    print(f"ONNX: {onnx_time*1000:.2f}ms")
    print(f"加速比: {torch_time/onnx_time:.2f}x")
```

---

## 性能基准测试
```python
def comprehensive_benchmark(model, test_loader, device='cuda'):
    """全面性能测试"""
    model = model.to(device)
    model.eval()
    
    metrics = {}
    
    # 1. 准确率
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    
    metrics['accuracy'] = 100 * correct / total
    
    # 2. 推理速度
    times = []
    dummy_input = torch.randn(1, 3, 224, 224).to(device)
    
    # 预热
    for _ in range(10):
        _ = model(dummy_input)
    
    # 测试
    with torch.no_grad():
        for _ in range(100):
            start = time.time()
            _ = model(dummy_input)
            if device == 'cuda':
                torch.cuda.synchronize()
            times.append(time.time() - start)
    
    metrics['latency_ms'] = np.mean(times) * 1000
    metrics['fps'] = 1000 / metrics['latency_ms']
    
    # 3. 参数计算     参数    metrics             metrics metrics['    metrics             metrics metrics       metrics metrics    metrics['  sum(p for for if    .cuda['        metrics[' metrics memory metrics  metrics  metrics memory memory metrics  metrics memory memory    cuda cuda metrics  metrics metrics metrics metrics metrics  metrics       metrics    metrics    metrics  cuda       =    =        metrics       metrics      metrics   

    

                  metrics  metrics  metrics
       metrics                  

    
  
  
      1e6:.2f}M")
    print(f"{'计算量':<15} {flops/1e9:.2f}G FLOPs")
    print(f"{'内存占用':<15} {memory_mb:.2f}MB")
    print(f"{'卷积层':<15} {conv_count}")
    print(f"{'BN层':<15} {bn_count}")
    print(f"{'全连接层':<15} {linear_count}")
    
    # 效率指标
    accuracy_efficiency = 76.2 / (params/1e6) if params > 0 else 0  # 假设ResNet50准确率为76.2%
    print(f"{'参数效率':<15} {accuracy_efficiency:.2f}% per M params")
    
    return {
        'params': params,
        'flops': flops,
        'memory_mb': memory_mb,
        'layers': {
            'conv': conv_count,
            'bn': bn_count,
            'linear': linear_count
        }
    }

# 批量测试
def batch_benchmark(models_dict, test_loader, device='cuda'):
    """批量测试多个模型"""
    results = {}
    
    for name, model in models_dict.items():
        print(f"测试 {name}...")
        try:
            results[name] = comprehensive_benchmark(model, test_loader, device)
        except Exception as e:
            print(f"  错误: {e}")
            results[name] = None
    
    # 打印结果
    print("\n" + "="*80)
    print(f"{'模型':<20} {'准确率':<10} {'延迟(ms)':<10} {'FPS':<10} {'参数(M)':<10}")
    print("="*80)
    
    for name, metrics in results.items():
        if metrics:
            print(f"{name:<20} {metrics['accuracy']:<10.2f} {metrics['latency_ms']:<10.2f} "
                  f"{metrics['fps']:<10.1f} {metrics['params']/1e6:<10.2f}")
    
    return results
```

---

## 调试检查清单
### 训练前检查
- [ ] 模型参数量是否符合要求
- [ ] 数据预处理是否正确
- [ ] 学习率是否合理
- [ ] 损失函数是否匹配任务
- [ ] GPU内存是否足够

### 训练中监控
- [ ] Loss是否下降
- [ ] 准确率是否提升
- [ ] 梯度是否正常
- [ ] 激活分布是否合理
- [ ] 是否过拟合

### 训练后分析
- [ ] 模型性能是否达标
- [ ] 推理速度是否满足要求
- [ ] 模型大小是否合适
- [ ] 是否需要进一步优化

---

**上一章：[PROJECT-CIFAR10](../tracks/cv/M3/PROJECT-CIFAR10.md)**  
**下一章：[README](../tracks/cv/M3/README.md) - 返回主文档**

