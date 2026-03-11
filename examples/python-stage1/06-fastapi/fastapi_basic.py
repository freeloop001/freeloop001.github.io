# FastAPI 示例
# 需要安装: pip install fastapi uvicorn

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    description: str | None = None

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.post("/items/")
def create_item(item: Item):
    return {
        "item_name": item.name,
        "item_price": item.price,
        "item_description": item.description
    }

# 运行方式: uvicorn fastapi_basic:app --reload
# 访问文档: http://127.0.0.1:8000/docs

if __name__ == "__main__":
    print("运行: uvicorn fastapi_basic:app --reload")
    print("访问: http://127.0.0.1:8000/docs")
