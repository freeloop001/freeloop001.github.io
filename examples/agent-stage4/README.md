# AI Agent - 代码示例

本文件夹包含 AI 阶段4（Agent）的代码示例。

## 目录结构

```
agent-stage4/
├── 01-agent-basics/      # Agent 基础
│   └── simple_agent.py
├── 02-langgraph/        # LangGraph
│   └── langgraph_demo.py
├── 03-crewai/           # CrewAI
│   └── crewai_demo.py
├── 04-autogen/          # AutoGen
│   └── autogen_demo.py
├── 05-tools/            # 工具开发
│   └── custom_tools.py
├── 06-projects/         # 实战项目
└── README.md
```

## 快速开始

### 1. 安装依赖

```bash
pip install langgraph langchain langchain-openai crewai pyautogen
```

### 2. 运行示例

```bash
# Agent 基础
python 01-agent-basics/simple_agent.py

# LangGraph
python 02-langgraph/langgraph_demo.py

# CrewAI
python 03-crewai/crewai_demo.py

# AutoGen
python 04-autogen/autogen_demo.py

# 自定义工具
python 05-tools/custom_tools.py
```

## 环境要求

- Python 3.8+
- API Key（各平台）
