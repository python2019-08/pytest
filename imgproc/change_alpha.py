# 要将PNG图片的**所有Alpha通道值统一改为156**，可以用`Pillow`库读取图片的RGBA通道，直接修改Alpha通道的数值，再保存为PNG即可。

 
from PIL import Image
import numpy as np


# ### 补充说明
# 1. **Alpha值范围**：Alpha的取值是`0~255`（0完全透明，255完全不透明），156属于半透明状态；
# 2. **兼容性**：如果原始图片是JPG（无Alpha通道），代码会自动转为RGBA模式，但JPG转PNG后新增的Alpha通道会被设为156；
# 3. **局部修改**：如果只需修改**部分区域**的Alpha值（而非全部），可以在`img_array[:, :, 3] = target_alpha`前加条件判断（例如只修改某个颜色区域的Alpha）。
def set_alpha_to_value(image_path, output_path, target_alpha=156):
    """
    将PNG图片的所有Alpha通道值设置为指定数值（如156）
    :param image_path: 输入PNG图片路径
    :param output_path: 输出图片路径（需为PNG）
    :param target_alpha: 目标Alpha值（0~255）
    """
    # 打开图片并强制转为RGBA模式（确保包含Alpha通道）
    img = Image.open(image_path).convert("RGBA")
    # 转为numpy数组，方便通道操作
    img_array = np.array(img)
    
    # 提取Alpha通道，将所有像素的Alpha值设为target_alpha
    # img_array的形状是 (高度, 宽度, 4)，第4个通道是Alpha
    img_array[:, :, 3] = target_alpha  # 直接覆盖所有Alpha值
    
    # 转回PIL图片并保存
    result_img = Image.fromarray(img_array)
    result_img.save(output_path, format="PNG")
    print(f"Alpha值已统一设为{target_alpha}，保存至：{output_path}")


### 局部修改Alpha的扩展示例（可选）
# 比如：只将“黑色区域”的Alpha设为156，其他区域保持原Alpha：
 
def set_alpha_for_specific_color(image_path, output_path, target_color=(0,0,0), target_alpha=156, tolerance=10):
    img = Image.open(image_path).convert("RGBA")
    img_array = np.array(img)
    r, g, b, a = img_array[:, :, 0], img_array[:, :, 1], img_array[:, :, 2], img_array[:, :, 3]
    
    # 识别目标颜色区域
    color_mask = (abs(r - target_color[0]) <= tolerance) & \
                 (abs(g - target_color[1]) <= tolerance) & \
                 (abs(b - target_color[2]) <= tolerance)
    
    # 仅目标区域的Alpha设为156
    img_array[color_mask, 3] = target_alpha
    
    result_img = Image.fromarray(img_array)
    result_img.save(output_path, format="PNG")

# 调用示例
if __name__ == "__main__":
    input_png = "/mnt/disk2/abner/zdev/3d/u3d/core3d0dv01building/Assets/ui-res/ui-pic/headbg01.png"   # 原始PNG图片
    output_png = "/home/abner/Downloads/output.png"  # 输出图片
    set_alpha_to_value(input_png, output_png, target_alpha=156)
 





 