# AI 对话助手项目
# 需要安装: pip install openai

from openai import OpenAI

class ChatAssistant:
    """带上下文的对话助手"""

    def __init__(self, api_key: str, system_prompt: str = "你是一个有帮助的助手"):
        self.client = OpenAI(api_key=api_key)
        self.system_prompt = system_prompt
        self.history = [{"role": "system", "content": system_prompt}]

    def chat(self, message: str) -> str:
        """发送消息并获取回复"""
        self.history.append({"role": "user", "content": message})

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=self.history,
            temperature=0.7
        )

        reply = response.choices[0].message.content
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def clear_history(self):
        """清空对话历史"""
        self.history = [{"role": "system", "content": self.system_prompt}]

    def print_history(self):
        """打印对话历史"""
        print("\n=== 对话历史 ===")
        for msg in self.history[1:]:  # 跳过 system
            role = "用户" if msg["role"] == "user" else "助手"
            print(f"{role}: {msg['content'][:50]}...")

# 使用示例
if __name__ == "__main__":
    # 创建助手
    assistant = ChatAssistant(
        api_key="your-api-key",
        system_prompt="你是一个Python专家，擅长解释代码概念，用简洁的语言回答"
    )

    # 对话
    print("助手: 你好！有什么Python问题可以问我。")

    # 示例对话（需要替换为实际 API Key）
    # response = assistant.chat("什么是装饰器？")
    # print(f"助手: {response}")
    #
    # response = assistant.chat("它和闭包有什么关系？")
    # print(f"助手: {response}")
    #
    # # 查看历史
    # assistant.print_history()
    #
    # # 清空历史
    # assistant.clear_history()

    print("请替换 API Key 后运行测试")
