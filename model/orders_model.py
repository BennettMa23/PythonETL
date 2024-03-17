# 导包
import json
from util import strutil, timeutil
from config import project_config as conf

# 创建模型类
class OrdersModel(object):
    # 定义相关属性，目标表有多少字段，类中就应该有多少个属性，数据来源JSON（字符串）
    def __init__(self, data):
        # JSON字符串不方便具体数据拆解
        data = json.loads(data)  # Python对象 => 字典格式
        # 初始化订单数据模型对象 => 表名映射类名，表中字段映射为对象属性 => 注意区分大小写，对象属性小写，JSON解析都是区分大小写
        self.discount_rate = data['discountRate']  # 折扣率
        self.store_shop_no = data['storeShopNo']  # 店铺店号（无用列）
        self.day_order_seq = data['dayOrderSeq']  # 本单为当日第几单
        self.store_district = data['storeDistrict']  # 店铺所在行政区
        self.is_signed = data['isSigned']  # 是否签约店铺（签约第三方支付体系）
        self.store_province = data['storeProvince']  # 店铺所在省份
        self.origin = data['origin']  # 原始信息（无用）
        self.store_gps_longitude = data['storeGPSLongitude']  # 店铺GPS经度
        self.discount = data['discount']  # 折扣金额
        self.store_id = data['storeID']  # 店铺ID
        self.product_count = data['productCount']  # 本单售卖商品数量
        self.operator_name = data['operatorName']  # 操作员姓名
        self.operator = data['operator']  # 操作员ID
        self.store_status = data['storeStatus']  # 店铺状态
        self.store_own_user_tel = data['storeOwnUserTel']  # 店铺店主电话
        self.pay_total = data['payedTotal']  # 支付总金额
        self.pay_type = data['payType']  # 支付类型
        self.discount_type = data['discountType']  # 折扣类型
        self.store_name = data['storeName']  # 店铺名称
        self.store_own_user_name = data['storeOwnUserName']  # 店铺店主名称
        self.date_ts = data['dateTS']  # 订单时间
        self.small_change = data['smallChange']  # 找零金额
        self.store_gps_name = data['storeGPSName']  # 店铺GPS名称
        self.erase = data['erase']  # 是否抹零
        self.store_gps_address = data['storeGPSAddress']  # 店铺GPS地址
        self.order_id = data['orderID']  # 订单ID
        self.money_before_whole_discount = data['moneyBeforeWholeDiscount']  # 折扣前金额
        self.store_category = data['storeCategory']  # 店铺类别
        self.receivable = data['receivable']  # 应收金额
        self.face_id = data['faceID']  # 面部识别ID
        self.store_own_user_id = data['storeOwnUserId']  # 店铺店主ID
        self.payment_channel = data['paymentChannel']  # 付款通道
        self.payment_scenarios = data['paymentScenarios']  # 付款情况（无用）
        self.store_address = data['storeAddress']  # 店铺地址
        self.total_no_discount = data['totalNoDiscount']  # 整体价格（无折扣）
        self.payed_total = data['payedTotal']  # 已付款金额
        self.store_gps_latitude = data['storeGPSLatitude']  # 店铺GPS纬度
        self.store_create_date_ts = data['storeCreateDateTS']  # 店铺创建时间
        self.store_city = data['storeCity']  # 店铺所在城市
        self.member_id = data['memberID']  # 会员ID

    def generate_insert_sql(self):
        ''' 生成插入订单表的SQL语句 '''
        return f"insert ignore into {conf.target_orders_table_name}(order_id,store_id,store_name,store_status,store_own_user_id,store_own_user_name,store_own_user_tel,store_category,store_address,store_shop_no,store_province,store_city,store_district,store_gps_name,store_gps_address,store_gps_longitude,store_gps_latitude,is_signed,operator,operator_name,face_id,member_id,store_create_date_ts,origin,day_order_seq,discount_rate,discount_type,discount,money_before_whole_discount,receivable,erase,small_change,total_no_discount,pay_total,pay_type,payment_channel,payment_scenarios,product_count,date_ts) values (" \
               f"'{self.order_id}'," \
               f"{self.store_id}," \
               f"{strutil.check_str_null_and_transform_to_sql_null(self.store_name)}," \
               f"{strutil.check_str_null_and_transform_to_sql_null(self.store_status)}," \
               f"{self.store_own_user_id}," \
               f"{strutil.check_str_null_and_transform_to_sql_null(self.store_own_user_name)}," \
               f"{strutil.check_str_null_and_transform_to_sql_null(self.store_own_user_tel)}," \
               f"{strutil.check_str_null_and_transform_to_sql_null(self.store_category)}," \
               f"{strutil.check_str_null_and_transform_to_sql_null(self.store_address)}," \
               f"{strutil.check_str_null_and_transform_to_sql_null(self.store_shop_no)}," \
               f"{strutil.check_str_null_and_transform_to_sql_null(self.store_province)}," \
               f"{strutil.check_str_null_and_transform_to_sql_null(self.store_city)}," \
               f"{strutil.check_str_null_and_transform_to_sql_null(self.store_district)}," \
               f"{strutil.check_str_null_and_transform_to_sql_null(self.store_gps_name)}," \
               f"{strutil.check_str_null_and_transform_to_sql_null(self.store_gps_address)}," \
               f"{strutil.check_str_null_and_transform_to_sql_null(self.store_gps_longitude)}," \
               f"{strutil.check_str_null_and_transform_to_sql_null(self.store_gps_latitude)}," \
               f"{self.is_signed}," \
               f"{strutil.check_str_null_and_transform_to_sql_null(self.operator)},"\
               f"{strutil.check_str_null_and_transform_to_sql_null(self.operator_name)}," \
               f"{strutil.check_str_null_and_transform_to_sql_null(self.face_id)}," \
               f"{strutil.check_str_null_and_transform_to_sql_null(self.member_id)}," \
               f"'{timeutil.ts13_to_date_str(self.store_create_date_ts)}'," \
               f"{strutil.check_str_null_and_transform_to_sql_null(self.origin)}," \
               f"{self.day_order_seq}," \
               f"{self.discount_rate}," \
               f"{self.discount_type}," \
               f"{self.discount}," \
               f"{self.money_before_whole_discount}," \
               f"{self.receivable}," \
               f"{self.erase}," \
               f"{self.small_change}," \
               f"{self.total_no_discount}," \
               f"{self.payed_total}," \
               f"{strutil.check_str_null_and_transform_to_sql_null(self.pay_type)}," \
               f"{self.payment_channel}," \
               f"{strutil.check_str_null_and_transform_to_sql_null(self.payment_scenarios)}," \
               f"{self.product_count}," \
               f"'{timeutil.ts13_to_date_str(self.date_ts)}'" \
               f");"

    @staticmethod
    def get_csv_header(sep=','):
        # 普及快捷键 => Shift + Alt + 鼠标左键（同时选中多行）
        return f"order_id{sep}" \
               f"store_id{sep}" \
               f"store_name{sep}" \
               f"store_status{sep}" \
               f"store_own_user_id{sep}" \
               f"store_own_user_name{sep}" \
               f"store_own_user_tel{sep}" \
               f"store_category{sep}" \
               f"store_address{sep}" \
               f"store_shop_no{sep}" \
               f"store_province{sep}" \
               f"store_city{sep}" \
               f"store_district{sep}" \
               f"store_gps_name{sep}" \
               f"store_gps_address{sep}" \
               f"store_gps_longitude{sep}" \
               f"store_gps_latitude{sep}" \
               f"is_signed{sep}" \
               f"operator{sep}" \
               f"operator_name{sep}" \
               f"face_id{sep}" \
               f"member_id{sep}" \
               f"store_create_date_ts{sep}" \
               f"origin{sep}" \
               f"day_order_seq{sep}" \
               f"discount_rate{sep}" \
               f"discount_type{sep}" \
               f"discount{sep}" \
               f"money_before_whole_discount{sep}" \
               f"receivable{sep}" \
               f"erase{sep}" \
               f"small_change{sep}" \
               f"total_no_discount{sep}" \
               f"pay_total{sep}" \
               f"pay_type{sep}" \
               f"payment_channel{sep}" \
               f"payment_scenarios{sep}" \
               f"product_count{sep}" \
               f"date_ts\n"

    # 编写一个函数，check_and_transform_area() => 用于把空的省市区进行转化操作
    # 省份空 => 未知省份
    # 城市空 => 未知城市
    # 区域空 => 未知行政区
    def check_and_transform_area(self):
        if strutil.check_null(self.store_province):
            self.store_province = '未知省份'
        if strutil.check_null(self.store_city):
            self.store_city = '未知城市'
        if strutil.check_null(self.store_district):
            self.store_district = '未知行政区域'

    # 编写一个函数，check_and_transform_all_column > 检查所有属性值，如果空数据直接转换为空字符串形式
    # 因为数据写入到CSV文件，必须是有数据的，否则会导致写入CSV文件失败
    def check_and_transform_all_column(self):
        self.order_id = strutil.check_null_and_transform(self.order_id)
        self.store_id = strutil.check_null_and_transform(self.store_id)
        self.store_name = strutil.check_null_and_transform(self.store_name)
        self.store_status = strutil.check_null_and_transform(self.store_status)
        self.store_own_user_id = strutil.check_null_and_transform(self.store_own_user_id)
        self.store_own_user_name = strutil.check_null_and_transform(self.store_own_user_name)
        self.store_own_user_tel = strutil.check_null_and_transform(self.store_own_user_tel)
        self.store_category = strutil.check_null_and_transform(self.store_category)
        self.store_address = strutil.check_null_and_transform(self.store_address)
        self.store_shop_no = strutil.check_null_and_transform(self.store_shop_no)
        self.store_province = strutil.check_null_and_transform(self.store_province)
        self.store_city = strutil.check_null_and_transform(self.store_city)
        self.store_district = strutil.check_null_and_transform(self.store_district)
        self.store_gps_name = strutil.check_null_and_transform(self.store_gps_name)
        self.store_gps_address = strutil.check_null_and_transform(self.store_gps_address)
        self.store_gps_longitude = strutil.check_null_and_transform(self.store_gps_longitude)
        self.store_gps_latitude = strutil.check_null_and_transform(self.store_gps_latitude)
        self.is_signed = strutil.check_null_and_transform(self.is_signed)
        self.operator = strutil.check_null_and_transform(self.operator)
        self.operator_name = strutil.check_null_and_transform(self.operator_name)
        self.face_id = strutil.check_null_and_transform(self.face_id)
        self.member_id = strutil.check_null_and_transform(self.member_id)
        self.store_create_date_ts = strutil.check_null_and_transform(self.store_create_date_ts)
        self.origin = strutil.check_null_and_transform(self.origin)
        self.day_order_seq = strutil.check_null_and_transform(self.day_order_seq)
        self.discount_rate = strutil.check_null_and_transform(self.discount_rate)
        self.discount_type = strutil.check_null_and_transform(self.discount_type)
        self.discount = strutil.check_null_and_transform(self.discount)
        self.money_before_whole_discount = strutil.check_null_and_transform(self.money_before_whole_discount)
        self.receivable = strutil.check_null_and_transform(self.receivable)
        self.erase = strutil.check_null_and_transform(self.erase)
        self.small_change = strutil.check_null_and_transform(self.small_change)
        self.total_no_discount = strutil.check_null_and_transform(self.total_no_discount)
        self.pay_total = strutil.check_null_and_transform(self.pay_total)
        self.pay_type = strutil.check_null_and_transform(self.pay_type)
        self.payment_channel = strutil.check_null_and_transform(self.payment_channel)
        self.payment_scenarios = strutil.check_null_and_transform(self.payment_scenarios)
        self.product_count = strutil.check_null_and_transform(self.product_count)
        self.date_ts = strutil.check_null_and_transform(self.date_ts)

    # 定义一个to_csv()函数，用于把读取到的JSON订单数据写入到CSV文件中
    def to_csv(self, sep=','):
        # 调用刚才定义好的两个方法 => 区域转换以及所有列空值转换
        self.check_and_transform_area()
        self.check_and_transform_all_column()

        # 返回CSV行数据
        return f"{self.order_id}{sep}" \
               f"{self.store_id}{sep}" \
               f"{self.store_name}{sep}" \
               f"{self.store_status}{sep}" \
               f"{self.store_own_user_id}{sep}" \
               f"{self.store_own_user_name}{sep}" \
               f"{self.store_own_user_tel}{sep}" \
               f"{self.store_category}{sep}" \
               f"{self.store_address}{sep}" \
               f"{self.store_shop_no}{sep}" \
               f"{self.store_province}{sep}" \
               f"{self.store_city}{sep}" \
               f"{self.store_district}{sep}" \
               f"{self.store_gps_name}{sep}" \
               f"{self.store_gps_address}{sep}" \
               f"{self.store_gps_longitude}{sep}" \
               f"{self.store_gps_latitude}{sep}" \
               f"{self.is_signed}{sep}" \
               f"{self.operator}{sep}" \
               f"{self.operator_name}{sep}" \
               f"{self.face_id}{sep}" \
               f"{self.member_id}{sep}" \
               f"{timeutil.ts13_to_date_str(self.store_create_date_ts)}{sep}" \
               f"{self.origin}{sep}" \
               f"{self.day_order_seq}{sep}" \
               f"{self.discount_rate}{sep}" \
               f"{self.discount_type}{sep}" \
               f"{self.discount}{sep}" \
               f"{self.money_before_whole_discount}{sep}" \
               f"{self.receivable}{sep}" \
               f"{self.erase}{sep}" \
               f"{self.small_change}{sep}" \
               f"{self.total_no_discount}{sep}" \
               f"{self.pay_total}{sep}" \
               f"{self.pay_type}{sep}" \
               f"{self.payment_channel}{sep}" \
               f"{self.payment_scenarios}{sep}" \
               f"{self.product_count}{sep}" \
               f"{timeutil.ts13_to_date_str(self.date_ts)}\n"


# 构建订单详情模型 => 一个订单中可能包含多个商品，由于订单详情是由多个售卖商品组成
# 单个商品售卖模型实践
class SingleProductSoldModel(object):
    # 定义相关属性，由于商品必须属于某个订单，所以需要传递一个order_id；product_detail购买商品详细信息（单个） => dict
    def __init__(self, order_id, product_detail):
        self.order_id = order_id
        self.barcode = product_detail['barcode']
        self.name = product_detail['name']
        self.count = product_detail['count']
        self.price_per = product_detail['pricePer']
        self.retail_price = product_detail['retailPrice']
        self.trade_price = product_detail['tradePrice']
        self.category_id = product_detail['categoryID']
        self.unit_id = product_detail['unitID']

    # 正常情况下，应该编写一个generate_insert_sql语句，把商品数据插入到订单详情表
    # 由于订单详情有专门的订单详情模型，商品模型只是订单详情模型的一部分
    # 封装一个函数，这个函数，只是用于生成插入商品数据的SQL语句 => 不生成字段信息，只生成value插入那一部分数据
    # insert into orders_detail values (商品模型生成的value值),(商品模型生成的value值),(商品模型生成的value值)
    # ('001', '123456', '奥利奥', 1, 9.98, 9.98, 8, 10, 1),('001', '123456', '奥利奥', 1, 9.98, 9.98, 8, 10, 1)
    def generate_value_segment_for_sql_insert(self):
        return f"(" \
               f"'{self.order_id}'," \
               f"{strutil.check_str_null_and_transform_to_sql_null(self.barcode)}," \
               f"{strutil.check_str_null_and_transform_to_sql_null(self.name)}," \
               f"{self.count}," \
               f"{self.price_per}," \
               f"{self.retail_price}," \
               f"{self.trade_price}," \
               f"{self.category_id}," \
               f"{self.unit_id}" \
               f")"

    def to_csv(self, sep=','):
        return f"{self.order_id}{sep}" \
               f"{self.barcode}{sep}" \
               f"{self.name}{sep}" \
               f"{self.count}{sep}" \
               f"{self.price_per}{sep}" \
               f"{self.retail_price}{sep}" \
               f"{self.trade_price}{sep}" \
               f"{self.category_id}{sep}" \
               f"{self.unit_id}\n"

# 订单详情模型编写 => OrdersDetailModel => MySQL/CSV真正写入订单详情数据
class OrdersDetailModel(object):
    # 定义相关属性 => 编写__init__魔术方法
    def __init__(self, data):
        # 把接收到的json数据，转换为Python中的对象 => 字典类型
        data = json.loads(data)
        order_products_list = data['product']  # 提出JSON订单中，所有商品数据 => [{奥利奥}, {农夫山泉}, {红牛}]
        self.order_id = data['orderID']  # 提取订单编号
        # 定义一个products_detail属性，用于保存所有单个商品售卖模型对象
        self.products_detail = []
        # 对orders_products_list进行遍历，获取每一个商品的JSON信息传递给SingleProductSoldModel模型，生成商品模型对象
        for single_product in order_products_list:
            product = SingleProductSoldModel(self.order_id, single_product)
            self.products_detail.append(product)

    # 定义一个generate_insert_sql方法，专门用于生成SQL语句
    def generate_insert_sql(self):
        sql = f"insert ignore into {conf.target_orders_detail_table_name}(order_id, barcode, name, count, price_per, retail_price, trade_price, category_id, unit_id) values "
        # 把单个商品售卖模型中的generate_value_segment_for_sql_insert函数生成SQL values
        for single_product in self.products_detail:
            sql += single_product.generate_value_segment_for_sql_insert() + ', '  # 注意：两个符号，逗号+空格
        # SQL中语句中最后一个圆括号，多了一个逗号+空格 => insert into T values (), (), (),  => 最后一个空格是-1，最后一个逗号是-2
        sql = sql[:-2]
        return sql

    # CSV文件生成函数：生成标头
    @staticmethod
    def get_csv_header(sep=','):
        return f'order_id{sep}' \
               f'barcode{sep}' \
               f'name{sep}' \
               f'count{sep}' \
               f'price_per{sep}' \
               f'retail_price{sep}' \
               f'trade_price{sep}' \
               f'category_id{sep}' \
               f'unit_id\n'

    # CSV文件生成函数：生成内容
    def to_csv(self, sep=','):
        # 定义一个字符串，用于接收所有CSV行信息
        lines = ''
        for single_product in self.products_detail:
            lines += single_product.to_csv()
        return lines


# 定义一个RetailOriginModel原始业务模型，专门用于接收JSON格式的数据，然后生成订单模型以及订单详情模型
class RetailOriginModel(object):
    # 原始模型要获取一个data => json格式的订单数据，然后拆分为两个模型：订单模型 + 订单详情模型
    def __init__(self, data):
        self.order_model = OrdersModel(data)
        self.order_detail_model = OrdersDetailModel(data)
    # 获取订单模型对象
    def get_order_model(self):
        return self.order_model
    # 获取订单详情模型对象
    def get_order_detail_model(self):
        return self.order_detail_model
    # 获取订单编号
    def get_order_id(self):
        return self.order_model.order_id
    # 获取订单中商品列表信息
    def get_products_list(self):
        return self.order_detail_model.products_detail


if __name__ == '__main__':
    orders = OrdersModel('{"discountRate": 1, "storeShopNo": "277551753310004", "dayOrderSeq": 26, "storeDistrict": "开福区", "isSigned": 1, "storeProvince": "湖南省", "origin": 0, "storeGPSLongitude": "112.99564674496649", "discount": 0, "storeID": 622, "productCount": 3, "operatorName": "OperatorName", "operator": "NameStr", "storeStatus": "open", "storeOwnUserTel": 12345678910, "payType": "cash", "discountType": 2, "storeName": "刘伟明便利店", "storeOwnUserName": "OwnUserNameStr", "dateTS": 1542436507000, "smallChange": 0, "storeGPSName": "None", "erase": 0, "product": [{"count": 1, "name": "健达缤纷乐T40g", "unitID": 3, "barcode": "80177609", "pricePer": 8, "retailPrice": 8, "tradePrice": 6, "categoryID": 1}, {"count": 1, "name": "娃哈哈氧道饮用水 550ml", "unitID": 2, "barcode": "6902083901233", "pricePer": 2, "retailPrice": 2, "tradePrice": 0, "categoryID": 1}, {"count": 1, "name": "红牛维生素功能饮料250ml", "unitID": 4, "barcode": "6920202888883", "pricePer": 6, "retailPrice": 6, "tradePrice": 0, "categoryID": 1}], "storeGPSAddress": "None", "orderID": "15424365069006223306", "moneyBeforeWholeDiscount": 16, "storeCategory": "normal", "receivable": 16, "faceID": "", "storeOwnUserId": 463, "paymentChannel": 0, "paymentScenarios": "OTHER", "storeAddress": "StoreAddress", "totalNoDiscount": 16, "payedTotal": 16, "storeGPSLatitude": "28.249745727366196", "storeCreateDateTS": 1531790437000, "storeCity": "长沙市", "memberID": "0"}')
    print(orders.generate_insert_sql())
    print(orders.get_csv_header())
    print(orders.to_csv())

    orders_detail = OrdersDetailModel('{"discountRate": 1, "storeShopNo": "277551753310004", "dayOrderSeq": 26, "storeDistrict": "开福区", "isSigned": 1, "storeProvince": "湖南省", "origin": 0, "storeGPSLongitude": "112.99564674496649", "discount": 0, "storeID": 622, "productCount": 3, "operatorName": "OperatorName", "operator": "NameStr", "storeStatus": "open", "storeOwnUserTel": 12345678910, "payType": "cash", "discountType": 2, "storeName": "刘伟明便利店", "storeOwnUserName": "OwnUserNameStr", "dateTS": 1542436507000, "smallChange": 0, "storeGPSName": "None", "erase": 0, "product": [{"count": 1, "name": "健达缤纷乐T40g", "unitID": 3, "barcode": "80177609", "pricePer": 8, "retailPrice": 8, "tradePrice": 6, "categoryID": 1}, {"count": 1, "name": "娃哈哈氧道饮用水 550ml", "unitID": 2, "barcode": "6902083901233", "pricePer": 2, "retailPrice": 2, "tradePrice": 0, "categoryID": 1}, {"count": 1, "name": "红牛维生素功能饮料250ml", "unitID": 4, "barcode": "6920202888883", "pricePer": 6, "retailPrice": 6, "tradePrice": 0, "categoryID": 1}], "storeGPSAddress": "None", "orderID": "15424365069006223306", "moneyBeforeWholeDiscount": 16, "storeCategory": "normal", "receivable": 16, "faceID": "", "storeOwnUserId": 463, "paymentChannel": 0, "paymentScenarios": "OTHER", "storeAddress": "StoreAddress", "totalNoDiscount": 16, "payedTotal": 16, "storeGPSLatitude": "28.249745727366196", "storeCreateDateTS": 1531790437000, "storeCity": "长沙市", "memberID": "0"}')
    print(orders_detail.generate_insert_sql())

    print(orders_detail.get_csv_header())
    print(orders_detail.to_csv())