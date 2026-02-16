

# ### 步骤说明：
# 1. 安装 Pillow 库（若未安装）；
# 2. 创建 32×32 透明画布（RGBA 模式，alpha=0）；
# 3. 绘制 cyan 色圆角矩形（可自定义圆角半径）；
# 4. 保存为 PNG 格式（仅 PNG 支持透明通道）。
 
from PIL import Image, ImageDraw

# def draw_rounded_rect01(img, x1, y1, x2, y2, radius, color):
def draw_rounded_rect01( ):
    """绘制圆角矩形（Pillow 9.1.0+ 支持）
    # 以下是使用 Python 的 Pillow 库实现绘制 透明底色、青蓝色（cyan）圆角矩形线框并保存为 PNG 的代码。
    """
    # -------------------------- 配置参数 --------------------------
    IMAGE_SIZE = (100, 100)       # 图片尺寸  
    BG_COLOR = (0, 0, 0, 0)     # 背景色：全透明 (R, G, B, alpha)
    LINE_COLOR = (0, 255, 255, 255)  # Cyan 色（青蓝），alpha=255 完全不透明
    LINE_WIDTH = 2              # 线框宽度
    CORNER_RADIUS = 4           # 圆角半径（可根据需求调整，如 2/4/6）
    SAVE_PATH = "/home/abner/abner2/zdev/ai/pytest/cyan_rounded_rect.png"  # 保存路径

    # -------------------------- 绘制逻辑 --------------------------
    # 1. 创建透明画布（RGBA 模式支持 alpha 通道）
    img = Image.new("RGBA", IMAGE_SIZE, BG_COLOR)
    draw = ImageDraw.Draw(img)

    # 2. 计算圆角矩形的坐标（线框居中，避免超出画布）
    # 画布范围：0,0 到 31,31（32x32），预留线宽避免边缘截断
    left = LINE_WIDTH // 2
    top = LINE_WIDTH // 2
    right = IMAGE_SIZE[0] - LINE_WIDTH // 2 - 1
    bottom = IMAGE_SIZE[1] - LINE_WIDTH // 2 - 1

    # 3. 绘制圆角矩形线框（outline=线色，width=线宽）
    # rounded_rectangle 格式：(左上角x, 左上角y, 右下角x, 右下角y)
    draw.rounded_rectangle(
        xy=(left, top, right, bottom),
        radius=CORNER_RADIUS,
        outline=LINE_COLOR,
        width=LINE_WIDTH
    )

    # 4. 保存图片（PNG 支持透明通道，JPG 不支持）
    img.save(SAVE_PATH, format="PNG")

    print(f"图片已保存至：{SAVE_PATH}")
    print(f"图片信息：尺寸={IMAGE_SIZE}，背景透明，线框颜色=cyan，圆角半径={CORNER_RADIUS}")

# 
### 低版本 Pillow 兼容方案（若无法升级）：
# 如果 Pillow 版本低于 9.1.0，可通过绘制圆形+矩形拼接实现圆角矩形：
# from PIL import Image, ImageDraw
def draw_rounded_rect02(img, x1, y1, x2, y2, radius, color):
    """绘制圆角矩形（拼接法）"""
    IMAGE_SIZE = (32, 32)
    BG_COLOR = (0, 0, 0, 0)
    RECT_COLOR = (0, 255, 255, 255)
    R = 4  # 圆角半径
    x1, y1, x2, y2 = 2, 2, 30, 30
    SAVE_PATH = "cyan_rounded_rect_32x32.png"

    # 创建画布
    img = Image.new("RGBA", IMAGE_SIZE, BG_COLOR)
    draw = ImageDraw.Draw(img)

    # 绘制圆角矩形（拼接法）
    # 1. 绘制中间矩形
    draw.rectangle([x1+R, y1, x2-R, y2], fill=RECT_COLOR)
    draw.rectangle([x1, y1+R, x2, y2-R], fill=RECT_COLOR)
    # 2. 绘制四个圆角（椭圆）
    draw.ellipse([x1, y1, x1+2*R, y1+2*R], fill=RECT_COLOR)  # 左上
    draw.ellipse([x2-2*R, y1, x2, y1+2*R], fill=RECT_COLOR)  # 右上
    draw.ellipse([x1, y2-2*R, x1+2*R, y2], fill=RECT_COLOR)  # 左下
    draw.ellipse([x2-2*R, y2-2*R, x2, y2], fill=RECT_COLOR)  # 右下

    # 保存
    img.save(SAVE_PATH, format="PNG")
    print(f"图片已保存：{SAVE_PATH}")
    

from PIL import Image, ImageDraw, ImageFilter
import math
 
def draw_rect3():
    from PIL import Image, ImageDraw
    import math

    # -------------------------- 配置参数 --------------------------
    IMAGE_SIZE = (800, 400)       # 图片尺寸 800x400
    BG_COLOR = (0, 0, 0, 0)       # 背景色：全透明 (R, G, B, alpha)
    CENTER_COLOR = (0, 255, 255, 255)  # 中心色：纯白色（不透明）
    FRAME_COLOR = (255, 234, 0, 255)     # 外框色：明黄色（#FFEA00）
    FRAME_WIDTH = 10                # 外框宽度（像素）
    GRADIENT_DEPTH = 0.8           # 渐变深度（0-1，越大颜色加深越快）

    # -------------------------- 绘制逻辑 --------------------------
    # 1. 创建透明画布（RGBA模式支持alpha通道）
    img = Image.new("RGBA", IMAGE_SIZE, BG_COLOR)
    draw = ImageDraw.Draw(img)

    # 2. 计算画布中心点
    center_x = IMAGE_SIZE[0] // 2
    center_y = IMAGE_SIZE[1] // 2

    # 3. 计算画布到中心点的最大距离（渐变的最大半径）
    max_distance = math.hypot(center_x, center_y)

    # 4. 绘制径向渐变（中点白色向外加深）
    for y in range(IMAGE_SIZE[1]):
        for x in range(IMAGE_SIZE[0]):
            # 计算当前像素到中心点的距离
            distance = math.hypot(x - center_x, y - center_y)
            # 计算渐变系数（距离越远，系数越大，颜色越深）
            gradient_ratio = min(distance / max_distance * GRADIENT_DEPTH, 1.0)
            
            # 计算当前像素的RGB值（白色基础上降低亮度）
            r = int(CENTER_COLOR[0] * (1 - gradient_ratio))
            g = int(CENTER_COLOR[1] * (1 - gradient_ratio))
            b = int(CENTER_COLOR[2] * (1 - gradient_ratio))
            a = CENTER_COLOR[3]  # alpha保持不透明
            
            # 绘制像素
            img.putpixel((x, y), (r, g, b, a))

    # 5. 绘制明黄色外框（预留外框宽度，避免超出画布）
    frame_left = FRAME_WIDTH // 2
    frame_top = FRAME_WIDTH // 2
    frame_right = IMAGE_SIZE[0] - FRAME_WIDTH // 2 - 1
    frame_bottom = IMAGE_SIZE[1] - FRAME_WIDTH // 2 - 1

    draw.rectangle(
        xy=(frame_left, frame_top, frame_right, frame_bottom),
        outline=FRAME_COLOR,
        width=FRAME_WIDTH
    )

    # 6. 保存图片（PNG支持透明通道）
    save_path = "gradient_rectangle.png"
    img.save(save_path, format="PNG")

    print(f"图片已保存至：{save_path}")
    print(f"图片信息：尺寸={IMAGE_SIZE}，背景透明，中心白色径向渐变，明黄色外框（宽度={FRAME_WIDTH}px）")  
        

if __name__ == "__main__":
    draw_rect3()