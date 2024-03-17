# 导入相关数据包
from util import mysqlutil
from util import loggingutil
from model.barcode_model import BarcodeModel
from config import project_config as conf

# 1、查询元数据表，获取最大采集时间
# - 创建元数据库连接对象
metadata_util = mysqlutil.get_mysql_util(
    host=conf.metadata_host,  # localhost
    user=conf.metadata_user,  # root
    password=conf.metadata_password  # root
)
# - 检查元数据表是否存在，不存在则创建
metadata_util.check_table_exists_and_create(
    db_name=conf.metadata_db,  # metadata
    tb_name=conf.metadata_barcode_table_name,  # barcode_monitor
    tb_cols=conf.metadata_barcode_table_create_cols  # 表中字段，如果表不存在，则根据这个字段自动创建
)
# - 查询商品采集元数据表中，上一次采集记录的 updateAt 的最大值
sql = f"select max(time_record) from {conf.metadata_barcode_table_name}"
result = metadata_util.query(sql)  # ((None,),)，取出第一个元素中的第一个元素值 => None提取出来，代表最大的采集时间

# - 判断获取到的数据集是否有值,创建变量保存该值
if result[0][0]:
    #   - 如果有值则保存
    barcode_max_time = result[0][0]  # 获取最大采集时间, 如2023-09-01, 采集商品表时，取updateAt > 2023-09-01
else:
    #   - 如果没有值则保存None
    barcode_max_time = None

# 2、根据上一次采集商品数据中 updateAt 的最大值，查询数据源库商品表，获取继上一次采集之后，新增和更新的商品数据
# - 创建数据源数据库连接对象
source_util = mysqlutil.get_mysql_util(
    host=conf.source_host,
    user=conf.source_user,
    password=conf.source_password
)
# - 判断数据源数据库是否存在
if not source_util.check_table_exists(conf.source_db, conf.source_barcode_table_name):
    #   - 如果不存在则退出程序
    exit('数据源表不存在，请与后端人员联系解决！')
# - 查询元数据库表,获取上次采集时间,然后在根据这个最大采集时间去商品源表中获取增量更新的条码商品数据
if not barcode_max_time:  # 没有最大采集时间，返回值是None
    #   - 没有最大采集时间(初次采集,全量采集)
    sql = f"select * from {conf.source_barcode_table_name} order by updateAt;"
else:
    # - 有最大采集时间(再次采集,增量采集)
    sql = f"select * from {conf.source_barcode_table_name} where updateAt > '{barcode_max_time}' order by updateAt;"
# - 执行sql语句
result = source_util.query(sql)  # (), ((), (), ())
# - 判断采集数据条目数
if not result:
    #   - 如果条目数为0则退出去程序
    exit('很抱歉，暂无需要采集的商品数据...')

# 3、针对新增及更新的商品数据，实现ETL采集工作
# 前提：更改barcode_model模型类
# - 创建目标数据库连接对象
target_util = mysqlutil.get_mysql_util(
    host=conf.target_host,
    user=conf.target_user,
    password=conf.target_password
)
# - 检查目标数据库表是否存在,如果不存在则创建
target_util.check_table_exists_and_create(
    db_name=conf.target_db,
    tb_name=conf.target_barcode_table_name,
    tb_cols=conf.target_barcode_table_create_cols
)
# - 创建目标csv文件
csv_file = open(conf.barcode_output_csv_root_path + conf.barcode_orders_output_csv_file_name, 'a')
# - 写入csv的标头
csv_file.write(BarcodeModel.get_csv_header())
# - 根据数据源采集结果创建数据模型
for row_data in result:  # ((), (), ())
    #   - 写入mysql数据库
    model = BarcodeModel(row_data)
    target_util.insert_single_sql(model.generate_insert_sql())
    #   - 写入csv文件
    csv_file.write(model.to_csv())
# - 关闭数据库连接
csv_file.close()
target_util.close()
source_util.close()
metadata_util.close()
