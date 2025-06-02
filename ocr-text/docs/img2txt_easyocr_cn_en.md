# 1.easyocr 识别中英文

以下是一个使用 EasyOCR 识别中英文的 Python 脚本。EasyOCR 是一个强大的开源 OCR 库，支持超过 80 种语言，包括中文和英文。

 ```py
import easyocr
import cv2
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

# 设置中文字体，确保能正常显示中文
try:
    font = ImageFont.truetype("simhei.ttf", 20)  # 尝试加载系统中的黑体字体
except IOError:
    try:
        # 尝试其他可能的中文字体路径
        font = ImageFont.truetype("/usr/share/fonts/truetype/wqy/wqy-microhei.ttf", 20)
    except IOError:
        # 如果找不到中文字体，使用默认字体（可能无法正确显示中文）
        font = None

# 创建 EasyOCR 阅读器，指定识别语言为中文和英文
reader = easyocr.Reader(['ch_sim', 'en'])  # 'ch_sim' 表示简体中文，'en' 表示英文

def recognize_text(image_path, output_path=None):
    """
    识别图像中的中英文文字
    
    参数:
        image_path: 输入图像的路径
        output_path: 输出图像的路径（可选），如果提供则在原图上标注识别结果并保存
    """
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        print(f"无法读取图像: {image_path}")
        return
    
    # 转换为 RGB 格式（用于显示和 PIL 处理）
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # 使用 EasyOCR 识别文本
    results = reader.readtext(rgb_image)
    
    # 打印识别结果
    print("识别结果:")
    for (bbox, text, prob) in results:
        print(f"文本: {text}, 置信度: {prob:.2f}")
        
        # 如果有中文字体，在图像上标注识别结果
        if font and output_path:
            # 获取边界框坐标
            (top_left, top_right, bottom_right, bottom_left) = bbox
            top_left = (int(top_left[0]), int(top_left[1]))
            bottom_right = (int(bottom_right[0]), int(bottom_right[1]))
            
            # 使用 PIL 在图像上绘制文本和边框
            pil_image = Image.fromarray(rgb_image)
            draw = ImageDraw.Draw(pil_image)
            
            # 绘制边框
            draw.rectangle([top_left, bottom_right], outline=(0, 255, 0), width=2)
            
            # 绘制文本背景
            text_width, text_height = draw.textsize(text, font=font)
            draw.rectangle(
                [top_left[0], top_left[1] - text_height, top_left[0] + text_width, top_left[1]],
                fill=(0, 255, 0)
            )
            
            # 绘制文本
            draw.text((top_left[0], top_left[1] - text_height), text, font=font, fill=(0, 0, 0))
            
            # 转换回 OpenCV 格式
            rgb_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    
    # 如果指定了输出路径，保存标注后的图像
    if output_path:
        cv2.imwrite(output_path, rgb_image)
        print(f"标注后的图像已保存至: {output_path}")
    
    # 显示识别结果
    plt.figure(figsize=(10, 8))
    plt.imshow(rgb_image)
    plt.axis('off')
    plt.show()
    
    return results

if __name__ == "__main__":
    # 使用示例
    image_path = "example.jpg"  # 替换为你的图像路径
    output_path = "output.jpg"  # 替换为输出图像的路径
    
    results = recognize_text(image_path, output_path)    
 ```

### 使用说明

1. **安装依赖**：
   ```bash
   pip install easyocr opencv-python matplotlib pillow
   ```

2. **下载模型**：
   首次运行时，EasyOCR 会自动下载中文和英文的识别模型。模型较大，请确保网络连接稳定。

3. **准备图像**：
   将需要识别的图像放在脚本同一目录下，或修改 `image_path` 指向图像路径。

4. **运行脚本**：
   ```bash
   python ocr_script.py
   ```

### 注意事项

1. **中文字体**：
   脚本尝试加载系统中的中文字体（如黑体或文泉驿微米黑）。如果找不到合适的字体，识别结果可能无法正确显示中文。你可以根据自己的系统安装情况修改字体路径。

2. **识别效果**：
   识别效果受图像质量、文字清晰度、字体等因素影响。对于复杂场景，可能需要进行预处理（如灰度化、二值化、降噪等）。

3. **GPU 加速**：
   如果你的系统有 NVIDIA GPU 并安装了 CUDA，可以通过以下方式启用 GPU 加速：
   ```python
   reader = easyocr.Reader(['ch_sim', 'en'], gpu=True)
   ```

4. **多语言支持**：
   EasyOCR 支持多种语言组合。例如，同时识别中日英三国语言：
   ```python
   reader = easyocr.Reader(['ch_sim', 'ja', 'en'])
   ```

如需更复杂的应用，可以考虑结合图像处理技术（如边缘检测、形态学操作）对图像进行预处理，以提高识别准确率。