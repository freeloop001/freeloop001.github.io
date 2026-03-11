# Ollama 示例
# 需要安装: pip install ollama

print("=== Ollama 示例 ===")

# 注意：需要先安装 Ollama 并启动服务

"""
import ollama

# ============ 1. 基础对话 ============
print("=== 基础对话 ===")

response = ollama.chat(
    model='llama2',
    messages=[
        {'role': 'user', 'content': '你好'}
    ]
)

print(f"回复: {response['message']['content']}")

# ============ 2. 流式输出 ============
print("\n=== 流式输出 ===")

for chunk in ollama.chat(
    model='llama2',
    messages=[{'role': 'user', 'content': '用一句话介绍Python'}],
    stream=True
):
    print(chunk['message']['content'], end='')

# ============ 3. 生成 Embedding ============
print("\n=== Embedding ===")

response = ollama.embeddings(
    model='nomic-embed-text',
    prompt='Python是一门编程语言'
)
print(f"Embedding维度: {len(response['embedding'])}")
print(f"前5个值: {response['embedding'][:5]}")

# ============ 4. 列出模型 ============
print("\n=== 模型列表 ===")

models = ollama.list()
for model in models['models']:
    print(f"- {model['name']}: {model.get('size', 'N/A')}")

# ============ 5. 完整对话历史 ============
print("\n=== 对话历史 ===")

messages = [
    {'role': 'user', 'content': 'Python适合做什么？'},
    {'role': 'assistant', 'content': 'Python适合做Web开发、数据分析、AI等。'},
    {'role': 'user', 'content': '那JavaScript呢？'}
]

response = ollama.chat(model='llama2', messages=messages)
print(f"回复: {response['message']['content']}")
"""

print("需要先安装 Ollama: https://ollama.com")
print("\n常用命令:")
print("  ollama pull llama2     # 拉取模型")
print("  ollama list           # 列出模型")
print("  ollama run llama2     # 运行模型")
print("  ollama serve          # 启动API服务")
