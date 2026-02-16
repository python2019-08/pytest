# 用python 画一个图片，底色的alpha为0, 然后y轴中线的下部分画几片荷叶几朵荷花。最后把 刚画的几片荷叶几朵荷花以y轴中线为对称轴对称画到上部分。

# 首先确保安装 Pillow 库（Python 图像处理核心库）：
# pip install pillow

from PIL import Image, ImageDraw
import random
import math

# ===================== 基础配置 =====================
# 画布尺寸（宽x高），建议正方形更对称
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 800
# Y轴中线位置（PIL坐标原点在左上角，Y轴向下为正）
MID_Y = CANVAS_HEIGHT // 2
# 透明背景（RGBA模式，最后一位alpha=0表示完全透明）
BG_COLOR = (0, 0, 0, 0)

# ===================== 绘制函数定义 =====================
def draw_lotus_leaf(draw, center_x, center_y, radius, color=(34, 139, 34, 200)):
    """
    绘制荷叶（椭圆+轮廓，模拟荷叶形状）
    :param draw: ImageDraw对象
    :param center_x: 荷叶中心X坐标
    :param center_y: 荷叶中心Y坐标
    :param radius: 荷叶半径
    :param color: 荷叶颜色（RGBA，最后一位是透明度）
    """
    # 荷叶外轮廓（椭圆，略扁更贴近真实荷叶）
    leaf_rect = (
        center_x - radius, center_y - radius*0.8,
        center_x + radius, center_y + radius*0.8
    )
    # 填充荷叶主体（带透明度，更自然）
    draw.ellipse(leaf_rect, fill=color, outline=(20, 80, 20, 255), width=2)
    # 荷叶纹理（简单画几条曲线模拟叶脉）
    for angle in range(0, 360, 45):
        rad = angle * 3.14159 / 180
        end_x = center_x + radius * 0.8 * math.cos(rad)
        end_y = center_y + radius * 0.6 * math.sin(rad)
        draw.line([(center_x, center_y), (end_x, end_y)], fill=(10, 60, 10, 150), width=1)

def draw_lotus_flower(draw, center_x, center_y, petal_num=8, petal_size=20, color=(255, 0, 0, 220)):
    """
    绘制荷花（多花瓣+花蕊，简化版）
    :param draw: ImageDraw对象
    :param center_x: 荷花中心X坐标
    :param center_y: 荷花中心Y坐标
    :param petal_num: 花瓣数量
    :param petal_size: 花瓣大小
    :param color: 花瓣颜色（RGBA）
    """
    import math
    # 绘制花瓣（围绕中心旋转排列）
    for i in range(petal_num):
        angle = i * (360 / petal_num) * 3.14159 / 180
        # 花瓣位置（椭圆，模拟花瓣形状）
        petal_x = center_x + petal_size * 1.2 * math.cos(angle)
        petal_y = center_y + petal_size * math.sin(angle)
        petal_rect = (
            petal_x - petal_size, petal_y - petal_size*0.7,
            petal_x + petal_size, petal_y + petal_size*0.7
        )
        draw.ellipse(petal_rect, fill=color, outline=(200, 0, 0, 255), width=1)
    # 绘制花蕊（中心小圆）
    stamen_rect = (
        center_x - petal_size//3, center_y - petal_size//3,
        center_x + petal_size//3, center_y + petal_size//3
    )
    draw.ellipse(stamen_rect, fill=(255, 215, 0, 255), outline=(200, 180, 0, 255), width=1)

# ===================== 核心绘制流程 =====================
# 1. 创建透明画布（必须是RGBA模式，才能支持alpha通道）
img = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(img)

# 2. 定义中线下侧要绘制的荷叶荷花数量和参数（随机位置更自然）
# 荷叶参数：[(中心X, 中心Y, 半径), ...]
leaf_params = [
    (CANVAS_WIDTH//2 - 150, MID_Y + 100, 60),
    (CANVAS_WIDTH//2 + 80, MID_Y + 150, 75),
    (CANVAS_WIDTH//2 - 80, MID_Y + 200, 50)
]
# 荷花参数：[(中心X, 中心Y, 花瓣数, 花瓣大小), ...]
flower_params = [
    (CANVAS_WIDTH//2 - 120, MID_Y + 80, 8, 25),
    (CANVAS_WIDTH//2 + 50, MID_Y + 120, 10, 20)
]

# 3. 绘制中线下侧的荷叶荷花
print("绘制中线下侧荷叶荷花...")
for (x, y, r) in leaf_params:
    draw_lotus_leaf(draw, x, y, r)
for (x, y, pn, ps) in flower_params:
    draw_lotus_flower(draw, x, y, pn, ps)

# 4. 对称绘制中线上侧的荷叶荷花（核心：Y坐标对称计算）
print("对称绘制中线上侧荷叶荷花...")
# 荷叶对称：新Y坐标 = 2*中线Y - 原Y坐标
for (x, y, r) in leaf_params:
    sym_y = 2 * MID_Y - y  # 对称Y坐标
    draw_lotus_leaf(draw, x, sym_y, r)
# 荷花对称
for (x, y, pn, ps) in flower_params:
    sym_y = 2 * MID_Y - y
    draw_lotus_flower(draw, x, sym_y, pn, ps)

# 5. 保存图片（PNG格式支持透明，JPG不支持！）
img.save("lotus_symmetry.png", "PNG")
print("图片已保存为 lotus_symmetry.png，底色为完全透明")

# 可选：显示图片（需系统有图片查看器）
img.show()

