# 1、导入logging模块
import logging
# 2、创建一个日志对象
logger = logging.getLogger()
# 3、创建一个日志处理器，决定日志输出位置stream终端，file文件
stream_handler = logging.StreamHandler()
# 4、定义一个日志格式
# asctime创建时间，levelname日志级别名称，filename由哪个文件产生日志，lineno行号，message代表具体日志信息
fmt = logging.Formatter('%(asctime)s - [%(levelname)s] - %(filename)s[%(lineno)d]：%(message)s')  # Formatter日志对象
stream_handler.setFormatter(fmt)
# 5、把处理器绑定到日志对象
logger.addHandler(stream_handler)
# 6、设置输出日志级别
logger.setLevel(logging.DEBUG)
# 7、打印输出日志信息
logger.debug('这是一个debug级别的日志信息')
logger.info('这是一个info级别的日志信息')
logger.warning('这是一个warning级别的日志信息')
logger.error('这是一个error级别的日志信息')
logger.critical('这是一个critical级别的日志信息')