# 输入验证和输出过滤
# 确保 Agent 安全性
# 需要安装: pip install openai

from pydantic import BaseModel, validator
from typing import List, Optional
import re


# ============== 输入验证 ==============
class UserQuery(BaseModel):
    """用户查询验证"""
    query: str
    max_length: int = 500

    @validator('query')
    def query_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("查询不能为空")
        return v.strip()

    @validator('query')
    def query_must_be_safe(cls, v):
        # 检查危险内容
        dangerous_patterns = [
            r'<script',
            r'javascript:',
            r'onerror=',
            r'onclick='
        ]
        for pattern in dangerous_patterns:
            if re.search(pattern, v, re.IGNORECASE):
                raise ValueError("查询包含不安全内容")
        return v

    @validator('query')
    def query_length(cls, v, values):
        max_len = values.get('max_length', 500)
        if len(v) > max_len:
            raise ValueError(f"查询长度不能超过 {max_len} 个字符")
        return v


def validate_input(query: str, max_length: int = 500) -> tuple[bool, str]:
    """
    验证用户输入

    返回: (是否有效, 错误信息)
    """
    try:
        UserQuery(query=query, max_length=max_length)
        return True, ""
    except Exception as e:
        return False, str(e)


# ============== 输出过滤 ==============
class OutputFilter:
    """输出过滤器"""

    def __init__(self):
        # 敏感词列表（示例）
        self.sensitive_words = [
            "密码", "password", "secret", "api_key", "apikey",
            "信用卡", "credit card"
        ]

        # 需要过滤的模式
        self.sensitive_patterns = [
            (r'\d{16,}', '****'),  # 长数字
            (r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '[email]'),
            (r'https?://[^\s]+', '[url]'),
        ]

    def filter(self, text: str) -> str:
        """过滤敏感内容"""
        filtered = text

        # 替换敏感词
        for word in self.sensitive_words:
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            filtered = pattern.sub('***', filtered)

        # 替换敏感模式
        for pattern, replacement in self.sensitive_patterns:
            filtered = re.sub(pattern, replacement, filtered)

        return filtered

    def contains_sensitive(self, text: str) -> bool:
        """检查是否包含敏感内容"""
        for word in self.sensitive_words:
            if word.lower() in text.lower():
                return True
        return False


# ============== 完整的 Agent 安全层 ==============
class AgentSecurityLayer:
    """Agent 安全层"""

    def __init__(self, max_query_length: int = 500):
        self.validator = validate_input
        self.filter = OutputFilter()
        self.max_query_length = max_query_length

    def process_input(self, user_input: str) -> tuple[bool, str]:
        """
        处理用户输入

        返回: (是否通过, 处理后的输入)
        """
        # 验证
        is_valid, error = self.validator(user_input, self.max_query_length)
        if not is_valid:
            return False, error

        # 清理
        cleaned = user_input.strip()

        return True, cleaned

    def process_output(self, output: str) -> str:
        """
        处理 Agent 输出

        返回: 过滤后的输出
        """
        return self.filter.filter(output)


# 示例
if __name__ == "__main__":
    # 测试输入验证
    print("=== 输入验证测试 ===")

    test_queries = [
        "你好",
        "a" * 600,  # 太长
        "<script>alert('xss')</script>",  # 不安全
        "正常的问题"
    ]

    validator = validate_input
    for query in test_queries:
        is_valid, error = validator(query)
        print(f"查询: {query[:30]}... | 有效: {is_valid}", end="")
        if error:
            print(f" | 错误: {error}")
        else:
            print()

    # 测试输出过滤
    print("\n=== 输出过滤测试 ===")
    filter_obj = OutputFilter()

    test_outputs = [
        "我的密码是 1234567890123456",
        "请联系 test@example.com",
        "访问 https://example.com 了解更多信息",
        "这是一个正常回答"
    ]

    for output in test_outputs:
        filtered = filter_obj.filter(output)
        print(f"原文: {output}")
        print(f"过滤: {filtered}\n")

    # 测试完整安全层
    print("=== 完整安全层测试 ===")
    security = AgentSecurityLayer()

    is_valid, result = security.process_input("你好，世界！")
    print(f"输入: {result} | 有效: {is_valid}")

    output = security.process_output("请联系 admin@example.com 获取密码 12345678901234567890")
    print(f"输出: {output}")
