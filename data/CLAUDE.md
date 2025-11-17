# 模块导航：data/

> [根目录 CLAUDE.md](../CLAUDE.md)

---

## 📦 模块概述

`data/` 目录包含数据集处理和微调相关的数据加载器、数据增强和预处理工具。

---

## 📊 数据集支持

### 支持的数据集

| 数据集 | 用途 | 说话人数量 | 语言 | 采样率 |
|--------|------|------------|------|--------|
| LibriTTS | 训练/评估 | 1k+ | 英语 | 24kHz |
| M4Singer | 歌唱评估 | 4 | 中文 | 44.1kHz |
| 自定义数据集 | 微调 | 可配置 | 多语言 | 可配置 |

### 数据格式

**支持的音频格式**：
- WAV (推荐)
- FLAC
- MP3
- OGG

**数据组织**：
```
data/
├── train/
│   ├── speaker1/
│   │   ├── utt1.wav
│   │   ├── utt2.wav
│   │   └── ...
│   └── speaker2/
│       └── ...
├── val/
└── test/
```

---

## 🔧 数据处理工具

### [ft_dataset.py](ft_dataset.py) - 微调数据集

**功能**：为模型微调提供数据加载和处理能力

**主要特性**：
- 多说话人数据加载
- 说话人均衡采样
- 音频预处理
- 数据增强
- 批处理支持

**关键类**：
- `FineTuningDataset`: 微调数据集类
- `DataLoader`: 数据加载器
- `Collator`: 数据整理器

**使用示例**：
```python
from data.ft_dataset import FineTuningDataset

# 创建数据集
dataset = FineTuningDataset(
    data_dir="data/train",
    sample_rate=24000,
    segment_length=48000,
    hop_length=256,
    speaker2id_path="speaker2id.json"
)

# 加载数据
dataloader = torch.utils.data.DataLoader(
    dataset,
    batch_size=32,
    shuffle=True,
    num_workers=4,
    pin_memory=True
)
```

**参数说明**：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| data_dir | str | 必需 | 数据目录路径 |
| sample_rate | int | 24000 | 目标采样率 |
| segment_length | int | 48000 | 音频段长度 |
| hop_length | int | 256 | 跳跃长度 |
| speaker2id_path | str | None | 说话人ID映射 |
| use_aug | bool | False | 是否使用数据增强 |

---

## 📋 数据预处理流程

### 1. 音频加载

```python
def load_audio(file_path, target_sr=24000):
    """加载音频文件并转换采样率"""
    # 加载音频
    audio, sr = librosa.load(file_path, sr=None)

    # 转换采样率
    if sr != target_sr:
        audio = librosa.resample(audio, orig_sr=sr, target_sr=target_sr)

    # 归一化
    audio = audio / np.max(np.abs(audio))

    return audio
```

### 2. 音频分段

```python
def segment_audio(audio, segment_length=48000):
    """将音频分割为固定长度段"""
    if len(audio) < segment_length:
        # 填充
        padding = segment_length - len(audio)
        audio = np.pad(audio, (0, padding), mode='constant')
    else:
        # 随机截取
        start = np.random.randint(0, len(audio) - segment_length + 1)
        audio = audio[start:start + segment_length]

    return audio
```

### 3. 特征提取

```python
def extract_features(audio, sr=24000):
    """提取音频特征"""
    # 提取 F0
    f0 = extract_f0(audio, sr)

    # 提取梅尔频谱
    mel = librosa.feature.melspectrogram(
        y=audio,
        sr=sr,
        n_mels=80,
        hop_length=256,
        win_length=1024
    )

    # 转换为对数梅尔频谱
    mel = librosa.power_to_db(mel)

    return {
        'audio': audio,
        'f0': f0,
        'mel': mel
    }
```

---

## 🎭 数据增强

### 支持的数据增强

| 增强类型 | 方法 | 参数 | 效果 |
|----------|------|------|------|
| 音量增强 | 随机增益 | gain_range=(0.7, 1.3) | 提高鲁棒性 |
| 噪声增强 | 添加噪声 | snr_range=(20, 40) dB | 抗噪训练 |
| 时移增强 | 时间平移 | shift_range=0.1 | 位置不变性 |
| 音高增强 | 音高偏移 | pitch_range=±2 semitone | F0 鲁棒性 |
| 语速增强 | 语速变化 | speed_range=(0.9, 1.1) | 语速适应 |

### 数据增强示例

```python
from data.augmentation import TimeShift, PitchShift, SpeedChange

# 定义增强管道
augmentations = [
    TimeShift(shift_prob=0.3, max_shift=0.1),
    PitchShift(pitch_prob=0.2, max_shift=2),
    SpeedChange(speed_prob=0.2, speed_range=(0.9, 1.1)),
    VolumeJitter(vol_prob=0.3, gain_range=(0.7, 1.3)),
    AddNoise(noise_prob=0.1, snr_range=(20, 40))
]

# 应用增强
def apply_augmentation(audio, features):
    for aug in augmentations:
        audio, features = aug(audio, features)
    return audio, features
```

---

## 🔄 数据平衡

### 说话人均衡

```python
def balance_speakers(dataset, min_utterances=100):
    """均衡说话人数据分布"""
    speaker_counts = {}
    for idx in range(len(dataset)):
        speaker = dataset.speakers[idx]
        speaker_counts[speaker] = speaker_counts.get(speaker, 0) + 1

    # 识别数据不足的说话人
    under_represented = [
        spk for spk, count in speaker_counts.items()
        if count < min_utterances
    ]

    # 对不足的说话人进行过采样
    balanced_indices = []
    for spk in under_represented:
        indices = dataset.get_speaker_indices(spk)
        balanced_indices.extend(indices * (min_utterances // len(indices) + 1))

    return balanced_indices
```

---

## 📁 数据集创建

### 创建自定义数据集

```python
import json
from pathlib import Path

def create_dataset_metadata(data_dir, output_path):
    """创建数据集元数据"""
    metadata = {
        "sample_rate": 24000,
        "channels": 1,
        "format": "wav",
        "speakers": {}
    }

    # 扫描数据目录
    for speaker_dir in Path(data_dir).iterdir():
        if speaker_dir.is_dir():
            speaker_id = speaker_dir.name
            audio_files = list(speaker_dir.glob("*.wav"))

            metadata["speakers"][speaker_id] = {
                "utterances": len(audio_files),
                "files": [str(f) for f in audio_files],
                "total_duration": sum(get_duration(f) for f in audio_files)
            }

    # 保存元数据
    with open(output_path, 'w') as f:
        json.dump(metadata, f, indent=2)

# 使用
create_dataset_metadata("data/train", "data/metadata.json")
```

---

## 📊 数据统计

### 数据集统计信息

```python
def dataset_statistics(dataset):
    """计算数据集统计信息"""
    stats = {
        "num_speakers": len(dataset.speakers),
        "num_utterances": len(dataset),
        "total_duration": 0,
        "avg_duration": 0,
        "min_duration": float('inf'),
        "max_duration": 0,
        "sampling_rate": dataset.sample_rate
    }

    for idx in range(len(dataset)):
        audio = dataset[idx]['audio']
        duration = len(audio) / dataset.sample_rate

        stats["total_duration"] += duration
        stats["min_duration"] = min(stats["min_duration"], duration)
        stats["max_duration"] = max(stats["max_duration"], duration)

    stats["avg_duration"] = stats["total_duration"] / len(dataset)

    return stats

# 打印统计信息
stats = dataset_statistics(dataset)
print(f"说话人数量: {stats['num_speakers']}")
print(f"语音段数: {stats['num_utterances']}")
print(f"总时长: {stats['total_duration']:.2f} 秒")
print(f"平均时长: {stats['avg_duration']:.2f} 秒")
```

---

## 🎯 微调最佳实践

### 数据准备指南

1. **数据质量**
   - 使用清晰无噪的语音
   - 确保采样率一致
   - 移除过短(<1秒)或过长(>30秒)的音频

2. **说话人平衡**
   - 每个说话人至少 100 段语音
   - 保持时长分布均匀
   - 包含不同情感和语调

3. **数据增强**
   - 适度使用增强（不超过 30%）
   - 针对特定场景定制增强策略
   - 记录增强参数

4. **验证集划分**
   - 80% 训练 / 10% 验证 / 10% 测试
   - 保持说话人分布一致
   - 使用真实语音作为验证集

### 微调配置示例

```yaml
# config/finetune.yaml
data:
  train_dir: "data/train"
  val_dir: "data/val"
  batch_size: 32
  segment_length: 48000
  sample_rate: 24000
  num_workers: 4

  augmentation:
    time_shift: true
    pitch_shift: true
    volume_jitter: true
    add_noise: false

model:
  pretrained_path: "checkpoints/pretrained_v2.pt"
  freeze_encoder: false
  learning_rate: 1e-4
  weight_decay: 1e-5

training:
  epochs: 100
  save_interval: 10
  eval_interval: 5
  gradient_clip: 1.0
```

---

## 🚀 性能优化

### 数据加载优化

```python
# 使用预取缓冲区
dataloader = DataLoader(
    dataset,
    batch_size=32,
    num_workers=4,
    pin_memory=True,
    persistent_workers=True,
    prefetch_factor=2
)

# 缓存特征
dataset.cache_features = True
dataset.cache_dir = "data/cache"

# 内存映射
dataset.use_memory_map = True
dataset.map_file = "data/audios.dat"
```

---

*此文档由 Claude Code 自动生成于 2025-10-28*
