# Prompt 设计示例
# 需要安装: pip install openai

from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()

# ============ 1. System Prompt ============
print("=== System Prompt ===")
system_prompt = """你是一个专业的Python编程助手。
- 擅长写出简洁、高效的Python代码
- 代码遵循 PEP 8 规范
- 如果用户请求写代码，先解释思路再给出代码"""

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "如何快速排序？"}
    ]
)
print(response.choices[0].message.content)

# ============ 2. Few-shot Prompt ============
print("\n=== Few-shot Prompt ===")
few_shot_prompt = """把中文翻译成英文:
苹果 -> apple
香蕉 -> banana
橙子 -> orange
电脑 ->"""

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": few_shot_prompt}]
)
print(f"翻译结果: {response.choices[0].message.content}")

# ============ 3. 结构化输出 (Pydantic) ============
print("\n=== 结构化输出 ===")

class Recipe(BaseModel):
    name: str
    ingredients: list[str]
    steps: list[str]

response = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[{"role": "user", "content": "教我做蛋炒饭"}],
    response_format=Recipe
)

recipe = response.choices[0].message.parsed
print(f"菜名: {recipe.name}")
print(f"食材: {recipe.ingredients}")
print(f"步骤: {recipe.steps}")

# ============ 4. 分步思考 ============
print("\n=== 分步思考 Prompt ===")
chain_prompt = """请按以下步骤思考如何反转链表：
1. 首先解释什么是链表
2. 说明反转链表的思路
3. 给出Python代码实现
4. 分析时间复杂度和空间复杂度"""

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": chain_prompt}]
)
print(response.choices[0].message.content)

# ============ 5. 格式指定 ============
print("\n=== 格式指定 ===")
format_prompt = """用JSON格式返回Python的三大框架信息:
{"name": "框架名", "特点": "特点", "适用场景": "场景"}"""

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": format_prompt}]
)
print(response.choices[0].message.content)
