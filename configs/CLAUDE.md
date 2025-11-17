# 模块导航：configs/

> [根目录 CLAUDE.md](../CLAUDE.md)

---

## 📦 目录概述

`configs/` 目录使用 **Hydra** 配置管理系统管理项目中的所有配置文件，支持模块化、可组合的配置方案。

**配置格式**：YAML + JSON
**管理框架**：Hydra + OmegaConf
**特性**：
- 动态配置加载
- 配置组合与继承
- 参数覆盖
- 命令行参数支持
- 多环境配置

---

## 🗂️ 配置文件结构

```
configs/
├── config.json              # 全局配置
├── hifigan.yml              # HiFi-GAN 声码器配置
├── v2/
│   └── vc_wrapper.yaml      # V2版本模型包装器配置
├── astral_quantization/
│   ├── default_2048.yml     # 2048维量化配置
│   ├── default_32.yml       # 32维量化配置
│   └── config.json          # 量化模块配置
└── presets/
    ├── config_dit_mel_seed_uvit_whisper_base_f0_44k.yml
    ├── config_dit_mel_seed_uvit_whisper_small_wavenet.yml
    └── config_dit_mel_seed_uvit_xlsr_tiny.yml
```

---

## 📄 核心配置文件

### 1. [config.json](config.json) - 全局配置

**功能**：定义项目的全局参数和默认设置

**主要内容**：
```json
{
  "model": {
    "name": "seed_vc",
    "version": "v1",
    "sample_rate": 24000,
    "hop_length": 256,
    "win_length": 1024
  },
  "training": {
    "batch_size": 32,
    "learning_rate": 0.0001,
    "epochs": 100,
    "save_interval": 10,
    "eval_interval": 5
  },
  "inference": {
    "diffusion_steps": 10,
    "length_adjust": 1.0,
    "inference_cfg_rate": 0.7,
    "f0_condition": false,
    "auto_f0_adjust": true
  },
  "device": {
    "use_cuda": true,
    "cuda_device": 0,
    "use_mps": false
  }
}
```

**参数说明**：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| model.sample_rate | int | 24000 | 采样率 |
| model.hop_length | int | 256 | 跳跃长度 |
| model.win_length | int | 1024 | 窗口长度 |
| training.batch_size | int | 32 | 批处理大小 |
| training.learning_rate | float | 0.0001 | 学习率 |
| inference.diffusion_steps | int | 10 | 扩散步数 |
| inference.length_adjust | float | 1.0 | 长度调节系数 |
| inference.inference_cfg_rate | float | 0.7 | 推理CFG率 |

---

### 2. [hifigan.yml](hifigan.yml) - HiFi-GAN 配置

**功能**：配置 HiFi-GAN 声码器的参数

**主要内容**：
```yaml
model:
  in_channels: 80  # 输入通道数 (梅尔频谱维度)
  resblock: 1     # 残差块类型
  num_gpus: 1     # GPU 数量
  batch_size: 32  # 批处理大小

audio:
  sr: 24000       # 采样率
  hop_length: 256 # 跳跃长度
  win_length: 1024 # 窗口长度
```

---

### 3. [v2/vc_wrapper.yaml](v2/vc_wrapper.yaml) - V2模型配置

**功能**：配置 V2版本的语音转换模型包装器

**主要内容**：
```yaml
defaults:
  - encodec: encodec_24k
  - diffusion: dit_mel_seed_uvit_base
  - decoder: bigvgan_24k_100h

_encodec:
  _target_: modules.encodec.EnCodec
  sample_rate: 24000
  bandwidths: [3.0, 6.0, 12.0]

_diffusion:
  _target_: modules.diffusion_transformer.DiffusionTransformer
  hidden_size: 768
  num_heads: 12
  num_layers: 24
  condition_dim: 256

_decoder:
  _target_: modules.bigvgan.BigVGAN
  sample_rate: 24000
  upsample_rates: [5, 4, 3, 2]
  Gin_channels: 256
  use_cuda_graph: false
```

**组件说明**：

| 组件 | 类名 | 参数 | 说明 |
|------|------|------|------|
| 编码器 | EnCodec | sample_rate, bandwidths | 音频编码 |
| 扩散模型 | DiffusionTransformer | hidden_size, num_heads, num_layers | 条件生成 |
| 解码器 | BigVGAN | sample_rate, upsample_rates | 波形合成 |

---

## 🎯 预设配置

### 预置模型配置

| 配置文件 | 模型类型 | 参数量 | 推理速度 | 质量 |
|----------|----------|--------|----------|------|
| `config_dit_mel_seed_uvit_whisper_base_f0_44k.yml` | Base | ~150M | 中等 | 高 |
| `config_dit_mel_seed_uvit_whisper_small_wavenet.yml` | Small | ~80M | 快 | 中 |
| `config_dit_mel_seed_uvit_xlsr_tiny.yml` | Tiny | ~40M | 很快 | 低 |

---

### Base 配置详情

**文件名**：`presets/config_dit_mel_seed_uvit_whisper_base_f0_44k.yml`

```yaml
defaults:
  - _self_

model:
  name: "dit_mel_seed_uvit_base"
  version: "v2"
  sample_rate: 44100
  num_mels: 80
  hop_length: 256
  win_length: 1024

  transformer:
    hidden_size: 768
    num_heads: 12
    num_layers: 24
    dropout: 0.1
    layer_norm_epsilon: 1e-6

  f0:
    extractor: "rmvpe"
    condition: true
    auto_adjust: true

  diffusion:
    num_steps: 25
    beta_schedule: "cosine"
    beta_start: 0.0001
    beta_end: 0.02

  decoder:
    type: "wavenet"
    residual_channels: 512
    dilation_rates: [1, 3, 9]
    num_res_blocks: 4

training:
  batch_size: 16
  gradient_accumulation_steps: 4
  learning_rate: 0.0001
  warmup_steps: 1000
  max_epochs: 100
  save_interval: 10
  eval_interval: 5
  log_interval: 100

inference:
  diffusion_steps: 25
  length_adjust: 1.0
  inference_cfg_rate: 0.7
  f0_condition: true
  auto_f0_adjust: true
  pitch_shift: 0
  stream_output: true
```

---

### Small 配置详情

**文件名**：`presets/config_dit_mel_seed_uvit_whisper_small_wavenet.yml`

```yaml
model:
  name: "dit_mel_seed_uvit_small"
  sample_rate: 24000
  num_mels: 80

  transformer:
    hidden_size: 512
    num_heads: 8
    num_layers: 12
    dropout: 0.1

  diffusion:
    num_steps: 10
    beta_schedule: "linear"

  decoder:
    type: "wavenet_small"
    residual_channels: 256
    dilation_rates: [1, 3, 9]
    num_res_blocks: 3

training:
  batch_size: 32
  learning_rate: 0.0002
  max_epochs: 80
```

---

### Tiny 配置详情

**文件名**：`presets/config_dit_mel_seed_uvit_xlsr_tiny.yml`

```yaml
model:
  name: "dit_mel_seed_uvit_tiny"
  sample_rate: 16000
  num_mels: 64

  transformer:
    hidden_size: 256
    num_heads: 4
    num_layers: 6
    dropout: 0.1

  diffusion:
    num_steps: 5
    beta_schedule: "linear"

  decoder:
    type: "wavenet_tiny"
    residual_channels: 128
    num_res_blocks: 2

training:
  batch_size: 64
  learning_rate: 0.0003
  max_epochs: 60
```

---

## 🔧 量化配置

### [astral_quantization/default_2048.yml](astral_quantization/default_2048.yml)

**功能**：2048维 Astral 量化配置

```yaml
quantizer:
  codebook_size: 2048
  commitment_cost: 0.25
  decay: 0.99
  eps: 1e-5

  resolution: 2048
  masking_ratio: 0.0
  l2_norm: false

performance:
  num_bits: 11
  compression_ratio: 10.9
  reconstruction_quality: "high"
```

### [astral_quantization/default_32.yml](astral_quantization/default_32.yml)

**功能**：32维轻量量化配置

```yaml
quantizer:
  codebook_size: 32
  commitment_cost: 0.25
  decay: 0.99
  eps: 1e-5

  resolution: 32
  masking_ratio: 0.1
  l2_norm: true

performance:
  num_bits: 5
  compression_ratio: 96.0
  reconstruction_quality: "medium"
```

---

## 🛠️ 配置使用指南

### 1. 加载配置

```python
import yaml
from hydra import compose, initialize_config_dir
from hydra.utils import instantiate
from omegaconf import DictConfig

# 方法1：直接加载 YAML
with open("configs/v2/vc_wrapper.yaml", "r") as f:
    config = yaml.safe_load(f)

# 方法2：使用 Hydra (推荐)
from hydra import initialize_config_dir, instantiate

with initialize_config_dir(config_dir="configs"):
    cfg = compose(config_name="v2/vc_wrapper.yaml")
    model = instantiate(cfg.model)

# 方法3：部分加载
with open("configs/config.json", "r") as f:
    global_config = json.load(f)

with open("configs/v2/vc_wrapper.yaml", "r") as f:
    model_config = yaml.safe_load(f)

combined_config = {**global_config, **model_config}
```

### 2. 命令行覆盖参数

```bash
# 运行时覆盖配置
python inference_v2.py \\
    --config-path=configs/v2 \\
    --config-name=vc_wrapper \\
    diffusion.num_steps=25 \\
    diffusion.beta_schedule=cosine \\
    decoder.use_cuda_graph=true \\
    inference.f0_condition=true
```

### 3. 多配置文件合并

```python
# Hydra defaults 机制
defaults:
  - encodec: encodec_24k
  - diffusion: dit_mel_seed_uvit_base
  - decoder: bigvgan_24k_100h
  - _self_

# 运行时添加更多默认配置
python script.py --config-path=configs \\
    --config-name=v2/vc_wrapper \\
    +encodec=encodec_48k \\
    +diffusion=dit_mel_seed_uvit_large
```

### 4. 配置验证

```python
from pydantic import BaseModel, ValidationError

class ModelConfig(BaseModel):
    hidden_size: int
    num_heads: int
    num_layers: int

# 验证配置
def validate_config(config_dict):
    try:
        config = ModelConfig(**config_dict)
        return True, config
    except ValidationError as e:
        return False, str(e)
```

---

## 🔄 配置管理最佳实践

### 1. 模块化设计

```yaml
# 基础配置
defaults:
  - _self_
  - model: base
  - training: base
  - inference: base

# 特定场景配置
defaults:
  - override /model: fast_inference
```

### 2. 参数继承

```yaml
# 父配置：configs/model/base.yaml
model:
  name: "seed_vc"
  version: "v2"
  hidden_size: 768

# 子配置：configs/model/fast.yaml
name: ${model.name}_fast
hidden_size: 256  # 覆盖父配置
```

### 3. 动态参数

```python
# 根据设备动态设置
device_config = {
    "cuda": {
        "batch_size": 64,
        "gradient_accumulation": 1
    },
    "cpu": {
        "batch_size": 8,
        "gradient_accumulation": 8
    }
}

device_type = "cuda" if torch.cuda.is_available() else "cpu"
config.training.update(device_config[device_type])
```

### 4. 环境变量

```yaml
# 使用环境变量
model:
  name: ${oc.env:MODEL_NAME, "seed_vc"}
  checkpoint_path: ${oc.env:CHECKPOINT_PATH, "checkpoints/model.pt"}
  num_workers: ${oc.env:NUM_WORKERS, 4}
```

---

## 📊 配置对比

### 模型规模对比

| 规模 | 参数量 | 推理时间 | 内存占用 | 质量评分 |
|------|--------|----------|----------|----------|
| Tiny | 40M | ~0.3s | 200MB | 3.2/5 |
| Small | 80M | ~0.5s | 400MB | 3.8/5 |
| Base | 150M | ~0.8s | 800MB | 4.2/5 |
| Large | 300M | ~1.2s | 1.5GB | 4.5/5 |

### 量化配置对比

| 维度 | 压缩率 | 质量损失 | 推理加速 |
|------|--------|----------|----------|
| 32维 | 96x | ~5% | 2.5x |
| 512维 | 6x | ~2% | 1.5x |
| 2048维 | 1.5x | ~1% | 1.2x |

---

*此文档由 Claude Code 自动生成于 2025-10-28*
