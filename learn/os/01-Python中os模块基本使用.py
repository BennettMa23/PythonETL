'''
os模块中的相关方法：
os.getcwd() : get current working directory
os.listdir(目录) : 获取指定目录下的所有文件信息，返回列表
os.mkdir() : 创建目录
os.rmdir() : 删除文件夹 => 空文件夹，扩展：删除非空文件夹 => shutil模块里面有一个rmtree()方法（慎重）
os.chdir() : change directory，切换到指定目录

案例：
创建一个files目录，创建几个文件file1/file2/file3
① 创建一个avatar文件夹（头像文件夹）
② 切换到files目录，获取目录下的所有文件信息
③ 切换到files目录外面
④ 删除avatar空文件夹
⑤ 获取当前所在的路径

注意：判断文件/文件夹是否存在
os.path.exists()，如果文件/文件夹已存在，返回为True；不存在就返回为False
'''
import os
# 获取当前所在路径
print(os.getcwd())
# ① 创建一个avatar文件夹
if not os.path.exists('avatar'):
    os.mkdir('avatar')
# ② 切换files目录
os.chdir('files')
# 获取目录下的所有文件，以列表 => 重点 => 获取日志/获取json文件
print(os.listdir())
# ③ 切换到files外面
os.chdir('../')
# os.chdir('avatar')
# ④ 删除avatar空文件夹
os.rmdir('avatar')
# ⑤ 获取当前所在路径
print(os.getcwd())