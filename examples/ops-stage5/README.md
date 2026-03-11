# AI 系统工程 - 代码示例

本文件夹包含 AI 阶段5（系统工程）的代码示例。

## 目录结构

```
ops-stage5/
├── 01-ollama/           # Ollama 本地模型
│   └── ollama_demo.py
├── 02-vllm/            # vLLM 生产级
│   └── vllm_demo.py
├── 03-litellm/         # LiteLLM 路由
│   └── litellm_demo.py
├── 04-langsmith/       # LangSmith 可观测性
│   └── langsmith_demo.py
├── 05-n8n/             # n8n 工作流
│   └── n8n_examples.py
├── 06-projects/        # 实战项目
└── README.md
```

## 快速开始

### 1. 安装依赖

```bash
pip install ollama vllm litellm langchain langchain-openai langsmith
```

### 2. 运行示例

```bash
# Ollama
python 01-ollama/ollama_demo.py

# vLLM
python 02-vllm/vllm_demo.py

# LiteLLM
python 03-litellm/litellm_demo.py

# LangSmith
python 04-langsmith/langsmith_demo.py

# n8n
python 05-n8n/n8n_examples.py
```

## 环境要求

- Python 3.8+
- 部分需要 Ollama/vLLM 服务
- API Key
