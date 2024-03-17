# 1、打开文件
f = open('python.txt', 'a+')
# 2、读写文件
# 重置指针 =>
# f.seek(0, 0)  # 把文件指针指向开头位置
# f.seek(0, 2)  # 把文件指针指向结尾位置
f.seek(0, 0)
content = f.read(3)
print(content)
# content = f.read(3)
# print(content)
# 3、关闭文件
f.close()