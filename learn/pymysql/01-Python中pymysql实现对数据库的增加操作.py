'''
前提：提前开启MySQL数据库
pymysql六步走：
① 导入pymysql模块
② 创建连接对象 => MySQL
③ 获取游标 => cursor
④ 定义SQL语句
⑤ 执行SQL语句获取获取返回结果，如果是增删改操作，返回受影响的行数（正常大于0）；查询操作，返回结果集
⑥ 关闭游标、关闭连接对象
'''
# ① 导入pymysql模块
import pymysql
# ② 创建连接对象 => MySQL
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123123', database='db_shun', charset='utf8')
# ③ 获取游标 => cursor
cursor = conn.cursor()
# ④ 定义SQL语句
sql = "insert into tb_students values (null, 'Rose', 25, '女', '10086')"
# ⑤ 执行SQL语句获取获取返回结果
row_nums = cursor.execute(sql)
# 还需要手工提交事务 => 默认情况下，pymysql采用事务操作保证数据操作安全，但是增删改，需要用户手工提交事务处理，否则增删改不能成功。
conn.commit()
# 如果是增删改操作，返回受影响的行数（正常大于0）；查询操作，返回结果集
if row_nums:
    print('恭喜您，信息录入成功')
else:
    print('很抱歉，信息录入失败')
# ⑥ 关闭游标、关闭连接对象
cursor.close()
conn.close()