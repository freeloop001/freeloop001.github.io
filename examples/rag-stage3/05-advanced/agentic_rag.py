# Agentic RAG 示例
# 结合 Agent 能力实现更智能的 RAG 系统
# 需要安装: pip install openai langchain langchain-openai

from langchain_openai import ChatOpenAI
from langchain.agents import AgentType, create_openai_functions_agent
from langchain.tools import Tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


llm = ChatOpenAI(model="gpt-4o")


def create_agentic_rag(documents: list):
    """创建 Agentic RAG 系统"""

    # 1. 构建知识库
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_text("\n\n".join(documents))

    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_texts(texts, embeddings)
    retriever = vectorstore.as_retriever()

    # 2. 定义检索工具
    def retrieve_context(query: str) -> str:
        """检索相关上下文"""
        docs = retriever.get_relevant_documents(query)
        return "\n\n".join([doc.page_content for doc in docs])

    retrieve_tool = Tool(
        name="retrieve_context",
        func=retrieve_context,
        description="当需要从知识库中查找信息时使用"
    )

    # 3. 定义回答工具
    def answer_with_context(query: str) -> str:
        """基于上下文回答问题"""
        context = retrieve_context(query)

        prompt = f"""基于以下上下文回答问题。如果上下文中没有相关信息，请说明无法回答。

上下文:
{context}

问题: {query}

回答:"""

        response = llm.invoke(prompt)
        return response.content

    answer_tool = Tool(
        name="answer_question",
        func=answer_with_stratey,
        description="用于回答用户问题"
    )

    # 4. 创建 Agent
    tools = [retrieve_tool, answer_tool]

    prompt = ChatPromptTemplate.from_messages([
        ("system", """你是一个智能问答助手。
你可以使用以下工具:
- retrieve_context: 从知识库检索相关信息
- answer_question: 回答用户问题

请根据问题选择合适的工具来回答。"""),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])

    agent = create_openai_functions_agent(llm, tools, prompt)

    return agent


# 更简单的实现：使用 LangChain 的 AgentExecutor
def simple_agentic_rag():
    """简化版 Agentic RAG"""

    from langchain.agents import AgentExecutor

    # 示例知识库
    documents = [
        "Python 是一种高级编程语言。",
        "FastAPI 是一个现代的 Python Web 框架。",
        "RAG 是检索增强生成技术。"
    ]

    # 构建向量库
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
    texts = text_splitter.split_text("\n\n".join(documents))

    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_texts(texts, embeddings)
    retriever = vectorstore.as_retriever()

    # 定义工具函数
    def search_knowledge_base(query: str) -> str:
        """搜索知识库"""
        docs = retriever.get_relevant_documents(query)
        return "\n".join([doc.page_content for doc in docs])

    # 创建 Agent
    tools = [
        Tool(
            name="search_knowledge_base",
            func=search_knowledge_base,
            description="搜索知识库获取相关信息"
        )
    ]

    # Agent 提示词
    from langchain.prompts import PromptTemplate

    prompt = PromptTemplate.from_template("""你是一个问答助手。
使用 search_knowledge_base 工具搜索知识库来回答问题。

问题: {question}

请先搜索相关上下文，然后给出答案。""")

    # 创建 Agent
    from langchain.agents import LLMSingleActionAgent

    agent = LLMSingleActionAgent(
        llm_chain=llm,
        output_parser=None,
        stop=["\n"],
        tools=tools
    )

    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        verbose=True
    )

    return agent_executor


# 示例
if __name__ == "__main__":
    print("=== Agentic RAG 示例 ===")

    # 注意：需要设置 OPENAI_API_KEY
    # import os
    # os.environ["OPENAI_API_KEY"] = "your-api-key"

    # 示例查询
    # executor = simple_agentic_rag()
    # result = executor.run("Python 是什么?")
    # print(f"回答: {result}")

    print("请设置 OPENAI_API_KEY 后运行完整示例")
