# 1、导入单元测试类
from unittest import TestCase

# 2、编写自定义测试类
class FileTest(TestCase):
    # 3、定义一个setUp()方法，执行测试前初始化工作
    def setUp(self) -> None:
        print('当某个测试方法执行之前会自动被执行1次！')

    # 5、编写真正的单元测试代码 => 测试我们编写的功能函数是否可用
    def test_func1(self):
        print('func1方法单元测试')

    def test_func2(self):
        print('func2方法单元测试')

    # 4、定义一个tearDown()方法，执行测试后清理工作
    def tearDown(self) -> None:
        print('当某个测试方法执行之后会自动被执行1次！')