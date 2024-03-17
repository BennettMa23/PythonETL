# 导入工具包
from util import fileutil
from util import mysqlutil
from util import loggingutil
from model.orders_model import RetailOriginModel
from model import orders_model
from config import project_config as conf

# 1. 获取订单文件夹下面有哪些订单JSON文件 => [x00, x01, x02, x03]
all_json_files = fileutil.get_dir_files_list(conf.json_data_path)
# 2. 查询元数据库表中已经被采集的订单JSON文件，来对比确定要采集新的订单JSON文件
# - 创建元数据连接
metadata_util = mysqlutil.get_mysql_util(
    host=conf.metadata_host,
    user=conf.metadata_user,
    password=conf.metadata_password
)
# - 检查数据表是否存在,不存在则创建
metadata_util.check_table_exists_and_create(
    db_name=conf.metadata_db,
    tb_name=conf.file_monitor_meta_table_name,
    tb_cols=conf.file_monitor_meta_table_create_cols
)
# - 获取元数据中已经被采集的Json文件路径列表 => [x00, x01]
sql = f"select * from {conf.file_monitor_meta_table_name}"
result = metadata_util.query(sql)  # ((1, 'x00'), (2, 'x01'), (3, 'x02'))
processed_json_files = [i[1] for i in result]
# - 对比确定要采集的新订单文件 => [x02, x03]
new_json_files = fileutil.get_new_by_compare_lists(processed_json_files, all_json_files)
# 3. 针对待采集的新订单JSON文件，进行数据采集（ETL操作->mysql->csv）
# - 创建csv文件,并打开文件(订单表+订单详情表)
csv_order_file = open(conf.retail_output_csv_root_path + conf.retail_orders_output_csv_file_name, 'a')
csv_order_detail_file = open(conf.retail_output_csv_root_path + conf.retail_orders_detail_output_csv_file_name, 'a')
# - 向csv文件中写入标头信息(订单表+订单详情表)
csv_order_file.write(orders_model.OrdersModel.get_csv_header())
csv_order_detail_file.write(orders_model.OrdersDetailModel.get_csv_header())
# - 创建一个目标数据库连接对象
target_util = mysqlutil.get_mysql_util(
    host=conf.target_host,
    user=conf.target_user,
    password=conf.target_password
)
# - 检查目标数据表是否存在,不存在则创建
# 检查订单表
target_util.check_table_exists_and_create(
    db_name=conf.target_db,
    tb_name=conf.target_orders_table_name,
    tb_cols=conf.target_orders_table_create_cols
)
# 检查订单详情表
target_util.check_table_exists_and_create(
    db_name=conf.target_db,
    tb_name=conf.target_orders_detail_table_name,
    tb_cols=conf.target_orders_detail_table_create_cols
)
# - 遍历待处理的JSON文件
for json_file in new_json_files:
    #   - 按行读取JSON文件, 创建数据模型
    for json_data in open(json_file, 'r', encoding='utf-8'):
        #   - 创建原始业务数据模型对象
        model = RetailOriginModel(json_data)
        #   - 对模型进行处理,订单价格高于10000的记录直接剔除 => 异常数据
        if model.order_model.receivable <= 10000:
            #   - 写入到目标表中
            target_util.insert_single_sql(model.order_model.generate_insert_sql())
            target_util.insert_single_sql(model.order_detail_model.generate_insert_sql())
            #   - 写入到csv文件中
            csv_order_file.write(model.order_model.to_csv())
            csv_order_detail_file.write(model.order_detail_model.to_csv())

# 关闭文件以及数据库连接
csv_order_file.close()
csv_order_detail_file.close()
target_util.close()
metadata_util.close()

