# 第一步：导入模块
from util.strutil import clear_str
from util.strutil import check_str_null_and_transform_to_sql_null, check_number_null_and_transform_to_sql_null
from config import project_config as conf

# 第二步：定义模型类，并编写初始化方法 => 建立映射关系
class BarcodeModel(object):
    # 把商品条码库字段信息，作为属性
    def __init__(self, data_tuple:tuple):  # 数据是以元组方式发送给data_tuple => ('014779000888', '日本眉机', '', '', '', '个', 'null', 0.0000, 0.0000, '2017-07-10 16:56:44', '', 0, 'null', 'null')
        self.code = data_tuple[0]
        self.name = clear_str(data_tuple[1])
        self.spec = clear_str(data_tuple[2])
        self.trademark = clear_str(data_tuple[3])
        self.addr = clear_str(data_tuple[4])
        self.units = clear_str(data_tuple[5])
        self.factory_name = clear_str(data_tuple[6])
        self.trade_price = data_tuple[7]
        self.retail_price = data_tuple[8]
        self.update_at = str(data_tuple[9])
        self.wholeunit = clear_str(data_tuple[10])
        self.wholenum = data_tuple[11]
        self.img = data_tuple[12]
        self.src = data_tuple[13]
    # 第三步：生成SQL的插入语句
    def generate_insert_sql(self):
        # 由于商品数据既有新增又有更新操作，写入到数仓，更新数据不能重复，直接覆盖原始业务数据
        # 1 2 3 4 5 6 7（直接覆盖）
        # replace into xxx(字段) values (值) => 适合既有新增又有更新，因为更新数据直接覆盖原始数据
        # insert into xxx(字段) values (值) => 适合只有新增的情况
        sql = f"replace into {conf.target_barcode_table_name}(code,name,spec,trademark,addr,units,factory_name," \
              f"trade_price,retail_price,update_at,wholeunit,wholenum,img,src) values (" \
              f"'{self.code}'," \
              f"{check_str_null_and_transform_to_sql_null(self.name)}," \
              f"{check_str_null_and_transform_to_sql_null(self.spec)}," \
              f"{check_str_null_and_transform_to_sql_null(self.trademark)}," \
              f"{check_str_null_and_transform_to_sql_null(self.addr)}," \
              f"{check_str_null_and_transform_to_sql_null(self.units)}," \
              f"{check_str_null_and_transform_to_sql_null(self.factory_name)}," \
              f"{check_number_null_and_transform_to_sql_null(self.trade_price)}," \
              f"{check_number_null_and_transform_to_sql_null(self.retail_price)}," \
              f"{check_str_null_and_transform_to_sql_null(self.update_at)}," \
              f"{check_str_null_and_transform_to_sql_null(self.wholeunit)}," \
              f"{check_number_null_and_transform_to_sql_null(self.wholenum)}," \
              f"{check_str_null_and_transform_to_sql_null(self.img)}," \
              f"{check_str_null_and_transform_to_sql_null(self.src)}" \
              f");"
        return sql

    # 第四步：生成 csv 数据的标头内容
    @staticmethod
    def get_csv_header(sep=','):
        return f"code{sep}" \
               f"name{sep}" \
               f"spec{sep}" \
               f"trademark{sep}" \
               f"addr{sep}" \
               f"units{sep}" \
               f"factory_name{sep}" \
               f"trade_price{sep}" \
               f"retail_price{sep}" \
               f"update_at{sep}" \
               f"wholeunit{sep}" \
               f"wholenum{sep}" \
               f"img{sep}" \
               f"src\n"

    # 第五步：生成csv数据行
    def to_csv(self, sep=','):
        return f"{self.code}{sep}" \
               f"{self.name}{sep}" \
               f"{self.spec}{sep}" \
               f"{self.trademark}{sep}" \
               f"{self.addr}{sep}" \
               f"{self.units}{sep}" \
               f"{self.factory_name}{sep}" \
               f"{self.trade_price}{sep}" \
               f"{self.retail_price}{sep}" \
               f"{self.update_at}{sep}" \
               f"{self.wholeunit}{sep}" \
               f"{self.wholenum}{sep}" \
               f"{self.img}{sep}" \
               f"{self.src}\n"
    # 疑问：为什么日志采集中csv_str不需要添加\n，而商品数据采集to_csv要添加\n？
    # 答：日志采集读取的日志文件，日志文件中每一行的末尾都有一个\n，所以不加没有任何问题；
    # 商品数据来源于MySQL，读取数据默认是没有换行符的，所以必须手工添加


if __name__ == '__main__':
    barcode = BarcodeModel('014779000888', '日本眉机', '', '', '', '个', 'null', 0.0000, 0.0000, '2017-07-10 16:56:44', '', 0, 'null', 'null')
    # str = "014779000888, 日本眉机, , , , 个, null, 0.0000, 0.0000, 2017-07-10 16:56:44, , 0, null, null"
    # print(tuple(str.split(",")))
    # barcode = BarcodeModel(tuple(str.split(",")))
    print(barcode.generate_insert_sql())
    print(barcode.get_csv_header())
    print(barcode.to_csv())