# 1、导入pymysql模块以及日志模块
import pymysql
from util import loggingutil

# 2、创建一个日志对象，用于生成日志信息
logger = loggingutil.init_logger('mysql')

# 3、定义一个MysqlUtil工具类
class MysqlUtil(object):
    '''
    1. 初始化对象 2. 切换数据库 3. 执行非查询SQL 4. 执行查询SQL 5. 开启事务 6. 提交事务 7. 回滚事务
    8. 判断数据表是否存在 9. 检查表是否存在，不存在则创建
    10. 执行一条插入SQL 11. 关闭数据库连接
    '''
    # 创建数据库连接对象
    def __init__(self, host, user, password, port=3306, charset='utf8', autocommit=False):
        self.conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            charset=charset,
            autocommit=autocommit
        )
        logger.info(f'主机为{host}:{port}的MySQL数据库已经连接成功！')

    # 切换数据库
    def select_db(self, db_name):
        self.conn.select_db(db_name)

    # 执行非查询SQL => execute() => 增删改
    def execute(self, sql):
        # 获取游标
        cursor = self.conn.cursor()
        # 执行sql语句
        cursor.execute(sql)
        # 判断事务是否自动提交
        if not self.conn.get_autocommit():  # True:自动提交，False:非自动提交
            self.conn.commit()
        # 关闭游标
        cursor.close()
        # 打印日志信息
        logger.info(f'非查询SQL语句:{sql}执行成功')

    # 执行查询SQL => query() => 返回数据集 => ((记录), (记录), (记录))
    def query(self, sql):
        # 获取游标
        cursor = self.conn.cursor()
        # 执行SQL语句
        cursor.execute(sql)
        # 获取数据集
        result = cursor.fetchall()
        # 关闭游标
        cursor.close()
        # 打印日志信息
        logger.info(f'查询SQL语句:{sql}执行成功')
        # 把result作为返回值
        return result

    # 开启事务
    def begin_transaction(self):
        # 执行判断操作，判断MySQL系统是否已经开启自动提交
        if self.conn.get_autocommit():
            # 如果MySQL端默认开启事务，则会产生事务操作冲突，手工关闭自动提交
            logger.info('您的MySQL已经开启了事务自动提交，为了避免冲突，手工关闭自动提交')
            self.conn.autocommit(False)
        # 手工开启事务操作
        self.conn.begin()
        logger.info('开启事务操作成功')

    # 提交事务
    def commit_transaction(self):
        # 提交事务
        self.conn.commit()
        logger.info('事务执行成功，提交事务')

    # 回滚事务
    def rollback_transaction(self):
        # 回滚事务
        self.conn.rollback()
        logger.info('事务执行失败，回滚事务')

    # 检查数据表是否存在，存在返回True；不存在则返回False
    def check_table_exists(self, db_name, tb_name):  # db_name数据库名称，tb_name数据表名称
        # 第一步：切换数据库
        self.select_db(db_name)
        # 第二步：定义SQL语句 => show tables查看所有数据表信息
        sql = "show tables;"
        # 第三步：执行SQL查询 => 调用自身的query方法，传入参数为sql => ((a, ), (b, ), (c, ))
        result = self.query(sql)
        # 第四步：判断tb_name是否存在于以上查询结果中，返回布尔类型的值
        return (tb_name, ) in result

    # 检查数据表是否存在，如果不存在，则自动创建该数据表
    def check_table_exists_and_create(self, db_name, tb_name, tb_cols):  # create table T(id int, name varchar(20))
        # 第一步：判断数据表是否存在
        if not self.check_table_exists(db_name, tb_name):
            # 第二步：如果数据表不存在，则自动创建该数据表（错误演示位置）
            sql = f'create table {tb_name}({tb_cols}) engine=innodb default charset=utf8;'
            # print(sql)
            self.execute(sql)
            logger.info(f'{tb_name}在数据库{db_name}中已经创建成功')
        else:
            # 第三步：如果数据表已经存在，则打印输出日志信息
            logger.info(f'{tb_name}在数据库{db_name}中已经存在，跳过创建过程')

    # query_all(db_name, tb_name, limit=None)方法，限制查询数量 => 针对某个数据表进行全表查询
    def query_all(self, db_name, tb_name, limit=None):
        # 第一步：切换数据库
        self.select_db(db_name)
        # 第二步：定义SQL语句
        sql = f"select * from {tb_name}"
        # 第三步：判断limit参数是否为空 => Python中变量是否为None，不能使用等号，要使用is None以及is not None来进行判断
        if limit is not None:
            # 容易踩坑的地方，引号内部必须保留一个空格
            sql += f' limit {limit}'  # select * from T limit 5
        # 第四步：调用query方法，执行以上SQL语句并返回结果
        result = self.query(sql)
        # 第五步：打印输出日志信息
        logger.info(f'SQL查询语句：{sql}执行成功')
        return result

    # insert_single_sql函数编写，这个函数主要作用用于执行SQL插入操作
    # 疑问：前面已经编写了一个execute()方法，为什么还需要单独编写一个insert_single_sql方法？
    # 答：因为这个项目需要大量的插入操作，execute方法没有具体的报错信息，只能告诉我们成功或失败，为了标记插入异常，引入了一个insert_single_sql
    def insert_single_sql(self, sql):
        # 引入try...except...else，捕获异常
        try:
            self.execute(sql)  # 自动执行sql语句并提交事务
        except Exception as e:
            logger.error(f'{sql}插入语句执行异常，报错信息为：{e}')
            raise e  # 抛出异常到终端，阻碍代码的继续执行
        else:
            logger.info(f'{sql}插入语句执行成功，没有任何异常')

    # 添加一个insert_single_sql_without_commit
    def insert_single_sql_without_commit(self, sql):
        try:
            # 获取游标
            cursor = self.conn.cursor()
            # 执行sql语句
            cursor.execute(sql)  # 获取游标执行sql语句，但是没有自动提交
        except Exception as e:
            logger.error(f'{sql}插入语句执行异常，报错信息为：{e}')
            raise e
        else:
            logger.info(f'{sql}插入语句执行成功，没有任何异常')

    # close方法编写，主要用于关闭连接对象
    def close(self):
        if self.conn:
            self.conn.close()
        logger.info('conn连接对象关闭成功')


# 第一个函数：获取mysqlutil数据库对象
def get_mysql_util(host, user, password, port=3306, charset='utf8', autocommit=False):
    mysqlutil = MysqlUtil(host, user, password, port, charset, autocommit)
    return mysqlutil

# 第二个函数：获取元数据库表中已经处理过的文件列表
# 扩展：参数新形势 => 参数名称:期望的数据类型，如util:MysqlUtil，代表util这个参数要求是MysqlUtil类对象
def get_processed_files(util:MysqlUtil, db_name, tb_name, tb_cols):
    '''
    获取元数据库表中，已经处理过的文件列表
    :param util: 代表util这个参数要求是MysqlUtil类对象
    :param db_name: 元数据库名称
    :param tb_name: 元数据库中表名称
    :param tb_cols: 元数据表中表对应的字段，如果数据表本身不存在，需要自动创建改变
    :return: list列表类型，已经处理过的文件列表
    '''
    # 1. 定义一个空列表，用于接收已经处理过的文件信息
    new_list = []
    # 2. 使用util（MysqlUtil)对象，判断元数据表是否存在，不存在则自动创建该表
    util.check_table_exists_and_create(
        db_name=db_name,
        tb_name=tb_name,
        tb_cols=tb_cols
    )
    # 3. 查询数据表中的所有数据
    result = util.query_all(db_name, tb_name)  # ((1, 'D:/etl/json/x01', 1024, xxx), (1, 'D:/etl/json/x02', 1024, xxx))
    # 4. 对result进行遍历，获取要处理的文件信息并写入到new_list列表中
    for row in result:
        new_list.append(row[1])
    # 5. 返回已经处理过的列表信息
    return new_list