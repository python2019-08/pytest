# pip install pillow opencv-python numpy

from PIL import Image
import numpy as np

def make_background_transparent(image_path, output_path, bg_color=(0, 0, 0), tolerance=10):
    """
    将图片指定底色改为透明（alpha=0）
    :param image_path: 输入图片路径
    :param output_path: 输出透明图片路径（需为PNG）
    :param bg_color: 要去除的底色（默认黑色(0,0,0)）
    :param tolerance: 颜色容差（适配底色轻微色差）
    """
    # 打开图片并转换为RGBA模式（必须包含Alpha通道）
    img = Image.open(image_path).convert("RGBA")
    img_array = np.array(img)  # 转为numpy数组，方便像素操作
    
    # 拆分RGBA通道
    r, g, b, a = img_array[:, :, 0], img_array[:, :, 1], img_array[:, :, 2], img_array[:, :, 3]
    
    # 计算像素与底色的色差（容差范围内判定为底色）
    color_diff = (abs(r - bg_color[0]) <= tolerance) & \
                 (abs(g - bg_color[1]) <= tolerance) & \
                 (abs(b - bg_color[2]) <= tolerance)
    
    # 将底色像素的Alpha通道设为0（透明）
    img_array[color_diff, 3] = 0
    
    # 转回PIL图片并保存
    result_img = Image.fromarray(img_array)
    result_img.save(output_path, format="PNG")
    print(f"透明图片已保存至：{output_path}")

# 调用示例
if __name__ == "__main__":
    # 替换为你的图片路径和输出路径
    input_img = "/home/abner/Downloads/hehua.png"   # 原始带底色的图片
    output_img = "/home/abner/Downloads/hehua00.png" # 输出透明背景的图片
    make_background_transparent(input_img, output_img, bg_color=(0,0,0), tolerance=15)