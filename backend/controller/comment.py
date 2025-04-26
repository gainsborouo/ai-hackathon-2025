# controller/comment.py
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Comment, LiveStreaming
from datetime import datetime

@jwt_required()
def post_comment():
    """
    發布留言
    Body JSON: { "comment": "...", "is_question": true/false }
    """
    data = request.get_json(silent=True) or {}
    content = data.get("comment", "").strip()
    print(content)
    if not content:
        return jsonify({"msg": "留言內容不可為空"}), 400

    ls = get_current_ls()
    if not ls:
        return jsonify({"message": "No live streaming is being held"}), 404
    live_stream_id = ls.id
    new_comment = Comment(
        user_id=get_jwt_identity(),
        live_streaming_id=live_stream_id,
        comment=content,
        is_question=data.get("is_question", False),
    )
    db.session.add(new_comment)
    db.session.commit()

    return jsonify({"msg": "OK"}), 201


def fetch_comments():
    """
    取得該直播的全部留言（按留言時間排序）
    """
    ls = get_current_ls()
    if not ls:
        return jsonify({"message": "No live streaming is being held"}), 404
    live_stream_id = ls.id
    comments = (Comment.query
                .filter_by(live_streaming_id=live_stream_id)
                .order_by(Comment.id.asc())    # 這裡用 id 當排序（如果想要 created_at 再補欄位）
                .all())

    comment_list = []
    for c in comments:
        user = c.user
        comment_list.append({
            "id": c.id,
            "username": user.name,
            "user_avatar": user.avatar,
            "live_streaming_id": c.live_streaming_id,
            "comment": c.comment,
            "is_question": c.is_question,
            "priority": c.priority,
            "answered": c.answered,
            # 如果你有 `created_at` 欄位再加，這裡不會爆錯
            "created_at": c.created_at.strftime("%Y/%m/%d %H:%M:%S") if hasattr(c, "created_at") and c.created_at else None
        })

    return jsonify(comment_list), 200

def get_current_ls():
    now = datetime.utcnow()
    ls = LiveStreaming.query.filter(
        LiveStreaming.end_time.is_(None),
        LiveStreaming.start_time <= now
    ).first()
    return ls
