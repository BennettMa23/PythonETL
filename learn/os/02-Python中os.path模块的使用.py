"""
os.path.abspath()：获取绝对路径
os.path.dirname()：获取上一级路径
os.path.basename()：获取路径中的最后一部分
os.path.join(路径1, 路径2)：把两个路径拼接在一起
os.path.isfile()：判断是否为文件
os.path.isdir()：判断是否为文件夹
"""
# 1、导入模块
import os

# 2、获取当前文件所在位置
print(__file__, end="  => No 1  \n")
# 3、获取绝对路径 => ./ => 当前位置的绝对路径
print(os.path.abspath('./'))  # D:\PycharmProjects\ETLProject\learn\os，注意：这是反斜杠
# 4、dirname()获取上一级路径，basename()获取路径中的最后一部分 => 建议参数使用绝对路径
print(os.path.dirname(__file__))  # D:/PycharmProjects/ETLProject/learn/os，注意：这是斜杠
print(os.path.basename(__file__))  # D:/PycharmProjects/ETLProject/learn/os，注意：这是斜杠
# 5、os.path.join()路径拼接
# 路径1：D:/PycharmProjects/ETLProject，路径2：learn/os
# os.path.join()建议使用的拼接的路径最好使用\反斜杠，如果要拼接的路径/斜杠，可以考虑最终替换一下
print(os.path.join('D:/PycharmProjects/ETLProject/learn/os', 'learn/os').replace('\\', '/'))
# 6、判断isfile()与isdir()
if os.path.isfile(__file__):
    print('文件')
else:
    print('非文件')

if os.path.isdir('D:/PycharmProjects/ETLProject/learn/os'):
    print('文件夹')
else:
    print('非文件夹')
