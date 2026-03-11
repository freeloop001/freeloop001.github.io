# Anthropic Claude API 示例
# 需要安装: pip install anthropic

# 设置 API Key（生产环境建议使用环境变量）
# os.environ["ANTHROPIC_API_KEY"] = "your-api-key"

from anthropic import Anthropic

# 初始化客户端
client = Anthropic()

# 基础对话
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "用一句话介绍Python"}
    ]
)

print("=== Claude 对话 ===")
print(message.content[0].text)
print(f"\n使用 Token: {message.usage.input_tokens + message.usage.output_tokens}")

# 流式输出
print("\n=== Claude 流式输出 ===")
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "解释什么是RAG"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="")

print("\n")

# 带系统提示词
print("=== Claude 系统提示词 ===")
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system="你是一个Python编程专家，擅长解释代码概念",
    messages=[
        {"role": "user", "content": "什么是装饰器？"}
    ]
)
print(message.content[0].text)
