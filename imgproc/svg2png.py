# 使用 `cairosvg`（轻量、跨平台）
# 这是最常用的 SVG 转 PNG 库，安装和使用都很简单，适合大多数场景。

#### 1. 安装依赖
# 首先需要安装库和依赖（Windows/macOS/Linux 通用）：

# 安装 cairosvg 核心库
# pip install cairosvg

# 如果是 Linux 系统，需先安装系统依赖（可选但建议）
# sudo apt-get install libcairo2-dev libffi-dev python3-dev
###########################################################  
  
import cairosvg
import os

def svg_to_png(svg_path, png_path, scale=2):
    """
    将 SVG 文件转换为 PNG 格式
    :param svg_path: 输入的 SVG 文件路径
    :param png_path: 输出的 PNG 文件路径
    :param scale: 缩放比例（默认2倍，提升清晰度）
    """
    try:
        # 检查 SVG 文件是否存在
        if not os.path.exists(svg_path):
            raise FileNotFoundError(f"SVG 文件不存在：{svg_path}")
        
        # 核心转换逻辑
        cairosvg.svg2png(
            url=svg_path,          # SVG 文件路径
            write_to=png_path,     # PNG 输出路径
            scale=scale,           # 缩放比例（数值越大越清晰）
            dpi=300                # 分辨率（可选，默认96）
        )
        print(f"转换成功！PNG 文件已保存至：{png_path}")
        
    except Exception as e:
        print(f"转换失败：{str(e)}")

# 示例调用
if __name__ == "__main__":
    # 替换为你的 SVG 文件路径和想要输出的 PNG 路径
    svg_file = "/home/abner/programs/blender-4.5.6-linux-x64/blender.svg"
    png_file = "/home/abner/programs/blender-4.5.6-linux-x64/blender.png"
    
    # 执行转换（scale=2 表示 PNG 尺寸是 SVG 原尺寸的2倍）
    svg_to_png(svg_file, png_file, scale=1)
 
 