# n8n 工作流示例

print("=== n8n AI 工作流 ===")

# n8n 是一个可视化的工作流工具，这里展示 JSON 配置

# ============ 1. 基础 Chat 工作流 ============
basic_chat_workflow = {
    "name": "AI Chat",
    "nodes": [
        {
            "name": "Chat Trigger",
            "type": "n8n-nodes-base.chatTrigger",
            "position": [250, 300]
        },
        {
            "name": "OpenAI",
            "type": "openai",
            "parameters": {
                "operation": "chat",
                "model": "gpt-4",
                "prompt": "={{ $json.message }}"
            },
            "position": [450, 300]
        },
        {
            "name": "Respond",
            "type": "n8n-nodes-base.respondToChat",
            "parameters": {
                "text": "={{ $json.choices[0].message.content }}"
            },
            "position": [650, 300]
        }
    ],
    "connections": {
        "Chat Trigger": {"main": [[{"node": "OpenAI"}]]},
        "OpenAI": {"main": [[{"node": "Respond"}]]}
    }
}

print("1. 基础 Chat 工作流:")
print(f"   触发器: Chat Trigger")
print(f"   AI节点: OpenAI (GPT-4)")
print(f"   响应: Respond to Chat")

# ============ 2. RAG 工作流 ============
rag_workflow = {
    "name": "AI RAG Chat",
    "nodes": [
        {"name": "Webhook", "type": "n8n-nodes-base.webhook"},
        {"name": "Embed", "type": "openai", "parameters": {"operation": "embeddings"}},
        {"name": "Vector DB", "type": "qdrant"},
        {"name": "Search", "type": "qdrant", "parameters": {"operation": "search"}},
        {"name": "OpenAI", "type": "openai", "parameters": {"operation": "chat"}},
        {"name": "Respond", "type": "n8n-nodes-base.respondToChat"}
    ]
}

print("\n2. RAG 工作流:")
print("   Webhook -> Embed -> Vector DB Search -> OpenAI -> Respond")

# ============ 3. 多 Agent 工作流 ============
multi_agent_workflow = {
    "name": "Multi-Agent Workflow",
    "nodes": [
        {"name": "Trigger", "type": "n8n-nodes-base.webhook"},
        {"name": "Router", "type": "switch", "parameters": {"dataType": "string", "value1": "={{ $json.category }}"}},
        {"name": "Research Agent", "type": "openai"},
        {"name": "Code Agent", "type": "openai"},
        {"name": "Write Agent", "type": "openai"},
        {"name": "Aggregator", "type": "merge"}
    ]
}

print("\n3. 多 Agent 工作流:")
print("   Switch 路由 -> Research/Code/Write Agent -> Merge")

# ============ 4. 代码实现 ============
print("\n=== Python 调用 n8n Webhook ===")

webhook_example = '''
import requests

# 触发 n8n Webhook
url = "https://your-n8n.com/webhook/ai-chat"

data = {
    "message": "你好",
    "user_id": "user123"
}

response = requests.post(url, json=data)
result = response.json()

print(f"AI回复: {result['reply']}")
'''

print(webhook_example)

# ============ 5. 自定义 n8n 节点 ============
print("=== 自定义 n8n 节点 (JavaScript) ===")

custom_node = '''
// n8n 自定义节点示例
class CustomAI extends n8n.CustomNode {
    async execute() {
        const prompt = this.getInputData()[0].json.prompt;

        // 调用 AI
        const response = await this.callOpenAI(prompt);

        return [this.returnResponse([{ json: { response } }])];
    }
}
'''

print(custom_node)

print("\n访问 https://n8n.io 获取更多教程")
