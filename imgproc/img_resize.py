# # Pillow（推荐，适合普通图片处理）
# pip install pillow

# # OpenCV（适合批量/高性能场景）
# pip install opencv-python

from PIL import Image


def resize_pic(img_inPath,   img_outPath):
    # 1. 打开图片（替换为你的背景图路径）
     
    img = Image.open(img_inPath)

    # 2. 定义目标尺寸（示例：缩放到1280*720，或按比例缩放）
    target_size = (1024, 1024)  # (宽度, 高度)
    # 若需等比例缩放（避免变形），可先计算比例（示例：宽度缩为1000，高度按比例）
    # w, h = img.size
    # new_w = 1000
    # new_h = int(h * new_w / w)
    # target_size = (new_w, new_h)

    # 3. 调整尺寸（推荐Lanczos插值，缩小时画质最优）
    resized_img = img.resize(target_size, Image.Resampling.LANCZOS)  # Pillow 9.1+用Resampling，旧版本用Image.LANCZOS

    # 4. 保存调整后的图片
    resized_img.save(img_outPath)  # 保存路径
    print(f"原尺寸：{img.size}，新尺寸：{resized_img.size}")


# -------------------------------------------------------------------------------- 

def resizeJpg_and_pad(img, target_size=(1980, 1080), bg_color=(255, 255, 255)):
    """等比例缩放后补边，保证尺寸为1980*1080，避免变形"""
    w, h = img.size
    target_w, target_h = target_size
    
    # 计算缩放比例（取宽/高中较小的比例，保证图片完整）
    scale = min(target_w / w, target_h / h)
    new_w = int(w * scale)
    new_h = int(h * scale)
    
    # 缩放图片
    resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # 创建新画布，补边
    new_img = Image.new("RGB", target_size, bg_color)
    # 计算居中位置（若需左侧对齐，x=0即可）
    x = (target_w - new_w) // 2  # 居中：(target_w - new_w)//2；左侧对齐：0
    y = (target_h - new_h) // 2
    new_img.paste(resized, (x, y))
    return new_img




# --------------------------------------------------------------------------------
# from PIL import Image

def resize_pad_png(img, target_size=(1980, 1080), bg_color=(255, 255, 255, 255)):
    """
    等比例缩放后补边，支持PNG透明通道（RGBA），保证尺寸为1980*1080
    :param img: 打开的PIL Image对象
    :param target_size: 目标尺寸 (宽, 高)
    :param bg_color: 补边背景色，RGBA格式（如(255,255,255,0)为全透明）
    """
    # 统一图片模式：若为PNG透明图，转为RGBA；否则为RGB
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGBA" if "transparency" in img.info else "RGB")
    
    w, h = img.size
    target_w, target_h = target_size
    
    # 计算缩放比例（保证图片完整）
    scale = min(target_w / w, target_h / h)
    new_w = int(w * scale)
    new_h = int(h * scale)
    
    # 缩放图片（LANCZOS插值，画质最优）
    resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # 创建新画布：匹配原图模式（RGB/RGBA），保留透明通道
    new_img = Image.new(resized.mode, target_size, bg_color)
    
    # 计算粘贴位置（居中/左侧对齐可调整）
    x = (target_w - new_w) // 2  # 居中：(target_w-new_w)//2；左侧对齐：0
    y = (target_h - new_h) // 2
    new_img.paste(resized, (x, y))
    
    return new_img

# --------------------------------------------------------------------------------

def resizeJpg():
    # 调用示例
    img = Image.open("login_bg.jpg")
    final_img = resizeJpg_and_pad(img, (1980, 1080), bg_color=(245, 245, 245))  # 浅灰色背景补边
    final_img.save("login_bg_1980x1080.jpg")    

def resizePng():
    # 打开PNG图片（支持透明通道）
    img = Image.open("/home/abner/Downloads/big_bg/login01.png")   
    
    # 补边背景色：若需透明背景，设为(0,0,0,0)；若需浅灰色，设为(245,245,245,255)
    final_img = resize_pad_png(img, (1980, 1080), bg_color=(245, 245, 245, 255))
    
    # 保存PNG（需指定格式，避免默认转为JPG丢失透明）
    final_img.save("/home/abner/Downloads/big_bg/login01_1980x1080.png", format="PNG")


# 调用示例（适配PNG）
if __name__ == "__main__":
    rootPath="/home/abner/Downloads/"
    # for i in range(1,5):
    #     inPath = rootPath + "login_right0" + str(i) + ".png"
    #     outPath = rootPath + "login_right0" + str(i) + "_820x1080.png"
    #     resize_pic(inPath, outPath )    
    inPath  = rootPath + "cn-fashion-meadow01.jpg"
    outPath = rootPath + "cn-fashion-meadow01_1024x1024.png"
    resize_pic(inPath, outPath ) 