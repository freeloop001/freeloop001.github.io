# 自定义工具示例
# 包含 Web Search、数据库查询、Code Interpreter 等

from langchain.tools import Tool
from pydantic import BaseModel
from typing import Optional
import requests


# ============== Web Search 工具 ==============
class SearchInput(BaseModel):
    query: str
    num_results: Optional[int] = 5


def web_search(query: str, num_results: int = 5) -> str:
    """
    Web Search 工具
    使用免费的 DuckDuckGo API
    """
    url = "https://duckduckgo.com/"
    params = {
        "q": query,
        "format": "json",
        "no_html": 1,
        "skip_disambig": 1
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        results = data.get("Results", [])[:num_results]
        if not results:
            return "未找到相关结果"

        output = f"搜索 '{query}' 的结果:\n\n"
        for i, r in enumerate(results, 1):
            output += f"{i}. {r.get('text', '')}\n"
            output += f"   URL: {r.get('url', '')}\n\n"

        return output
    except Exception as e:
        return f"搜索出错: {str(e)}"


def create_search_tool():
    """创建搜索工具"""
    return Tool(
        name="web_search",
        func=web_search,
        description="""搜索互联网获取最新信息。
        输入: 搜索关键词
        输出: 搜索结果列表，包含标题和URL"""
    )


# ============== 数据库查询工具 ==============
import sqlite3


class QueryInput(BaseModel):
    query: str


def execute_sql(query: str) -> str:
    """
    SQL 查询工具
    注意：实际使用时应限制权限，防止 SQL 注入
    """
    # 示例：使用内存 SQLite 数据库
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # 创建示例表
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            age INTEGER
        )
    """)
    cursor.executemany(
        "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
        [
            ("Alice", "alice@example.com", 25),
            ("Bob", "bob@example.com", 30),
            ("Charlie", "charlie@example.com", 28)
        ]
    )
    conn.commit()

    # 执行查询（仅支持 SELECT）
    try:
        if not query.strip().lower().startswith("select"):
            return "错误: 只支持 SELECT 查询"

        cursor.execute(query)
        results = cursor.fetchall()

        if not results:
            return "查询结果为空"

        # 获取列名
        columns = [description[0] for description in cursor.description]

        # 格式化输出
        output = "查询结果:\n"
        output += " | ".join(columns) + "\n"
        output += "-" * 50 + "\n"

        for row in results:
            output += " | ".join(str(x) for x in row) + "\n"

        return output

    except Exception as e:
        return f"查询错误: {str(e)}"
    finally:
        conn.close()


def create_db_tool():
    """创建数据库查询工具"""
    return Tool(
        name="sql_query",
        func=execute_sql,
        description="""执行 SQL 查询（仅支持 SELECT）。
        输入: SQL 查询语句
        输出: 查询结果"""
    )


# ============== Code Interpreter 工具 ==============
import subprocess
import tempfile
import os
import shutil


def execute_code(code: str, language: str = "python") -> str:
    """
    Code Interpreter 工具
    执行代码并返回结果
    """
    # 安全检查
    dangerous_patterns = ["import os", "import sys", "import subprocess", "open(", "__import__"]
    for pattern in dangerous_patterns:
        if pattern in code:
            return f"错误: 不允许使用 '{pattern}'"

    # 创建临时文件
    temp_dir = tempfile.mkdtemp()

    try:
        if language == "python":
            filepath = os.path.join(temp_dir, "script.py")
            with open(filepath, "w") as f:
                f.write(code)

            # 执行代码
            result = subprocess.run(
                ["python", filepath],
                capture_output=True,
                text=True,
                timeout=10
            )

            output = result.stdout
            if result.stderr:
                output += f"\n错误: {result.stderr}"

            return output or "代码执行完成，无输出"

        elif language == "javascript":
            filepath = os.path.join(temp_dir, "script.js")
            with open(filepath, "w") as f:
                f.write(code)

            result = subprocess.run(
                ["node", filepath],
                capture_output=True,
                text=True,
                timeout=10
            )

            output = result.stdout
            if result.stderr:
                output += f"\n错误: {result.stderr}"

            return output or "代码执行完成，无输出"

        else:
            return f"不支持的语言: {language}"

    except subprocess.TimeoutExpired:
        return "错误: 代码执行超时"
    except Exception as e:
        return f"执行错误: {str(e)}"
    finally:
        shutil.rmtree(temp_dir)


def create_code_tool():
    """创建代码执行工具"""
    return Tool(
        name="code_interpreter",
        func=execute_code,
        description="""执行 Python 或 JavaScript 代码。
        输入: 代码字符串
        输出: 代码执行结果"""
    )


# ============== 工具组合示例 ==============
def create_all_tools():
    """创建所有自定义工具"""
    return [
        create_search_tool(),
        create_db_tool(),
        create_code_tool()
    ]


if __name__ == "__main__":
    # 测试工具
    print("=== Web Search 测试 ===")
    result = web_search("Python 教程")
    print(result[:200])

    print("\n=== SQL 查询测试 ===")
    result = execute_sql("SELECT * FROM users WHERE age > 25")
    print(result)

    print("\n=== Code Interpreter 测试 ===")
    result = execute_code("print('Hello, World!')\nresult = 1 + 2\nprint(f'1 + 2 = {result}')")
    print(result)
