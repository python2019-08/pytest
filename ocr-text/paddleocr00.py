# pip install paddlepaddle -i https://mirror.baidu.com/pypi/simple
# pip install paddleocr
# 确保 /etc/resolv.conf 中dns 设置含有: nameserver 8.8.8.8 

import os
from paddleocr import PaddleOCR


# # 设置代理（根据实际情况替换为你的代理地址和端口）
# os.environ["http_proxy"] = "http://127.0.0.1:8123"
# os.environ["https_proxy"] = "http://127.0.0.1:8123"

# 创建OCR对象
ocr = PaddleOCR(use_angle_cls=True, lang='en')
# 进行图片转文字
result = ocr.ocr('/home/abner/Pictures/studentinfo.png', cls=True)
# 提取识别结果
text = [line[1][0] for line in result[0]]
print('\n'.join(text))