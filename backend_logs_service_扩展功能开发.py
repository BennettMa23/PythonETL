import time

from util import fileutil
from util import mysqlutil
from util import loggingutil
from config import project_config as conf
from model.backend_logs_model import BackendLogsModel

# 实例化日志对象
logger = loggingutil.init_logger('logs')

# 1. 获取后台访问日志文件夹下面有哪些日志文件
# 问题：到底这个采集日志是采集什么日志？日志目录到底是哪个位置？
# 答：只能采集Nginx格式的访问日志，普通日志无法处理
# 问题：如果用这个工具采集了普通的日志文件会导致什么问题？
# 答：普通日志没有7列，所有这个工具在采集普通日志的时候会直接报错 => out of range越界
all_files_list = fileutil.get_dir_files_list(conf.backend_logs_data_root_path)
# 2. 查询元数据库表中已经被采集的日志文件，来对比确定要采集新的访问日志文件
# 第一步：创建一个mysql连接对象 => 要基于这个mysql连接对象查metadata数据库
metadata_util = mysqlutil.get_mysql_util(
    host=conf.metadata_host,
    user=conf.metadata_user,
    password=conf.metadata_password
)
# 第二步：判断元数据表不存在，还需要提前构建；查询元数据表，获取已经处理过的文件列表
processed_files_list = mysqlutil.get_processed_files(
    util=metadata_util,
    db_name=conf.metadata_db,
    tb_name=conf.logs_monitor_meta_table_name,
    tb_cols=conf.logs_monitor_meta_table_create_cols
)
# 第三步：对比all_files_list与processed_files_list，获取还未处理的文件信息
new_files_list = fileutil.get_new_by_compare_lists(processed_files_list, all_files_list)

# 添加一个判断操作
if not new_files_list:  # []
    logger.info('暂无需要采集的日志文件')
    exit()

# 3. 创建目标CSV文件以及目标数据表
csv_file = open(conf.logs_output_csv_root_path + conf.logs_output_csv_file_name, 'a')
csv_file.write(BackendLogsModel.generate_csv_header())

# 获取目标数据库对象
target_util = mysqlutil.get_mysql_util(
    host=conf.target_host,
    user=conf.target_user,
    password=conf.target_password
)

target_util.check_table_exists_and_create(
    db_name=conf.target_db,
    tb_name=conf.target_logs_table_name,
    tb_cols=conf.target_logs_table_create_cols
)

start = time.time()
# 4. 使用循环遍历所有要采集的文件，把日志文件中的每一行数据写入到CSV文件以及MySQL数据库中
for file_path in new_files_list:  # 获取要采集的文件
    # 事务处理第一步
    target_util.begin_transaction()
    # 定义一个变量，用于记录文件总行数
    row_count = 0
    try:
        for row_content in open(file_path, 'r', encoding='utf-8'):  # 从获取到的每一个文件中获取具体的内容
            # 写入每一行数据到MySQL的目标表中
            backend_logs = BackendLogsModel(row_content)
            # 调用generate_insert_sql方法生成插入语句，然后结合target_util.insert_single_sql实现插入
            target_util.insert_single_sql_without_commit(backend_logs.generate_insert_sql())
            # 把使用csv_file.write()把得到的日志写入到CSV文件
            csv_file.write(backend_logs.generate_csv_str())
            # 在循环内部更新row_count这个变量，每循环1次进行+1操作
            row_count += 1
    except Exception as e:
        # 如果写入出现异常，则回滚事务
        target_util.rollback_transaction()
    else:
        # 如果try语句中的代码没有异常，则手工提交事务
        target_util.commit_transaction()
        # 把已经处理好的文件信息写入到metadata数据库中的backend_logs_monitor
        file_path = file_path.replace('\\', '/')
        sql = f"insert into {conf.logs_monitor_meta_table_name}(file_name, process_lines) values (" \
              f"'{file_path}', {row_count})"
        metadata_util.insert_single_sql(sql)
        print(f'恭喜您，{file_path}文件已经采集完毕！')

end = time.time()
file_count = len(new_files_list)
logger.info(f'本次采集共采集了{file_count}个文件，总耗时：{end-start}s')

# 5. 当循环结束，关闭csv文件以及数据库连接
csv_file.close()
target_util.close()
metadata_util.close()