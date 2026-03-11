# Python 基础语法示例

# 1. 变量与数据类型
name = "Freeloop"      # 字符串
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
message = greet("Freeloop", "Hi")
print(message)  # 输出: Hi, Freeloop!

# 3. 类与对象
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def say_hello(self):
        return f"你好，我叫 {self.name}"

# 创建对象
person = Person("Freeloop", 25)
print(person.say_hello())

# 4. 异常处理
try:
    result = 10 / 0
except ZeroDivisionError:
    print("不能除以零!")
finally:
    print("执行完成")
