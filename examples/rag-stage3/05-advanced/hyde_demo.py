# HyDE (Hypothetical Document Embeddings) 示例
# 通过让 LLM 生成假设文档来改进检索效果
# 需要安装: pip install openai langchain langchain-openai

from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

client = OpenAI()


def generate_hypothetical_document(query: str) -> str:
    """让 LLM 生成假设的理想文档"""
    prompt = f"""Given the question below, generate a hypothetical document that would
perfectly answer this question. Write in detail but be concise.

Question: {query}

Hypothetical Document:"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )

    return response.choices[0].message.content


defhyde_retrieval(query: str, documents: list, embeddings, top_k: int = 3):
    """使用 HyDE 方法进行检索"""

    # Step 1: 生成假设文档
    hypothetical_doc = generate_hypothetical_document(query)
    print(f"假设文档:\n{hypothetical_doc}\n")

    # Step 2: 对假设文档进行向量化
    hypothetical_vector = embeddings.embed_query(hypothetical_doc)

    # Step 3: 使用假设文档的向量进行检索
    # 这里使用 Chroma 作为示例
    vectorstore = Chroma.from_texts(documents, embeddings)
    results = vectorstore.similarity_search_by_vector(
        hypothetical_vector,
        k=top_k
    )

    return results


# 传统检索（对比用）
def traditional_retrieval(query: str, documents: list, embeddings, top_k: int = 3):
    """传统向量检索"""
    vectorstore = Chroma.from_texts(documents, embeddings)
    results = vectorstore.similarity_search(query, k=top_k)
    return results


# 示例
if __name__ == "__main__":
    # 示例文档
    documents = [
        "Python 是一种高级编程语言，由 Guido van Rossum 于 1991 年首次发布。",
        "JavaScript 是一种脚本语言，主要用于网页开发。",
        "Python 的主要特点包括简单易学、可读性强、生态丰富。",
        "机器学习是人工智能的一个分支，通过算法让计算机学习数据。",
        "FastAPI 是一个现代的 Python Web 框架，性能优秀，易于使用。"
    ]

    # 示例查询
    query = "Python 编程语言有什么特点？"

    print(f"查询: {query}\n")

    # 注意：需要设置环境变量 OPENAI_API_KEY
    # import os
    # os.environ["OPENAI_API_KEY"] = "your-api-key"

    # embeddings = OpenAIEmbeddings()
    #
    # print("=== 传统检索 ===")
    # traditional_results = traditional_retrieval(query, documents, embeddings)
    # for i, doc in enumerate(traditional_results):
    #     print(f"{i+1}. {doc.page_content}")
    #
    # print("\n=== HyDE 检索 ===")
    # hyde_results = hyde_retrieval(query, documents, embeddings)
    # for i, doc in enumerate(hyde_results):
    #     print(f"{i+1}. {doc.page_content}")

    print("请设置 OPENAI_API_KEY 后运行完整示例")
