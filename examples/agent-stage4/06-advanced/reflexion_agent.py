# Reflexion Agent 实现
# 带自我反思的 Agent
# 需要安装: pip install openai langchain

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from typing import List, Dict


llm = ChatOpenAI(model="gpt-4o")


def reflexion_agent(query: str, max_iterations: int = 3) -> str:
    """
    Reflexion Agent

    特点：
    1. 执行任务
    2. 评估结果
    3. 反思改进（如果需要）
    4. 重复直到满意
    """

    # 反思提示词
    reflection_prompt = PromptTemplate.from_template("""你是一个自我反思助手。

原始请求: {query}

你执行的结果: {result}

请反思这个结果是否足够好。如果有问题，说明需要改进的地方。

反思结果:""")

    # 执行循环
    for i in range(max_iterations):
        # 执行任务
        result = execute_task(query, i)

        print(f"迭代 {i+1}: {result[:100]}...")

        # 反思
        reflection = llm.invoke(
            reflection_prompt.format(query=query, result=result)
        ).content

        # 检查是否满意
        if is_satisfactory(reflection):
            return result

        # 如果不满意，继续迭代
        print(f"反思: {reflection[:100]}...")

    return result


def execute_task(query: str, iteration: int) -> str:
    """执行任务"""
    prompt = PromptTemplate.from_template("""你是一个助手。请完成以下任务:

任务: {query}

{flexion_hint}""")

    hint = f"(迭代 {iteration + 1})" if iteration > 0 else ""

    response = llm.invoke(
        prompt.format(query=query, flexion_hint=hint)
    )

    return response.content


def is_satisfactory(reflection: str) -> bool:
    """判断结果是否满意"""
    # 简单的判断逻辑
    negative_words = ["不好", "不够", "需要改进", "不满意", "错误"]
    return not any(word in reflection for word in negative_words)


# 类实现版本
class ReflexionAgent:
    """带自我反思的 Agent"""

    def __init__(self, llm, max_iterations: int = 3):
        self.llm = llm
        self.max_iterations = max_iterations
        self.history = []

    def execute(self, query: str) -> str:
        """执行带反思的任务"""
        for iteration in range(self.max_iterations):
            # 执行
            result = self.llm.invoke(
                f"请回答以下问题: {query}\n{'如果有之前的反思，请改进:' + str(self.history) if self.history else ''}"
            ).content

            self.history.append({"iteration": iteration, "result": result})

            # 反思
            reflection = self.llm.invoke(
                f"评估以下回答是否解决了问题: {result}\n"
                f"原始问题: {query}\n"
                f"如果有问题，说明需要改进的地方:"
            ).content

            # 检查是否满意
            if self._is_good_enough(reflection):
                return result

            self.history.append({"iteration": iteration, "reflection": reflection})

        return result

    def _is_good_enough(self, reflection: str) -> bool:
        """判断是否足够好"""
        # 这里可以使用更复杂的判断逻辑
        return "满意" in reflection or "足够" in reflection


# 示例
if __name__ == "__main__":
    agent = ReflexionAgent(llm)

    # 示例
    # result = agent.execute("解释什么是机器学习")
    # print(result)

    print("请设置 OPENAI_API_KEY 后运行完整示例")
