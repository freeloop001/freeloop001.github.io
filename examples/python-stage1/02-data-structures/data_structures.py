# 数据结构示例

# 1. List（列表）
fruits = ["apple", "banana", "orange"]

# 添加元素
fruits.append("grape")
fruits.insert(0, "mango")

# 删除元素
fruits.remove("banana")
deleted = fruits.pop()

# 列表推导式
squares = [x**2 for x in range(10)]
print(f"列表: {fruits}")
print(f"平方数: {squares}")

# 2. Dict（字典）
person = {
    "name": "Freeloop",
    "age": 25,
    "city": "Beijing"
}

# 访问值
print(f"姓名: {person['name']}")
print(f"邮箱: {person.get('email', 'N/A')}")

# 字典推导式
scores = {"Alice": 90, "Bob": 85, "Charlie": 92}
passing = {k: v for k, v in scores.items() if v >= 60}
print(f"及格: {passing}")

# 3. Set（集合）
colors = {"red", "green", "blue"}
print(f"集合: {colors}")

# 集合运算
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}
print(f"交集: {set1 & set2}")
print(f"并集: {set1 | set2}")

# 4. Tuple（元组）
point = (10, 20)
x, y = point
print(f"x={x}, y={y}")
