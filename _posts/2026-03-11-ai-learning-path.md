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
- OpenAI API 调用
- Anthropic API（Claude）调用
- 国内模型：DeepSeek、Qwen、GLM
- Prompt 设计：system prompt / user prompt
- 参数掌握：temperature, top_p, max_tokens, chunk

### 实战
- 调用 Claude/OpenAI API 实现简单对话
- 设计 Few-shot prompt

---

## 阶段3：LLM 核心技术（3-4周）

### 目标
掌握 RAG 技术栈

### 内容
- **Embedding**
  - Chunk 策略
  - 向量模型（Dimension 概念）
- **向量数据库**
  - 选型：Qdrant / Milvus / FAISS
  - 实战部署和使用
- **RAG 框架**
  - LangChain（生态丰富）
  - LlamaIndex（专注索引）
  - 对比选择
- **MCP**
  - Claude Desktop 配置
  - LibreChat 部署

### 实战
- 实现本地知识库问答系统
- 对比不同 Embedding 模型效果

---

## 阶段4：AI Agent（3-4周）

### 目标
掌握 Agent 开发

### 内容
- Agent 概念：LLM + Tool + Memory
- 任务拆解与工具调用
- **框架学习**
  - LangGraph（推荐）
  - CrewAI
  - AutoGen
- 工具开发
  - Web search/fetch
  - Database 查询
  - Code interpreter

### 实战
- 开发一个多功能 Agent（可调用搜索、数据库、计算器）

---

## 阶段5：AI 系统工程（2-3周）

### 目标
掌握生产环境部署和监控

### 内容
- **模型管理**
  - Ollama 本地部署
  - vLLM（生产级）
- **LLM Router**
  - LiteLLM
  - OpenRouter
- **可观测性**
  - LangSmith
  - Helicone
- **工作流编排**
  - n8n（推荐）
  - Dify
  - Flowise

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
