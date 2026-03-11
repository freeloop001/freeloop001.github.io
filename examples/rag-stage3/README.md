# LLM 核心技术 (RAG) - 代码示例

本文件夹包含 AI 阶段3（RAG、向量数据库、Embedding）的代码示例。

## 目录结构

```
rag-stage3/
├── 01-embedding/           # Embedding
│   ├── embedding_demo.py
│   └── chunk_strategies.py
├── 02-vector-db/           # 向量数据库
│   └── chroma_demo.py
├── 03-langchain/          # LangChain
│   └── langchain_rag.py
├── 04-llamaindex/         # LlamaIndex
│   └── llamaindex_rag.py
├── 05-mcp/                # MCP
├── 06-projects/           # 实战项目
└── README.md
```

## 快速开始

### 1. 安装依赖

```bash
pip install sentence-transformers numpy chromadb langchain langchain-openai langchain-community llama-index llama-index-llms-openai
```

### 2. 运行示例

```bash
# Embedding 基础
python 01-embedding/embedding_demo.py

# Chunk 策略
python 01-embedding/chunk_strategies.py

# Chroma 向量数据库
python 02-vector-db/chroma_demo.py

# LangChain RAG
python 03-langchain/langchain_rag.py

# LlamaIndex RAG
python 04-llamaindex/llamaindex_rag.py
```

## 环境要求

- Python 3.8+
- 部分功能需要 API Key
