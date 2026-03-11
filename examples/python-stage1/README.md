# Python 开发基础 - 代码示例

本文件夹包含 Python 阶段1 各章节的代码示例。

## 目录结构

```
python-stage1/
├── 01-basics/              # Python 基础语法
│   └── basics.py
├── 02-data-structures/     # 数据结构
│   └── data_structures.py
├── 03-file-handling/      # 文件处理
│   ├── json_file.py
│   ├── csv_file.py
│   ├── excel_file.py
│   ├── pdf_file.py
│   └── word_file.py
├── 04-http-requests/       # 网络请求
│   ├── requests_demo.py
│   └── httpx_demo.py
├── 05-async/              # 异步编程
│   ├── async_basics.py
│   └── async_api.py
├── 06-fastapi/            # FastAPI 框架
│   ├── fastapi_basic.py
│   └── fastapi_chat.py
├── 07-flask/              # Flask 框架
│   ├── flask_basic.py
│   └── flask_todo.py
├── 08-package-management/ # 包管理
│   └── requirements.txt
└── README.md
```

## 快速开始

### 1. 安装依赖

```bash
# 推荐：使用 uv（更快）
pip install uv
uv pip install -r 08-package-management/requirements.txt

# 或者使用 pip
pip install -r 08-package-management/requirements.txt
```

### 2. 运行示例

```bash
# 基础语法
python 01-basics/basics.py

# 数据结构
python 02-data-structures/data_structures.py

# 文件处理
python 03-file-handling/json_file.py
python 03-file-handling/csv_file.py

# 网络请求
python 04-http-requests/requests_demo.py
python 04-http-requests/httpx_demo.py

# 异步编程
python 05-async/async_basics.py

# FastAPI（需要运行服务）
python 06-fastapi/fastapi_basic.py
# 然后访问 http://127.0.0.1:8000/docs

# Flask（需要运行服务）
python 07-flask/flask_basic.py
# 然后访问 http://127.0.0.1:5000
```

## 环境要求

- Python 3.8+
- 推荐使用虚拟环境:
  ```bash
  python -m venv venv
  source venv/bin/activate  # Linux/Mac
  # 或
  venv\Scripts\activate    # Windows
  ```

## 注意事项

1. 部分示例需要安装额外库（已在代码中注明）
2. PDF 和 Word 示例需要实际的测试文件
3. Web 框架示例需要启动服务才能测试完整功能
