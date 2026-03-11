# API 参数演示示例
# 需要安装: pip install openai

from openai import OpenAI

client = OpenAI()

# ============ Temperature 对比 ============
print("=== Temperature 对比 ===")

prompt = "写一个关于AI的创意故事开头"

# 低温度 - 确定性输出
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.2
)
print(f"temperature=0.2 (确定):\n{response.choices[0].message.content[:200]}...")

# 中温度 - 平衡
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7
)
print(f"\ntemperature=0.7 (平衡):\n{response.choices[0].message.content[:200]}...")

# 高温度 - 创意
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt}],
    temperature=1.0
)
print(f"\ntemperature=1.0 (创意):\n{response.choices[0].message.content[:200]}...")

# ============ top_p 对比 ============
print("\n\n=== top_p 对比 ===")

# top_p=0.5 - 保守
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Python的优势是"}],
    top_p=0.5,
    temperature=0.7
)
print(f"top_p=0.5 (保守): {response.choices[0].message.content[:150]}")

# top_p=1.0 - 开放
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Python的优势是"}],
    top_p=1.0,
    temperature=0.7
)
print(f"top_p=1.0 (开放): {response.choices[0].message.content[:150]}")

# ============ max_tokens ============
print("\n=== max_tokens 限制 ===")

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "详细介绍Python语言"}],
    max_tokens=100  # 限制输出
)
print(f"max_tokens=100: {response.choices[0].message.content}")
print(f"实际使用: {response.usage.output_tokens} tokens")

# ============ stop 序列 ============
print("\n=== stop 序列 ===")

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "数到5"}],
    stop=["4"]  # 遇到4停止
)
print(f"输出(遇到4停止): {response.choices[0].message.content}")

# ============ 常用场景参数 ============
SCENARIOS = {
    "代码生成": {"temperature": 0.2, "top_p": 0.95},
    "创意写作": {"temperature": 0.9, "top_p": 0.95},
    "问答对话": {"temperature": 0.7, "top_p": 0.9},
    "摘要总结": {"temperature": 0.5, "max_tokens": 500},
    "翻译": {"temperature": 0.3, "top_p": 0.95},
}

print("\n=== 常用场景参数 ===")
for scenario, params in SCENARIOS.items():
    print(f"{scenario}: {params}")
