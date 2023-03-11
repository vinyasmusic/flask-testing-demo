from flask import jsonify
from app import app, db
from app.models import User

@app.route('/')
def index():
    return jsonify({'message': 'Hello, world!'})

@app.route('/users')
def get_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'name': u.name} for u in users])
