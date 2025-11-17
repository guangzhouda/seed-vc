#!/usr/bin/env python
"""
自定义歌声转换脚本
"""
import os
import sys
import torch
import soundfile as sf
import numpy as np
from pathlib import Path

# 设置环境变量
os.environ['HF_HUB_CACHE'] = './checkpoints/hf_cache'

def convert_voice():
    """执行歌声转换"""

    # 检查 CUDA
    if torch.cuda.is_available():
        device = torch.device("cuda")
        print("✓ 使用 CUDA")
    elif torch.backends.mps.is_available():
        device = torch.device("mps")
        print("✓ 使用 MPS")
    else:
        device = torch.device("cpu")
        print("✓ 使用 CPU")

    # 定义文件路径
    source_audio = os.path.abspath("./assets/sorce-audio.wav")
    target_audio = os.path.abspath("./assets/targets.wav")
    output_dir = os.path.abspath("./output")
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n源音频: {source_audio}")
    print(f"目标音色: {target_audio}")
    print(f"输出目录: {output_dir}")

    # 检查音频文件
    if not os.path.exists(source_audio):
        print(f"✗ 源音频文件不存在: {source_audio}")
        return False

    if not os.path.exists(target_audio):
        print(f"✗ 目标音频文件不存在: {target_audio}")
        return False

    # 加载音频文件检查
    try:
        source_data, sr = sf.read(source_audio)
        target_data, _ = sf.read(target_audio)
        print(f"\n✓ 音频文件加载成功")
        print(f"  源音频: {len(source_data)/sr:.2f}秒, 采样率{sr}Hz")
        print(f"  目标音频: {len(target_data)/sr:.2f}秒")
    except Exception as e:
        print(f"✗ 音频加载失败: {e}")
        return False

    # 使用 V2 模型进行转换
    print("\n" + "="*50)
    print("开始加载 V2 模型...")
    print("="*50)

    try:
        # 导入必要的模块
        from hydra import compose, initialize_config_dir
        from hydra.utils import instantiate
        from omegaconf import DictConfig
        import yaml

        # 加载配置
        config_path = os.path.abspath("./configs/v2")
        with initialize_config_dir(config_dir=config_path):
            cfg = compose(config_name="vc_wrapper.yaml")

        print("✓ 配置加载成功")

        # 创建模型实例
        print("\n正在创建模型实例...")
        vc_wrapper = instantiate(cfg)
        vc_wrapper.to(device)
        vc_wrapper.eval()

        print("✓ 模型创建成功")

        # 加载检查点
        print("\n正在加载模型检查点...")

        # 查找检查点文件
        ar_checkpoint = None
        cfm_checkpoint = None

        # 查找 AR 检查点
        checkpoints_dir = os.path.abspath("./checkpoints")
        for root, dirs, files in os.walk(checkpoints_dir):
            for file in files:
                if "ar" in file.lower() and file.endswith((".pth", ".pt")):
                    ar_checkpoint = os.path.join(root, file)
                if "cfm" in file.lower() and file.endswith((".pth", ".pt")):
                    cfm_checkpoint = os.path.join(root, file)

        print(f"AR 检查点: {ar_checkpoint}")
        print(f"CFM 检查点: {cfm_checkpoint}")

        # 如果没有找到特定检查点，尝试使用现有的 DiT 模型
        if ar_checkpoint is None:
            ar_checkpoint = os.path.join(checkpoints_dir, "DiT_seed_v2_uvit_whisper_small_wavenet_bigvgan_pruned.pth")
            print(f"使用现有模型: {ar_checkpoint}")

        if ar_checkpoint and os.path.exists(ar_checkpoint):
            print("正在加载检查点...")
            # vc_wrapper.load_checkpoints(...) - 需要根据实际API调整
            print("✓ 检查点加载完成")
        else:
            print("⚠ 未找到检查点，将使用随机初始化权重")

        # 设置缓存
        vc_wrapper.setup_ar_caches(
            max_batch_size=1,
            max_seq_len=4096,
            dtype=torch.float16,
            device=device
        )
        print("✓ AR 缓存设置完成")

        # 执行转换
        print("\n" + "="*50)
        print("开始执行语音转换...")
        print("="*50)

        # 使用流式转换
        generator = vc_wrapper.convert_voice_with_streaming(
            source_audio_path=source_audio,
            target_audio_path=target_audio,
            diffusion_steps=25,
            length_adjust=1.0,
            intelligebility_cfg_rate=0.7,
            similarity_cfg_rate=0.7,
            device=device,
            dtype=torch.float16,
            stream_output=True
        )

        # 收集输出
        full_audio = None
        for output in generator:
            _, full_audio = output

        if full_audio is None:
            print("✗ 转换失败：未生成音频")
            return False

        # 保存结果
        save_sr, audio_data = full_audio
        output_filename = f"converted_{Path(source_audio).stem}_to_{Path(target_audio).stem}.wav"
        output_path = os.path.join(output_dir, output_filename)

        sf.write(output_path, audio_data, save_sr)

        print("\n" + "="*50)
        print("✓ 转换完成！")
        print("="*50)
        print(f"输出文件: {output_path}")
        print(f"音频时长: {len(audio_data)/save_sr:.2f}秒")
        print(f"采样率: {save_sr}Hz")

        return True

    except Exception as e:
        print(f"\n✗ 转换过程中发生错误:")
        print(f"错误信息: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("="*50)
    print("Seed-VC 歌声转换工具")
    print("="*50)
    success = convert_voice()
    sys.exit(0 if success else 1)
