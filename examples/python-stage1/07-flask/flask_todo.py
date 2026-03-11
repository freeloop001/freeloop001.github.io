# Flask TODO List API 示例
# 需要安装: pip install flask

from flask import Flask, jsonify, request
import uuid

app = Flask(__name__)

# 内存存储（生产环境请使用数据库）
todos = []

@app.route('/')
def index():
    return jsonify({
        "message": "TODO API",
        "endpoints": {
            "GET /todos": "获取所有 TODO",
            "POST /todos": "创建 TODO",
            "PUT /todos/<id>": "更新 TODO",
            "DELETE /todos/<id>": "删除 TODO"
        }
    })

@app.route('/todos', methods=['GET'])
def get_todos():
    """获取所有 TODO"""
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def create_todo():
    """创建 TODO"""
    data = request.get_json()
    todo = {
        "id": str(uuid.uuid4()),
        "title": data.get("title"),
        "completed": False
    }
    todos.append(todo)
    return jsonify(todo), 201

@app.route('/todos/<todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """更新 TODO"""
    data = request.get_json()
    for todo in todos:
        if todo["id"] == todo_id:
            if "title" in data:
                todo["title"] = data["title"]
            if "completed" in data:
                todo["completed"] = data["completed"]
            return jsonify(todo)
    return jsonify({"error": "TODO not found"}), 404

@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """删除 TODO"""
    global todos
    todos = [t for t in todos if t["id"] != todo_id]
    return jsonify({"message": "Deleted"}), 200

if __name__ == '__main__':
    print("运行: python flask_todo.py")
    print("访问: http://127.0.0.1:5000")
    app.run(debug=True)
