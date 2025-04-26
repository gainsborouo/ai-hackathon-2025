from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Enum as SQLEnum

db = SQLAlchemy()

class RoleEnum(PyEnum):
    FANS = "fans"
    IDOL = "idol"

class User(db.Model):
    __tablename__ = 'users'
    id   = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    avatar = db.Column(db.Integer, nullable=False, default=1)
    fan_class = db.Column(db.Integer, nullable=False, default=1)
    credit = db.Column(db.Integer, nullable=False, default=0)
    role = db.Column(
        SQLEnum(RoleEnum, name="role_enum"),
        nullable=False,
        default=RoleEnum.FANS,
        server_default=RoleEnum.FANS.value
    )
    join_time  = db.Column(
        db.DateTime, 
        nullable=False, 
        default=datetime.utcnow
    )

    def __repr__(self):
        return f'<User {self.name}>'