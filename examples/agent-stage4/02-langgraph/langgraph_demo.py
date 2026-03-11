# LangGraph 示例
# 需要安装: pip install langgraph langchain langchain-openai

from langgraph.graph import StateGraph, END
from typing import TypedDict

print("=== LangGraph 基础 ===")

# ============ 1. 定义状态 ============
class GraphState(TypedDict):
    messages: list
    result: str
    step: int

# ============ 2. 定义节点 ============
def node_start(state):
    """起始节点"""
    print(f"步骤 {state.get('step', 0)}: 起始")
    return {
        "messages": state["messages"] + ["开始处理"],
        "step": (state.get("step", 0) + 1)
    }

def node_process(state):
    """处理节点"""
    print(f"步骤 {state.get('step', 0)}: 处理中")
    return {
        "messages": state["messages"] + ["处理完成"],
        "step": (state.get("step", 0) + 1)
    }

def node_end(state):
    """结束节点"""
    print(f"步骤 {state.get('step', 0)}: 结束")
    return {
        "messages": state["messages"] + ["任务完成"],
        "result": "处理成功",
        "step": (state.get("step", 0) + 1)
    }

# ============ 3. 创建图 ============
graph = StateGraph(GraphState)

# 添加节点
graph.add_node("start", node_start)
graph.add_node("process", node_process)
graph.add_node("end", node_end)

# 设置入口
graph.set_entry_point("start")

# 添加边
graph.add_edge("start", "process")
graph.add_edge("process", "end")
graph.add_edge("end", END)

# 编译
app = graph.compile()

# ============ 4. 执行 ============
print("\n执行工作流:")
result = app.invoke({
    "messages": [],
    "result": "",
    "step": 0
})

print(f"\n最终结果: {result['result']}")
print(f"消息历史: {result['messages']}")

# ============ 5. 带条件分支 ============
print("\n=== 带条件分支 ===")

from langgraph.graph import Branch

def should_continue(state):
    """判断是否继续"""
    if len(state.get("messages", [])) < 3:
        return "process"
    return "end"

# 重新创建图
graph2 = StateGraph(GraphState)
graph2.add_node("start", node_start)
graph2.add_node("process", node_process)
graph2.add_node("end", node_end)

graph2.set_entry_point("start")
graph2.add_conditional_edges(
    "start",
    should_continue,
    {
        "process": "process",
        "end": "end"
    }
)
graph2.add_edge("process", "start")  # 循环
graph2.add_edge("end", END)

app2 = graph2.compile()

print("\n执行条件分支工作流:")
result2 = app2.invoke({
    "messages": [],
    "result": "",
    "step": 0
})

print(f"最终结果: {result2['messages']}")
