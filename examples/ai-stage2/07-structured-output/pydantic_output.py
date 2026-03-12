# Pydantic 结构化输出示例
# 需要安装: pip install openai pydantic

from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List, Optional

client = OpenAI()


# 定义输出结构
class PersonInfo(BaseModel):
    name: str = Field(description="人名")
    age: int = Field(description="年龄")
    occupation: Optional[str] = Field(None, description="职业")


class PeopleList(BaseModel):
    people: List[PersonInfo]
    total_count: int


# 使用函数定义获取结构化输出
def extract_person_info(text: str) -> PersonInfo:
    """从文本中提取人物信息"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "你是一个信息提取助手。"},
            {"role": "user", "content": f"从以下文本中提取人物信息：{text}"}
        ],
        tools=[{
            "type": "function",
            "function": {
                "name": "extract_person",
                "description": "提取人物信息",
                "parameters": PersonInfo.model_json_schema()
            }
        }],
        tool_choice={"type": "function", "function": {"name": "extract_person"}}
    )

    # 解析工具调用结果
    tool_call = response.choices[0].message.tool_calls[0]
    return PersonInfo.model_validate_json(tool_call.function.arguments)


# 更简单的方式：使用 response_format (GPT-4o 新特性)
def extract_with_format(text: str) -> PersonInfo:
    """使用 response_format 获取结构化输出"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "你是一个信息提取助手。"},
            {"role": "user", "content": f"从以下文本中提取人物信息：{text}"}
        ],
        response_format=PersonInfo
    )

    return PersonInfo.model_validate_json(
        response.choices[0].message.content
    )


# 测试
if __name__ == "__main__":
    text = "张三是一位28岁的软件工程师，目前在阿里巴巴工作。"

    print("使用 function calling:")
    result = extract_person_info(text)
    print(f"  姓名: {result.name}")
    print(f"  年龄: {result.age}")
    print(f"  职业: {result.occupation}")

    print("\n使用 response_format:")
    result2 = extract_with_format(text)
    print(f"  姓名: {result2.name}")
    print(f"  年龄: {result2.age}")
    print(f"  职业: {result2.occupation}")
