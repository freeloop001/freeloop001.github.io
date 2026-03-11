# vLLM 示例
# 需要安装: pip install vllm openai

print("=== vLLM 示例 ===")

# 注意：需要先启动 vLLM 服务

"""
from openai import OpenAI

# 连接本地 vLLM 服务
client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="EMPTY"
)

# ============ 1. 基础对话 ============
print("=== 基础对话 ===")

response = client.chat.completions.create(
    model="qwen",
    messages=[{"role": "user", "content": "你好"}]
)

print(f"回复: {response.choices[0].message.content}")

# ============ 2. 流式输出 ============
print("\n=== 流式输出 ===")

stream = client.chat.completions.create(
    model="qwen",
    messages=[{"role": "user", "content": "写一首关于春天的诗"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")

# ============ 3. 带参数的请求 ============
print("\n=== 参数控制 ===")

response = client.chat.completions.create(
    model="qwen",
    messages=[{"role": "user", "content": "用5个字回答"}],
    max_tokens=20,
    temperature=0.3
)
print(f"回复: {response.choices[0].message.content}")

# ============ 4. Embedding ============
print("\n=== Embedding ===")

response = client.embeddings.create(
    model="qwen",
    input="Python是一门编程语言"
)
print(f"Embedding维度: {len(response.data[0].embedding)}")

# ============ 5. 批量请求 ============
print("\n=== 批量请求 ===")

# vLLM 支持连续批处理
messages_list = [
    [{"role": "user", "content": "你好"}],
    [{"role": "user", "content": "Python是什么？"}],
    [{"role": "user", "content": "你会什么？"}]
]

# 发送多个请求
for messages in messages_list:
    response = client.chat.completions.create(model="qwen", messages=messages)
    print(f"Q: {messages[0]['content'][:15]}... -> A: {response.choices[0].message.content[:20]}...")
"""

print("需要先启动 vLLM 服务:")
print("  pip install vllm")
print("  vllm serve Qwen/Qwen2-7B-Instruct --dtype half")
print("\n然后运行此脚本")
