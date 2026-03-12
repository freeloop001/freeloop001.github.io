import requests

# requests 库示例

# GET 请求
response = requests.get("https://httpbin.org/get")
print(f"GET 状态码: {response.status_code}")
print(f"GET 响应: {response.json()}")

# POST 请求
data = {"username": "testuser", "age": 25}
response = requests.post("https://httpbin.org/post", json=data)
print(f"\nPOST 状态码: {response.status_code}")
print(f"POST 响应: {response.json()}")

# 带参数的 GET 请求
params = {"search": "python", "page": 1}
response = requests.get("https://httpbin.org/get", params=params)
print(f"\n带参数 GET URL: {response.url}")
