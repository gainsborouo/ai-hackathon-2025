from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Enum as SQLEnum, ForeignKey

db = SQLAlchemy()

class RoleEnum(PyEnum):
    FANS = "fans"
    IDOL = "idol"

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    avatar = db.Column(db.Integer, nullable=False, default=1)
    fan_class = db.Column(db.Integer, nullable=False, default=1)
    credit = db.Column(db.Integer, nullable=False, default=0)
    role = db.Column(SQLEnum(RoleEnum, name="role_enum"), nullable=False, default=RoleEnum.FANS, server_default=RoleEnum.FANS.value)
    join_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    comments = db.relationship(
        'Comment',
        back_populates='user',
        cascade='all, delete-orphan',
        lazy='selectin'
    )


class LiveStreaming(db.Model):
    __tablename__ = 'live_streamings'
    id = db.Column(db.Integer, primary_key=True)
    fans_class = db.Column(db.Integer, nullable=False, default=1)
    title = db.Column(db.String(255), nullable=False)
    initiator_id = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)

class WatchTime(db.Model):
    __tablename__ = 'watch_times'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    live_streaming_id = db.Column(db.Integer, ForeignKey('live_streamings.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    credit = db.Column(db.Integer, nullable=False, default=1)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    live_streaming_id = db.Column(db.Integer, ForeignKey('live_streamings.id'), nullable=False)
    is_question = db.Column(db.Boolean, nullable=False, default=False)
    comment = db.Column(db.Text, nullable=False)
    priority = db.Column(db.Integer, nullable=False, default=0)
    answered = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # 新增

    user = db.relationship(
        'User',
        back_populates='comments'
    )