import easyocr

# 创建阅读器对象，指定语言
reader = easyocr.Reader(['en'])
# 进行图片转文字
result = reader.readtext('/home/abner/Pictures/studentinfo.png')
# 提取识别结果
text = ' '.join([res[1] for res in result])
print(text)