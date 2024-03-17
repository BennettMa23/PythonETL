'''
json.loads()：把JSON格式的字符串转换为Python对象形式。
'''
# 1、导入json模块
import json
# 2、定义一个json格式的数据 => 类似Python字典，key和value值，如果是非数字类型，如果是字符串必须使用双引号引起来
json_str = '{"id":1, "name":"Tom", "age":23}'
# 3、打印输出Python对象
json_obj = json.loads(json_str)
print(json_obj)
print(type(json_obj))
