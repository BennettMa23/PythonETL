# 1、导入时间模块
import time
# 2、让程序休眠，单位s
# print(111)
# time.sleep(3)
# print(222)
# 3、返回当前时间的时间戳（单位s）
print(time.time())
# 4、返回当前时间的时间戳（单位ns）
print(time.time_ns())
# 5、获取本地时间 => 返回的struct_time对象
st1 = time.localtime()
print(st1)
print(st1.tm_year)
print(st1.tm_mon)
print(st1.tm_mday)
# 6、把一个时间戳转换为struct_time对象（时间戳 => struct_time对象）
st2 = time.localtime(1693033456.3961368)
print(st2)
# 7、把一个struct_time对象转换为时间戳（struct_time对象 => 时间戳）
print(time.mktime(st2))
# 8、把一个struct_time对象转换为时间格式字符串 => %Y-%m-%d %H:%M:%S
print(time.strftime('%Y-%m-%d %H:%M:%S', st2))
# 9、把一个日期格式字符串转换为struct_time对象
print(time.strptime('2023-08-26 15:10:20', '%Y-%m-%d %H:%M:%S'))