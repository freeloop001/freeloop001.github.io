import asyncio
import time

# 异步编程基础示例

# 1. 基础概念
async def fetch_data():
    """定义异步函数"""
    print("开始获取数据...")
    await asyncio.sleep(2)  # 模拟 I/O 操作
    print("数据获取完成!")
    return {"data": "hello"}

# 运行异步函数
result = asyncio.run(fetch_data())
print(f"结果: {result}")

# 2. 并发执行
async def task(name, delay):
    """模拟任务"""
    print(f"{name} 开始")
    await asyncio.sleep(delay)
    print(f"{name} 完成 (耗时 {delay}s)")
    return f"{name} done"

async def main():
    """并发执行多个任务"""
    start = time.time()
    results = await asyncio.gather(
        task("任务1", 2),
        task("任务2", 1),
        task("任务3", 3)
    )
    elapsed = time.time() - start
    print(f"\n总耗时: {elapsed:.2f}s")  # 约 3s（最长任务时间）
    print(f"结果: {results}")

asyncio.run(main())
