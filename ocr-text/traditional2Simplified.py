import opencc

# 创建一个转换器对象，配置为将繁体中文转换为简体中文
converter = opencc.OpenCC('t2s')

# 定义要转换的繁体文本
traditional_text = """
[**上一篇文學** 
 
我從小就生長在單 
 
"""


# 进行转换
simplified_text = converter.convert(traditional_text)

# 输出转换后的简体文本 
print("----------------------n", simplified_text)
with open("./simp.txt","wt") as f:
    f.write(simplified_text)
