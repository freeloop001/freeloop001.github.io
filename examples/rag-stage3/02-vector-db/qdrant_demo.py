# Qdrant 云端向量数据库示例
# 需要安装: pip install qdrant-client

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid


def create_collection(client: QdrantClient, collection_name: str, vector_size: int = 768):
    """创建集合"""
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
    )
    print(f"集合 '{collection_name}' 已创建")


def add_vectors(client: QdrantClient, collection_name: str, vectors: list, payloads: list):
    """添加向量"""
    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload=payload
        )
        for vector, payload in zip(vectors, payloads)
    ]

    client.upsert(
        collection_name=collection_name,
        points=points
    )
    print(f"已添加 {len(vectors)} 个向量")


def search(client: QdrantClient, collection_name: str, query_vector: list, limit: int = 5):
    """搜索"""
    results = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=limit
    )

    return [
        {
            "id": result.id,
            "score": result.score,
            "payload": result.payload
        }
        for result in results
    ]


# 本地模式示例
def local_demo():
    """本地模式演示"""
    client = QdrantClient(host="localhost", port=6333)

    # 创建集合
    collection_name = "demo_collection"
    create_collection(client, collection_name, vector_size=4)

    # 添加示例向量
    vectors = [
        [0.1, 0.2, 0.3, 0.4],
        [0.9, 0.8, 0.7, 0.6],
        [0.5, 0.5, 0.5, 0.5]
    ]
    payloads = [
        {"text": "第一个文档", "category": "A"},
        {"text": "第二个文档", "category": "B"},
        {"text": "第三个文档", "category": "C"}
    ]
    add_vectors(client, collection_name, vectors, payloads)

    # 搜索
    query = [0.1, 0.2, 0.3, 0.4]
    results = search(client, collection_name, query)
    print("\n搜索结果:")
    for r in results:
        print(f"  - {r['payload']['text']} (相似度: {r['score']:.4f})")


# 云端模式示例（需要 API Key）
def cloud_demo():
    """云端模式演示"""
    # 从环境变量获取 API Key
    import os
    api_key = os.getenv("QDRANT_API_KEY", "your-api-key")

    client = QdrantClient(
        host="cloud.qdrant.io",
        api_key=api_key
    )

    # 后续操作同上
    pass


if __name__ == "__main__":
    print("=== Qdrant 本地模式 ===")
    # 本地模式需要先启动 Qdrant:
    # docker run -p 6333:6333 qdrant/qdrant
    local_demo()
