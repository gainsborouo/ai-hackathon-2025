from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, LiveStreaming, User, RoleEnum
from datetime import datetime

@jwt_required()
def create_ls():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user or user.role != RoleEnum.IDOL:
        return jsonify({"error": "access denied"}), 403

    data = request.get_json() or {}
    fans_class = data.get("fans_class")
    title = data.get("title")
    if fans_class is None or title is None:
        return jsonify({"error": "validation fail"}), 400

    ls = LiveStreaming(
        fans_class=fans_class,
        title=title,
        initiator_id=user.id,
    )
    db.session.add(ls)
    db.session.commit()

    # TODO: do sth else to stream video

    return jsonify({
        "id": ls.id,
        "fans_class": ls.fans_class,
        "initiator_id": ls.initiator_id,
        "start_time": ls.start_time,
    }), 201

@jwt_required()
def end_ls(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user or user.role != RoleEnum.IDOL:
        return jsonify({"error": "access denied"}), 403

    ls = LiveStreaming.query.get(id)
    if not ls:
        return jsonify({"error": "Resource not found"}), 404
    if ls.initiator_id != user.id:
        return jsonify({"error": "Cannot end a stream you did not start"}), 403

    ls.end_time = datetime.utcnow()
    db.session.commit()

    return jsonify({
        "id": ls.id,
        "end_time": ls.end_time
    }), 200

def check_ls():
    now = datetime.utcnow()
    ls = LiveStreaming.query.filter(
        LiveStreaming.end_time.is_(None),
        LiveStreaming.start_time <= now
    ).first()
    if not ls:
        return jsonify({}), 200
    return jsonify({
        "id": ls.id,
        "fans_class": ls.fans_class,
        "title": ls.title,
        "initiator_id": ls.initiator_id,
        "start_time": ls.start_time
    }), 200
