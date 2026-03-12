---
layout: post
title: "AI 大模型应用开发学习计划"
date: 2026-03-11 10:00:00 +0800
tags: [AI, LLM, 学习计划, Python]
categories: [learning]
---

> 专注大模型工程和应用开发，不做机器学习和深度学习，不做研究、训练和推理，只做工程开发。

---

## 阶段1：Python 开发基础（2-3周）

### 目标
熟练使用 Python 进行后端开发

### 内容
- Python 语法（变量、函数、类、异常）
- 数据结构：list, dict, set, tuple
- 文件处理：PDF/DOCX/SPREADSHEET/JSON/CSV
- 网络请求：requests, httpx
- 异步编程基础
- Web 框架：FastAPI（重点）、Flask
- 包管理：pip/uv

### 实战
- 做一个文件处理工具（PDF转文本、Excel处理）
- 搭建一个简单的 REST API

---

## 阶段2：AI 开发基础（2周）

### 目标
掌握 LLM API 调用

### 内容

本阶段介绍主流大模型 API 服务，掌握如何通过代码调用这些服务。

#### OpenAI API
> 全球最流行的 LLM 服务商，GPT 系列模型的创造者

- **官网**: https://platform.openai.com
- **代表模型**: GPT-4o, GPT-4o-mini, GPT-4 Turbo
- **特点**: 生态完善，API 稳定，支持函数调用、视觉理解
- **费用**: 按 token 计费，GPT-4o 约 $5-15/百万 tokens

```python
from openai import OpenAI

client = OpenAI(api_key="sk-xxx")
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "你好"}]
)
print(response.choices[0].message.content)
```

#### Anthropic API (Claude)
> 由 OpenAI 创始团队创立的 AI 公司，主打安全可控

- **官网**: https://www.anthropic.com
- **代表模型**: Claude 3.5 Sonnet, Claude 3 Opus
- **特点**: 长上下文（20万 tokens），输出更稳定安全
- **费用**: Claude 3.5 Sonnet 约 $3/百万输入，$15/百万输出

```python
from anthropic import Anthropic

client = Anthropic(api_key="sk-ant-xxx")
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1000,
    messages=[{"role": "user", "content": "你好"}]
)
print(response.content[0].text)
```

#### 国内模型
适合国内业务场景，价格更便宜，响应速度快

| 服务商 | 代表模型 | 特点 | 官网 |
|--------|---------|------|------|
| DeepSeek | DeepSeek V2 | 性价比高，开源 | https://platform.deepseek.com |
| 阿里 Qwen | Qwen 2.5 | 中文优化好 | https://dashscope.aliyuncs.com |
| 智谱 GLM | GLM-4 | 清华技术背景 | https://open.bigmodel.cn |
| MiniMax | MiniMax-M2.5 | 长上下文 | https://api.minimax.com |

#### Prompt 设计
- **System Prompt**: 设置 AI 的角色和行为规则
- **User Prompt**: 用户的实际输入
- **Few-shot**: 提供示例帮助 AI 理解任务

#### 参数掌握
| 参数 | 作用 | 推荐值 |
|------|------|--------|
| temperature | 控制随机性，0 确定性高，1 创意多 | 0.7 |
| top_p | 核采样，控制输出多样性 | 0.9 |
| max_tokens | 限制输出长度 | 按需 |
| top_k | 控制候选词数量 | 40-100 |

### 实战
- 调用 Claude/OpenAI API 实现简单对话
- 设计 Few-shot prompt

---

## 阶段3：LLM 核心技术（3-4周）

### 目标
掌握 RAG 技术栈，让 AI 能够读取私有数据

### 内容

本阶段解决的核心问题：如何让 AI 回答私有的、实时的问题？

#### Embedding (向量嵌入)
> 将文本转换为数学向量，让计算机"理解"文本语义

- **原理**: 语义相似的文本，向量距离也近
- **应用**: 相似文本搜索、语义匹配
- **常用模型**: bge-base-zh-v1.5 (中文)、text-embedding-3-small
- **维度**: 常见 256/512/1024/1536 维

```python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
vector = embeddings.embed_query("Python是一门编程语言")
print(len(vector))  # 1536
```

##### Chunk 策略
将长文档切分成小片段的策略：
- **固定大小**: 每 500-1000 字符一切
- **递归分割**: 按段落、句子递归切分
- **语义分割**: 用 AI 判断在哪里切分

#### 向量数据库
> 专门存储和检索向量（Embedding）的数据库

| 数据库 | 特点 | 适用场景 |
|--------|------|----------|
| **Qdrant** | 开源、Go编写、性能高、云端/本地 | 通用场景，推荐 |
| Milvus | 功能丰富、分布式 | 大规模部署 |
| **Chroma** | 轻量、Python 原生 | 本地快速原型 |
| FAISS | Facebook 出品、纯内存 | 实验研究 |
| Pinecone | 云服务、托管 | 不想自己运维 |

```python
# Chroma 示例
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

vectorstore = Chroma.from_documents(
    documents=texts,
    embedding=OpenAIEmbeddings()
)
results = vectorstore.similarity_search("查询内容", k=3)
```

#### RAG 框架
> 帮助快速构建 RAG 应用的开发框架

| 框架 | 定位 | 特点 |
|------|------|------|
| **LangChain** | 全栈框架 | 生态最丰富，文档多，学习资源丰富 |
| **LlamaIndex** | 索引专家 | 专注数据索引，文档处理更强 |
| LangGraph | 工作流 | 可视化 Agent 流程 |

##### LangChain 适用场景
- 需要快速构建完整应用
- 需要丰富的 Agent、Memory 组件
- 需要对接多种数据源

##### LlamaIndex 适用场景
- 大量文档处理场景
- 需要更细粒度的索引控制
- 知识库问答为主

#### MCP (Model Context Protocol)
> 让 AI 能够调用外部工具的标准化协议

- **官网**: https://modelcontextprotocol.io
- **用途**: 让 Claude/Copilot 能够访问文件、数据库、浏览器等
- **类似**: AI 版的 "USB-C 接口"，统一各种工具的连接标准

```json
// Claude Desktop 配置示例
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"]
    }
  }
}
```

### 实战
- 实现本地知识库问答系统
- 对比不同 Embedding 模型效果

---

## 阶段4：AI Agent（3-4周）

### 目标
掌握 Agent 开发，让 AI 能够自主决策和执行任务

### 内容

本阶段核心公式：**Agent = LLM + Tool + Memory**

#### Agent 概念
> 能够自主规划、调用工具、完成复杂任务的 AI 系统

- **LLM**: 大脑，负责推理和决策
- **Tool**: 手脚，让 AI 能操作外部世界
- **Memory**: 记忆，让 AI 能记住上下文

#### 框架学习

##### LangGraph (推荐)
> LangChain 官方的工作流框架，用图的方式构建 Agent

- **特点**: 可视化流程、状态管理、循环支持
- **适合**: 复杂多步骤任务、需要精确控制流程

```python
from langgraph.graph import StateGraph, END

graph = StateGraph(State)
graph.add_node("think", think_node)
graph.add_node("act", act_node)
graph.set_entry_point("think")
graph.add_edge("think", "act")
agent = graph.compile()
```

##### CrewAI
> 多 Agent 协作框架，适合团队分工场景

- **特点**: 角色定义清晰，适合多 Agent 协作
- **概念**: Agent(角色) + Task(任务) + Crew(团队)

```python
from crewai import Agent, Task, Crew

researcher = Agent(role="研究员", goal="研究AI最新进展")
task = Task(description="调研2024年AI发展", agent=researcher)
crew = Crew(agents=[researcher], tasks=[task])
result = crew.kickoff()
```

##### AutoGen
> 微软出品的多 Agent 对话框架

- **特点**: 对话驱动、自动角色扮演
- **适合**: 需要多角色讨论的场景

```python
from autogen import ConversableAgent

agent1 = ConversableAgent("数学助手", llm_config=...)
agent2 = ConversableAgent("物理助手", llm_config=...)
agent1.initiate_chat(agent2, message="讨论牛顿定律")
```

#### 工具开发

##### Web Search/Fetch
让 Agent 能够搜索互联网

```python
from langchain.tools import tool
import requests

@tool
def search_web(query: str) -> str:
    """搜索互联网获取最新信息"""
    response = requests.get(f"https://api.search?query={query}")
    return response.json()
```

##### Database 查询
让 Agent 能够查询数据库

```python
@tool
def query_database(sql: str) -> str:
    """执行SQL查询"""
    # 注意：需要防止 SQL 注入
    return execute_sql(sql)
```

##### Code Interpreter
让 Agent 能够执行代码

```python
@tool
def run_code(code: str) -> str:
    """安全执行 Python 代码"""
    result = subprocess.run(
        ["python", "-c", code],
        capture_output=True, text=True
    )
    return result.stdout or result.stderr
```

### 实战
- 开发一个多功能 Agent（可调用搜索、数据库、计算器）

---

## 阶段5：AI 系统工程（2-3周）

### 目标
掌握生产环境部署和监控

### 内容

#### 模型管理

##### Ollama
> 本地运行大模型的工具，类似"Docker for AI 模型"

- **官网**: https://ollama.com
- **特点**: 一键本地部署，支持 llama2/qwen/mistral 等
- **用途**: 开发测试、完全离线、私有数据场景

```bash
# 安装和运行
ollama pull llama2
ollama run llama2

# Python API
import ollama
response = ollama.chat(model='llama2', messages=[{'role': 'user', 'content': '你好'}])
```

##### vLLM
> 生产级大模型推理框架，高性能、易部署

- **官网**: https://docs.vllm.ai
- **特点**: PagedAttention 技术，显存利用率高，吞吐量大
- **用途**: 生产环境、API 服务、高并发场景

```bash
# 启动服务
vllm serve Qwen/Qwen2-7B-Instruct --dtype half

# OpenAI 兼容 API
curl http://localhost:8000/v1/chat/completions -d {...}
```

| 对比 | Ollama | vLLM |
|------|--------|------|
| 定位 | 本地开发测试 | 生产级服务 |
| 性能 | 一般 | 高吞吐 |
| 部署 | 简单 | 中等 |
| 适用 | 个人/团队 | 企业生产 |

#### LLM Router

##### LiteLLM
> 统一 API 调用框架，一套代码切换任意模型

- **官网**: https://docs.litellm.ai
- **特点**: 支持 100+ 模型，一个接口调用所有
- **用途**: 避免供应商锁定、成本优化

```python
from litellm import completion

# 切换模型无需改代码
response = completion(model="gpt-4", messages=[...])
response = completion(model="claude-3-sonnet", messages=[...])
response = completion(model="ollama/llama2", messages=[...])
```

##### OpenRouter
> 模型聚合平台，汇集数百种模型

- **官网**: https://openrouter.ai
- **特点**: 统一 API、聚合优惠、按量计费
- **用途**: 快速尝试多种模型、成本优化

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="your-key"
)
response = client.chat.completions.create(
    model="meta-llama/llama-3-70b-instruct",
    messages=[...]
)
```

#### 可观测性

##### LangSmith
> LangChain 官方监控平台，追踪 AI 应用全链路

- **官网**: https://smith.langchain.com
- **功能**: 调用日志、耗时分析、调试追踪、成本统计
- **用途**: 生产监控、问题排查、A/B 测试

```python
from langsmith import traceable

@traceable
def my_function(prompt: str):
    # 自动追踪
    return llm.invoke(prompt)
```

##### Helicone
> OpenAI API 代理层监控

- **官网**: https://helicone.ai
- **特点**: 即插即用、只需换 API 地址
- **用途**: 成本分析、请求日志、缓存优化

```python
# 只需把 base_url 改成 Helicone 的代理地址
client = OpenAI(
    base_url="https://oai.helicone.ai/v1",
    api_key="your-key",
    default_headers={"Helicone-Auth": "Bearer your-helicone-key"}
)
```

#### 工作流编排

##### n8n (推荐)
> 强大的开源自动化工作流工具，可本地部署

- **官网**: https://n8n.io
- **特点**: 300+ 集成、视觉化流程、本地部署
- **用途**: 定时任务、数据同步、AI 流程编排

```bash
# Docker 部署
docker run -it --name n8n -p 5678:5678 n8nio/n8n
```

##### Dify
> 开源 LLMs 应用开发平台

- **官网**: https://dify.ai
- **特点**: 可视化 Prompt、运维监控、企业版
- **用途**: 快速构建 AI 应用、内部知识库

##### Flowise
> 低代码 AI 流程构建工具

- **官网**: https://flowiseai.com
- **特点**: 拖拽界面、LangChain 深度集成
- **用途**: 快速原型、非技术人员使用

| 工具 | 定位 | 适合人群 |
|------|------|----------|
| **n8n** | 通用自动化 | 开发者、全人群 |
| Dify | AI 应用平台 | 产品经理、开发者 |
| Flowise | 低代码流程 | 非技术、爱好者 |

### 实战
- 搭建本地模型服务
- 部署 n8n 工作流

---

## 阶段6-7
达到阶段5后单独沟通

---

## 建议
1. 每个阶段以**项目驱动**，边学边做
2. 重点理解：AI 是基于概率的推算，结果需验证
3. 避免误区：不要把 LangChain 当成全部
4. 善用博客记录学习心得

---

## 误区纠正

> 1. **Python + LangChain ≠ 大模型应用开发**
> 这只不过是冰山一角，典型的基础概念模糊，知识量严重匮乏

> 2. **AI 赋能后不要自信心爆棚**
> 正确认知 AI 是基于概率的推算，以及边界和上下限，切勿盲目自大

> 3. **不要100%相信 AI**
> 丧失思考力就等于自杀，必须有自己的独立思考和验证能力
