# 多模型对比工具
# 需要安装: pip install openai

from openai import OpenAI

# 模型配置
MODELS = {
    "GPT-4o": {
        "base_url": None,  # 默认 OpenAI
        "api_key": "your-openai-key",
        "model": "gpt-4o"
    },
    "DeepSeek": {
        "base_url": "https://api.deepseek.com",
        "api_key": "your-deepseek-key",
        "model": "deepseek-chat"
    },
    "Qwen": {
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "api_key": "your-qwen-key",
        "model": "qwen-turbo"
    },
    "GLM": {
        "base_url": "https://open.bigmodel.cn/api/paas/v4",
        "api_key": "your-glm-key",
        "model": "glm-4"
    }
}

def call_model(config: dict, prompt: str) -> str:
    """调用指定模型"""
    client = OpenAI(
        api_key=config["api_key"],
        base_url=config["base_url"]
    )

    response = client.chat.completions.create(
        model=config["model"],
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500
    )

    return response.choices[0].message.content

def compare_models(prompt: str):
    """对比所有模型"""
    print(f"\n{'='*50}")
    print(f"Prompt: {prompt}")
    print(f"{'='*50}\n")

    results = {}

    for name, config in MODELS.items():
        try:
            print(f"[{name}] 正在请求...")
            result = call_model(config, prompt)
            results[name] = result
            print(f"[{name}] ✓ 完成\n")
        except Exception as e:
            results[name] = f"错误: {str(e)}"
            print(f"[{name}] ✗ 失败: {e}\n")

    # 打印对比结果
    print(f"\n{'='*50}")
    print("对比结果:")
    print(f"{'='*50}\n")

    for name, result in results.items():
        print(f"--- {name} ---")
        print(result[:300] + "..." if len(result) > 300 else result)
        print()

    return results

# 使用示例
if __name__ == "__main__":
    prompt = "用一句话介绍Python及其特点"

    # 方法1: 对比所有模型
    # compare_models(prompt)

    # 方法2: 单个模型测试
    # result = call_model(MODELS["DeepSeek"], "你好")
    # print(result)

    print("请配置 API Key 后测试")
    print("\n模型配置说明:")
    for name, config in MODELS.items():
        print(f"- {name}: {config['model']}")
