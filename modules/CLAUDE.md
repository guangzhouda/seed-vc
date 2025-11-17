# 模块导航：modules/

> [根目录 CLAUDE.md](../CLAUDE.md)

---

## 📦 模块概述

`modules/` 目录包含 Seed-VC 的核心模型组件，按功能分为以下子模块：

---

## 🧩 核心组件

### 1. [commons.py](commons.py) - 通用工具

**功能**：提供项目全局共享的工具函数和基础类

**主要特性**：
- 参数解析工具 (`str2bool`)
- 模型权重初始化 (`init_weights`)
- 音频处理工具 (`get_padding`, `convert_pad_shape`)
- 注意力机制工具 (`attention`)
- 损失函数计算 (`kl_divergence`, `generator_loss`)
- 对抗训练工具 (`feature_loss`)

**关键类**：
- `AttrDict`: 字典转对象工具
- ` Mish`: Mish 激活函数
- `ResBlk`: 残差块
- `SPKResBlk`: 说话人感知残差块

**使用示例**：
```python
from modules.commons import AttrDict, str2bool, init_weights

# 参数解析
args = argparse.Namespace()
args.use_cuda = str2bool(True)

# 权重初始化
model = SomeModel()
init_weights(model, mean=0.0, std=0.01)
```

**依赖**：PyTorch, NumPy, munch, argparse, math

---

### 2. [audio.py](audio.py) - 音频处理

**功能**：提供音频数据的加载、预处理和后处理工具

**主要特性**：
- 音频文件读取 (WAV, FLAC, MP3)
- 采样率转换
- 音频归一化
- 幅度裁剪
- 音频拼接

**关键函数**：
- `load_wav()`: 加载 WAV 音频
- `melspectrogram()`: 生成梅尔频谱
- `spectrogram()`: 生成频谱

**使用示例**：
```python
from modules.audio import load_wav, melspectrogram

# 加载音频
audio = load_wav("input.wav", 24000)

# 生成梅尔频谱
mel = melspectrogram(audio)
```

**依赖**：librosa (可选), soundfile, PyTorch

---

### 3. [diffusion_transformer.py](diffusion_transformer.py) - 扩散Transformer

**功能**：实现基于扩散Transformer的语音转换模型

**主要特性**：
- Transformer 编码器架构
- 扩散过程建模
- 条件生成支持
- 多头注意力机制
- 位置编码
- 层归一化

**关键类**：
- `MultiHeadAttention`: 多头注意力
- `FeedForward`: 前馈网络
- `DiffusionTransformer`: 主模型类
- `SinusoidalPositionalEncoding`: 正弦位置编码

**使用示例**：
```python
from modules.diffusion_transformer import DiffusionTransformer

model = DiffusionTransformer(
    hidden_size=512,
    num_heads=8,
    num_layers=12,
    condition_dim=256
)
```

**依赖**：PyTorch

---

### 4. [encodec.py](encodec.py) - EnCodec 音频编码器

**功能**：基于 EnCodec 的音频编码解码器

**主要特性**：
- 变分自编码器
- 多尺度分析
- 残差量化
- 码本学习

**关键类**：
- `EnCodec`: 主编码器
- `EnCodecDecoder`: 解码器
- `ResidualVectorQuantizer`: 残差向量量化器

**使用示例**：
```python
from modules.encodec import EnCodec

encoder = EnCodec(
    sample_rate=24000,
    target_bandwidths=[1.5, 3.0, 6.0],
)
```

**依赖**：PyTorch, numpy

---

### 5. [flow_matching.py](flow_matching.py) - 流匹配

**功能**：实现连续归一化流 (Continuous Normalizing Flows)

**主要特性**：
- 变分推理
- ODE 求解
- 潜在变量建模

**关键类**：
- `CNF`: 连续归一化流
- `ODEFunc`: ODE 函数定义

---

### 6. [length_regulator.py](length_regulator.py) - 长度调节器

**功能**：调节语音序列的长度，实现时长控制

**主要特性**：
- 预测长度分布
- 对齐机制
- 流式生成支持

**关键类**：
- `LengthRegulator`: 长度调节器
- `Predictor`: 长度预测器

---

### 7. [rmvpe.py](rmvpe.py) - RMVPE F0 提取

**功能**：RMVPE (Reference-free Multi-view Pitch Estimation) F0 提取

**主要特性**：
- 无参考 F0 估计
- 多视角分析
- 端到端 F0 预测

**使用示例**：
```python
from modules.rmvpe import RMVPE

f0_extractor = RMVPE("rmvpe.pt")
f0 = f0_extractor.extract(audio)
```

---

### 8. [wavenet.py](wavenet.py) - WaveNet 声码器

**功能**：基于 WaveNet 的波形生成器

**主要特性**：
- 扩张卷积
- 条件生成
- 高质量波形合成

**关键类**：
- `WaveNet`: WaveNet 模型

---

## 🎯 子模块详解

### [astral_quantization/](astral_quantization/)

**功能**：Astral 量化压缩技术实现

**文件**：
- `bsq.py`: 二进制序列量化
- `convnext.py`: ConvNeXt 架构
- `transformer.py`: Transformer 组件
- `default_model.py`: 默认模型定义

**配置**：
- `default_2048.yml`: 2048 维量化配置
- `default_32.yml`: 32 维量化配置

**使用场景**：模型压缩、推理加速

---

### [bigvgan/](bigvgan/)

**功能**：BigVGAN 声码器实现

**主要特性**：
- 实时语音合成
- 高保真度音质
- 支持多说话人
- 高效推理

**子模块**：
- `activations.py`: 激活函数
- `alias_free_activation/`: 无混叠激活
  - `cuda/`: CUDA 实现
  - `cpu/`: CPU 实现
  - `activation1d.py`: 1D 激活

**关键类**：
- `BigVGAN`: 主模型
- `BigVGANBigGANDiscriminator`: 判别器

---

### [campplus/](campplus/)

**功能**：CAM++ 说话人编码器

**主要特性**：
- 说话人嵌入提取
- 端到端训练
- 说话人验证

**使用场景**：
- 说话人识别
- 语音转换中的说话人条件

---

### [hifigan/](hifigan/)

**功能**：HiFi-GAN 声码器

**主要特性**：
- 生成对抗网络
- 多周期判别器
- 高效推理

**子模块**：
- 多个判别器实现
- 生成器架构

---

### [openvoice/](openvoice/)

**功能**：OpenVoice 基线模型实现

**说明**：作为对比基线，复现 OpenVoice 的核心功能

---

### [v2/](v2/)

**功能**：V2版本模型专用组件

**说明**：包含 V2 版本特有的模型架构和组件

---

## 🔧 使用指南

### 模块导入

```python
# 导入特定模块
from modules.diffusion_transformer import DiffusionTransformer
from modules.audio import load_wav

# 导入通用工具
from modules.commons import AttrDict, init_weights, str2bool
```

### 依赖安装

```bash
# 核心依赖
pip install torch torchaudio
pip install numpy munch
pip install librosa soundfile  # 音频处理

# 可选依赖
pip install encodec  # EnCodec
pip install hydra-core omegaconf  # 配置管理
```

### 开发规范

1. **模块解耦**：每个模块应职责单一，独立测试
2. **接口统一**：遵循 PyTorch 模型接口约定
3. **类型注解**：使用 Python 类型提示
4. **文档字符串**：使用 docstring 描述功能
5. **单元测试**：为关键函数编写测试用例

---

## 📊 性能分析

### 计算复杂度

| 模块 | 复杂度 | 主要参数 | 优化建议 |
|------|--------|----------|----------|
| DiffusionTransformer | O(n²) | num_layers, hidden_size | 使用 torch.compile |
| BigVGAN | O(n) | upsample_rates | 混合精度 |
| RMVPE | O(n) | window_size | GPU 加速 |
| EnCodec | O(n log n) | codebook_size | 量化推理 |

### 内存占用

| 模块 | 参数量 | 推理内存 | 训练内存 |
|------|--------|----------|----------|
| V1 Base | ~80M | ~500MB | ~2GB |
| V2 Enhanced | ~150M | ~800MB | ~3GB |
| BigVGAN | ~15M | ~300MB | ~1GB |

---

*此文档由 Claude Code 自动生成于 2025-10-28*
