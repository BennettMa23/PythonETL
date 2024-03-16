"""
字符串工具方法
"""
def check_null(data):
    """
    功能：检查传入的字符串是否为空、None或其他无意义的内容，True表示空，False表示非空
    """
    if not data:
        return True

    # 转小写
    data = data.lower()  # data = data.lower() == data ABCD => data.lower() abcd
    if data in ('null', 'none', 'undefined'):
        return True

    return False


def check_null_and_transform(data):
    """
    功能：检查字符串，如果是空内容，返回空字符串，同时兼具去除字符串两边空字符的功能
    """
    if check_null(str(data)):
        return ''
    elif isinstance(data, str):  # 判断左边的变量是否为右边的数据类型 => True or False
        return data.strip()  # strip()：去除字符串两边的空格
    else:
        return data


def check_str_null_and_transform_to_sql_null(data):
    """
    功能：检查传入字符串
        如果是空内容，返回'null'字符串，用于sql插入
        否则返回数据本身，并带上""包裹用于sql插入
    """
    if check_null(str(data)):
        return 'null'
    else:
        return f"'{data}'"  # Tom => 'Tom', insert into T values (null, data)


def check_number_null_and_transform_to_sql_null(data):
    """
    功能：检查传入的数字或字符串数据是否是空
    如果是空内容，则返回'null'字符串
    否则返回数据本身
    """
    if not data or check_null(str(data)):
        return 'null'
    else:
        return data  # 10


def clear_str(data):
    """
    功能：处理字符串中异常字符，如 单引号,双引号,逗号,分号等
    Note：这个API有可能破坏数据本身的内容,慎用
    """
    if check_null(data):
        # 如果是无意义内容,直接返回不处理了.
        return data

    data = data.replace("'", "")
    data = data.replace("\"", "")
    data = data.replace(";", "")
    data = data.replace(",", "")
    data = data.replace("@", "")
    data = data.replace("\\", "")  # 把字符串中的反斜杠去除 => abc\bcd > abcbcd

    return data
