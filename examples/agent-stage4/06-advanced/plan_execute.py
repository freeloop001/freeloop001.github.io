# Plan-and-Execute Agent 实现
# 先生成计划，再逐步执行
# 需要安装: pip install openai langchain

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from typing import List


llm = ChatOpenAI(model="gpt-4o")


def plan_execute_agent(query: str) -> str:
    """
    Plan-and-Execute Agent

    1. 规划阶段：生成执行计划
    2. 执行阶段：按计划逐步执行
    """

    # 阶段1: 生成计划
    planning_prompt = PromptTemplate.from_template("""你是一个任务规划助手。
用户请求: {query}

请生成一个详细的执行计划，列出完成这个任务需要的所有步骤。
每个步骤应该清晰、具体。

执行计划:""")

    planning_response = llm.invoke(planning_prompt.format(query=query))
    plan = planning_response.content

    print(f"生成的计划:\n{plan}\n")

    # 阶段2: 执行计划
    execute_prompt = PromptTemplate.from_template("""你是一个任务执行助手。

原始请求: {query}

执行计划:
{plan}

请按照上述计划逐步执行，并报告每一步的结果。
如果某一步失败，说明原因并尝试替代方案。

执行结果:""")

    execute_response = llm.invoke(execute_prompt.format(query=query, plan=plan))
    result = execute_response.content

    return result


# 类实现版本
class PlanAndExecuteAgent:
    """Plan-and-Execute Agent 类"""

    def __init__(self, llm):
        self.llm = llm
        self.plan = []

    def planning(self, query: str) -> List[str]:
        """生成计划"""
        prompt = PromptTemplate.from_template("""将以下任务分解为具体的执行步骤。
每个步骤应该可以独立完成。

任务: {query}

步骤列表（每行一个步骤）:""")

        response = self.llm.invoke(prompt.format(query=query))
        steps = [s.strip() for s in response.content.split("\n") if s.strip()]

        self.plan = steps
        return steps

    def executing(self, query: str) -> str:
        """执行计划"""
        if not self.plan:
            return "请先生成计划"

        results = []
        for i, step in enumerate(self.plan, 1):
            print(f"执行步骤 {i}: {step}")

            prompt = PromptTemplate.from_template("""你正在执行一个任务。

原始请求: {query}

当前步骤: {step}
已完成的步骤: {completed}

请执行当前步骤并报告结果。""")

            response = self.llm.invoke(
                prompt.format(
                    query=query,
                    step=step,
                    completed="\n".join(results)
                )
            )

            step_result = response.content
            results.append(f"步骤{i}: {step}")

            print(f"  结果: {step_result[:100]}...")

        return "\n\n".join(results)

    def run(self, query: str) -> str:
        """运行完整的 Plan-and-Execute"""
        print("=== 阶段1: 规划 ===")
        steps = self.planning(query)

        print(f"\n=== 阶段2: 执行 ({len(steps)} 步骤) ===")
        result = self.executing(query)

        return result


# 示例
if __name__ == "__main__":
    agent = PlanAndExecuteAgent(llm)

    # 示例任务
    # result = agent.run("帮我写一个 Python 程序，计算斐波那契数列")
    # print(result)

    # 或者直接调用函数
    # result = plan_execute_agent("帮我写一个 Python 程序，计算斐波那契数列")
    # print(result)

    print("请设置 OPENAI_API_KEY 后运行完整示例")
