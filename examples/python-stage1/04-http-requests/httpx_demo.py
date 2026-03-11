import httpx
import asyncio

# httpx 库示例
# 需要安装: pip install httpx

# 1. 同步用法（类似 requests）
response = httpx.get("https://httpbin.org/get")
print(f"同步 GET 状态码: {response.status_code}")
print(f"同步 GET 响应: {response.json()}")

# 2. 异步用法
async def fetch_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://httpbin.org/get")
        return response.json()

# 调用异步函数
result = asyncio.run(fetch_data())
print(f"\n异步 GET 响应: {result}")

# 3. 并发多个请求
async def fetch_all(urls):
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        return [r.json() for r in responses]

if __name__ == "__main__":
    urls = [
        "https://httpbin.org/get",
        "https://httpbin.org/ip",
        "https://httpbin.org/headers"
    ]
    results = asyncio.run(fetch_all(urls))
    print("\n并发请求结果:")
    for i, r in enumerate(results):
        print(f"  请求 {i+1}: {r.get('origin', 'N/A')}")
