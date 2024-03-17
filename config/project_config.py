import time
# 日志模块公共配置，要求：设置PythonETL项目日志公共存放位置 + 日志文件名称（每小时产生一个.log日志文件）
log_path = 'D:/IT-gongcheng/ETL/PythonETL/logs/'  #D:\IT-gongcheng\ETL\PythonETL\logs
log_name = f"pyetl-{time.strftime('%Y-%m-%d_%H', time.localtime())}.log"

# ################## --元数据库metadata配置项-- ###################
# 元数据库配置
metadata_host = 'localhost'
metadata_port = 3306
metadata_user = 'root'
metadata_password = '123456'
metadata_db = 'metadata'

# ################## --后台日志数据采集配置项-- ###################
# 待采集 日志 文件所在的目录
backend_logs_data_root_path = 'D:/IT-gongcheng/ETL/input/logs/'

# 定义目标数仓信息（MySQL具体信息）
target_host = 'localhost'
target_port = 3306
target_user = 'root'
target_password = '123456'
target_db = 'retail'

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


# ################## --数据库barcode商品数据采集配置项-- ###################
# barcode业务：update_at字段的监控表的名称
metadata_barcode_table_name = 'barcode_monitor'
# barcode业务：update_at字段的监控表的建表语句的列信息
metadata_barcode_table_create_cols = "id INT PRIMARY KEY AUTO_INCREMENT COMMENT '自增ID', " \
                                     "time_record TIMESTAMP NOT NULL COMMENT '本次采集记录的最大时间', " \
                                     "gather_line_count INT NULL COMMENT '本次采集条数'"
# 数据源库配置
source_host = 'localhost'
source_user = 'root'
source_password = '123456'
source_port = 3306
source_db = 'source_data'
# 数据源表名称
source_barcode_table_name = 'sys_barcode'

# 目标数据表与数据表结构
target_barcode_table_name = 'sys_barcode'
target_barcode_table_create_cols = """
    `code` varchar(50) PRIMARY KEY COMMENT '商品条码',
    `name` varchar(200) DEFAULT '' COMMENT '商品名称',
    `spec` varchar(200) DEFAULT '' COMMENT '商品规格',
    `trademark` varchar(100) DEFAULT '' COMMENT '商品商标',
    `addr` varchar(200) DEFAULT '' COMMENT '商品产地',
    `units` varchar(50) DEFAULT '' COMMENT '商品单位(个、杯、箱、等)',
    `factory_name` varchar(200) DEFAULT '' COMMENT '生产厂家',
    `trade_price` DECIMAL(50, 5) DEFAULT 0.0 COMMENT '贸易价格(指导进价)',
    `retail_price` DECIMAL(50, 5) DEFAULT 0.0 COMMENT '零售价格(建议卖价)',
    `update_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `wholeunit` varchar(50) DEFAULT NULL COMMENT '大包装单位',
    `wholenum` int(11) DEFAULT NULL COMMENT '大包装内装数量',
    `img` varchar(500) DEFAULT NULL COMMENT '商品图片',
    `src` varchar(20) DEFAULT NULL COMMENT '源信息', 
    INDEX (update_at)
"""

# 商品数据写出 csv 根路径
barcode_output_csv_root_path = "D:/IT-gongcheng/ETL/output/barcode/"
# 商品数据写出 csv 文件名
barcode_orders_output_csv_file_name = f'barcode-{time.strftime("%Y-%m-%d-%H_%M", time.localtime())}.csv'

# ################## --订单JSON数据采集配置项-- ###################
# 采集订单JSON数据，元数据表配置项
file_monitor_meta_table_name = "json_file_monitor"
file_monitor_meta_table_create_cols = \
    "id INT PRIMARY KEY AUTO_INCREMENT, " \
    "file_name VARCHAR(255) NOT NULL COMMENT '处理文件名称', " \
    "process_lines INT NULL COMMENT '文件处理行数', " \
    "process_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '文件处理时间'"
