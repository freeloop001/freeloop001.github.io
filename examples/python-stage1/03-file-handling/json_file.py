import json
import os

# JSON 文件处理

# 写入 JSON 文件
data = {"name": "Freeloop", "age": 25}
with open("user.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 读取 JSON 文件
with open("user.json", "r", encoding="utf-8") as f:
    loaded_data = json.load(f)
    print(f"读取: {loaded_data}")

# 清理
if os.path.exists("user.json"):
    os.remove("user.json")
