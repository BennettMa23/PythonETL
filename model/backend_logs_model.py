'''
日志文件映射为模型类，每一条日志又包含了很多信息，这些信息可以拆解为一个一个字符串，每个字符串就是模型对象属性
'''
from config import project_config as conf


class BackendLogsModel(object):
    # 1、定义一个初始化方法
    # log_data:2023-08-29 17:29:03.476065	[INFO]	orders_service.py	响应时间:62ms	重庆市	万州区	这里是日志信息......
    def __init__(self, log_data: str):
        # 第一步：对log_data进行切割操作
        data = log_data.split('\t')
        # 第二步：建立映射关系
        self.log_time = data[0]
        self.log_level = data[1].strip('[]')
        self.log_module = data[2]
        self.response_time = data[3][5:-2]
        self.province = data[4]
        self.city = data[5]
        self.log_text = data[6]

    # 2、定义一个生成SQL函数，用于向数仓插入数据
    def generate_insert_sql(self):
        return f'insert into {conf.target_logs_table_name}(log_time, log_level, log_module, response_time, province, ' \
               f'city, log_text) values (' \
               f'"{self.log_time}",' \
               f'"{self.log_level}",' \
               f'"{self.log_module}",' \
               f'{self.response_time},' \
               f'"{self.province}",' \
               f'"{self.city}",' \
               f'"{self.log_text}"' \
               f');'

    # 3、定义一个生成csv头信息函数，用于生成CSV的头信息
    @staticmethod
    def generate_csv_header(sep=','):
        # log_time, log_level, log_module,...
        return f'log_time{sep}' \
               f'log_level{sep}' \
               f'log_module{sep}' \
               f'response_time{sep}' \
               f'province{sep}' \
               f'city{sep}' \
               f'log_text\n'

    # 4、定义一个生成csv内容函数，用于生成CSV的行信息
    def generate_csv_str(self, sep=','):
        # 时间,级别,页面,响应时间,...
        return f'{self.log_time}{sep}' \
               f'{self.log_level}{sep}' \
               f'{self.log_module}{sep}' \
               f'{self.response_time}{sep}' \
               f'{self.province}{sep}' \
               f'{self.city}{sep}' \
               f'{self.log_text}'


if __name__ == '__main__':
    backend_logs = BackendLogsModel(
        '2023-08-29 17:29:03.476065	[INFO]	orders_service.py	响应时间:62ms	山东市	济南区	这里是日志信息......')
    print(backend_logs.generate_insert_sql())
    print(backend_logs.generate_csv_header())
    print(backend_logs.generate_csv_str())
    # 模拟生成csv文件
    f = open('backend_logs.csv', 'a')
    f.write(backend_logs.generate_csv_header())
    f.write(backend_logs.generate_csv_str())
    f.close()
