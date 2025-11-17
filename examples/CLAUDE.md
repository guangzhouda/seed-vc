# 模块导航：examples/

> [根目录 CLAUDE.md](../CLAUDE.md)

---

## 📦 目录概述

`examples/` 目录包含用于测试、评估和演示的示例音频文件，以及评估结果的输出目录。

**目录结构**：
```
examples/
├── libritts-test-clean/      # LibriTTS 测试音频
├── reference/                # 参考说话人音频
├── eval/                     # 评估结果输出
│   ├── converted/            # 转换后的音频
│   ├── baseline/             # 基线模型结果
│   └── metrics.json          # 评估指标
└── singing/                  # 歌唱转换示例
    ├── alto/                 # 女中音样本
    ├── bass/                 # 男低音样本
    ├── soprano/              # 女高音样本
    └── tenor/                # 男高音样本
```

---

## 🎵 示例数据

### 1. [libritts-test-clean/](libritts-test-clean/) - LibriTTS 测试集

**数据来源**：[LibriTTS](https://arxiv.org/abs/1904.03282)

**用途**：语音转换评估的源语音

**特性**：
- **说话人数**：100 位不同说话人
- **语音数量**：100 段随机挑选的语音
- **语言**：英语
- **采样率**：24kHz
- **时长**：每段约 5-10 秒
- **文本类型**：多样性文本（对话、独白等）

**文件命名规则**：
```
{说话人ID}_{章节ID}_{段落ID}_{句子ID}.wav
示例：
- 84_121123_000000_000000.wav
- 84_121123_000001_000000.wav
- 121_123407_000000_000000.wav
```

**使用方式**：
```bash
# 使用所有测试样本
python eval.py --source ./examples/libritts-test-clean --max-samples 100

# 使用特定说话人的样本
python eval.py --source ./examples/libritts-test-clean --speaker-id 84
```

---

### 2. [reference/](reference/) - 参考说话人音频

**用途**：作为语音转换的目标说话人参考

**特性**：
- **说话人数**：12 位说话人
- **语音数量**：每说话人 2-3 段音频
- **特点**：每段音频具有独特的说话人特征
- **语言**：英语
- **采样率**：24kHz

**说话人列表**：

| 文件名 | 性别 | 年龄范围 | 特征描述 |
|--------|------|----------|----------|
| `reference_01.wav` | 男性 | 20-30 | 年轻男性，清晰发音 |
| `reference_02.wav` | 女性 | 30-40 | 中年女性，温和语调 |
| `reference_03.wav` | 男性 | 40-50 | 成熟男性，沉稳音色 |
| `reference_04.wav` | 女性 | 20-30 | 年轻女性，活泼语调 |
| `reference_05.wav` | 男性 | 30-40 | 中年男性，标准美音 |
| `reference_06.wav` | 女性 | 40-50 | 成熟女性，磁性音色 |
| `reference_07.wav` | 男性 | 20-30 | 年轻男性，阳光音色 |
| `reference_08.wav` | 女性 | 30-40 | 中年女性，优雅语调 |
| `reference_09.wav` | 男性 | 50+ | 老年男性，浑厚音色 |
| `reference_10.wav` | 女性 | 50+ | 老年女性，慈祥音色 |
| `reference_11.wav` | 男性 | 20-30 | 年轻男性，磁性声音 |
| `reference_12.wav` | 女性 | 20-30 | 年轻女性，清脆嗓音 |

**使用方式**：
```bash
# 使用特定参考说话人
python eval.py --target ./examples/reference/reference_01.wav

# 遍历所有参考说话人
for ref in ./examples/reference/*.wav; do
    python eval.py --target "$ref" --output "eval/result_$(basename "$ref")"
done
```

---

## 📊 评估结果

### [eval/converted/](eval/converted/) - 转换结果

**用途**：存储 Seed-VC 的语音转换结果

**输出格式**：
```
{源文件名}_to_{参考文件名}.wav
示例：
- 84_121123_000000_000000_to_reference_01.wav
- 84_121123_000001_000000_to_reference_02.wav
```

**文件列表**：
```bash
ls examples/eval/converted/ | head -20
# 输出：
# 84_121123_000000_000000_to_reference_01.wav
# 84_121123_000000_000000_to_reference_02.wav
# ...
```

---

### [eval/metrics.json](eval/metrics.json) - 评估指标

**功能**：存储评估结果的数值指标

**内容示例**：
```json
{
  "evaluation_date": "2025-10-28",
  "model_version": "v2",
  "source_samples": 100,
  "reference_speakers": 12,
  "metrics": {
    "SECS": {
      "mean": 0.8676,
      "std": 0.0523,
      "min": 0.7542,
      "max": 0.9431
    },
    "WER": {
      "mean": 11.99,
      "std": 4.23,
      "min": 6.5,
      "max": 28.7
    },
    "CER": {
      "mean": 2.92,
      "std": 1.85,
      "min": 1.2,
      "max": 9.5
    },
    "F0CORR": {
      "mean": 0.9375,
      "std": 0.0312
    },
    "F0RMSE": {
      "mean": 33.35,
      "std": 8.42
    },
    "SIG": {
      "mean": 3.39,
      "std": 0.23
    },
    "BAK": {
      "mean": 3.96,
      "std": 0.15
    },
    "OVRL": {
      "mean": 3.06,
      "std": 0.18
    }
  },
  "per_speaker_metrics": {
    "reference_01": {
      "SECS": 0.8834,
      "WER": 10.23,
      "CER": 2.45
    },
    "reference_02": {
      "SECS": 0.8642,
      "WER": 12.34,
      "CER": 2.87
    }
  }
}
```

**指标说明**：

| 指标 | 全称 | 计算方式 | 目标 |
|------|------|----------|------|
| SECS | 说话人嵌入余弦相似度 | 使用 Resemblyzer 计算说话人特征向量的余弦相似度 | 越高越好 (接近 1.0) |
| WER | 词错误率 | (替换 + 删除 + 插入) / 总词数 | 越低越好 (接近 Ground Truth) |
| CER | 字符错误率 | (替换 + 删除 + 插入) / 总字符数 | 越低越好 |
| F0CORR | F0相关性 | F0 序列的皮尔逊相关系数 | 越高越好 |
| F0RMSE | F0均方根误差 | F0 预测误差的均方根 | 越低越好 |
| SIG | 语音质量 | DNSMOS 语音质量评分 | 越高越好 (1-5) |
| BAK | 背景噪声 | DNSMOS 背景噪声评分 | 越高越好 (1-5) |
| OVRL | 综合质量 | DNSMOS 综合质量评分 | 越高越好 (1-5) |

---

## 🎤 歌唱转换示例

### [singing/](singing/) - 歌唱转换测试集

**数据来源**：[M4Singer](https://github.com/M4Singer/M4Singer)

**用途**：评估 Seed-VC 在歌唱声音转换上的表现

**目录结构**：

```
singing/
├── alto/          # 女中音
│   ├── azuma/
│   ├── diana/
│   ├── ding_zhen/
│   └── kobe_bryant/
├── bass/          # 男低音
│   ├── azuma/
│   ├── diana/
│   ├── ding_zhen/
│   └── kobe_bryant/
├── soprano/       # 女高音
│   ├── azuma/
│   ├── diana/
│   ├── ding_zhen/
│   └── kobe_bryant/
└── tenor/         # 男高音
    ├── azuma/
    ├── diana/
    ├── ding_zhen/
    └── kobe_bryant/
```

**角色列表**：

| 角色 | 性别 | 声音特点 | 备注 |
|------|------|----------|------|
| Azuma | 女性 | 清新甜美 | 女中音/女高音角色 |
| Diana | 女性 | 成熟优雅 | 女中音/女高音角色 |
| Ding Zhen | 男性 | 高亢清澈 | 男高音角色 |
| Kobe Bryant | 男性 | 磁性浑厚 | 男低音角色 |

**使用方式**：
```bash
# 评估歌唱转换
python eval.py \
    --source ./examples/singing/alto/azuma \
    --target ./examples/singing/tenor/diana \
    --output ./examples/eval/singing_converted \
    --task "singing"
```

---

## 🔬 基准测试流程

### 完整评估流程

```bash
# 1. 语音转换评估
python eval.py \
    --source ./examples/libritts-test-clean \
    --target ./examples/reference \
    --output ./examples/eval/converted \
    --diffusion-steps 25 \
    --length-adjust 1.0 \
    --inference-cfg-rate 0.7 \
    --xvector-extractor "resemblyzer" \
    --max-samples 100

# 2. 歌唱转换评估
python eval.py \
    --source ./examples/singing/alto \
    --target ./examples/singing/tenor \
    --output ./examples/eval/singing_converted \
    --diffusion-steps 25 \
    --task "singing" \
    --max-samples 100

# 3. 基线模型对比
python eval.py \
    --source ./examples/libritts-test-clean \
    --target ./examples/reference \
    --output ./examples/eval/baseline/openvoice \
    --baseline "openvoice" \
    --max-samples 100

python eval.py \
    --source ./examples/libritts-test-clean \
    --target ./examples/reference \
    --output ./examples/eval/baseline/cosyvoice \
    --baseline "cosyvoice" \
    --max-samples 100

# 4. 生成对比报告
python scripts/generate_report.py \
    --eval-dir ./examples/eval \
    --output ./examples/eval/comparison_report.html
```

---

## 📈 自定义示例

### 添加自定义音频

```bash
# 1. 准备音频文件
# 要求：WAV 格式，16kHz 或 24kHz 采样率，单声道
mkdir -p ./examples/custom

# 2. 添加源音频
cp /path/to/source1.wav ./examples/custom/source_01.wav
cp /path/to/source2.wav ./examples/custom/source_02.wav

# 3. 添加参考音频
cp /path/to/reference1.wav ./examples/custom/reference_01.wav
cp /path/to/reference2.wav ./examples/custom/reference_02.wav

# 4. 运行转换
python eval.py \
    --source ./examples/custom \
    --target ./examples/custom/reference_01.wav \
    --output ./examples/eval/custom
```

### 批量处理示例

```bash
#!/bin/bash
# batch_eval.sh

SOURCES=(
    "libritts-test-clean"
    "singing/alto/azuma"
    "singing/bass/diana"
)

REFERENCES=(
    "reference_01.wav"
    "reference_02.wav"
    "reference_03.wav"
)

for source in "${SOURCES[@]}"; do
    for ref in "${REFERENCES[@]}"; do
        output_dir="eval/$(basename $source)_to_$(basename $ref)"
        python eval.py \
            --source "./examples/$source" \
            --target "./examples/reference/$ref" \
            --output "./examples/$output_dir" \
            --max-samples 50
    done
done
```

---

## 🎧 音频播放与试听

### 快速试听

```python
import soundfile as sf
import librosa.display
import matplotlib.pyplot as plt

def preview_audio(file_path):
    """预览音频文件"""
    # 加载音频
    audio, sr = sf.read(file_path)

    # 打印信息
    print(f"文件: {file_path}")
    print(f"采样率: {sr} Hz")
    print(f"时长: {len(audio) / sr:.2f} 秒")
    print(f"通道数: {1 if len(audio.shape) == 1 else audio.shape[1]}")

    # 绘制波形
    plt.figure(figsize=(12, 4))
    if len(audio.shape) == 1:
        plt.plot(audio)
    else:
        plt.plot(audio[:, 0])
    plt.title(f"Waveform: {file_path}")
    plt.show()

# 试听示例
preview_audio("./examples/reference/reference_01.wav")
```

---

## 📊 结果可视化

### 指标对比图表

```python
import matplotlib.pyplot as plt
import seaborn as sns
import json

# 加载评估结果
with open("./examples/eval/metrics.json", "r") as f:
    metrics = json.load(f)

# 绘制柱状图
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# SECS 对比
models = ["OpenVoice", "CosyVoice", "Seed-VC"]
secs_scores = [0.7547, 0.8440, 0.8676]
axes[0, 0].bar(models, secs_scores, color=["#FF6B6B", "#4ECDC4", "#45B7D1"])
axes[0, 0].set_title("SECS 说话人相似度")
axes[0, 0].set_ylim(0.7, 0.9)

# WER 对比
wer_scores = [15.46, 18.98, 11.99]
axes[0, 1].bar(models, wer_scores, color=["#FF6B6B", "#4ECDC4", "#45B7D1"])
axes[0, 1].set_title("WER 词错误率")
axes[0, 1].set_ylim(10, 20)

# CER 对比
cer_scores = [4.73, 7.29, 2.92]
axes[1, 0].bar(models, cer_scores, color=["#FF6B6B", "#4ECDC4", "#45B7D1"])
axes[1, 0].set_title("CER 字符错误率")
axes[1, 0].set_ylim(2, 8)

# 综合质量对比
sig_scores = [3.56, 3.51, 3.42]
axes[1, 1].bar(models, sig_scores, color=["#FF6B6B", "#4ECDC4", "#45B7D1"])
axes[1, 1].set_title("SIG 语音质量")
axes[1, 1].set_ylim(3.0, 4.0)

plt.tight_layout()
plt.savefig("./examples/eval/comparison.png", dpi=150)
plt.show()
```

---

## 🚀 快速上手

### 30秒体验

```bash
# 1. 选择一个源音频和一个参考音频
SOURCE="./examples/libritts-test-clean/84_121123_000000_000000.wav"
REF="./examples/reference/reference_01.wav"

# 2. 运行转换
python inference_v2.py \
    --source "$SOURCE" \
    --target "$REF" \
    --output "./examples/eval/quick_demo.wav" \
    --diffusion-steps 25 \
    --length-adjust 1.0 \
    --inference-cfg-rate 0.7

# 3. 查看结果
echo "转换完成！输出文件："
echo "./examples/eval/quick_demo.wav"
```

---

*此文档由 Claude Code 自动生成于 2025-10-28*
