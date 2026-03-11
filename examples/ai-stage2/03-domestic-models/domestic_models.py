# 国内模型 API 示例
# 需要安装: pip install openai python-dotenv

import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载 .env 配置
load_dotenv()

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

# ============ MiniMax ============
def test_minimax():
    print("\n=== MiniMax ===")
    client = OpenAI(
        api_key=os.getenv("LLM_API_KEY"),
        base_url=os.getenv("LLM_BASE_URL")
    )

    response = client.chat.completions.create(
        model=os.getenv("LLM_MODEL_ID"),
        messages=[{"role": "user", "content": "你好，请用一句话介绍自己"}]
    )
    print(response.choices[0].message.content)

# ============ 统一调用接口 ============
def call_model(provider: str, prompt: str, api_key: str = None) -> str:
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
        },
        "minimax": {
            "base_url": os.getenv("LLM_BASE_URL"),
            "model": os.getenv("LLM_MODEL_ID"),
            "api_key": os.getenv("LLM_API_KEY")
        }
    }

    # MiniMax 使用 .env 中的配置
    if provider == "minimax":
        config = configs[provider]
        client = OpenAI(api_key=config["api_key"], base_url=config["base_url"])
        response = client.chat.completions.create(
            model=config["model"],
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    config = configs[provider]
    client = OpenAI(api_key=api_key, base_url=config["base_url"])

    response = client.chat.completions.create(
        model=config["model"],
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# 测试（需要替换为实际的 API Key）
if __name__ == "__main__":
    # 测试 MiniMax（使用 .env 配置）
    test_minimax()

    # 示例：统一接口调用 MiniMax
    # prompt = "用一句话介绍Python"
    # result = call_model("minimax", prompt)
    # print(result)

    print("\n国内模型对比:")
    print("- DeepSeek: 性价比高，开源能力强")
    print("- Qwen: 阿里生态，稳定性好")
    print("- GLM: 中文优化，响应速度快")
    print("- MiniMax: MoE架构，多模态能力强")
