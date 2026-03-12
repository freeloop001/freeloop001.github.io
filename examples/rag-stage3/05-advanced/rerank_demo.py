# Rerank 模型示例
# 用于对初步检索结果进行重新排序
# 需要安装: pip install sentence-transformers rank-bm25

from sentence_transformers import CrossEncoder
import numpy as np


# 使用 Cross-Encoder 进行重排
def rerank_with_cross_encoder(query: str, documents: list, top_k: int = 3):
    """使用 Cross-Encoder 进行重排"""

    # 使用预训练的 Cross-Encoder 模型
    # 可以选择其他模型: ms-marco-MiniLM-L-6-v2, ms-marco-MultiBERT-L-12 等
    model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

    # 创建查询-文档对
    pairs = [(query, doc) for doc in documents]

    # 获取相关性分数
    scores = model.predict(pairs)

    # 按分数排序
    results = sorted(
        zip(documents, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return results[:top_k]


# 使用 BM25 进行重排
from rank_bm25 import BM25Okapi
import re


def preprocess_text(text: str) -> list:
    """预处理文本"""
    # 分词（小写，去除标点）
    return re.findall(r'\w+', text.lower())


def rerank_with_bm25(query: str, documents: list, top_k: int = 3):
    """使用 BM25 进行重排"""

    # 预处理文档
    tokenized_docs = [preprocess_text(doc) for doc in documents]
    tokenized_query = preprocess_text(query)

    # 创建 BM25 模型
    bm25 = BM25Okapi(tokenized_docs)

    # 获取 BM25 分数
    scores = bm25.get_scores(tokenized_query)

    # 按分数排序
    results = sorted(
        zip(documents, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return results[:top_k]


# 结合向量检索和重排
def hybrid_rerank(query: str, documents: list, vector_scores: dict, top_k: int = 3):
    """
    结合多种分数进行重排
    vector_scores: dict of {doc: score}
    """

    # 归一化向量分数
    max_score = max(vector_scores.values())
    norm_vector_scores = {doc: score/max_score for doc, score in vector_scores.items()}

    # BM25 分数
    bm25_results = rerank_with_bm25(query, documents, top_k=len(documents))
    bm25_scores = {doc: score for doc, score in bm25_results}
    max_bm25 = max(bm25_scores.values()) if bm25_scores else 1
    norm_bm25 = {doc: score/max_bm25 for doc, score in bm25_scores.items()}

    # 组合分数（可调整权重）
    alpha = 0.5  # 向量检索权重
    beta = 0.5   # BM25 权重

    combined_scores = {}
    for doc in documents:
        vector_score = norm_vector_scores.get(doc, 0)
        bm25_score = norm_bm25.get(doc, 0)
        combined_scores[doc] = alpha * vector_score + beta * bm25_score

    # 排序
    results = sorted(
        combined_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return results[:top_k]


# 示例
if __name__ == "__main__":
    # 示例文档
    documents = [
        "Python 是一种高级编程语言，简单易学。",
        "Java 是面向对象的编程语言，企业级应用广泛。",
        "Python 在数据科学和机器学习领域非常流行。",
        "JavaScript 主要用于网页前端开发。",
        "Python 的生态系统丰富，有大量的第三方库。"
    ]

    # 示例查询
    query = "Python 编程语言有什么优势？"

    print(f"查询: {query}\n")

    # Cross-Encoder 重排
    print("=== Cross-Encoder 重排 ===")
    reranked = rerank_with_cross_encoder(query, documents)
    for i, (doc, score) in enumerate(reranked):
        print(f"{i+1}. 分数: {score:.4f} | {doc}")

    # BM25 重排
    print("\n=== BM25 重排 ===")
    reranked = rerank_with_bm25(query, documents)
    for i, (doc, score) in enumerate(reranked):
        print(f"{i+1}. 分数: {score:.4f} | {doc}")
