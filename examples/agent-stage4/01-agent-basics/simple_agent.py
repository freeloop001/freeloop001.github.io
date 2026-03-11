# 简单 Agent 示例
# 需要安装: pip install openai

from openai import OpenAI

client = OpenAI()

# ============ 1. 基础 Agent 结构 ============
print("=== 基础 Agent ===")

# 模拟工具
def calculate(expression: str) -> str:
    """数学计算工具"""
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"计算错误: {e}"

def search(query: str) -> str:
    """搜索工具"""
    return f"关于'{query}'的搜索结果..."

# 可用工具定义
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "执行数学计算",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "数学表达式"}
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": "搜索互联网",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    }
]

# ============ 2. Agent 循环 ============
def run_agent(query: str, max_turns=3):
    """运行 Agent"""
    messages = [{"role": "user", "content": query}]

    for turn in range(max_turns):
        print(f"\n--- 轮次 {turn + 1} ---")

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools
        )

        msg = response.choices[0].message

        # 检查是否需要调用工具
        if msg.tool_calls:
            # 添加助手消息（包含工具调用）
            messages.append(msg)

            # 调用工具
            for tool_call in msg.tool_calls:
                func_name = tool_call.function.name
                func_args = eval(tool_call.function.arguments)

                print(f"调用工具: {func_name}({func_args})")

                # 执行工具
                if func_name == "calculate":
                    result = calculate(func_args["expression"])
                elif func_name == "search":
                    result = search(func_args["query"])
                else:
                    result = "未知工具"

                print(f"工具结果: {result}")

                # 添加工具结果
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
        else:
            # 直接返回回答
            print(f"回答: {msg.content}")
            return msg.content

    return "达到最大轮次"

# 测试
# result = run_agent("计算123+456")
# print(result)
print("需要配置 API Key 才能运行")
