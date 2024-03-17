# 1、导入模块
import logging
from config import project_config as conf


# 2、封装一个LoggingUtil工具类
class LoggingUtil(object):
    # 其实就是为了获得logger对象
    def __init__(self, level=logging.INFO):
        self.logger = logging.getLogger()
        self.logger.setLevel(level)


# 3、定义一个init_logger()方法，用于初始化对象
def init_logger():
    # 第一步：创建日志对象
    logger = LoggingUtil().logger
    # 第二步：创建日志处理器
    file_handler = logging.FileHandler(
        filename=conf.log_path + conf.log_name,
        mode='a',
        encoding='utf-8'
    )
    # 第三步：设置日志输出格式
    fmt = logging.Formatter('%(asctime)s - [%(levelname)s] - %(filename)s[%(lineno)d]：%(message)s')
    file_handler.setFormatter(fmt)
    # 第四步：绑定日志处理器到日志对象
    logger.addHandler(file_handler)
    # 第五步：设置日志级别（略）
    # 第六步：打印输出日志（在调用位置） => 直接返回日志对象即可
    return logger
