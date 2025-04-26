from flask import request, jsonify, render_template
from models import db, User

def init_routes(app):
    @app.route('/', methods=['GET'])
    def index():
        return jsonify({"data": "hello, world!"})

    @app.route('/users', methods=['GET'])
    def list_users():
        users = User.query.all()
        return jsonify([{'id': u.id, 'name': u.name} for u in users])

    @app.route('/users', methods=['POST'])
    def add_user():
        data = request.get_json() or {}
        if not data.get('name'):
            return jsonify({'error': 'name required'}), 400
        user = User(name=data['name'])
        db.session.add(user)
        db.session.commit()
        return jsonify({'id': user.id, 'name': user.name}), 201
