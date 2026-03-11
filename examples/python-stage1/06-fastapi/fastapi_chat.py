# FastAPI AI 对话 API 示例
# 需要安装: pip install fastapi uvicorn

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="AI Chat API")

class ChatRequest(BaseModel):
    message: str
    model: str = "gpt-3.5-turbo"

@app.get("/")
def read_root():
    return {"message": "AI Chat API", "version": "1.0"}

@app.post("/chat")
async def chat(request: ChatRequest):
    """处理聊天请求"""
    if not request.message:
        raise HTTPException(status_code=400, detail="消息不能为空")

    # 这里可以替换为实际的 LLM API 调用
    # 示例：调用 OpenAI API
    return {
        "response": f"收到消息: {request.message}",
        "model": request.model,
        "status": "success"
    }

# 运行方式: uvicorn fastapi_chat:app --reload
# 访问文档: http://127.0.0.1:8000/docs

if __name__ == "__main__":
    print("运行: uvicorn fastapi_chat:app --reload")
    print("访问: http://127.0.0.1:8000/docs")
