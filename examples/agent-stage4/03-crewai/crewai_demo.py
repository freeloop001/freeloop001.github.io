# CrewAI 示例
# 需要安装: pip install crewai langchain-openai

print("=== CrewAI 示例 ===")

# 注意：需要 API Key 才能运行完整示例

"""
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# ============ 1. 创建 Agent ============
researcher = Agent(
    role="研究员",
    goal="研究最新的AI技术发展",
    backstory="你是一个资深的AI研究员，擅长分析技术趋势",
    verbose=True,
    allow_delegation=False
)

writer = Agent(
    role="科技作家",
    goal="撰写通俗易懂的科技文章",
    backstory="你是一个科技作家，擅长把复杂的技术用简单的语言解释",
    verbose=True,
    allow_delegation=False
)

# ============ 2. 创建 Task ============
research_task = Task(
    description="研究LangChain和LlamaIndex的最新功能",
    agent=researcher,
    expected_output="关于LangChain和LlamaIndex的详细对比报告"
)

write_task = Task(
    description="基于研究报告撰写一篇科技文章",
    agent=writer,
    expected_output="一篇1500字的科技文章"
)

# ============ 3. 创建 Crew ============
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential,  # 顺序执行
    verbose=True
)

# ============ 4. 执行 ============
result = crew.kickoff()
print(result)

# ============ 5. 并行执行 ============
# 创建多个任务
task1 = Task(description="任务1描述", agent=agent1)
task2 = Task(description="任务2描述", agent=agent2)
task3 = Task(description="任务3描述", agent=agent3)

crew_parallel = Crew(
    agents=[agent1, agent2, agent3],
    tasks=[task1, task2, task3],
    process=Process.hierarchical,  # 层级协作
    manager_agent=manager  # 需要一个管理 Agent
)

result = crew_parallel.kickoff()
"""

print("需要配置 API Key 才能运行完整示例")

# ============ 6. Agent 配置说明 ============
print("\n=== Agent 配置说明 ===")

agent_config = {
    "role": "角色名称",
    "goal": "角色目标",
    "backstory": "角色背景故事",
    "verbose": "是否详细输出",
    "allow_delegation": "是否允许委托任务",
    "tools": ["工具列表"]
}

print("Agent 关键参数:")
for key, value in agent_config.items():
    print(f"  {key}: {value}")
