---
layout: post-toc
title: "Python 开发基础 - 阶段1"
date: 2026-03-11
categories: [learning]
tags: [Python, 基础, 学习笔记]
toc: |
  <a href="#1-python-基础语法">1. Python 基础语法</a>
  <a href="#2-数据结构">2. 数据结构</a>
  <a href="#3-文件处理">3. 文件处理</a>
  <a href="#4-网络请求">4. 网络请求</a>
  <a href="#5-异步编程">5. 异步编程</a>
  <a href="#6-fastapi-框架">6. FastAPI 框架</a>
  <a href="#7-flask-框架">7. Flask 框架</a>
  <a href="#8-包管理">8. 包管理</a>
---

## 1. Python 基础语法

### 变量与数据类型

Python 是动态类型语言，不需要声明变量类型。

```python
# 基础变量
name = "Freeloop"      # 字符串
age = 25               # 整数
height = 1.75          # 浮点数
is_student = True      # 布尔值

# 打印输出
print(f"姓名: {name}, 年龄: {age}")
```

### 函数定义

使用 `def` 关键字定义函数。

```python
def greet(name, greeting="Hello"):
    """简单的问候函数"""
    return f"{greeting}, {name}!"

# 调用函数
message = greet("Freeloop", "Hi")
print(message)  # 输出: Hi, Freeloop!
```

### 类与对象

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def say_hello(self):
        return f"你好，我叫 {self.name}"

# 创建对象
person = Person("Freeloop", 25)
print(person.say_hello())
```

### 异常处理

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("不能除以零!")
finally:
    print("执行完成")
```

---

## 2. 数据结构

Python 有四种内置数据结构：list, dict, set, tuple

### List（列表）

有序可变的集合，类似于数组。

```python
# 创建列表
fruits = ["apple", "banana", "orange"]

# 添加元素
fruits.append("grape")
fruits.insert(0, "mango")

# 删除元素
fruits.remove("banana")
deleted = fruits.pop()

# 列表推导式
squares = [x**2 for x in range(10)]
print(squares)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

### Dict（字典）

键值对，无序但可通过键快速查找。

```python
# 创建字典
person = {
    "name": "Freeloop",
    "age": 25,
    "city": "Beijing"
}

# 访问值
print(person["name"])
print(person.get("email", "N/A"))

# 字典推导式
scores = {"Alice": 90, "Bob": 85, "Charlie": 92}
passing = {k: v for k, v in scores.items() if v >= 60}
```

### Set（集合）

无序不重复的元素集合。

```python
# 创建集合
colors = {"red", "green", "blue"}

# 集合运算
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}
print(set1 & set2)  # 交集: {3, 4}
print(set1 | set2)  # 并集: {1, 2, 3, 4, 5, 6}
```

### Tuple（元组）

有序不可变的列表。

```python
# 创建元组
point = (10, 20)

# 解包
x, y = point
print(f"x={x}, y={y}")
```

---

## 3. 文件处理

### JSON 文件处理

```python
import json

# 写入 JSON 文件
data = {"name": "Freeloop", "age": 25}
with open("user.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 读取 JSON 文件
with open("user.json", "r", encoding="utf-8") as f:
    loaded_data = json.load(f)
```

### CSV 文件处理

```python
import csv

# 写入 CSV
users = [["name", "age"], ["Alice", "25"], ["Bob", "30"]]
with open("users.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(users)

# 读取 CSV
with open("users.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["name"], row["age"])
```

### Excel 文件处理

需要安装 `openpyxl` 库：

```bash
pip install openpyxl
```

```python
import openpyxl

# 创建 Excel 文件
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "学生成绩"

# 写入数据
ws.append(["姓名", "数学", "语文", "英语"])
ws.append(["张三", 95, 88, 92])
ws.append(["李四", 87, 90, 85])

# 保存文件
wb.save("scores.xlsx")

# 读取 Excel 文件
wb = openpyxl.load_workbook("scores.xlsx")
ws = wb.active
for row in ws.iter_rows(values_only=True):
    print(row)
```

### PDF 文件处理

需要安装 `PyPDF2` 或 `pdfplumber`：

```bash
pip install PyPDF2 pdfplumber
```

```python
import pdfplumber

# 读取 PDF 文本
with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)

# 使用 PyPDF2
from PyPDF2 import PdfReader

reader = PdfReader("document.pdf")
for page in reader.pages:
    print(page.extract_text())
```

### Word 文件处理

需要安装 `python-docx`：

```bash
pip install python-docx
```

```python
from docx import Document

# 创建 Word 文档
doc = Document()
doc.add_heading('Python 学习笔记', 0)

doc.add_paragraph('这是一篇关于 Python 基础的文章')
doc.add_paragraph('内容包括：变量、函数、类等')

# 添加表格
table = doc.add_table(rows=2, cols=2)
table.cell(0, 0).text = '姓名'
table.cell(0, 1).text = '年龄'

doc.save("notes.docx")

# 读取 Word 文档
doc = Document("notes.docx")
for para in doc.paragraphs:
    print(para.text)
```

---

## 4. 网络请求

### requests 库

```python
import requests

# GET 请求
response = requests.get("https://api.github.com/users/freeloop001")
print(response.status_code)
print(response.json())

# POST 请求
data = {"username": "freeloop"}
response = requests.post("https://httpbin.org/post", json=data)
```

### 实战：调用 OpenAI API

```python
import requests

API_KEY = "your-api-key"

def call_openai(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers, json=data
    )
    return response.json()["choices"][0]["message"]["content"]

result = call_openai("用一句话介绍 Python")
print(result)
```

### httpx 库

`httpx` 是一个支持异步的 HTTP 客户端，兼容 `requests` API 的同时支持 async/await。

```bash
pip install httpx
```

```python
import httpx

# 同步用法（类似 requests）
response = httpx.get("https://api.github.com/users/freeloop001")
print(response.status_code)
print(response.json())

# 异步用法
import asyncio

async def fetch_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.github.com/users/freeloop001")
        return response.json()

# 调用异步函数
result = asyncio.run(fetch_data())
print(result)
```

**httpx vs requests**：
| 特性 | requests | httpx |
|------|----------|-------|
| 同步调用 | ✓ (原生) | ✓ |
| 异步调用 | ✗ (需 grequests) | ✓ (原生) |
| HTTP/2 | ✗ | ✓ |
| API 兼容 | - | 高度兼容 |

---

## 5. 异步编程

Python 的异步编程基于 `asyncio` 模块，使用 `async/await` 关键字。

### 基础概念

```python
import asyncio

# 定义异步函数
async def fetch_data():
    print("开始获取数据...")
    await asyncio.sleep(2)  # 模拟 I/O 操作
    print("数据获取完成!")
    return {"data": "hello"}

# 运行异步函数
result = asyncio.run(fetch_data())
print(result)
```

### 并发执行

```python
import asyncio
import time

async def task(name, delay):
    print(f"{name} 开始")
    await asyncio.sleep(delay)
    print(f"{name} 完成 (耗时 {delay}s)")
    return f"{name} done"

async def main():
    # 并发执行多个任务
    start = time.time()
    results = await asyncio.gather(
        task("任务1", 2),
        task("任务2", 1),
        task("任务3", 3)
    )
    elapsed = time.time() - start
    print(f"总耗时: {elapsed:.2f}s")  # 约 3s（最长任务时间）
    print(results)

asyncio.run(main())
```

### 异步上下文管理器

```python
import asyncio
import httpx

async def fetch_all(urls):
    async with httpx.AsyncClient() as client:
        # 并发请求多个 URL
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        return [r.json() for r in responses]

# 调用示例
if __name__ == "__main__":
    urls = [
        "https://httpbin.org/get",
        "https://httpbin.org/ip",
        "https://httpbin.org/headers"
    ]
    results = asyncio.run(fetch_all(urls))
    for r in results:
        print(r)
```

### 实战：异步 API 调用

```python
import asyncio
import httpx

async def fetch_user(client, user_id):
    """获取单个用户信息"""
    response = await client.get(f"https://jsonplaceholder.typicode.com/users/{user_id}")
    return response.json()

async def main():
    """批量获取用户信息"""
    async with httpx.AsyncClient() as client:
        # 并发获取 10 个用户
        tasks = [fetch_user(client, i) for i in range(1, 11)]
        users = await asyncio.gather(*tasks)

        for user in users:
            print(f"{user['name']} - {user['email']}")

asyncio.run(main())
```

## 6. FastAPI 框架

### 快速开始

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/items/")
def create_item(item: Item):
    return {"item_name": item.name, "item_price": item.price}
```

### 运行服务

```bash
uvicorn main:app --reload
```

访问 http://127.0.0.1:8000/docs 查看自动生成的 API 文档。

### 实战：AI 对话 API

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="AI Chat API")

class ChatRequest(BaseModel):
    message: str
    model: str = "gpt-3.5-turbo"

@app.post("/chat")
async def chat(request: ChatRequest):
    if not request.message:
        raise HTTPException(status_code=400, detail="消息不能为空")
    return {
        "response": f"收到: {request.message}",
        "model": request.model
    }
```

---

## 7. Flask 框架

Flask 是轻量级的 Web 框架，适合快速原型开发。

```bash
pip install flask
```

### 快速开始

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"message": "Hello World!"})

@app.route('/api/users', methods=['GET'])
def get_users():
    users = [
        {"id": 1, "name": "张三"},
        {"id": 2, "name": "李四"}
    ]
    return jsonify(users)

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    return jsonify({"id": 3, "name": data.get("name")}), 201

if __name__ == '__main__':
    app.run(debug=True)
```

运行：`python app.py`，访问 http://127.0.0.1:5000

### 模板渲染

```python
from flask import render_template

@app.route('/hello/<name>')
def hello(name):
    return render_template('hello.html', name=name)
```

### 请求对象

```python
from flask import request

@app.route('/search')
def search():
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    return f"搜索: {query}, 页码: {page}"
```

### Flask vs FastAPI

| 特性 | Flask | FastAPI |
|------|-------|---------|
| 性能 | 中等 | 高 |
| 自动 API 文档 | ✗ | ✓ (Swagger) |
| 类型校验 | ✗ | ✓ (Pydantic) |
| 异步支持 | 需额外配置 | 原生支持 |
| 适用场景 | 小型项目、原型 | API 服务、微服务 |

---

## 8. 包管理

Python 包管理工具主要有 `pip` 和 `uv`。

### pip 基础

```bash
# 安装包
pip install requests

# 安装指定版本
pip install requests==2.28.0

# 安装 requirements.txt 中的包
pip install -r requirements.txt

# 导出当前环境依赖
pip freeze > requirements.txt

# 卸载包
pip uninstall requests

# 查看已安装的包
pip list
```

### 虚拟环境

```bash
# 创建虚拟环境
python -m venv myenv

# 激活虚拟环境 (Linux/Mac)
source myenv/bin/activate

# 激活虚拟环境 (Windows)
myenv\Scripts\activate

# 退出虚拟环境
deactivate
```

### uv（推荐）

`uv` 是新一代 Python 包管理器，速度比 pip 快 10-100 倍。

```bash
# 安装 uv
pip install uv

# 创建项目并安装依赖
uv venv
uv pip install requests

# 或使用 uv 管理的虚拟环境
uv run python main.py

# 快速安装 requirements.txt
uv pip install -r requirements.txt
```

**uv 优势**：
- 安装速度极快
- 依赖解析更准确
- 内置虚拟环境管理
- 更好的缓存机制

---

## 练习题

### 基础练习
1. 编写一个函数，计算阶乘
2. 创建一个学生成绩管理系统（使用 dict 存储）
3. 实现一个冒泡排序算法

### 文件处理
4. 将数据保存到 JSON 文件并读取
5. 读取一个 CSV 文件，计算某列的平均值
6. 用 python-docx 创建一个带有表格的 Word 文档

### 网络请求
7. 调用一个公开 API（如 GitHub API）
8. 用 httpx 异步并发请求多个 API

### Web 框架
9. 用 FastAPI 创建一个天气查询 API
10. 用 Flask 创建一个 TODO List API

### 综合实战
11. 创建一个命令行工具：读取 Excel 文件，调用天气 API，将结果保存为 JSON
12. 用异步编程并发获取多个用户信息

> 下节预告：阶段2 - AI 开发基础（调用 LLM API）
