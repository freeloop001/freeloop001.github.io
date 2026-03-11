# LiteLLM 示例
# 需要安装: pip install litellm

print("=== LiteLLM 示例 ===")

# 注意：需要配置 API Key

"""
from litellm import completion, batch_completion
import os

# 设置 API Key
os.environ["OPENAI_API_KEY"] = "your-openai-key"
os.environ["ANTHROPIC_API_KEY"] = "your-anthropic-key"

# ============ 1. 统一 API 调用 ============
print("=== 统一 API ===")

# OpenAI
response = completion(
    model="gpt-4",
    messages=[{"role": "user", "content": "你好"}]
)
print(f"GPT-4: {response.choices[0].message.content}")

# Claude
response = completion(
    model="claude-3-sonnet-20240229",
    messages=[{"role": "user", "content": "你好"}]
)
print(f"Claude: {response.choices[0].message.content}")

# ============ 2. 本地模型 ============
print("\n=== 本地模型 ===")

# Ollama
response = completion(
    model="ollama/llama2",
    messages=[{"role": "user", "content": "你好"}]
)
print(f"Ollama: {response.choices[0].message.content}")

# ============ 3. 路由功能 ============
print("\n=== 智能路由 ===")

# 根据任务类型选择模型
def route_task(task_type, messages):
    routing = {
        "fast": "gpt-3.5-turbo",
        "smart": "gpt-4",
        "code": "claude-3-sonnet-20240229"
    }
    model = routing.get(task_type, "gpt-3.5-turbo")
    return completion(model=model, messages=messages)

# 使用
response = route_task("smart", [{"role": "user", "content": "解释量子计算"}])
print(f"智能路由: {response.choices[0].message.content[:100]}...")

# ============ 4. 批量请求 ============
print("\n=== 批量请求 ===")

messages_list = [
    [{"role": "user", "content": "你好"}],
    [{"role": "user", "content": "Python是什么？"}]
]

# 批量处理
responses = batch_completion(
    model="gpt-3.5-turbo",
    messages=messages_list
)

for i, response in enumerate(responses):
    print(f"请求{i+1}: {response.choices[0].message.content[:30]}...")
"""

print("需要配置 API Key 才能运行完整示例")
print("\n配置环境变量:")
print("  export OPENAI_API_KEY='your-key'")
print("  export ANTHROPIC_API_KEY='your-key'")
print("\n然后运行脚本")
