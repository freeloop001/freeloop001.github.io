# AutoGen 示例
# 需要安装: pip install pyautogen

print("=== AutoGen 示例 ===")

# 注意：需要 API Key 才能运行完整示例

"""
from autogen import ConversableAgent, GroupChat, GroupChatManager

# ============ 1. 创建 Agent ============
assistant = ConversableAgent(
    name="assistant",
    system_message="你是一个有帮助的AI助手，擅长编程和数据分析",
    llm_config={
        "model": "gpt-4o",
        "api_key": "your-key"
    }
)

user_proxy = ConversableAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "").strip().endswith("STOP"),
    human_input_mode="NEVER"
)

# ============ 2. 双方对话 ============
result = user_proxy.initiate_chat(
    assistant,
    message="解释什么是机器学习 STOP"
)
print(result.summary)

# ============ 3. 多 Agent 群聊 ============
python_expert = ConversableAgent(
    name="Python专家",
    system_message="你擅长Python编程",
    llm_config={"model": "gpt-4o"}
)

js_expert = ConversableAgent(
    name="JavaScript专家",
    system_message="你擅长JavaScript编程",
    llm_config={"model": "gpt-4o"}
)

data_expert = ConversableAgent(
    name="数据分析师",
    system_message="你擅长数据分析",
    llm_config={"model": "gpt-4o"}
)

# 创建群聊
group_chat = GroupChat(
    agents=[python_expert, js_expert, data_expert],
    messages=[],
    max_round=5
)

# 管理员
manager = GroupChatManager(groupchat=group_chat)

# 启动讨论
python_expert.initiate_chat(
    manager,
    message="讨论Python和JavaScript在数据科学领域的应用"
)
"""

print("需要配置 API Key 才能运行完整示例")

# ============ 4. AutoGen 配置 ============
print("\n=== AutoGen 配置说明 ===")

autogen_config = {
    "ConversableAgent": "可对话的智能体",
    "GroupChat": "群聊管理",
    "GroupChatManager": "群聊管理员",
    "llm_config": "LLM 配置（模型、API Key等）",
    "is_termination_msg": "终止条件",
    "human_input_mode": "人工输入模式（NEVER/TERMINATE/ALWAYS）"
}

print("AutoGen 核心组件:")
for key, value in autogen_config.items():
    print(f"  {key}: {value}")
