from PIL import Image
import numpy as np

# 打开图片
img = Image.open('/mnt/disk2/abner/zdev/3d/u3d/towerdefence/Assets/_lan-game/texture/hehua00.png').convert('RGBA')
data = np.array(img)

# 找到所有白色背景像素
white_pixels = (data[:, :, 0] == 255) & (data[:, :, 1] == 255) & (data[:, :, 2] == 255)

# 将白色背景的Alpha值设为0（完全透明）
data[white_pixels, 3] = 0

# 保存修复后的图片
fixed_img = Image.fromarray(data)
fixed_img.save('/mnt/disk2/abner/zdev/3d/u3d/towerdefence/Assets/_lan-game/texture/hehua01.png', 'PNG')