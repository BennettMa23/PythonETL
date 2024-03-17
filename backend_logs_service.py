from util import fileutil
from util import mysqlutil
from config import project_config as conf
from model.backend_logs_model import BackendLogsModel

# 1. 获取后台访问日志文件夹下面有哪些日志文件
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
# print(new_files_list)

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

# 4. 使用循环遍历所有要采集的文件，把日志文件中的每一行数据写入到CSV文件以及MySQL数据库中
for file_path in new_files_list:  # 获取要采集的文件
    for row_content in open(file_path, 'r', encoding='utf-8'):  # 从获取到的每一个文件中获取具体的内容
        # 写入每一行数据到MySQL的目标表中
        backend_logs = BackendLogsModel(row_content)
        # 调用generate_insert_sql方法生成插入语句，然后结合target_util.insert_single_sql实现插入
        target_util.insert_single_sql(backend_logs.generate_insert_sql())
        # 把使用csv_file.write()把得到的日志写入到CSV文件
        csv_file.write(backend_logs.generate_csv_str())
    print(f'恭喜您，{file_path}文件已经采集完毕！')

# 5. 当循环结束，关闭csv文件以及数据库连接
csv_file.close()
target_util.close()
metadata_util.close()