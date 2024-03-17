'''
模型类编写：
① 把表名映射为模型类名称
② 把表中的字段映射为对象属性

模型类应用场景：
① 使用模型类快速生成一个SQL插入语句，可以将数据快速插入到SQL表中
② 使用模型类快速生成一个CSV格式的数据，可以将数据快速插入到CSV文件中

准备一个json_str字符串作为测试数据，包含：id、name、age、gender、register_date注册日期
json格式字符串 => Python中，json格式数据的就是一个字符串，格式有要求：
json_str = '{"id":1, "name":"Tom", "age":23, "gender":"male", "register_date":"2023-10-01"}'
注意：JSON格式要求比较严格，key:value结构如果是字符串类型，必须使用双引号引起来

import json

json_str = '{"id":1, "name":"Tom", "age":23, "gender":"male", "register_date":"2023-10-01"}'
# 在Python代码中，有一个json模块，可以专门处理json格式的数据，把json字符串转换为Python中的数据格式
obj = json.loads(json_str)
print(obj)
print(type(obj))

print(obj['id'])
print(obj['name'])
print(obj['age'])
print(obj['gender'])
'''
import json


# 第一步：定义一个模型类（表名映射为类名）
class PersonModel(object):
    # 第二步：把接收到的JSON/日志数据转换为对象属性（表中字段映射为对象属性）
    def __init__(self, json_str: str):
        data = json.loads(json_str)  # 字典
        self.id = data['id']
        self.name = data['name']
        self.age = data['age']
        self.gender = data['gender']
        self.register_date = data['register_date']

    # 第三步：定义一个函数generate_insert_sql()，用于把接收到的数据转换为插入的SQL语句
    def generate_insert_sql(self):
        return f"insert into 数据表(id, name, age, gender, register_date) values (" \
               f"{self.id}," \
               f"'{self.name}'," \
               f"{self.age}," \
               f"'{self.gender}'," \
               f"'{self.register_date}'" \
               f");"

    # 第四步：定义一个函数generate_csv_header()，用于生成CSV的表头信息（类似Excel文件，表头，表中内容）
    # CSV文件其实就是类似于Excel文档，底层结构和txt文档非常类似
    # id, name, age
    # 1, Tom, 23
    def generate_csv_header(self, sep=','):
        return f'id{sep}' \
               f'name{sep}' \
               f'age{sep}' \
               f'gender{sep}' \
               f'register_date\n'

    # 第五步：定义一个函数generate_csv_str()，用于生成CSV中的单元格信息
    def generate_csv_str(self, sep=','):
        return f'{self.id}{sep}' \
               f'{self.name}{sep}' \
               f'{self.age}{sep}' \
               f'{self.gender}{sep}' \
               f'{self.register_date}'


if __name__ == '__main__':
    pm = PersonModel('{"id":1, "name":"Tom", "age":23, "gender":"male", "register_date":"2023-10-01"}')
    print(pm.generate_insert_sql())

    print(pm.generate_csv_header())
    print(pm.generate_csv_str())
