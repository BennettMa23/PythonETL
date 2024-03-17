# 导入数据包
import unittest
from util import mysqlutil


# 定义一个自定义测试类，继承TestCase
class TestMySQLUtil(unittest.TestCase):
    # 封装两个方法setUp()、tearDown()
    def setUp(self) -> None:
        # 创建一个数据库
        self.util = mysqlutil.get_mysql_util(host='localhost', user='root', password='123456')
        # 创建一个test数据库
        self.util.execute('create database if not exists test default charset=utf8;')
        # 创建一个测试用数据表
        self.util.execute('create table if not exists test.tb_students(id int, name varchar(20));')

    def tearDown(self) -> None:
        # # 删除setUp创建的数据表
        self.util.execute('drop table if exists test.tb_students;')
        # 删除setUp创建的测试数据库
        self.util.execute('drop database if exists test;')
        # 关闭连接对象
        self.util.close()

    # 封装测试方法，以test_开头即可
    def test_insert_single_sql(self):
        self.util.insert_single_sql('insert into test.tb_students values (1, "Tom");')
        result = self.util.query_all(db_name='test', tb_name='tb_students')  # ((), (), ())
        self.assertEqual((1, 'Tom'), result[0])  # 如果两个输入值相等，则assertEqual()将返回true，否则返回false。
