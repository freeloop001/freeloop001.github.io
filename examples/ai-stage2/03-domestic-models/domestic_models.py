# 国内模型 API 示例
# 需要安装: pip install openai

from openai import OpenAI

# ============ DeepSeek ============
def test_deepseek():
    print("=== DeepSeek ===")
    client = OpenAI(
        api_key="your-deepseek-key",  # 替换为你的 key
        base_url="https://api.deepseek.com"
    )

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": "你好，请介绍一下自己"}]
    )
    print(response.choices[0].message.content)

# ============ Qwen (阿里云) ============
def test_qwen():
    print("\n=== Qwen ===")
    client = OpenAI(
        api_key="your-qwen-key",  # 替换为你的 key
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )

    response = client.chat.completions.create(
        model="qwen-turbo",
        messages=[{"role": "user", "content": "你好，请介绍一下自己"}]
    )
    print(response.choices[0].message.content)

# ============ GLM (智谱) ============
def test_glm():
    print("\n=== GLM ===")
    client = OpenAI(
        api_key="your-glm-key",  # 替换为你的 key
        base_url="https://open.bigmodel.cn/api/paas/v4"
    )

    response = client.chat.completions.create(
        model="glm-4",
        messages=[{"role": "user", "content": "你好，请介绍一下自己"}]
    )
    print(response.choices[0].message.content)

# ============ 统一调用接口 ============
def call_model(provider: str, prompt: str, api_key: str) -> str:
    """统一调用接口"""
    configs = {
        "deepseek": {
            "base_url": "https://api.deepseek.com",
            "model": "deepseek-chat"
        },
        "qwen": {
            "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "model": "qwen-turbo"
        },
        "glm": {
            "base_url": "https://open.bigmodel.cn/api/paas/v4",
            "model": "glm-4"
        }
    }

    config = configs[provider]
    client = OpenAI(api_key=api_key, base_url=config["base_url"])

    response = client.chat.completions.create(
        model=config["model"],
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# 测试（需要替换为实际的 API Key）
if __name__ == "__main__":
    # 示例：统一接口调用
    # prompt = "用一句话介绍Python"
    # result = call_model("deepseek", prompt, "your-key")
    # print(result)

    print("请替换为实际的 API Key 后测试")
    print("国内模型对比:")
    print("- DeepSeek: 性价比高，开源能力强")
    print("- Qwen: 阿里生态，稳定性好")
    print("- GLM: 中文优化，响应速度快")
