# 1、导入logging日志模块
import logging
# 2、创建日志对象
logger = logging.getLogger()
# 3、创建日志处理器 => 决定了日志输出位置 stream终端，file文件
file_handler = logging.FileHandler(
    filename='./test.log',
    mode='w',
    encoding='utf-8'
)
# 4、设置日志格式
fmt = logging.Formatter('%(asctime)s - [%(levelname)s] - %(filename)s[%(lineno)d]：%(message)s')
file_handler.setFormatter(fmt)
# 5、绑定日志处理器到日志对象中
logger.addHandler(file_handler)

# 控制台显示
stream_handler=logging.StreamHandler()#获取一个将日志输出到控制台的Handler对象
stream_handler.setFormatter(fmt)
logger.addHandler(stream_handler)#给logger对象添加了将日志输出到控制台的功能

# 6、设置日志级别
logger.setLevel(logging.DEBUG)
# 7、打印输出日志
logger.debug('这是一个debug级别日志信息')
logger.info('这是一个info级别日志信息')
logger.warning('这是一个warning级别日志信息')
logger.error('这是一个error级别日志信息')
logger.critical('这是一个critical级别日志信息')