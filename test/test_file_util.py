# 1、导入模块
import os
import unittest
from util import fileutil

# 2、定义一个测试类，继承自unittest.TestCase
class TestFileUtil(unittest.TestCase):
    # 3、定义setUp()以及tearDown()方法
    def setUp(self) -> None:
        pass
    def tearDown(self) -> None:
        pass
    # 4、针对文件模块中的相关函数进行测试
    def test_get_dir_files_list(self):
        # 定义文件名称列表
        file_name_list = []
        # 获取./files中，所有文件的绝对路径
        file_path_list = fileutil.get_dir_files_list('./files/')  # ['D:/xxx/files/1', 'D:/xxx/files/2']
        # 对file_path_list进行遍历，得出每个文件绝对路径
        for file_path in file_path_list:
            # 使用os.path.basename()，获取每个文件路径中的文件名称（只要名称，不要路径）
            file_name = os.path.basename(file_path)  # ['D:/xxx/files/1', 'D:/xxx/files/2'] => 1/2
            file_name_list.append(file_name)  # ['1', '2']
        # 使用self.assertListEqual()比对返回结果是否正确
        self.assertListEqual(file_name_list, ['1', '2'])

        # 定义文件名称列表
        file_name_list = []
        # 获取./files中，所有文件的绝对路径
        file_path_list = fileutil.get_dir_files_list('./files/', True)  # ['D:/xxx/files/1', 'D:/xxx/files/2']
        # 对file_path_list进行遍历，得出每个文件绝对路径
        for file_path in file_path_list:
            # 使用os.path.basename()，获取每个文件路径中的文件名称（只要名称，不要路径）
            file_name = os.path.basename(file_path)  # ['D:/xxx/files/1', 'D:/xxx/files/2'] => 1/2
            file_name_list.append(file_name)  # ['1', '2', '3', '4', '5']
        # 因为数据较多，为了防止出现比对异常，可以提前对列表进行排序操作
        file_name_list.sort()  # ['1', '2', '3', '4', '5']
        # 使用self.assertListEqual()比对返回结果是否正确
        self.assertListEqual(file_name_list, ['1', '2', '3', '4', '5'])

    # 5、针对get_new_by_compare_lists函数进行单元测试
    def test_get_new_by_compare_lists(self):
        # 第一步：调用get_new_by_compare_lists，传入两个参数，processed_list以及all_list
        processed_list = ['a.txt', 'b.txt', 'c.txt']
        all_list = ['a.txt', 'b.txt', 'c.txt', 'd.txt', 'e.txt']
        # 第二步：获取返回结果
        result = fileutil.get_new_by_compare_lists(processed_list, all_list)
        # 第三步：self.assertListEqual()对比返回结果与预期结果是否一致
        self.assertListEqual(result, ['d.txt', 'e.txt'])

    # 小结：单元测试，必须让自定义测试类继承自(unittest.TestCase)；编写测试函数时，比如以(test_)开头 + 要测试函数名称；最终结果判断函数的执行与
    # 预期结果是否一致，如果一致，测试成功。