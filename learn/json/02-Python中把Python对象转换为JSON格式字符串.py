'''
json.dumps()：把Python中的对象转化为JSON格式字符串
'''
# 1、导入json模块
import json
# 2、定义一个Python对象（可以是列表也可以是字典）
dict1 = {
    'id':1,
    'name':'Tom',
    'age':23
}
# 3、使用json.dumps()实现生成JSON格式字符串
json_str = json.dumps(dict1)
print(json_str)
print(type(json_str))
print(type(dict1))
