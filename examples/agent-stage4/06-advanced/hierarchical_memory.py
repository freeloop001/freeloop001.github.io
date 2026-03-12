# 分层记忆系统
# 实现短期记忆、长期记忆和向量记忆
# 需要安装: pip install langchain

from typing import List, Dict
from datetime import datetime
import json


class ShortTermMemory:
    """短期记忆 - 对话历史"""

    def __init__(self, max_size: int = 10):
        self.max_size = max_size
        self.messages = []

    def add(self, role: str, content: str):
        """添加消息"""
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })

        # 超过最大容量时删除最早的
        if len(self.messages) > self.max_size:
            self.messages.pop(0)

    def get_recent(self, n: int = 5) -> List[Dict]:
        """获取最近 n 条消息"""
        return self.messages[-n:]

    def get_all(self) -> List[Dict]:
        """获取所有消息"""
        return self.messages

    def clear(self):
        """清空记忆"""
        self.messages = []


class LongTermMemory:
    """长期记忆 - 持久化存储"""

    def __init__(self, storage_file: str = "longterm_memory.json"):
        self.storage_file = storage_file
        self.facts = []
        self._load()

    def _load(self):
        """从文件加载"""
        try:
            with open(self.storage_file, "r", encoding="utf-8") as f:
                self.facts = json.load(f)
        except FileNotFoundError:
            self.facts = []

    def _save(self):
        """保存到文件"""
        with open(self.storage_file, "w", encoding="utf-8") as f:
            json.dump(self.facts, f, ensure_ascii=False, indent=2)

    def add(self, fact: str, category: str = "general"):
        """添加事实"""
        self.facts.append({
            "fact": fact,
            "category": category,
            "timestamp": datetime.now().isoformat()
        })
        self._save()

    def get_by_category(self, category: str) -> List[Dict]:
        """按类别获取"""
        return [f for f in self.facts if f["category"] == category]

    def search(self, keyword: str) -> List[Dict]:
        """搜索"""
        return [f for f in self.facts if keyword in f["fact"]]

    def get_all(self) -> List[Dict]:
        """获取所有"""
        return self.facts


class VectorMemory:
    """向量记忆 - 语义检索"""

    def __init__(self):
        # 简单实现：使用关键词匹配
        # 实际应使用向量数据库
        self.memories = []
        self.embeddings = {}

    def add(self, content: str, metadata: dict = None):
        """添加记忆"""
        memory = {
            "content": content,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        }
        self.memories.append(memory)

        # 简单向量化：提取关键词
        keywords = self._extract_keywords(content)
        for kw in keywords:
            if kw not in self.embeddings:
                self.embeddings[kw] = []
            self.embeddings[kw].append(len(self.memories) - 1)

    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        # 简单实现：分词并过滤短词
        words = text.lower().split()
        return [w for w in words if len(w) > 2]

    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """语义搜索"""
        query_keywords = self._extract_keywords(query)

        # 统计每个记忆的匹配度
        scores = {}
        for kw in query_keywords:
            if kw in self.embeddings:
                for idx in self.embeddings[kw]:
                    scores[idx] = scores.get(idx, 0) + 1

        # 排序
        sorted_idx = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        # 返回 top_k
        return [self.memories[idx] for idx, _ in sorted_idx[:top_k]]

    def get_all(self) -> List[Dict]:
        """获取所有"""
        return self.memories


# 分层记忆管理器
class HierarchicalMemory:
    """分层记忆管理器"""

    def __init__(self):
        self.short_term = ShortTermMemory()
        self.long_term = LongTermMemory()
        self.vector = VectorMemory()

    def add_message(self, role: str, content: str):
        """添加对话消息"""
        self.short_term.add(role, content)

        # 重要信息提取到长期记忆
        if self._is_important(content):
            self.long_term.add(content, "conversation")

        # 添加到向量记忆
        self.vector.add(content, {"role": role})

    def _is_important(self, content: str) -> bool:
        """判断是否重要"""
        important_keywords = ["记住", "重要", "不要忘记", "preference", "prefers"]
        return any(kw in content.lower() for kw in important_keywords)

    def get_context(self, current_query: str = None) -> str:
        """获取上下文"""
        context_parts = []

        # 短期记忆
        recent = self.short_term.get_recent(3)
        if recent:
            context_parts.append("最近对话:")
            for m in recent:
                context_parts.append(f"  {m['role']}: {m['content']}")

        # 长期记忆（相关）
        if current_query:
            related = self.long_term.search(current_query)
            if related:
                context_parts.append("\n重要事实:")
                for f in related[:3]:
                    context_parts.append(f"  - {f['fact']}")

            # 向量记忆
            semantic = self.vector.search(current_query)
            if semantic:
                context_parts.append("\n相关记忆:")
                for m in semantic:
                    context_parts.append(f"  - {m['content']}")

        return "\n".join(context_parts)


# 示例
if __name__ == "__main__":
    # 创建记忆系统
    memory = HierarchicalMemory()

    # 添加对话
    memory.add_message("user", "我喜欢喝咖啡，不喝茶")
    memory.add_message("assistant", "好的，我记住了")
    memory.add_message("user", "我最喜欢的编程语言是 Python")

    # 获取上下文
    context = memory.get_context("我喝什么?")
    print("上下文:\n", context)

    context2 = memory.get_context("编程语言")
    print("\n上下文2:\n", context2)
