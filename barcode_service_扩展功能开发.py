# 导入相关数据包
import time

from util import mysqlutil
from util import loggingutil
from model.barcode_model import BarcodeModel
from config import project_config as conf

# 6、创建日志对象并记录日志信息
logger = loggingutil.init_logger('barcode')  # 每个日志对象都应该有自己的名字，避免产生重复输出日志的问题
logger.info('商品数据采集开始...')

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
    logger.error('很抱歉，您要访问的商品源数据库表并不存在！')
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
    logger.info('很抱歉，暂无商品数据需要采集！')
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

# 4、事务处理功能实现 => ① 打开事务 ② 每循环1000次（读取1000个商品数据），提交一次事务 ③ 插入执行失败，回滚事务
# 定义一个data_count变量，用于记录读取的商品数量
data_count = 0
# 手工开启事务操作
target_util.begin_transaction()

start = time.time()
# - 根据数据源采集结果创建数据模型
for row_data in result:  # ((), (), ())
    #   - 在循环体内部，每循环1次（读取一个商品信息），手工更新data_count变量
    data_count += 1
    try:
        #   - 写入mysql数据库
        model = BarcodeModel(row_data)
        #   - 如果开启了事务处理，则insert_single_sql方法需要更改为insert_single_sql_without_commit
        target_util.insert_single_sql_without_commit(model.generate_insert_sql())
        #   - 写入csv文件
        csv_file.write(model.to_csv())
    except Exception as e:
        # 如果插入SQL以及写入数据到Excel失败，则回滚整个事务
        target_util.rollback_transaction()
        # 终止采集程序
        exit('插入数据执行失败，回滚事务！')
    else:
        # 读取的商品数量是否为1000的倍数 => 手工提交一次事务
        if data_count % 1000 == 0:  # 2000 % 1000 == 0
            # 手工提交一次事务操作
            target_util.commit_transaction()
            # 5、把每次采集数据的update_at时间写入到元数据表中
            # 第一步：定义SQL语句
            sql = f"insert into {conf.metadata_barcode_table_name}(time_record, gather_line_count) values (" \
                  f"'{model.update_at}', 1000);"
            # 第二步：执行SQL语句
            metadata_util.insert_single_sql(sql)
            # 打印输出一下事务提交成功的提示信息
            print(f'{data_count}条记录已经采集成功！')
            # 提前再次开启事务方便，为下一次事务处理做准备
            target_util.begin_transaction()
            # 关闭csv文件，创建一个新的csv文件
            csv_file.close()
            # 创建一个新的目标csv文件
            csv_file = open(conf.barcode_output_csv_root_path + conf.barcode_orders_output_csv_file_name, 'a+')
            # 重置指针到第一行
            csv_file.seek(0, 0)
            # 读取文件内容，判断目标文件中是否已经存在数据，如果不存在数据，则相当于是一个新CSV文件，追加标头
            content = csv_file.read(1)
            if not content:
                # 写入csv的标头
                # CSV文件中，出现了多个标头（原因：每次采集速度比较快，每1000行数据采集耗时不到1分钟，这就会导致所有采集到数据都写入到同一个CSV文件）
                csv_file.write(BarcodeModel.get_csv_header())
            # 如果文件中本身已经存在数据，则把指针指向文件尾部，继续追加新数据即可
            csv_file.seek(0, 2)

# 假设数据表中只有2001条数据，前2000条已经提交事务了，剩余的1条怎么办？
# 答：可以在循环结束，不管剩余多少条，不管是否满足1000的倍数，都可以统一提交一次事务
else:
    # 不管剩余多少条数据，手工提交一次事务
    target_util.commit_transaction()
    # 假设我们要采集的数据一共2001条数据，for循环内部记录的是2000条数据的采集操作，但是还有1条数据没有记录下来
    # 第一步：准备SQL语句
    sql = f"insert into {conf.metadata_barcode_table_name}(time_record, gather_line_count) values (" \
          f"'{model.update_at}', {data_count % 1000});"
    # 第二步：执行SQL语句
    metadata_util.insert_single_sql(sql)
    print(f'恭喜您，本次采集已经圆满结束，共采集{data_count}条记录！')

end = time.time()
logger.info(f'恭喜您，本次采集已经圆满结束，共采集{data_count}条记录，共耗时{end-start}s')

# - 关闭数据库连接
csv_file.close()
target_util.close()
source_util.close()
metadata_util.close()
