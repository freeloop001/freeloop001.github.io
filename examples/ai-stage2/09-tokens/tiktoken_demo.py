# Token 计算与成本计算示例
# 需要安装: pip install tiktoken

import tiktoken
from openai import OpenAI
import os

# API 定价（单位：美元，每百万 tokens）
# 参考: https://openai.com/pricing
PRICING = {
    "gpt-4o": {"input": 5.00, "output": 15.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4-turbo": {"input": 10.00, "output": 30.00},
    "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
}


def count_tokens(text: str, model: str = "gpt-4o") -> int:
    """计算文本的 token 数量"""
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    return len(tokens)


def count_tokens_messages(messages: list, model: str = "gpt-4o") -> int:
    """计算对话消息的 token 数量"""
    encoding = tiktoken.encoding_for_model(model)

    num_tokens = 0
    for message in messages:
        # 每条消息有额外开销
        num_tokens += 4
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += -1  # name 字段有特殊处理

    # 添加结束标记开销
    num_tokens += 2
    return num_tokens


def calculate_cost(input_tokens: int, output_tokens: int, model: str) -> dict:
    """计算 API 调用成本"""
    pricing = PRICING.get(model, PRICING["gpt-4o"])

    input_cost = (input_tokens / 1_000_000) * pricing["input"]
    output_cost = (output_tokens / 1_000_000) * pricing["output"]
    total_cost = input_cost + output_cost

    return {
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "input_cost": round(input_cost, 6),
        "output_cost": round(output_cost, 6),
        "total_cost": round(total_cost, 6)
    }


# 示例使用
if __name__ == "__main__":
    # 示例文本
    text = """
    Python 是一种广泛使用的解释型、高级和通用的编程语言。
    Python 支持多种编程范式，包括结构化、过程式、反射式、面向对象和函数式编程。
    它拥有动态类型系统和垃圾回收功能，能够自动管理内存使用。
    """

    print("=== Token 计算示例 ===")

    # 计算单文本 token
    for model in ["gpt-4o", "gpt-3.5-turbo"]:
        tokens = count_tokens(text, model)
        print(f"{model}: {tokens} tokens")

    # 计算对话消息 token
    messages = [
        {"role": "system", "content": "你是一个有帮助的助手。"},
        {"role": "user", "content": "请用一句话介绍 Python。"},
        {"role": "assistant", "content": "Python 是一种高级编程语言，以简洁易读的语法著称。"},
        {"role": "user", "content": "它的主要特点是什么？"}
    ]

    tokens = count_tokens_messages(messages)
    print(f"\n对话消息 tokens: {tokens}")

    # 计算成本
    print("\n=== 成本计算示例 ===")
    cost = calculate_cost(input_tokens=1000, output_tokens=500, model="gpt-4o")
    print(f"输入: {cost['input_tokens']} tokens, 成本: ${cost['input_cost']}")
    print(f"输出: {cost['output_tokens']} tokens, 成本: ${cost['output_cost']}")
    print(f"总计: ${cost['total_cost']}")

    # 估算一篇文章的成本
    article = "Python 是一种..." * 100  # 模拟长文章
    article_tokens = count_tokens(article)
    response_tokens = 500

    cost = calculate_cost(article_tokens, response_tokens, "gpt-4o")
    print(f"\n文章处理成本: ${cost['total_cost']}")
