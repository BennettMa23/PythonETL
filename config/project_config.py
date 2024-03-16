import time
# 日志模块公共配置，要求：设置PythonETL项目日志公共存放位置 + 日志文件名称（每小时产生一个.log日志文件）
log_path = 'D:/IT-gongcheng/ETL/PythonETL/logs/'  #D:\IT-gongcheng\ETL\PythonETL\logs
log_name = f"pyetl-{time.strftime('%Y-%m-%d_%H', time.localtime())}.log"

# ################## --元数据库metadata配置项-- ###################
# 元数据库配置
metadata_host = 'localhost'
metadata_port = 3306
metadata_user = 'root'
metadata_password = '123123'
metadata_db = 'metadata'

# ################## --后台日志数据采集配置项-- ###################
# 待采集 日志 文件所在的目录
backend_logs_data_root_path = 'D:/IT-gongcheng/ETL/input/logs/'

# 采集后台日志数据，元数据表配置项
logs_monitor_meta_table_name = "backend_logs_monitor"
logs_monitor_meta_table_create_cols = \
    "id INT PRIMARY KEY AUTO_INCREMENT, " \
    "file_name VARCHAR(255) NOT NULL COMMENT '处理文件名称', " \
    "process_lines INT NULL COMMENT '文件处理行数', " \
    "process_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '文件处理时间'"

# 后台日志表名称
target_logs_table_name = "backend_logs"
target_logs_table_create_cols = \
        f"id int PRIMARY KEY AUTO_INCREMENT COMMENT '自增ID', " \
        f"log_time TIMESTAMP(6) COMMENT '日志时间,精确到6位毫秒值', " \
        f"log_level VARCHAR(10) COMMENT '日志级别', " \
        f"log_module VARCHAR(50) COMMENT '输出日志的功能模块名', " \
        f"response_time INT COMMENT '接口响应时间毫秒', " \
        f"province VARCHAR(30) COMMENT '访问者省份', " \
        f"city VARCHAR(30) COMMENT '访问者城市', " \
        f"log_text VARCHAR(255) COMMENT '日志正文', " \
        f"INDEX(log_time)"

# 后台日志数据写出 csv 的根路径
logs_output_csv_root_path = "D:/IT-gongcheng/ETL/output/backend_logs/"
# 每一次运行，后台日志文件写出路径
logs_output_csv_file_name = f"logs-{time.strftime('%Y-%m-%d_%H', time.localtime())}.csv"


# ################## --订单JSON数据采集配置项-- ###################
# 采集订单JSON数据，元数据表配置项
file_monitor_meta_table_name = "json_file_monitor"
file_monitor_meta_table_create_cols = \
    "id INT PRIMARY KEY AUTO_INCREMENT, " \
    "file_name VARCHAR(255) NOT NULL COMMENT '处理文件名称', " \
    "process_lines INT NULL COMMENT '文件处理行数', " \
    "process_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '文件处理时间'"
