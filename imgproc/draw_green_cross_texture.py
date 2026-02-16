from PIL import Image, ImageDraw

# 创建一个空白图像，大小为256x256，背景透明
def draw_green_cross(aWidth: int =1024, aHeight: int =1024, 
                     aLineWidth: int =50, 
                     aImageName : str='green_cross.png'):
    # width, height = 256, 256
    width, height = aWidth, aHeight
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # 定义绿色
    green_color = (0, 255, 0, 255)

    # 绘制十字
    # 竖线
    start_y = height // 4
    end_y = height - start_y
    draw.line([(width // 2, start_y), (width // 2, end_y)], fill=green_color, width=aLineWidth)

    # 横线
    start_x = width // 4
    end_x = width - start_x
    draw.line([(start_x, height // 2), (end_x, height // 2)], fill=green_color, width=aLineWidth)
    
    # 保存图像
    image.save(aImageName)

draw_green_cross(aWidth=1024, aHeight=1024, 
                     aLineWidth=200, 
                     aImageName='green_cross1024.png')    

draw_green_cross(aWidth=256, aHeight=256, 
                     aLineWidth=50, 
                     aImageName='green_cross256.png')  
