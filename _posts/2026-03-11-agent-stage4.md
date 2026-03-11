---
layout: post-toc
title: "AI Agent - 阶段4"
date: 2026-03-11 14:00:00 +0800
categories: [learning]
tags: [AI, Agent, LangGraph, CrewAI, Tool]
toc: |
  <a href="#1-agent概念">1. Agent 概念</a>
  <a href="#2-langgraph">2. LangGraph</a>
  <a href="#3-crewai">3. CrewAI</a>
  <a href="#4-autogen">4. AutoGen</a>
  <a href="#5-工具开发">5. 工具开发</a>
  <a href="#6-实战项目">6. 实战项目</a>
---

## 1. Agent 概念

### 什么是 Agent？

Agent = LLM + Tool + Memory

- **LLM**：大脑，负责理解和推理
- **Tool**：工具，扩展能力（搜索、计算、数据库等）
- **Memory**：记忆，存储上下文和历史

```python
# 简单 Agent 示例
from openai import OpenAI

client = OpenAI()

# 定义可用工具
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "执行数学计算",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string"}
                },
                "required": ["expression"]
            }
        }
    }
]

# 模拟工具
def calculate(expression):
    return eval(expression)

# Agent 循环
def agent(query, max_turns=5):
    messages = [{"role": "user", "content": query}]

    for _ in range(max_turns):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools
        )

        if response.choices[0].finish_reason == "tool_calls":
            # 调用工具
            tool_call = response.choices[0].message.tool_calls[0]
            result = calculate(eval(tool_call.function.arguments)["expression"])

            messages.append(response.choices[0].message)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })
        else:
            return response.choices[0].message.content

    return "达到最大轮次"

# 使用
print(agent("计算 (123 + 456) * 789"))
```

### Agent vs RAG

| 特性 | RAG | Agent |
|------|-----|-------|
| 能力 | 检索增强 | 自主决策 |
| 交互 | 问答 | 多轮对话 |
| 工具 | 可选 | 必须 |
| 适用 | 知识问答 | 复杂任务 |

---

## 2. LangGraph

### 核心概念

- **State**：状态，管理整个工作流的数据
- **Node**：节点，执行具体任务
- **Edge**：边，控制流程走向

### 快速开始

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

# 定义状态
class GraphState(TypedDict):
    messages: list
    result: str

# 创建图
graph = StateGraph(GraphState)

# 定义节点
def node1(state):
    print("执行节点1")
    return {"messages": state["messages"] + ["node1完成"]}

def node2(state):
    print("执行节点2")
    return {"result": "最终结果"}

# 添加节点
graph.add_node("node1", node1)
graph.add_node("node2", node2)

# 添加边
graph.set_entry_point("node1")
graph.add_edge("node1", "node2")
graph.add_edge("node2", END)

# 编译
app = graph.compile()

# 执行
result = app.invoke({"messages": [], "result": ""})
print(result)
```

### 带工具的 Agent

```python
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool

# 定义工具
@tool
def calculate(expression: str) -> str:
    """执行数学计算"""
    return str(eval(expression))

@tool
def search(query: str) -> str:
    """搜索信息"""
    return f"{query}的搜索结果..."

# 创建 Agent
llm = ChatOpenAI(api_key="your-key")
tools = [calculate, search]
agent = create_react_agent(llm, tools)

# 执行
result = agent.invoke({
    "messages": [("user", "计算123+456并搜索结果")]
})
print(result["messages"][-1].content)
```

---

## 3. CrewAI

### 核心概念

- **Agent**：智能体，有角色和目标
- **Task**：任务，具体工作
- **Crew**：团队，管理多个 Agent

### 快速开始

```python
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# 创建 Agent
researcher = Agent(
    role="研究员",
    goal="研究最新的AI技术",
    backstory="你是一个资深的AI研究员",
    verbose=True
)

writer = Agent(
    role="作家",
    goal="撰写科技文章",
    backstory="你是一个科技作家",
    verbose=True
)

# 创建 Task
research_task = Task(
    description="研究LangChain的最新功能",
    agent=researcher
)

write_task = Task(
    description="基于研究结果写一篇文章",
    agent=writer
)

# 创建 Crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential  # 顺序执行
)

# 执行
result = crew.kickoff()
print(result)
```

### 多 Agent 协作

```python
# 并行执行
crew = Crew(
    agents=[agent1, agent2, agent3],
    tasks=[task1, task2, task3],
    process=Process.hierarchical,  # 层级协作
    manager_agent=manager  # 管理员 Agent
)
```

---

## 4. AutoGen

### 快速开始

```python
from autogen import ConversableAgent, GroupChat, GroupChatManager

# 创建 Agent
assistant = ConversableAgent(
    name="assistant",
    system_message="你是一个有帮助的助手",
    llm_config={"model": "gpt-4o"}
)

user_proxy = ConversableAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "").strip().endswith("STOP"),
    human_input_mode="NEVER"
)

# 对话
result = user_proxy.initiate_chat(
    assistant,
    message="解释什么是机器学习 STOP"
)
```

### 多 Agent 讨论

```python
# 创建多个 Agent
agent1 = ConversableAgent(name="Alice", system_message="你擅长Python")
agent2 = ConversableAgent(name="Bob", system_message="你擅长JavaScript")
agent3 = ConversableAgent(name="Charlie", system_message="你擅长数据分析")

# 创建群聊
group_chat = GroupChat(
    agents=[agent1, agent2, agent3],
    messages=[],
    max_round=5
)

# 管理员
manager = GroupChatManager(groupchat=group_chat)

# 启动讨论
agent1.initiate_chat(
    manager,
    message="讨论Python和JavaScript的区别"
)
```

---

## 5. 工具开发

### Web Search 工具

```python
from langchain.tools import tool
import requests

@tool
def search_web(query: str) -> str:
    """搜索互联网获取信息"""
    # 使用搜索 API
    response = requests.get(
        "https://api.search.example.com/search",
        params={"q": query}
    )
    results = response.json()
    return "\n".join([r["title"] + ": " + r["snippet"] for r in results[:5]])
```

### 数据库查询工具

```python
import sqlite3

@tool
def query_database(query: str) -> str:
    """查询SQLite数据库"""
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return str(results)
```

### Code Interpreter

```python
@tool
def execute_code(code: str) -> str:
    """执行Python代码"""
    import subprocess
    result = subprocess.run(
        ["python", "-c", code],
        capture_output=True,
        text=True
    )
    return result.stdout or result.stderr
```

---

## 6. 实战项目

### 项目：多功能 Agent

```python
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.graph import StateGraph, END
from typing import TypedDict

# 1. 定义工具
@tool
def calculate(expression: str) -> str:
    """数学计算"""
    return str(eval(expression))

@tool
def get_weather(city: str) -> str:
    """查询天气"""
    # 实际使用天气 API
    return f"{city}今天晴转多云，25°C"

@tool
def search_news(topic: str) -> str:
    """搜索新闻"""
    return f"{topic}的最新新闻：..."

# 2. 创建 Agent
llm = ChatOpenAI(api_key="your-key")
tools = [calculate, get_weather, search_news]
agent = create_react_agent(llm, tools)

# 3. 执行任务
def run_agent_task(task: str):
    result = agent.invoke({
        "messages": [("user", task)]
    })
    return result["messages"][-1].content

# 测试
print(run_agent_task("北京天气怎么样？"))
print(run_agent_task("计算100+200"))
print(run_agent_task("搜索AI最新新闻"))
```

---

## 练习题

1. 理解 Agent = LLM + Tool + Memory 概念
2. 使用 LangGraph 实现一个简单工作流
3. 使用 CrewAI 创建多 Agent 团队
4. 使用 AutoGen 实现多 Agent 讨论
5. 开发一个 Web Search 工具
6. 开发一个数据库查询工具
7. 实现 Code Interpreter 工具
8. 创建一个多功能 Agent 系统

> 下节预告：阶段5 - AI 系统工程（Ollama、vLLM、n8n）
