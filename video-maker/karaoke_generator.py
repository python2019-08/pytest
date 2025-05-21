"""
Whisper CLI中的`--output-srt`或`--output-vtt`选项可生成字幕文件，这些文件可用于制作卡拉OK视频。以下是具体步骤和示例：


### 1. **生成字幕文件**
使用Whisper CLI生成SRT或VTT格式的字幕：
```bash
whisper audio.mp3 --model medium --output-srt
# 或生成VTT格式
whisper audio.mp3 --model medium --output-vtt
```
这将生成`audio.srt`或`audio.vtt`文件，包含精确的时间戳和歌词。




### 3. **使用方法**
1. **安装依赖**：
   ```bash
   pip install ffmpeg-python  # 用于调用FFmpeg
   ```

2. **基本用法**：
   ```bash
   python karaoke_generator.py --audio audio.mp3 --subtitle audio.srt
   ```

3. **高级选项**：
   ```bash
   # 指定输出文件名
   python karaoke_generator.py --audio audio.mp3 --subtitle audio.srt --output karaoke.mp4

   # 使用图片作为背景
   python karaoke_generator.py --audio audio.mp3 --subtitle audio.srt --background bg.jpg

   # 使用视频作为背景
   python karaoke_generator.py --audio audio.mp3 --subtitle audio.srt --background bg_video.mp4
   ```


### 4. **效果说明**
- 脚本会将Whisper生成的精确字幕逐行显示在视频上
- 支持自定义背景（纯色、图片或视频）
- 字幕样式可通过修改`force_style`参数调整（字体、颜色、大小等）


### 5. **注意事项**
- 需要预先安装FFmpeg（确保命令行可调用）
- 字幕文件必须与音频匹配
- 视频分辨率默认为1920×1080，可在脚本中修改
- 如需更复杂的效果（如歌词逐字变色），可扩展脚本中的滤镜设置
"""

import os
import subprocess
import argparse
from pathlib import Path

def create_karaoke_video(audio_file, subtitle_file, output_file=None, background=None):
    """
    基于Whisper生成的字幕文件创建卡拉OK视频
    
    参数:
        audio_file: 输入音频文件路径
        subtitle_file: 字幕文件路径(SRT/VTT)
        output_file: 输出视频文件名，默认为音频文件名+_karaoke.mp4
        background: 背景图片/视频路径，默认为黑色背景
    """
    # 设置输出文件名
    if not output_file:
        splitRet =os.path.splitext(audio_file)
        print(splitRet)

        base_name = os.path.splitext(audio_file)[0]
        output_file = f"{base_name}_karaoke.mp4"
    
    # 确定字幕格式
    subtitle_ext = os.path.splitext(subtitle_file)[1].lower()
    subtitle_format = "srt" if subtitle_ext == ".srt" else "webvtt" if subtitle_ext == ".vtt" else ""
    
    if not subtitle_format:
        raise ValueError("不支持的字幕格式，仅支持SRT和VTT")
    
    # 构建FFmpeg命令
    cmd = [
        "ffmpeg",
        "-y",  # 覆盖已存在的文件
        "-i", audio_file,  # 输入音频
    ]
    
    # 添加背景
    if background:
        if background.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            # 图片背景
            cmd.extend(["-loop", "1", "-i", background])
            # 设置图片持续时间为音频长度
            cmd.extend(["-t", f"{get_audio_duration(audio_file)}"])
        else:
            # 视频背景
            cmd.extend(["-i", background])
    else:
        # 默认黑色背景
        cmd.extend([
            "-f", "lavfi", 
            "-i", "color=c=black:s=1920x1080:d=" + str(get_audio_duration(audio_file))
        ])
    
    # 添加字幕滤镜
    title = "网坟奇文"
    cmd.extend([
        "-filter_complex",
        f"scale=1920:1080[scaled];\
            [scaled]drawtext=text='{title}':fontsize=36: \
                   fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2:enable='between(t,0,0)'[text],\
           [text]subtitles={os.path.abspath(subtitle_file)}:\
            force_style='Fontsize=36,PrimaryColour=&HFFFFFF,OutlineColour=&H0,BackColour=&H80000000,MarginV=50,Alignment=2'[outv]" 
    ])

# ffmpeg -i input.mp4 \
#   -filter_complex "[0:v]scale=1920:1080[scaled]; \
#                    [scaled]drawtext=text='':fontsize=36:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2:enable='between(t,0,0)'[text]; \
#                    [text]subtitles=story_male_cn.wav.srt:force_style='Fontsize=36,PrimaryColour=&HFFFFFF,OutlineColour=&H0,BackColour=&H80000000,MarginV=50,Alignment=2'[outv]" \
#   -map "[outv]" -map 0:a \
#   output.mp4
# ffmpeg -loop 1 -i "$image_pattern" -i "$midFile_mp3" -i "$midFile_whisper_srt" \
#   -c:v libx264 -s 1920x1080 -pix_fmt yuv420p -c:a aac -b:a 192k \
#   -vf "scale=1920:1080:\
#        force_original_aspect_ratio=decrease,\
#        pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,\
#        subtitles=$midFile_whisper_srt:\
#        force_style='Fontname=SimHei,Fontsize=28,PrimaryColour=&HFFFFFF&,Outline=2,Shadow=1.5'" \
#   -shortest "$midFile_video"  

# ffmpeg -i input.mp4 \
#   -filter_complex "[0:v]scale=1920:1080[scaled]; \
#                    [scaled]drawtext=text='':fontsize=36:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2:enable='between(t,0,0)'[text]; \
#                    [text]subtitles=story_male_cn.wav.srt:force_style='Fontsize=36,PrimaryColour=&HFFFFFF,OutlineColour=&H0,BackColour=&H80000000,MarginV=50,Alignment=2'[outv]" \
#   -map "[outv]" -map 0:a \
#   output.mp4
    
    # 设置输出参数
    cmd.extend([
        "-map", "[outv]",
        "-map", "0:a",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_file
    ])
    
    # 执行命令
    print("正在生成卡拉OK视频...")
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)
    print(f"卡拉OK视频已生成: {output_file}")

def get_audio_duration(audio_file):
    """获取音频文件的时长（秒）"""
    result = subprocess.run(
        [
            "ffprobe", 
            "-v", "error", 
            "-show_entries", "format=duration", 
            "-of", "default=noprint_wrappers=1:nokey=1",
            audio_file
        ],
        capture_output=True,
        text=True
    )
    return float(result.stdout.strip())

def main():
    parser = argparse.ArgumentParser(description='基于Whisper字幕生成卡拉OK视频')
    parser.add_argument('--audio', required=True, help='输入音频文件')
    parser.add_argument('--subtitle', required=True, help='字幕文件(SRT/VTT)')
    parser.add_argument('--output', help='输出视频文件')
    parser.add_argument('--background', help='背景图片或视频')
    
    args = parser.parse_args()
    create_karaoke_video(args.audio, args.subtitle, args.output, args.background)

if __name__ == "__main__":
    main()    