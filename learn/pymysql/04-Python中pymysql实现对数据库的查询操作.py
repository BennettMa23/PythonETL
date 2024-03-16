# 1、导入pymysql模块
import pymysql
# 2、创建连接对象
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123123', database='db_shun', charset='utf8')
# 3、获取游标
cursor = conn.cursor()
# 4、定义SQL语句
sql = "select * from tb_students"
# 5、执行SQL语句并返回结果集
cursor.execute(sql)
# 游标在执行SQL以后，我们可以通过cursor.fetchall()获取所有数据/cursor.fetchone()获取第一条数据/cursor.fetchmany(num)获取多条数据
# result = cursor.fetchall()
# result = cursor.fetchone()
result = cursor.fetchmany(3)
print(result)
# 6、关闭游标与连接对象
cursor.close()
conn.close()