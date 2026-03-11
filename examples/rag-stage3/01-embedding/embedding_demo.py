# Embedding 向量嵌入示例
# 需要安装: pip install sentence-transformers numpy

from sentence_transformers import SentenceTransformer
import numpy as np

# ============ 1. 基础 Embedding ============
print("=== 基础 Embedding ===")

# 中文效果好的模型
model = SentenceTransformer('bge-base-zh-v1.5')

texts = [
    "Python是一门易学的编程语言",
    "JavaScript是网页脚本语言",
    "Rust是一门系统编程语言"
]

# 生成向量
embeddings = model.encode(texts)

print(f"文本数量: {len(texts)}")
print(f"向量维度: {embeddings.shape}")
print(f"第一个向量前5个元素: {embeddings[0][:5]}")

# ============ 2. 计算相似度 ============
print("\n=== 相似度计算 ===")

# 余弦相似度
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# 计算两两相似度
for i, text1 in enumerate(texts):
    for j, text2 in enumerate(texts):
        if i < j:
            sim = cosine_similarity(embeddings[i], embeddings[j])
            print(f"{text1[:15]} vs {text2[:15]}: {sim:.4f}")

# ============ 3. 检索示例 ============
print("\n=== 检索示例 ===")

query = "什么是Python？"
query_embedding = model.encode([query])[0]

# 计算与所有文档的相似度
scores = []
for i, text in enumerate(texts):
    sim = cosine_similarity(query_embedding, embeddings[i])
    scores.append((text, sim))

# 排序
scores.sort(key=lambda x: x[1], reverse=True)

print(f"查询: {query}")
print("检索结果:")
for text, score in scores:
    print(f"  {text[:20]}... 相似度: {score:.4f}")

# ============ 4. 不同模型对比 ============
print("\n=== 不同模型对比 ===")

models_to_test = [
    ('bge-base-zh-v1.5', '中文优化'),
    ('paraphrase-multilingual-MiniLM-L12-v2', '多语言'),
]

for model_name, desc in models_to_test:
    try:
        m = SentenceTransformer(model_name)
        emb = m.encode(["你好"])[0]
        print(f"{model_name} ({desc}): 维度 {len(emb)}")
    except Exception as e:
        print(f"{model_name}: 下载失败 - {e}")
