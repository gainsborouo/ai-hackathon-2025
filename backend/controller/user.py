from flask import jsonify, request
from flask_bcrypt import Bcrypt
from models import User, db
from flask_jwt_extended import create_access_token

bcrypt = Bcrypt()

def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400
    
    user = User.query.filter_by(email=email).first()
    if user is None or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "invalid credentials"}), 401
    
    additional_claims = { 
        "id": user.id, 
        "email": user.email,
        "name": user.name,
        "avatar": user.avatar,
        "class": user.fan_class,
        "credit": user.credit,
        "role": user.role.value,
    }
    token = create_access_token(identity=str(user.id), additional_claims=additional_claims)
    return jsonify({
        "token": token,
    }), 200

def register():
    data = request.get_json() or {}
    
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")
    avatar = data.get("avatar")

    if not email or not password:
        return jsonify({"error": "email and password required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "email already exists"}), 409

    pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(email=email, password=pw_hash, name=name, avatar=avatar)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "id": user.id, 
        "email": user.email,
        "name": user.name,
        "avatar": user.avatar,
        "class": user.fan_class,
        "credit": user.credit,
        "join_time": user.join_time,
        "role": user.role.value
    }), 201