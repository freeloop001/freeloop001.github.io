# Token 缓存机制示例
# 用于减少重复调用，节省成本

import hashlib
import json
from typing import Optional, Any
import tiktoken


class TokenCache:
    """简单的 Token 缓存机制"""

    def __init__(self, max_tokens: int = 1000):
        self.cache = {}
        self.max_tokens = max_tokens
        self.total_tokens_saved = 0
        self.encoding = tiktoken.encoding_for_model("gpt-4o")

    def _hash_messages(self, messages: list) -> str:
        """生成消息的哈希值"""
        # 排序确保顺序不影响缓存
        content = json.dumps(messages, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()

    def _count_tokens(self, messages: list) -> int:
        """计算消息的 token 数量"""
        num_tokens = 0
        for message in messages:
            num_tokens += 4
            for key, value in message.items():
                num_tokens += len(self.encoding.encode(value))
        return num_tokens

    def get(self, messages: list) -> Optional[Any]:
        """从缓存获取结果"""
        cache_key = self._hash_messages(messages)

        if cache_key in self.cache:
            cached = self.cache[cache_key]
            self.total_tokens_saved += self._count_tokens(messages)
            print(f"缓存命中! 节省约 {self._count_tokens(messages)} tokens")
            return cached["response"]

        return None

    def set(self, messages: list, response: str):
        """设置缓存"""
        # 检查是否超过缓存大小限制
        if len(self.cache) >= self.max_tokens:
            # 删除最早的缓存
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]

        cache_key = self._hash_messages(messages)
        self.cache[cache_key] = {
            "response": response,
            "tokens": self._count_tokens(messages)
        }

    def get_stats(self) -> dict:
        """获取缓存统计"""
        return {
            "cache_size": len(self.cache),
            "total_tokens_saved": self.total_tokens_saved,
            "estimated_savings_usd": round(
                self.total_tokens_saved / 1_000_000 * 5,  # 假设 $5/百万
                6
            )
        }


# 使用示例
if __name__ == "__main__":
    cache = TokenCache(max_tokens=100)

    # 模拟对话
    messages1 = [
        {"role": "user", "content": "什么是 Python?"}
    ]

    messages2 = [
        {"role": "user", "content": "什么是 Python?"}
    ]

    # 第一次调用（无缓存）
    print("=== 第一次调用 ===")
    cached_result = cache.get(messages1)
    if cached_result is None:
        print("缓存未命中，执行实际调用...")
        # 实际调用 API 的代码...
        response = "Python 是一种高级编程语言。"
        cache.set(messages1, response)

    # 第二次调用（有缓存）
    print("\n=== 第二次调用 ===")
    cached_result = cache.get(messages2)
    if cached_result:
        print(f"使用缓存: {cached_result}")

    # 查看统计
    print("\n=== 缓存统计 ===")
    stats = cache.get_stats()
    print(f"缓存条目数: {stats['cache_size']}")
    print(f"节省 tokens: {stats['total_tokens_saved']}")
    print(f"预估节省费用: ${stats['estimated_savings_usd']}")


# 进阶：结合 LangChain 的缓存
"""
from langchain.cache import InMemoryCache
from langchain.globals import set_llm_cache

# 设置全局缓存
set_llm_cache(InMemoryCache())

# 之后的 LLM 调用会自动使用缓存
"""
