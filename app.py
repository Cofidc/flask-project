from flask import Flask, request, jsonify, render_template_string, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id':self.id,
            'title':self.title,
            'completed':self.completed
        }
    
# 创建数据库表
with app.app_context():
    db.create_all()

# web路由
@app.route('/')
def index():
    todos = Todo.query.all()
    # 简单的 HTML 展示，你也可以直接返回 JSON 用于测试，但页面能直观感受
    return render_template_string('''
    <!doctype html>
    <title>Todo App</title>
    <h1>Todo List</h1>
    <ul>
    {% for todo in todos %}
        <li>{{ todo.title }} - {{ '完成' if todo.completed else '未完成' }}</li>
    {% endfor %}
    </ul>
    <form method="post" action="/add">
        <input type="text" name="title" placeholder="输入新任务">
        <button type="submit">添加</button>
    </form>
    ''', todos=todos)

@app.route('/add',methods=['post'])
def add():
    title = request.form.get('title')
    if title:
        todo = Todo(title=title)
        db.session.add(todo)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/api/todos',methods=['get'])
def get_todos():
    todos = Todo.query.all()
    return jsonify([todo.to_dict() for todo in todos])

@app.route('/api/todos',methods=['POST'])
def create_todo():
    data = request.get_json()
    if 'title' not in data or not data['title'].strip():
        return jsonify({'error':'缺少标题'}),400
    todo = Todo(title=data['title'])
    db.session.add(todo)
    db.session.commit()
    return jsonify(todo.to_dict()),201

@app.route('/api/todos/<int:id>',methods=['GET'])
def get_todo(id):
    todo = Todo.query.get(id)
    if not todo:
        return jsonify({'error':'任务不存在'}),404
    return jsonify(todo.to_dict()),200

@app.route('/api/todos/<int:id>',methods=['PUT'])
def update_todo(id):
    todo = Todo.query.get(id)
    if not todo:
        return jsonify({'error':'任务不存在'}),404
    data = request.get_json()
    if 'title' in data:
        todo.title = data['title']
    if 'completed' in data:
        todo.completed = data['completed']
    db.session.commit()
    return jsonify(todo.to_dict()),200

@app.route('/api/todos/<int:id>',methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get(id)
    if not todo:
        return jsonify({'error':'任务不存在'}),404
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message':'任务删除成功'}),204

if __name__ ==  '__main__':
    app.run(debug=True)