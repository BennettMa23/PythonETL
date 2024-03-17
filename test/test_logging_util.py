# 1、导入模块（导入测试模块unittest、导入logging日志模块、导入loggingutil工具类）
import unittest
import logging
from util import loggingutil


# 2、定义一个测试类 => 继承TestCase
class TestLoggingUtil(unittest.TestCase):
    # 3、定义setUp、tearDown方法
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    # 4、编写测试用例 => 判断init_logger方法返回的对象是否为logging日志对象
    def test_init_logger(self):
        # 获取日志对象
        logger = loggingutil.init_logger()
        # 判断返回的对象是否为logging日志对象
        self.assertIsInstance(logger, logging.RootLogger)
