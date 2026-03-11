# Chroma 向量数据库示例
# 需要安装: pip install chromadb sentence-transformers

from sentence_transformers import SentenceTransformer
import chromadb

# ============ 1. 基础使用 ============
print("=== Chroma 基础使用 ===")

# 初始化客户端（内存模式）
client = chromadb.Client()

# 创建集合
collection = client.create_collection("my_docs")

# 加载 Embedding 模型
model = SentenceTransformer('bge-base-zh-v1.5')

# 文档
documents = [
    "Python是一门易学的编程语言，语法简洁优雅",
    "JavaScript主要用于网页前端开发，也可以用于后端",
    "Rust是一门系统编程语言，强调安全性和并发性",
    "Go语言由Google开发，适合构建微服务"
]

# 生成向量
embeddings = model.encode(documents)

# 添加文档
collection.add(
    documents=documents,
    embeddings=embeddings.tolist(),
    ids=["doc1", "doc2", "doc3", "doc4"]
)

print(f"文档数量: {collection.count()}")

# ============ 2. 检索 ============
print("\n=== 检索示例 ===")

query = "什么是Python？"
query_embedding = model.encode([query])[0]

results = collection.query(
    query_embeddings=[query_embedding.tolist()],
    n_results=2
)

print(f"查询: {query}")
print("检索结果:")
for i, (doc, distance) in enumerate(zip(results['documents'][0], results['distances'][0])):
    print(f"  {i+1}. {doc[:30]}... (距离: {distance:.4f})")

# ============ 3. 持久化存储 ============
print("\n=== 持久化存储 ===")

# 使用持久化客户端
persistent_client = chromadb.PersistentClient(path="./chroma_db")

# 创建或获取集合
collection = persistent_client.get_or_create_collection("docs")

# 添加更多文档
docs = [
    "机器学习是人工智能的一个分支",
    "深度学习是机器学习的一个分支",
    "神经网络是深度学习的基础"
]
embs = model.encode(docs)

collection.add(
    documents=docs,
    embeddings=embs.tolist(),
    ids=["doc5", "doc6", "doc7"]
)

print(f"持久化后文档数量: {collection.count()}")

# ============ 4. 元数据过滤 ============
print("\n=== 元数据过滤 ===")

# 添加带元数据的文档
docs_with_metadata = [
    {"id": "doc8", "text": "Python基础语法", "category": "编程", "level": "入门"},
    {"id": "doc9", "text": "Python高级特性", "category": "编程", "level": "进阶"},
    {"id": "doc10", "text": "数据分析入门", "category": "数据", "level": "入门"},
]

for doc in docs_with_metadata:
    emb = model.encode([doc["text"]])[0]
    collection.upsert(
        ids=[doc["id"]],
        documents=[doc["text"]],
        embeddings=[emb.tolist()],
        metadatas=[{"category": doc["category"], "level": doc["level"]}]
    )

# 过滤查询
results = collection.query(
    query_embeddings=[query_embedding.tolist()],
    n_results=3,
    where={"category": "编程"}  # 只返回编程类
)

print("过滤结果 (category=编程):")
for doc in results['documents'][0]:
    print(f"  - {doc}")
