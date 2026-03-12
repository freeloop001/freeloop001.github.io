# ReAct Agent 实现
# 结合推理和行动的 Agent 架构
# 需要安装: pip install openai langchain langchain-openai

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.tools import Tool
from typing import List, Tuple


llm = ChatOpenAI(model="gpt-4o")


def react_agent(query: str, tools: List[Tool], max_iterations: int = 5) -> str:
    """
    ReAct (Reasoning + Acting) Agent 实现

    核心思想：交替进行推理和行动
    - 推理 (Thought): 分析当前情况
    - 行动 (Action): 执行工具
    - 观察 (Observation): 获取行动结果
    """

    # 定义 ReAct 提示词
    react_prompt = PromptTemplate.from_template("""你是一个 ReAct Agent。请按照以下格式思考并行动:

问题: {query}

可用工具:
{tools_desc}

请按以下格式回答:
Thought: 分析当前情况，决定下一步行动
Action: 工具名称 [参数]
Observation: 工具返回的结果
... (重复以上步骤直到得出答案)
Answer: 最终答案

开始:
""")

    # 解析工具描述
    tools_desc = "\n".join([f"- {t.name}: {t.description}" for t in tools])

    context = react_prompt.format(
        query=query,
        tools_desc=tools_desc
    )

    # 模拟 ReAct 循环
    # 实际实现中需要更复杂的解析逻辑
    for i in range(max_iterations):
        # 获取 LLM 的响应
        response = llm.invoke(context + f"\nThought {i+1}:")
        thought = response.content

        # 检查是否可以直接回答
        if "Answer:" in thought:
            return thought.split("Answer:")[-1].strip()

        # 解析行动
        if "Action:" in thought:
            action_line = thought.split("Action:")[-1].strip()

            # 提取工具名和参数
            if "[" in action_line and "]" in action_line:
                tool_name = action_line.split("[")[0].strip()
                tool_args = action_line.split("[")[1].split("]")[0].strip()

                # 找到对应的工具
                tool = next((t for t in tools if t.name == tool_name), None)
                if tool:
                    # 执行工具
                    observation = tool.func(tool_args)
                    context += f"\nThought {i+1}: {thought.split('Action:')[0].split('Thought:')[-1].strip()}\n"
                    context += f"Action: {action_line}\n"
                    context += f"Observation: {observation}\n"

    return "无法得出答案"


# 简化版 ReAct
class ReActAgent:
    """简化版 ReAct Agent"""

    def __init__(self, llm, tools: List[Tool]):
        self.llm = llm
        self.tools = tools
        self.tool_map = {t.name: t for t in tools}

    def run(self, query: str, max_steps: int = 5) -> str:
        """运行 Agent"""
        messages = [
            {
                "role": "system",
                "content": """你是一个 ReAct Agent。逐步推理并使用工具来回答问题。

格式:
Thought: 分析问题
Action: 工具名 [参数]
Observation: 结果
... (重复)
Answer: 最终答案"""
            },
            {"role": "user", "content": query}
        ]

        for step in range(max_steps):
            # 获取响应
            response = self.llm.invoke(messages)
            content = response.content

            # 检查是否有答案
            if "Answer:" in content:
                return content.split("Answer:")[-1].strip()

            # 解析行动
            if "Action:" in content:
                action_part = content.split("Action:")[-1].strip()

                # 提取工具和参数
                if "[" in action_part:
                    tool_name = action_part.split("[")[0].strip()
                    tool_args = action_part.split("[")[1].split("]")[0].strip()

                    # 执行工具
                    if tool_name in self.tool_map:
                        result = self.tool_map[tool_name].func(tool_args)

                        # 添加观察结果
                        messages.append({
                            "role": "assistant",
                            "content": content + f"\nObservation: {result}"
                        })

        return "无法完成"


# 示例工具
def search_wikipedia(query: str) -> str:
    """维基百科搜索（模拟）"""
    return f"关于 '{query}' 的信息..."


def calculate(expression: str) -> str:
    """计算器"""
    try:
        result = eval(expression)
        return str(result)
    except:
        return "计算错误"


# 示例
if __name__ == "__main__":
    # 创建工具
    tools = [
        Tool(name="search", func=search_wikipedia, description="搜索维基百科"),
        Tool(name="calculate", func=calculate, description="执行数学计算")
    ]

    # 创建 Agent
    agent = ReActAgent(llm, tools)

    # 运行
    # result = agent.run("计算 123 * 456 的结果")
    # print(result)

    print("请设置 OPENAI_API_KEY 后运行完整示例")
