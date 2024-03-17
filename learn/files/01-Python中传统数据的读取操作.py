'''
file文件读取三步走：
① 打开文件
② 读取文件
③ 关闭文件
'''
# f = open('../../logs/test.log', 'r', encoding='utf8')
# while True:
#     content = f.readline()
#     if not content:
#         break
#     print(content, end='')
# f.close()

# with上下文管理器实现文件的读取：with上下文管理器，可以在操作结束，自动关闭已经打开的资源
# 基本语法
# with open('../../logs/test.log', 'r', encoding='utf8') as f:
#     while True:
#         content = f.readline()
#         if not content:
#             break
#         print(content, end='')

# 使用for循环，实现文件按行读取 => 简洁语法
for row_content in open('../../logs/test.log', 'r', encoding='utf8'):
    print(row_content, end='')

