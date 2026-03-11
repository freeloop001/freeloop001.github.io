import asyncio
import httpx

# 异步 API 调用示例
# 需要安装: pip install httpx

async def fetch_user(client, user_id):
    """获取单个用户信息"""
    response = await client.get(f"https://jsonplaceholder.typicode.com/users/{user_id}")
    return response.json()

async def main():
    """批量获取用户信息"""
    async with httpx.AsyncClient() as client:
        # 并发获取 10 个用户
        tasks = [fetch_user(client, i) for i in range(1, 11)]
        users = await asyncio.gather(*tasks)

        print("用户列表:")
        for user in users:
            print(f"  - {user['name']} ({user['email']})")

if __name__ == "__main__":
    asyncio.run(main())
