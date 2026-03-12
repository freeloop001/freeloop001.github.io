# Function Calling 示例
# 需要安装: pip install openai

from openai import OpenAI
import json

client = OpenAI()


# 定义工具函数
def get_weather(city: str, country: str = "cn") -> dict:
    """获取城市天气（模拟）"""
    weather_data = {
        "北京": {"temp": 15, "condition": "晴朗"},
        "上海": {"temp": 18, "condition": "多云"},
        "广州": {"temp": 25, "condition": "阴天"},
        "深圳": {"temp": 26, "condition": "晴朗"},
    }

    city_weather = weather_data.get(city, {"temp": 20, "condition": "未知"})
    return {
        "city": city,
        "temperature": city_weather["temp"],
        "condition": city_weather["condition"],
        "humidity": 65
    }


def calculate(a: int, b: int, operation: str) -> dict:
    """计算器"""
    operations = {
        "add": a + b,
        "subtract": a - b,
        "multiply": a * b,
        "divide": a / b if b != 0 else "Error: Division by zero"
    }
    return {"result": operations.get(operation, "Unknown operation")}


# 注册工具列表
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取城市天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称"
                    },
                    "country": {
                        "type": "string",
                        "description": "国家代码，默认 cn",
                        "default": "cn"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "执行数学计算",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "integer", "description": "第一个数字"},
                    "b": {"type": "integer", "description": "第二个数字"},
                    "operation": {
                        "type": "string",
                        "description": "操作类型",
                        "enum": ["add", "subtract", "multiply", "divide"]
                    }
                },
                "required": ["a", "b", "operation"]
            }
        }
    }
]


# 处理函数调用
def handle_function_call(tool_call):
    """处理工具调用"""
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)

    if function_name == "get_weather":
        return get_weather(**arguments)
    elif function_name == "calculate":
        return calculate(**arguments)
    else:
        return {"error": f"Unknown function: {function_name}"}


def chat_with_tools(user_message: str):
    """带工具调用的对话"""
    messages = [
        {"role": "system", "content": "你是一个智能助手，可以调用工具来回答问题。"},
        {"role": "user", "content": user_message}
    ]

    # 第一次调用
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools
    )

    message = response.choices[0].message

    # 如果有工具调用
    if message.tool_calls:
        # 添加助手消息（包含工具调用）
        messages.append(message.model_dump())

        # 执行工具调用
        for tool_call in message.tool_calls:
            result = handle_function_call(tool_call)
            # 添加工具结果到消息
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "content": json.dumps(result)
            })

        # 第二次调用，获取最终回复
        final_response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )

        return final_response.choices[0].message.content

    return message.content


# 测试
if __name__ == "__main__":
    # 测试天气查询
    print("=== 测试天气查询 ===")
    result = chat_with_tools("北京今天天气怎么样？")
    print(f"回答: {result}")

    # 测试计算
    print("\n=== 测试计算 ===")
    result = chat_with_tools("15 乘以 23 等于多少？")
    print(f"回答: {result}")
