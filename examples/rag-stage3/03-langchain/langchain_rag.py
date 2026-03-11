# LangChain RAG 示例
# 需要安装: pip install langchain langchain-openai langchain-community sentence-transformers chromadb

# ============ 1. 简单 RAG ============
print("=== LangChain 简单 RAG ===")

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

# 模拟文档内容（实际使用时可用 TextLoader 加载文件）
from langchain.schema import Document

docs = [
    Document(
        page_content="Python是一种广泛使用的编程语言，特点是简洁易学。"
    ),
    Document(
        page_content="JavaScript主要用于网页前端开发，也可以用Node.js做后端。"
    ),
    Document(
        page_content="Rust是一门系统编程语言，强调内存安全和并发性能。"
    ),
]

# 分割文档
text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
split_docs = text_splitter.split_documents(docs)

print(f"分割后文档数量: {len(split_docs)}")

# 创建向量存储（使用模拟 Embedding）
# 实际使用时：
# embeddings = OpenAIEmbeddings()
# vectorstore = Chroma.from_documents(split_docs, embeddings)

# ============ 2. RetrievalQA 链 ============
print("\n=== RetrievalQA 链 ===")

# 完整示例（需要 API Key）
"""
# 初始化
llm = ChatOpenAI(api_key="your-key", model="gpt-4o")
embeddings = OpenAIEmbeddings()

# 创建向量存储
vectorstore = Chroma.from_documents(split_docs, embeddings)

# 创建 QA 链
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

# 问答
result = qa.invoke({"query": "Python有什么特点？"})
print(result["result"])
"""

print("需要配置 API Key 才能运行完整示例")

# ============ 3. 不同 Chain Type ============
print("\n=== Chain Type 说明 ===")

chain_types = {
    "stuff": "将所有相关文档塞入上下文，适合短文档",
    "map_reduce": "先对每个文档单独问答，再汇总结果",
    "refine": "基于前一个答案迭代优化",
    "map_rerank": "对每个文档打分，返回最高分答案"
}

for chain_type, desc in chain_types.items():
    print(f"- {chain_type}: {desc}")

# ============ 4. 带来源的问答 ============
print("\n=== 带来源的问答 ===")

"""
from langchain.chains import RetrievalQAWithSourcesChain

qa_with_sources = RetrievalQAWithSourcesChain.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

result = qa_with_sources.invoke({"question": "什么是Python？"})
print(f"答案: {result['answer']}")
print(f"来源: {result['sources']}")
"""

print("需要配置 API Key 才能运行完整示例")
