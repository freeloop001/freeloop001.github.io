# Chunk 策略示例

import re

# ============ 1. 固定大小分块 ============
def fixed_chunk(text: str, chunk_size: int = 500, overlap: int = 50):
    """固定大小分块"""
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)
    return chunks

# ============ 2. 递归分块 ============
def recursive_chunk(text: str, delimiters=None, min_length=50):
    """递归分块"""
    if delimiters is None:
        delimiters = ["\n\n", "\n", ". ", " "]

    if not delimiters:
        return [text] if len(text) >= min_length else []

    delimiter = delimiters[0]
    parts = text.split(delimiter)

    if len(parts) > 1:
        result = []
        for part in parts:
            result.extend(recursive_chunk(part, delimiters[1:], min_length))
        return result
    else:
        return recursive_chunk(text, delimiters[1:], min_length)

# ============ 3. 按段落分块 ============
def paragraph_chunk(text: str):
    """按段落分块"""
    paragraphs = text.split("\n\n")
    return [p.strip() for p in paragraphs if p.strip()]

# ============ 4. 语义分块 (简化版) ============
def semantic_chunk(text: str, max_length=500):
    """基于句子边界的语义分块"""
    # 按句子分割
    sentences = re.split(r'([。！？])', text)
    chunks = []
    current_chunk = ""

    for i in range(0, len(sentences)-1, 2):
        sentence = sentences[i] + (sentences[i+1] if i+1 < len(sentences) else "")

        if len(current_chunk) + len(sentence) > max_length:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            current_chunk += sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

# 测试
if __name__ == "__main__":
    sample_text = """
Python是一种广泛使用的解释型、高级和通用的编程语言。

Python支持多种编程范式，包括结构化、过程式、反射式、面向对象和函数式编程。

它拥有动态类型系统和垃圾回收功能，能够自动管理内存使用。

Python的设计哲学强调代码的可读性和简洁的语法。
相比于C++或Java，Python让开发者能够用更少的代码表达想法。
    """

    print("=== 固定大小分块 ===")
    chunks = fixed_chunk(sample_text, chunk_size=100, overlap=20)
    for i, c in enumerate(chunks):
        print(f"Chunk {i}: {c[:50]}...")

    print("\n=== 按段落分块 ===")
    chunks = paragraph_chunk(sample_text)
    for i, c in enumerate(chunks):
        print(f"Chunk {i}: {c[:50]}...")

    print("\n=== 语义分块 ===")
    chunks = semantic_chunk(sample_text, max_length=100)
    for i, c in enumerate(chunks):
        print(f"Chunk {i}: {c[:50]}...")
