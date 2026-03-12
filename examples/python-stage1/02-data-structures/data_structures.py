# 数据结构示例

# 1. List（列表）
fruits = ["apple", "banana", "orange"]

# 添加元素
fruits.append("grape")
fruits.insert(0, "mango")

# 删除元素
fruits.remove("banana")
deleted = fruits.pop()
print(f"已删除: {deleted}")

# 列表推导式
squares = [x**2 for x in range(10)]
print(f"列表: {fruits}")
print(f"平方数: {squares}")

# 2. Dict（字典）
person = {
    "name": "Alice",
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

# ========== 练习题答案 ==========

# 练习2: 学生成绩管理系统（使用 dict 存储）
class StudentManager:
    def __init__(self):
        self.students = {}

    def add_student(self, name, score):
        """添加或更新学生成绩"""
        self.students[name] = score
        print(f"添加学生: {name}, 成绩: {score}")

    def get_score(self, name):
        """获取学生成绩"""
        return self.students.get(name, "不存在")

    def get_average(self):
        """计算平均成绩"""
        if not self.students:
            return 0
        return sum(self.students.values()) / len(self.students)

    def get_top(self, n=3):
        """获取前 n 名学生"""
        sorted_students = sorted(self.students.items(), key=lambda x: x[1], reverse=True)
        return sorted_students[:n]

    def list_all(self):
        """列出所有学生"""
        return self.students


# 测试学生成绩管理系统
manager = StudentManager()
manager.add_student("Alice", 95)
manager.add_student("Bob", 87)
manager.add_student("Charlie", 92)
manager.add_student("David", 78)

print(f"\n所有学生: {manager.list_all()}")
print(f"平均成绩: {manager.get_average():.2f}")
print(f"前三名: {manager.get_top(3)}")
print(f"前第一名: {manager.get_top(1)}")

# 练习3: 冒泡排序算法
def bubble_sort(arr):
    """冒泡排序"""
    n = len(arr)
    arr = arr.copy()  # 不修改原数组

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        # 如果没有交换，说明已经排序完成
        if not swapped:
            break

    return arr


# 测试冒泡排序
numbers = [64, 34, 25, 12, 22, 11, 90]
print(f"\n原始数组: {numbers}")
print(f"排序后: {bubble_sort(numbers)}")
