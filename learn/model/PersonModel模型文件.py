'''
person表
id name age
1  宝强  32
2  乃亮  35
把以上数据表结构转换为Model模型类
'''
class Person(object):
    # 初始化模型属性
    def __init__(self, id, name, age):
        self.id = id
        self.name = name
        self.age = age

person_list = [
    Person(1, '宝强', 32),
    Person(2, '乃亮', 25)
]

for i in person_list:
    print(i)
print(person_list)
# 整体就构成了一个完整的person数据表
# 为什么要构建模型类？
# 因为ETL项目目标地址有两个方面：MySQL（数据仓库）与 CSV文件（备份文件）
# CSV文件
# ① 生成头信息csv_header
# id, name, age
# ② 对person_list进行遍历操作，每遍历一次，获取一条记录 => 写入CSV的单元格中
# 1, 宝强, 32