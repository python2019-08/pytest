# 代码基于 Pillow 库，先安装：
# pip install pillow
from PIL import Image

def print_pixel_alpha(image_path, print_range=None):
    """
    按行打印图片每个像素的 Alpha 值（一行输出一整行像素）
    :param image_path: 图片路径
    :param print_range: 打印范围 (start_x, end_x, start_y, end_y)
    """
    try:
        img = Image.open(image_path).convert("RGBA")
    except Exception as e:
        print(f"打开图片失败：{e}")
        return

    width, height = img.size
    print(f"图片尺寸：宽 {width} 像素，高 {height} 像素")
    print("="*80)

    # 确定打印范围
    start_x, end_x = 0, width
    start_y, end_y = 0, height
    if print_range and len(print_range) == 4:
        start_x = max(0, print_range[0])
        end_x = min(width, print_range[1])
        start_y = max(0, print_range[2])
        end_y = min(height, print_range[3])
        print(f"打印范围：X({start_x}-{end_x}), Y({start_y}-{end_y})")
    else:
        print("⚠️ 未指定打印范围，将打印全图像素（建议小图测试！）")

    print("\n按行输出像素 Alpha 值（格式：行Y → <X,Y,A>,<X,Y,A>...）：")
    print("-"*80)
    
    # 核心修改：按行收集 + 整行打印
    for y in range(start_y, end_y):
        # 初始化列表，收集当前行的所有像素 Alpha 字符串
        row_alpha = []
        for x in range(start_x, end_x):
            r, g, b, a = img.getpixel((x, y))
            # 将当前像素的信息添加到行列表中
            # row_alpha.append(f"<{x},{y},{a}>")
            row_alpha.append(f"{a}")
        
        # 整行打印：拼接该行所有像素的字符串，用逗号分隔
        # print(f"行Y={y} → {','.join(row_alpha)}")
        print(f"Y={y} → {','.join(row_alpha)}")

    # 保留原有统计信息（可选）
    all_alpha = [img.getpixel((x, y))[3] for y in range(height) for x in range(width)]
    print("="*80)
    print(f"Alpha 通道统计：")
    print(f"- 最小值：{min(all_alpha)} | 最大值：{max(all_alpha)} | 平均值：{sum(all_alpha)/len(all_alpha):.2f}")
    print(f"- 完全透明像素(Alpha=0)：{all_alpha.count(0)} | 完全不透明像素(Alpha=255)：{all_alpha.count(255)}")


# ===================== 调用示例 =====================
if __name__ == "__main__":
    # 替换为你的图片路径（建议用 PNG 透明图测试）
    IMAGE_PATH = "/home/abner/Downloads/hehua01.png"  # 比如之前生成的对称荷叶荷花图
    
    # 方式1：打印指定范围（推荐！比如只打印前10x10像素，避免刷屏）
    # print_pixel_alpha(IMAGE_PATH, print_range=(0, 10, 0, 10))
    
    # 方式2：打印全图（仅小图用！大图会输出几万行）
    print_pixel_alpha(IMAGE_PATH)