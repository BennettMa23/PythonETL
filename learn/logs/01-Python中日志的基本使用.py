# 1、导入模块
import logging
# 2、创建日志对象
logger = logging.getLogger()
# 3、创建一个处理器 => 决定日志输出位置 => StreamHandler终端？FileHandler文件？
stream_handler = logging.StreamHandler()
# 4、定义格式（略）
# 5、绑定处理器到logger日志对象
logger.addHandler(stream_handler)
# 6、定义打印输出日志级别
logger.setLevel(logging.DEBUG)
# 7、输出日志信息 => 日志一共有以下几种形式 => debug < info < warning < error < critical，默认为warning
logger.debug('这是一个debug级别信息')
logger.info('这是一个info级别信息')
logger.warning('这是一个warning警告级别信息')
logger.error('这是一个error级别信息')
logger.critical('这是一个critical严重级别信息')