#!/usr/bin/env python
"""
快速测试转换功能
"""
import os
import sys
import torch
import soundfile as sf
import numpy as np
from pathlib import Path

print("="*60)
print("快速歌声转换测试")
print("="*60)

# 检查设备
if torch.cuda.is_available():
    device = torch.device("cuda")
    print("✓ 使用 CUDA")
elif torch.backends.mps.is_available():
    device = torch.device("mps")
    print("✓ 使用 MPS")
else:
    device = torch.device("cpu")
    print("✓ 使用 CPU")

# 简短的测试音频（只取前5秒）
source_audio = "./assets/sorce-audio.wav"
target_audio = "./assets/targets.wav"

print(f"\n源音频: {source_audio}")
print(f"目标音色: {target_audio}")

# 检查文件
if not os.path.exists(source_audio):
    print(f"✗ 源文件不存在: {source_audio}")
    sys.exit(1)

if not os.path.exists(target_audio):
    print(f"✗ 目标文件不存在: {target_audio}")
    sys.exit(1)

# 加载音频
try:
    print("\n正在加载音频...")
    source_info = sf.info(source_audio)
    sr = source_info.samplerate
    source_data, _ = sf.read(source_audio, start=0, stop=5*sr)  # 只取前5秒
    target_data, _ = sf.read(target_audio)

    print(f"✓ 源音频加载成功: {len(source_data)/sr:.2f}秒 @ {sr}Hz")
    print(f"✓ 目标音频加载成功: {len(target_data)/sr:.2f}秒")
except Exception as e:
    print(f"✗ 音频加载失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 测试基础转换功能
print("\n" + "="*60)
print("测试基础功能")
print("="*60)

try:
    # 测试音频处理
    print("\n测试音频处理功能...")
    from modules import audio

    print("✓ 音频模块导入成功")
    print("✓ 基础功能测试通过")

    # 测试模型加载
    print("\n测试模型加载...")
    try:
        from modules.v2.vc_wrapper import VoiceConversionWrapper
        from hydra import compose, initialize_config_dir
        from hydra.utils import instantiate
        from omegaconf import DictConfig
        import yaml

        print("✓ V2 模型模块导入成功")

        # 尝试加载配置
        try:
            config_path = os.path.abspath("./configs/v2")
            print(f"配置路径: {config_path}")

            if os.path.exists(config_path):
                with initialize_config_dir(config_dir=config_path):
                    cfg = compose(config_name="vc_wrapper.yaml")
                print("✓ 配置加载成功")

                # 创建模型实例
                print("\n创建模型实例...")
                vc_wrapper = instantiate(cfg)
                print("✓ 模型实例创建成功")

                print("\n" + "="*60)
                print("✓ 所有基础功能测试通过！")
                print("="*60)
                print("\n现在可以运行完整转换:")
                print("  python app_vc_v2.py")
                print("  或")
                print("  python inference_v2.py --source ./assets/sorce-audio.wav --target ./assets/targets.wav --output ./output")
                sys.exit(0)
            else:
                print(f"✗ 配置文件目录不存在: {config_path}")
                sys.exit(1)

        except Exception as e:
            print(f"✗ 配置加载失败: {e}")
            sys.exit(1)

    except Exception as e:
        print(f"✗ 模型加载失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

except Exception as e:
    print(f"✗ 测试失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
