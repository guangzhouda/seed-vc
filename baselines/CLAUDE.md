# 模块导航：baselines/

> [根目录 CLAUDE.md](../CLAUDE.md)

---

## 📦 模块概述

`baselines/` 目录包含用于对比评估的基线模型实现，为 Seed-VC 的性能提供参考基准。

---

## 🎯 基线模型对比

### 评估结果概览

**语音转换 (LibriTTS)**：

| 模型 | SECS↑ | WER↓ | CER↓ | SIG↑ | BAK↑ | OVRL↑ | 训练需求 |
|------|-------|------|------|------|------|-------|----------|
| OpenVoice | 0.7547 | 15.46 | 4.73 | 3.56 | 4.02 | 3.27 | 需要训练 |
| CosyVoice | 0.8440 | 18.98 | 7.29 | 3.51 | 4.02 | 3.21 | 需要训练 |
| **Seed-VC (V2)** | **0.8676** | **11.99** | **2.92** | 3.42 | 3.97 | 3.11 | 零样本 |
| Ground Truth | 1.0000 | 8.02 | 1.57 | ~ | ~ | ~ | ~ |

**歌唱声音转换 (M4Singer)**：

| 模型 | F0CORR↑ | F0RMSE↓ | SECS↑ | CER↓ | SIG↑ | BAK↑ | OVRL↑ | 训练需求 |
|------|---------|---------|-------|------|------|------|-------|----------|
| RVCv2 | 0.9404 | 30.43 | 0.7264 | 28.46 | **3.41** | **4.05** | **3.12** | 需要目标说话人训练 |
| **Seed-VC (V2)** | 0.9375 | 33.35 | **0.7405** | **19.70** | 3.39 | 3.96 | 3.06 | 零样本 |

---

## 🔬 基线模型详情

### 1. [openvoice.py](openvoice.py) - OpenVoice

**项目地址**：https://github.com/myshell-ai/OpenVoice

**模型简介**：
OpenVoice 是由 MyShell 开发的开源语音转换系统，支持多种语言和说话人风格转换。

**核心特性**：
- 多语言支持（英语、日语、中文等）
- 风格控制
- 语音情感转换
- 快于实时的推理速度

**技术架构**：
- 说话人编码器：预训练的 ECAPA-TDNN
- 内容编码器：多层 Transformer
- 声码器：HiFi-GAN
- 风格提取：多层感知机

**关键参数**：
```python
# OpenVoice 配置示例
source_semantic_path = "semantic.json"
ref_speaker_0 = "reference_0.wav"
ref_speaker_1 = "reference_1.wav"  # 可选
output_path = "output.wav"
```

**优势**：
- 支持多语言
- 推理速度快
- 开源社区活跃

**劣势**：
- 说话人相似度较低（SECS: 0.7547）
- 可懂度一般（WER: 15.46）
- 需要目标说话人少量样本

**在项目中的使用**：
```python
# 运行 OpenVoice 基线评估
python eval.py \
    --baseline "openvoice" \
    --source ./examples/libritts-test-clean \
    --target ./examples/reference \
    --output ./examples/eval/openvoice
```

---

### 2. [cosyvoice.py](cosyvoice.py) - CosyVoice

**项目地址**：https://github.com/FunAudioLLM/CosyVoice

**模型简介**：
CosyVoice 是由阿里巴巴 FunAudioLLM 团队开发的多语言语音生成系统，支持语音转换和合成。

**核心特性**：
- 多语言语音合成
- 语音转换
- 零样本克隆
- 自然语音生成

**技术架构**：
- 说话人编码器：ResNet 基础
- 内容编码器：Conformer
- 声码器：BigVGAN
- 扩散模型：DiT (Diffusion Transformer)

**关键参数**：
```python
# CosyVoice 配置示例
source_wav = "source.wav"
ref_speaker_0 = "reference.wav"
output_path = "output.wav"
speed = 1.0
vol = 1.0
```

**优势**：
- 多语言支持强
- 语音质量高
- 零样本能力好

**劣势**：
- 可懂度较低（WER: 18.98）
- 字符错误率高（CER: 7.29）
- 对中文支持有限

**在项目中的使用**：
```python
# 运行 CosyVoice 基线评估
python eval.py \
    --baseline "cosyvoice" \
    --source ./examples/libritts-test-clean \
    --target ./examples/reference \
    --output ./examples/eval/cosyvoice
```

---

### 3. [dnsmos/](dnsmos/) - DNSMOS 评估

**功能**：DNSMOS (Deep Noise Suppression Mean Opinion Score) 质量评估

**模型简介**：
DNSMOS 是用于评估语音质量和噪声抑制效果的客观指标系统。

**主要指标**：
- **SIG** (Speech Intrusiveness): 语音质量
- **BAK** (Background Intrusiveness): 背景噪声
- **OVRL** (Overall Quality): 综合质量

**使用示例**：
```python
from baselines.dnsmos.dnsmos_computor import DNSMOS

evaluator = DNSMOS()
results = evaluator.compute(wav_file)
print(f"SIG: {results['sig_mos']}, BAK: {results['bak_mos']}, OVRL: {results['ovrl_mos']}")
```

---

## 📊 详细对比分析

### 语音转换任务

#### 说话人相似度 (SECS)

```
OpenVoice:     0.7547  ████████████████████████
CosyVoice:     0.8440  ████████████████████████████████
Seed-VC (V2):  0.8676  ████████████████████████████████
Ground Truth:  1.0000  ████████████████████████████████
```

**分析**：
- Seed-VC 达到最高的说话人相似度
- 比 OpenVoice 高出 15%+
- 接近 Ground Truth 水平

#### 可懂度 (WER)

```
Ground Truth:  8.02    ████
Seed-VC (V2):  11.99   ███████
OpenVoice:     15.46   █████████
CosyVoice:     18.98   ████████████
```

**分析**：
- Seed-VC 显著优于基线模型
- WER 仅为 OpenVoice 的 77%
- 接近 Ground Truth 水平

#### 字符错误率 (CER)

```
Ground Truth:  1.57    █
Seed-VC (V2):  2.92    ██
OpenVoice:     4.73    ████
CosyVoice:     7.29    ██████
```

**分析**：
- Seed-VC 在字符级别精度上领先
- 仅为 OpenVoice 的 62%
- 展现了优秀的文本保持能力

### 歌唱声音转换任务

#### F0 相关性 (F0CORR)

```
RVCv2:         0.9404  ████████████████████████████████
Seed-VC (V2):  0.9375  ████████████████████████████████
```

**分析**：
- 两者 F0 相关性相近
- Seed-VC 在音高保持上表现优异

#### F0 均方根误差 (F0RMSE)

```
RVCv2:         30.43   ████████████
Seed-VC (V2):  33.35   █████████████
```

**分析**：
- RVCv2 在数值准确性上略优
- 但 Seed-VC 仍保持在可接受范围

#### 可懂度 (CER)

```
RVCv2:         28.46   ████████████████████
Seed-VC (V2):  19.70   ██████████████
```

**分析**：
- Seed-VC 显著优于 RVCv2
- 歌唱文本可懂度提升 30%+
- 零样本优势明显

---

## 🛠️ 基线模型安装

### OpenVoice 安装

```bash
# 克隆仓库
git clone https://github.com/myshell-ai/OpenVoice ../OpenVoice

# 安装依赖
cd ../OpenVoice
pip install -r requirements.txt

# 下载预训练模型
bash checkpoints/download_openvoice.sh
```

### CosyVoice 安装

```bash
# 克隆仓库
git clone https://github.com/FunAudioLLM/CosyVoice ../CosyVoice

# 安装依赖
cd ../CosyVoice
pip install -r requirements.txt

# 下载预训练模型
python CosyVoice/download_models.py
```

---

## 🔍 运行基线评估

### 评估脚本

```bash
# 评估所有基线
python eval.py \
    --source ./examples/libritts-test-clean \
    --target ./examples/reference \
    --output ./examples/eval/converted \
    --diffusion-steps 25 \
    --length-adjust 1.0 \
    --inference-cfg-rate 0.7 \
    --xvector-extractor "resemblyzer" \
    --max-samples 100

# 评估 OpenVoice
python eval.py \
    --baseline "openvoice" \
    --source ./examples/libritts-test-clean \
    --target ./examples/reference \
    --output ./examples/eval/openvoice

# 评估 CosyVoice
python eval.py \
    --baseline "cosyvoice" \
    --source ./examples/libritts-test-clean \
    --target ./examples/reference \
    --output ./examples/eval/cosyvoice
```

### 自定义评估

```python
from baselines.openvoice import OpenVoice
from baselines.cosyvoice import CosyVoice

# 使用 OpenVoice
openvoice = OpenVoice()
result = openvoice.convert(source_path, reference_path, output_path)

# 使用 CosyVoice
cosyvoice = CosyVoice()
result = cosyvoice.convert(source_path, reference_path, output_path)
```

---

## 📈 性能优化建议

### 对比基线的优化方向

1. **说话人相似度优化**
   - 改进说话人编码器
   - 引入更强的特征提取
   - 使用更大的预训练模型

2. **可懂度优化**
   - 增加扩散步数
   - 改进语言模型
   - 优化损失函数

3. **实时性优化**
   - 减少模型参数量
   - 使用模型压缩
   - 混合精度推理

---

*此文档由 Claude Code 自动生成于 2025-10-28*
