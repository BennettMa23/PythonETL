'''
在Python代码中，我们可以使用(json)模块使用对json数据的处理？
（json.loads()）：把JSON格式字符串转换为Python对象
（json.dumps()）：把Python对象转化为内JSON格式字符串

练习：把json格式的字符串 => json_str = '{"order_id":"001", "order_amount":"59.80", "user":"Tom"}'
请使用相关方法，将JSON格式字符串转换为Python对象的形式。
'''
import json
from collections import namedtuple
from json import JSONEncoder


def customStudentDecoder(studentDict):
    return namedtuple('X', studentDict.keys())(*studentDict.values())


# Assume you received this JSON response
studentJsonData = '{"order_id":"001", "order_amount":"59.80", "user":"Tom"}'

# Parse JSON into an object with attributes corresponding to dict keys.
student = json.loads(studentJsonData, object_hook=customStudentDecoder)

print("After Converting JSON Data into Custom Python Object")
print(student.rollNumber, student.name)