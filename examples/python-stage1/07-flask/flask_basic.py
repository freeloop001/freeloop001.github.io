# Flask 示例
# 需要安装: pip install flask

from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"message": "Hello World!"})

@app.route('/api/users', methods=['GET'])
def get_users():
    """获取用户列表"""
    users = [
        {"id": 1, "name": "张三"},
        {"id": 2, "name": "李四"}
    ]
    return jsonify(users)

@app.route('/api/users', methods=['POST'])
def create_user():
    """创建用户"""
    data = request.get_json()
    return jsonify({"id": 3, "name": data.get("name")}), 201

@app.route('/search')
def search():
    """查询参数示例"""
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    return f"搜索: {query}, 页码: {page}"

# 运行方式: python flask_basic.py
# 访问: http://127.0.0.1:5000

if __name__ == '__main__':
    print("运行: python flask_basic.py")
    print("访问: http://127.0.0.1:5000")
    app.run(debug=True)
