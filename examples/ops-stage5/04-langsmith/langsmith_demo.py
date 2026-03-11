# LangSmith 示例
# 需要安装: pip install langchain langchain-openai langsmith

print("=== LangSmith 示例 ===")

# 注意：需要配置 API Key 和 LangSmith

"""
import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langsmith import traceable

# 配置
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-langsmith-key"
os.environ["OPENAI_API_KEY"] = "your-openai-key"

# ============ 1. 基本追踪 ============
print("=== 基本追踪 ===")

llm = ChatOpenAI(model="gpt-4")
prompt = PromptTemplate.from_template("{product}的创始人是谁？")
chain = LLMChain(llm=llm, prompt=prompt)

# 执行（自动追踪到 LangSmith）
result = chain.invoke({"product": "Apple"})
print(f"结果: {result['text'][:100]}...")

# ============ 2. 追踪特定函数 ============
print("\n=== 函数追踪 ===")

@traceable
def process_user_request(user_input: str) -> str:
    """处理用户请求的函数"""
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    response = llm.invoke(user_input)
    return response.content

# 调用函数，会自动追踪
result = process_user_request("解释什么是机器学习")
print(f"结果: {result[:100]}...")

# ============ 3. 自定义追踪数据 ============
print("\n=== 自定义元数据 ===")

from langsmith.run_helpers import trace

@traceable(run_type="chain")
def complex_pipeline(input_data: str):
    """复杂流水线"""
    # 步骤1
    result1 = llm.invoke(f"总结: {input_data}")
    # 步骤2
    result2 = llm.invoke(f"翻译成英文: {result1.content}")
    return result2.content

# 执行并查看 LangSmith
result = complex_pipeline("Python是一门强大的编程语言")
print(f"结果: {result[:100]}...")

# ============ 4. LangChain 集成 ============
print("\n=== LangChain 集成 ===")

from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool

@tool
def calculate(expression: str) -> str:
    """数学计算"""
    return str(eval(expression))

# 创建 Agent（会自动追踪）
llm = ChatOpenAI(model="gpt-4")
tools = [calculate]

prompt = PromptTemplate.from_template("你是一个助手。{input}")
agent = create_openai_functions_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools)

# 执行
result = executor.invoke({"input": "计算 (10+5)*2"})
print(f"结果: {result['output']}")
"""

print("需要配置环境变量:")
print("  export LANGCHAIN_TRACING_V2=true")
print("  export LANGCHAIN_API_KEY='your-key'")
print("  export OPENAI_API_KEY='your-key'")
print("\n访问 https://smith.langchain.com 查看追踪数据")
