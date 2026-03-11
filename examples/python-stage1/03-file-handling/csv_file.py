import csv
import os

# CSV 文件处理

# 写入 CSV
users = [["name", "age"], ["Alice", "25"], ["Bob", "30"]]
with open("users.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(users)

# 读取 CSV
with open("users.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"姓名: {row['name']}, 年龄: {row['age']}")

# 清理
if os.path.exists("users.csv"):
    os.remove("users.csv")
