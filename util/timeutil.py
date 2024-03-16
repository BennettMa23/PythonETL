import time

def ts13_to_ts10(ts):
    """将13位的时间戳规范成10位的时间戳"""
    # JSON数据当中,时间戳是以毫秒为单位的
    # 从JSON中读取出来的时间戳要被python使用要转换为秒为单位(10位)
    return ts // 1000


def ts10_to_date_str(ts, format_str='%Y-%m-%d %H:%M:%S'):
    """将10位的时间戳转换为日期字符串"""
    struct_time = time.localtime(ts)
    return time.strftime(format_str, struct_time)


def ts13_to_date_str(ts, format_str='%Y-%m-%d %H:%M:%S'):
    """将13位时间戳转换为日期字符串"""
    ts = ts13_to_ts10(ts)
    return ts10_to_date_str(ts, format_str)
