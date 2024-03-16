# 1、导入pymysql模块
import pymysql
# 2、创建连接对象
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123123', database='db_shun', charset='utf8')
# 3、获取游标
cursor = conn.cursor()
# 4、定义SQL语句
sql = "delete from tb_students where id = 2"
# 5、执行SQL语句并提交事务
row_nums = cursor.execute(sql)
conn.commit()

if row_nums:
    print('恭喜您，信息删除成功')
else:
    print('很抱歉，信息删除失败')
# 6、关闭游标与连接
cursor.close()
conn.close()