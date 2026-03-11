# LlamaIndex RAG 示例
# 需要安装: pip install llama-index llama-index-llms-openai

# ============ 1. 简单示例 ============
print("=== LlamaIndex 简单示例 ===")

from llama_index.core import Document, VectorStoreIndex
from llama_index.llms.openai import OpenAI

# 创建文档
documents = [
    Document(text="Python是一种广泛使用的编程语言，特点是简洁易学。"),
    Document(text="JavaScript主要用于网页前端开发，也可以用Node.js做后端。"),
    Document(text="Rust是一门系统编程语言，强调内存安全和并发性能。"),
]

# 创建索引（简化版，无需 API Key）
index = VectorStoreIndex.from_documents(documents)

print(f"索引中的节点数: {len(index.docstore.docs)}")

# ============ 2. 查询引擎 ============
print("\n=== 查询引擎 ===")

# 创建查询引擎（使用默认 LLM）
query_engine = index.as_query_engine()

# 查询
response = query_engine.query("Python有什么特点？")
print(f"查询: Python有什么特点？")
print(f"回答: {response}")

# ============ 3. 带 LLM 的完整示例 ============
print("\n=== 带 LLM 的完整示例 ===")

"""
# 需要 API Key
from llama_index.llms.openai import OpenAI

llm = OpenAI(api_key="your-key", model="gpt-4o")

# 使用自定义 LLM
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine(llm=llm)

response = query_engine.query("Python和JavaScript有什么区别？")
print(f"回答: {response}")
"""

print("需要配置 API Key 才能运行完整示例")

# ============ 4. 不同查询模式 ============
print("\n=== 不同查询模式 ===")

# 基础查询
response = query_engine.query("什么是Rust？")
print(f"基础查询: {response}")

# 带相似度阈值
from llama_index.core import Settings

# Settings 可以配置各种参数
print("\n可配置参数:")
print("- chunk_size: 分块大小")
print("- similarity_top_k: 返回前k个最相似的文档")
print("- response_mode: 响应模式")

# ============ 5. 自定义 Embedding ============
print("\n=== 自定义 Embedding ===")

"""
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# 使用 OpenAI Embedding
embed_model = OpenAIEmbedding()

# 使用 HuggingFace Embedding
# embed_model = HuggingFaceEmbedding(model_name="bge-base-zh-v1.5")

index = VectorStoreIndex.from_documents(
    documents,
    embed_model=embed_model
)
"""

print("需要配置相应 Embedding 模型才能运行")
