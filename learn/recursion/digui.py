# 递归是一种算法
# 算法是 将数学知识以代码的形式呈现出来的一种{思想}

# # 递归就是在函数体内部调用函数本身的一种代码书写形式
# def func1():
#     func1()
#     print('123')
#
# # RecursionError: maximum recursion depth exceeded
# func1()

# 上述内容就是递归,但是不是一个合理的递归,合理的递归有如下三个条件
"""
1. 在函数体内部调用函数本身
2. 要有明确的递归出口(递归跳出条件)
3. 不能超出最大调用深度(python默认函数最多嵌套1000层)
"""

# 举例: 计算1-n的累加和
"""
递归第一步要找规律
f(1) = 1                    = 1
f(2) = 1 + 2                = f(1) + 2
f(3) = 1 + 2 + 3            = f(2) + 3
f(4) = 1 + 2 + 3 + 4        = f(3) + 4
....
f(n) = 1 + 2 + 3 ... + n    = f(n-1) + n

结论:
计算1-n的累加和的规律就是 f(n-1) + n
"""


# 递归第二步.将数学规律转换为代码逻辑
# def sum_1_to_n(n):
#     return sum_1_to_n(n-1) + n
#
# sum_1_to_n(100)

# 递归第三步. 找到递归地跳出条件
# 根据上边的规律,f(1)函数中,没有调用函数本身,则此时就是f函数的递归出口
def digui(n):
    if n == 1:
        return 1
    return digui(n - 1) + n


print(digui(100)) # 5050
# RecursionError: maximum recursion depth exceeded in comparison
# print(digui(1000)) # 超出最大的调用深度,所以报错