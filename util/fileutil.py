# 1、导入os模块
import os

# 2、封装第一个函数，用于采集指定目录下的文件信息
def get_dir_files_list(path='./', recursion=False):
    # 参数1: path，获取文件列表的目标路径
    # 参数2: recursion，bool类型，是否在获取文件列表过程中递归；不加这个参数，默认只会采集1.txt/2.txt
    # 第一步：定义一个列表 => path_list，用于保存所有文件的信息
    path_list = []
    # 第二步：定义一个变量file_name_lists，用于获取指定目录下的所有文件信息 => os.listdir() => ['1.txt', '2.txt', 'inner']
    file_name_lists = os.listdir(path)
    # 第三步：对os.listdir()产生的结果进行遍历操作
    for file_name in file_name_lists:
        # 第四步：把参数中的path路径 与 每次遍历时产生的文件名称进行join拼接操作 => os.path.join() => 相对路径
        file_path = os.path.join(path, file_name)  # ./files/1.txt
        # 第五步：使用os.path.abspath()，把以上相对路径转换为绝对路径
        abs_path = os.path.abspath(file_path)  # D:/PyCharmProject/ETLProject/util/files/1.txt
        # 第六步：使用if...else对文件类型进行判断，如果是普通文件，直接追加文件路径到path_list列表中
        if os.path.isfile(abs_path):
            path_list.append(abs_path)
        else:
            # 第七步：如果文件路径是一个文件夹
            if recursion:  # 还要进一步判断，判断recursion参数是否为True，递归调用get_dir_files_list
                sub_path_list = get_dir_files_list(abs_path, True)
                path_list += sub_path_list  # [1.txt, 2.txt] + [3.txt]
    # 第八步：当所有程序执行完毕后，把文件列表直接返回
    return path_list

# 3、封装第二个函数，用于获取还未采集的文件信息
def get_new_by_compare_lists(processed_list, all_list):
    # 参数1: processed_list，已经处理过的文件列表 => [1, 2, 3]
    # 参数2: all_list，所有文件的文件列表 => [1, 2, 3, 4, 5]
    # 返回结果：[4, 5] => 比较经典Python面试题 => 筛选出两个列表中不重复的数据
    # 方案一：对all_list列表进行遍历，然后拿出遍历结果，判断是否出现在processed_list
    # 方案二：还可以把all_list与processed_list转换为集合类型，直接使用-，相减操作
    new_list = []
    for i in all_list:
        if i not in processed_list:
            new_list.append(i)
    # 当循环结束，返回new_list新列表
    return new_list