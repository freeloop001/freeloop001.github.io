# FastAPI 天气查询 API 示例
# 需要安装: pip install fastapi uvicorn requests

from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional
import requests
import os

app = FastAPI(title="天气查询 API")

# 免费天气 API 示例（需要替换为真实 API Key）
# 推荐: https://openweathermap.org/api
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "demo")
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"


class WeatherResponse(BaseModel):
    city: str
    country: str
    temperature: float
    humidity: int
    description: str
    wind_speed: float


@app.get("/")
def read_root():
    return {"message": "天气查询 API", "docs": "/docs"}


@app.get("/weather/{city}", response_model=WeatherResponse)
def get_weather(city: str, country: Optional[str] = None):
    """
    获取城市天气信息

    - **city**: 城市名称（英文）
    - **country**: 国家代码（可选），如 cn, us, jp
    """
    params = {
        "q": f"{city},{country}" if country else city,
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(WEATHER_API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            return WeatherResponse(
                city=data["name"],
                country=data["sys"]["country"],
                temperature=data["main"]["temp"],
                humidity=data["main"]["humidity"],
                description=data["weather"][0]["description"],
                wind_speed=data["wind"]["speed"]
            )
        elif response.status_code == 401:
            return {"error": "请设置有效的 API Key", "hint": "export WEATHER_API_KEY=your_key"}
        else:
            return {"error": f"API 返回错误: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}


@app.get("/weather/")
def get_weather_by_query(city: str = Query(..., description="城市名称")):
    """通过查询参数获取天气"""
    return get_weather(city)


# 运行方式:
# 1. 设置环境变量: export WEATHER_API_KEY=your_key
# 2. 启动服务: uvicorn fastapi_weather:app --reload
# 3. 访问: http://127.0.0.1:8000/docs (交互式文档)

if __name__ == "__main__":
    import uvicorn
    print("设置 API Key: export WEATHER_API_KEY=your_key")
    print("启动服务: uvicorn fastapi_weather:app --reload")
    uvicorn.run(app, host="0.0.0.0", port=8000)
