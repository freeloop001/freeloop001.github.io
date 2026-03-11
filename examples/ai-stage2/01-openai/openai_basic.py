# OpenAI API 示例
# 需要安装: pip install openai

import os

# 设置 API Key（生产环境建议使用环境变量）
# os.environ["OPENAI_API_KEY"] = "your-api-key"

from openai import OpenAI

# 初始化客户端
client = OpenAI()

# 基础对话
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "你是一个有帮助的助手"},
        {"role": "user", "content": "用一句话介绍Python"}
    ]
)

print("=== 基础对话 ===")
print(response.choices[0].message.content)

# 获取使用信息
print(f"\n使用 Token: {response.usage.total_tokens}")

# 流式输出示例
print("\n=== 流式输出 ===")
stream = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "写一首关于春天的诗"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")

print("\n")

# 带参数的对话
print("=== 带参数的对话 ===")
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "解释什么是递归"}],
    temperature=0.3,  # 低温度，更确定性
    max_tokens=500
)
print(response.choices[0].message.content)
