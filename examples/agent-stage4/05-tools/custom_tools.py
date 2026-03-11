# 自定义工具示例
# 需要安装: pip install langchain langchain-openai requests

from langchain.tools import tool
import requests

print("=== LangChain 工具示例 ===")

# ============ 1. 数学计算工具 ============
@tool
def calculate(expression: str) -> str:
    """执行数学计算。
    参数: expression - 数学表达式，如 "2+2" 或 "(10+5)*3"
    返回: 计算结果"""
    try:
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"计算错误: {str(e)}"

# ============ 2. 天气查询工具 ============
@tool
def get_weather(city: str) -> str:
    """查询城市天气。
    参数: city - 城市名称，如 "北京"、"上海"
    返回: 天气信息"""
    # 模拟天气数据
    weather_db = {
        "北京": "晴，15-25°C",
        "上海": "多云，18-26°C",
        "广州": "雨，22-30°C",
        "深圳": "晴，23-28°C"
    }
    return weather_db.get(city, f"未知城市{city}")

# ============ 3. 搜索工具 ============
@tool
def search_web(query: str) -> str:
    """搜索互联网获取信息。
    参数: query - 搜索关键词
    返回: 搜索结果摘要"""
    # 模拟搜索结果
    results = [
        f"{query}的最新发展",
        f"{query}的技术原理",
        f"{query}的应用场景"
    ]
    return "\n".join([f"- {r}" for r in results])

# ============ 4. 数据库查询工具 ============
import sqlite3

@tool
def query_database(query: str) -> str:
    """执行SQL查询。
    参数: query - SQL查询语句
    返回: 查询结果"""
    # 内存数据库示例
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # 创建测试表
    cursor.execute("CREATE TABLE users (id INTEGER, name TEXT, age INTEGER)")
    cursor.execute("INSERT INTO users VALUES (1, '张三', 25)")
    cursor.execute("INSERT INTO users VALUES (2, '李四', 30)")
    cursor.execute("INSERT INTO users VALUES (3, '王五', 28)")
    conn.commit()

    # 执行查询
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return str(results)
    except Exception as e:
        conn.close()
        return f"查询错误: {str(e)}"

# ============ 5. 测试工具 ============
print("\n测试工具:")

# 测试计算
result = calculate.invoke({"expression": "10+20*3"})
print(f"calculate: {result}")

# 测试天气
result = get_weather.invoke({"city": "北京"})
print(f"get_weather: {result}")

# 测试搜索
result = search_web.invoke({"query": "Python"})
print(f"search_web: {result}")

# 测试数据库
result = query_database.invoke({"query": "SELECT * FROM users WHERE age > 25"})
print(f"query_database: {result}")

# ============ 6. 组合工具 ============
print("\n=== 组合多个工具 ===")

tools = [calculate, get_weather, search_web]

# 在 LangGraph 或 Agent 中使用
# agent = create_react_agent(llm, tools)
# result = agent.invoke({"messages": [("user", "北京天气怎么样？")]})

print("工具可以在 Agent 中组合使用")
