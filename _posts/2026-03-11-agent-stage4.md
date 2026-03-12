---
layout: post-toc
title: "AI Agent - 阶段4"
date: 2026-03-11 14:00:00 +0800
categories: [learning]
tags: [AI, Agent, LangGraph, CrewAI, Tool, ReAct, Memory]
toc: |
  <a href="#1-agent-概念">1. Agent 概念</a>
  <a href="#2-agent-架构模式">2. Agent 架构模式</a>
  <a href="#3-langgraph">3. LangGraph</a>
  <a href="#4-crewai">4. CrewAI</a>
  <a href="#5-autogen">5. AutoGen</a>
  <a href="#6-memory-实现">6. Memory 实现</a>
  <a href="#7-工具开发">7. 工具开发</a>
  <a href="#8-安全护栏">8. 安全护栏</a>
  <a href="#9-实战项目">9. 实战项目</a>
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

## 2. Agent 架构模式

### ReAct (Reason + Act)

ReAct 结合推理和行动，让 Agent 思考下一步做什么，然后执行。

```python
from openai import OpenAI

client = OpenAI(api_key="your-key")

# 定义工具
tools = [
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": "搜索信息",
            "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "执行数学计算",
            "parameters": {"type": "object", "properties": {"expr": {"type": "string"}}, "required": ["expr"]}
        }
    }
]

# ReAct Agent
def react_agent(query: str, max_steps: int = 10):
    thoughts = []
    actions = []
    observations = []
    messages = [{"role": "user", "content": query}]

    for _ in range(max_steps):
        # 1. 思考
        thought_prompt = f"""根据对话历史，思考下一步应该做什么。

可用工具: search, calculate

对话历史:
{format_messages(messages)}

你的思考格式: "我需要[搜索/计算]来回答用户问题"

请只输出一行思考，不要其他内容。"""

        thought = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": thought_prompt}]
        ).choices[0].message.content

        thoughts.append(thought)

        # 2. 行动
        action_prompt = f"""基于以下思考，选择并执行工具。

思考: {thought}

可用工具:
- search: 搜索信息，参数: query
- calculate: 数学计算，参数: expr

请用以下格式输出:
TOOL_NAME: 参数

例如: search: Python历史"""

        action_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": action_prompt}]
        ).choices[0].message.content

        actions.append(action_response)

        # 解析并执行
        if action_response.startswith("search:"):
            tool_name = "search"
            tool_arg = {"query": action_response.split(":")[1].strip()}
        elif action_response.startswith("calculate:"):
            tool_name = "calculate"
            tool_arg = {"expr": action_response.split(":")[1].strip()}
        else:
            break

        # 3. 观察结果
        observation = f"[执行了{tool_name}工具]"
        observations.append(observation)

        # 添加到上下文
        messages.append({"role": "assistant", "content": f"思考: {thought}\n行动: {action_response}\n结果: {observation}"})

        # 检查是否完成
        messages.append({"role": "user", "content": "请基于以上信息给出最终答案，或者继续下一步行动。"})

        final_response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )

        if "最终答案" in final_response.choices[0].message.content:
            return final_response.choices[0].message.content

    return "达到最大步数"
```

### Plan-and-Execute

先规划，再执行。

```python
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from typing import TypedDict

llm = ChatOpenAI(api_key="your-key")

class PlanExecuteState(TypedDict):
    task: str
    plan: list
    current_step: int
    results: list
    final_answer: str

# 规划节点
def planner(state: PlanExecuteState):
    task = state["task"]

    # LLM 生成计划
    prompt = f"""为以下任务生成执行计划:

任务: {task}

输出格式（每行一个步骤）:
1. 步骤描述
2. 步骤描述
..."""

    response = llm.invoke(prompt)
    plan = [line.strip() for line in response.content.split("\n") if line.strip()]

    return {"plan": plan, "current_step": 0, "results": []}

# 执行节点
def executor(state: PlanExecuteState):
    plan = state["plan"]
    current = state["current_step"]
    results = state["results"]

    if current >= len(plan):
        return {"current_step": current + 1}

    # 执行当前步骤
    step = plan[current]
    prompt = f"执行以下步骤: {step}"

    result = llm.invoke(prompt)
    results.append({"step": step, "result": result.content})

    return {"current_step": current + 1, "results": results}

# 判断是否完成
def should_continue(state: PlanExecuteState):
    if state["current_step"] >= len(state["plan"]):
        return "answer"
    return "continue"

# 生成最终答案
def answer_generator(state: PlanExecuteState):
    results = state["results"]
    task = state["task"]

    summary = "\n".join([f"步骤{i+1}: {r['step']}\n结果: {r['result']}" for i, r in enumerate(results)])

    prompt = f"""基于以下执行结果，给出最终答案:

任务: {task}

执行过程:
{summary}
"""

    response = llm.invoke(prompt)
    return {"final_answer": response.content}

# 构建图
graph = StateGraph(PlanExecuteState)
graph.add_node("plan", planner)
graph.add_node("execute", executor)
graph.add_node("answer", answer_generator)

graph.set_entry_point("plan")
graph.add_edge("plan", "execute")
graph.add_conditional_edges("execute", should_continue, {"continue": "execute", "answer": "answer"})
graph.add_edge("answer", END)

agent = graph.compile()

# 执行
result = agent.invoke({
    "task": "比较Python和JavaScript的优缺点",
    "plan": [],
    "current_step": 0,
    "results": [],
    "final_answer": ""
})

print(result["final_answer"])
```

### Reflexion

带自我反思的 Agent。

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(api_key="your-key")

def reflect_agent(query: str, max_cycles: int = 3):
    context = [{"role": "user", "content": query}]
    reflection_history = []

    for cycle in range(max_cycles):
        # 生成回答
        response = llm.invoke(context)
        answer = response.content
        context.append({"role": "assistant", "content": answer})

        # 反思
        if cycle < max_cycles - 1:
            reflection_prompt = f"""审查以下回答，找出可能的问题或改进空间:

回答: {answer}

请列出:
1. 可能的错误
2. 遗漏的重要点
3. 改进建议

如果没有问题，请回复"无需改进"。"""

            reflection = llm.invoke(reflection_prompt)

            if "无需改进" in reflection.content:
                break

            reflection_history.append(reflection.content)

            # 基于反思改进
            improvement_prompt = f"""基于以下反思意见，改进你的回答:

原回答: {answer}

反思意见: {reflection.content}

请给出改进后的回答:"""

            improved = llm.invoke(improvement_prompt)
            answer = improved.content
            context[-1] = {"role": "assistant", "content": answer}

    return answer

# 使用
result = reflect_agent("解释什么是机器学习")
print(result)
```

---

## 3. LangGraph

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

## 4. CrewAI

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

## 5. AutoGen

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

## 6. Memory 实现

### Memory 类型

| 类型 | 说明 | 适用场景 |
|------|------|----------|
| 短期记忆 | 对话历史 | 单轮对话 |
| 长期记忆 | 持久化存储 | 跨会话 |
| 向量记忆 | 语义检索 | 上下文扩展 |

### 短期记忆 (BufferMemory)

```python
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

llm = ChatOpenAI(api_key="your-key")

# 创建记忆
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# 添加历史
memory.save_context(
    {"input": "我叫张三"},
    {"output": "你好张三，很高兴认识你"}
)

# 加载历史
history = memory.load_memory_variables({})
print(history["chat_history"])

# 用于 Chain
template = """你是一个助手。
历史对话:
{chat_history}

用户: {human_input}
助手:"""

chain = LLMChain(
    llm=llm,
    prompt=PromptTemplate.from_template(template),
    memory=memory
)

response = chain.invoke({"human_input": "我叫什么名字?"})
print(response["text"])
```

### 向量记忆 (VectorStoreRetrieverMemory)

```python
from langchain.memory import VectorStoreRetrieverMemory
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# 创建向量存储
vectorstore = Chroma(persist_directory="./memory_db", embedding_function=OpenAIEmbeddings())

# 创建向量记忆
memory = VectorStoreRetrieverMemory(
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
    memory_key="history"
)

# 保存记忆
memory.save_context(
    {"input": "用户喜欢Python"},
    {"output": "Python是一门优秀的编程语言"}
)

# 检索相关记忆
related = memory.load_memory_variables({"query": "用户的编程偏好"})
print(related["history"])
```

### 分层记忆系统

```python
class HierarchicalMemory:
    """分层记忆系统：短期 + 长期 + 向量"""

    def __init__(self):
        self.short_term = []  # 短期记忆
        self.long_term = {}    # 长期记忆（关键信息）
        self.vector_memory = Chroma(persist_directory="./mem", embedding_function=OpenAIEmbeddings())

    def add(self, user_input: str, ai_output: str):
        self.short_term.append({"user": user_input, "ai": ai_output})
        if len(self.short_term) > 10:
            self.short_term.pop(0)
        self._extract_to_long_term(user_input, ai_output)

    def _extract_to_long_term(self, user_input: str, ai_output: str):
        if "我叫" in user_input:
            name = user_input.split("我叫")[1].split("。")[0]
            self.long_term["name"] = name

    def get_context(self, query: str) -> str:
        parts = []
        if self.short_term:
            history = "\n".join([f"用户: {h['user']}\n助手: {h['ai']}" for h in self.short_term[-3:]])
            parts.append(f"最近对话:\n{history}")
        if self.long_term:
            facts = "\n".join([f"{k}: {v}" for k, v in self.long_term.items()])
            parts.append(f"用户信息:\n{facts}")
        return "\n\n".join(parts)
```

---

## 7. 工具开发

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

## 8. 安全护栏

### 输入验证

```python
from pydantic import BaseModel, validator

class UserInput(BaseModel):
    query: str

    @validator('query')
    def validate_query(cls, v):
        # 长度限制
        if len(v) > 1000:
            raise ValueError("输入过长")

        # 禁止关键词
        forbidden = ["注入", "攻击", "恶意"]
        for word in forbidden:
            if word in v.lower():
                raise ValueError(f"包含禁止内容: {word}")

        return v

# 使用
try:
    validated = UserInput(query="正常查询")
except ValueError as e:
    print(f"验证失败: {e}")
```

### 输出过滤

```python
import re

class OutputFilter:
    def __init__(self):
        self.forbidden_patterns = [
            r"\d{15,18}",  # 身份证号
            r"\d{4}-\d{4}-\d{4}-\d{4}",  # 信用卡号
            r"sk-[a-zA-Z0-9]+",  # API Key
        ]

    def filter(self, text: str) -> str:
        for pattern in self.forbidden_patterns:
            text = re.sub(pattern, "[已过滤]", text)
        return text

    def check(self, text: str) -> bool:
        """检查是否包含敏感信息"""
        for pattern in self.forbidden_patterns:
            if re.search(pattern, text):
                return True
        return False

# 使用
output_filter = OutputFilter()
result = output_filter.filter("我的API Key是sk-123456789")
print(result)  # 我的API Key是[已过滤]
```

### 内容安全检查

```python
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import Literal

class SafetyCheck(BaseModel):
    is_safe: bool
    reason: str = ""
    category: Literal["safe", "harmful", "Sensitive"] = "safe"

def safe_generate(prompt: str, llm) -> str:
    """带安全检查的生成"""
    # 检查输入
    if any(word in prompt for word in ["暴力", "色情", "诈骗"]):
        return "抱歉，我无法处理此类请求。"

    # 生成
    response = llm.invoke(prompt)

    # 检查输出
    safety_parser = PydanticOutputParser(pydantic_object=SafetyCheck)
    # 简化：直接返回，实际应接入内容安全API

    return response.content
```

### Rate Limiting

```python
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, max_calls: int = 10, period: int = 60):
        self.max_calls = max_calls
        self.period = period
        self.calls = defaultdict(list)

    def check(self, user_id: str) -> bool:
        now = time.time()

        # 清理过期记录
        self.calls[user_id] = [
            t for t in self.calls[user_id]
            if now - t < self.period
        ]

        if len(self.calls[user_id]) >= self.max_calls:
            return False

        self.calls[user_id].append(now)
        return True

# 使用
limiter = RateLimiter(max_calls=10, period=60)

def handle_request(user_id: str, query: str):
    if not limiter.check(user_id):
        return "请求过于频繁，请稍后再试。"

    # 处理请求
    return "处理中..."
```

---

## 9. 实战项目

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
9. 实现 ReAct 架构的 Agent
10. 实现 Plan-and-Execute 模式
11. 实现带自我反思的 Reflexion Agent
12. 使用分层记忆系统
13. 实现输入验证和输出过滤

> 下节预告：阶段5 - AI 系统工程（Ollama、vLLM、n8n）
