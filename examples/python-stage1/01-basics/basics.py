# Python 基础语法示例

# 1. 变量与数据类型
name = "Alice"      # 字符串
age = 25               # 整数
height = 1.75          # 浮点数
is_student = True      # 布尔值

# 打印输出
print(f"姓名: {name}, 年龄: {age}")

# 2. 函数定义
def greet(name, greeting="Hello"):
    """简单的问候函数"""
    return f"{greeting}, {name}!"

# 调用函数
message = greet("Alice", "Hi")
print(message)  # 输出: Hi, Alice!

# 3. 练习：计算阶乘
def factorial(n):
    """计算 n 的阶乘"""
    if n < 0:
        raise ValueError("阶乘不能为负数")
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

# 测试阶乘函数
print(f"5! = {factorial(5)}")  # 输出: 120
print(f"10! = {factorial(10)}") # 输出: 3628800

# 4. 类与对象
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def say_hello(self):
        return f"你好，我叫 {self.name}"

# 创建对象
person = Person("Alice", 25)
print(person.say_hello())

# 5. 异常处理
try:
    result = 10 / 0
except ZeroDivisionError:
    print("不能除以零!")
finally:
    print("执行完成")
