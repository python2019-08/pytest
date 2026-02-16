import cv2
import numpy as np
from PIL import Image

def precise_remove_background(image_path, output_path, bg_hsv_range):
    """
    精准去除复杂底色（HSV色彩范围匹配）
    :param bg_hsv_range: 底色的HSV范围，例：黑色→[(0,0,0), (180,255,46)]
    """
    # 读取图片（OpenCV默认BGR格式）
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    # 转换为HSV色彩空间（更易区分颜色）
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # 定义底色的HSV范围，生成掩码（mask）
    lower_bg = np.array(bg_hsv_range[0])
    upper_bg = np.array(bg_hsv_range[1])
    mask = cv2.inRange(hsv, lower_bg, upper_bg)
    
    # 膨胀+腐蚀去除杂色（可选，优化边缘）
    kernel = np.ones((2,2), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    # 将掩码区域（底色）设为透明
    if img.shape[2] == 3:  # 图片无Alpha通道，先添加
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    img[mask > 0, 3] = 0  # 掩码区域Alpha设为0
    
    # 转换为PIL格式保存（避免OpenCV保存PNG的兼容问题）
    img_rgba = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
    pil_img = Image.fromarray(img_rgba)
    pil_img.save(output_path, format="PNG")
    print(f"精准抠图完成，保存至：{output_path}")

# 调用示例（黑色底色的HSV范围）
if __name__ == "__main__":
    input_img = "/mnt/disk2/abner/zdev/3d/u3d/core3d0dv01building/Assets/ui-res/ui-pic/headbg01.png"   # 原始带底色的图片
    output_img = "/home/abner/Downloads/output.png" # 输出透明背景的图片
    # 黑色的HSV范围（可根据实际底色调整）
    black_hsv = [(0, 0, 0), (180, 255, 46)]
    precise_remove_background(input_img, output_img, black_hsv)