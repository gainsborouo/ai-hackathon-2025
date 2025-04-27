from models import db, User, RoleEnum, WatchTime, Comment, LiveStreaming
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
import random

bcrypt = Bcrypt()

def seed_database():
    idol = User (
        email="fenix@gmail.com",
        password=bcrypt.generate_password_hash("hi").decode("utf-8"),
        name="FEniX",
        role=RoleEnum.IDOL,
        avatar=6
    )
    fans = []
    for i in range(5):
        fans.append(User(
            email="user" + str(i) + "@gmail.com",
            password=bcrypt.generate_password_hash("hi").decode("utf-8"),
            name="user" + str(i),
            role=RoleEnum.FANS
        ))

    fans[0].fan_class = 2
    fans[1].fan_class = 3
    db.session.add_all([idol] + fans)
    db.session.commit()

    now = datetime.utcnow()
    ls_start = now - timedelta(minutes=150)
    ls_end = now - timedelta(minutes=20)
    ls = LiveStreaming(
        fans_class=1,
        initiator_id=idol.id,
        title="Late-Night Chat Session",
        start_time=ls_start,
        end_time=ls_end
    )
    db.session.add(ls)
    db.session.commit()

    watch_times = []
    for fan in fans:
        start_time = ls_start + timedelta(minutes=random.randint(0, 10))
        end_time = ls_start + timedelta(minutes=random.randint(15, 100))
        credit = int((end_time - start_time).total_seconds() // 60)
        wt = WatchTime(
            user_id=fan.id,
            live_streaming_id=ls.id,
            start_time=start_time,
            end_time=end_time,
            credit=credit
        )
        watch_times.append(wt)
        fan.credit += credit
    db.session.add_all(watch_times)
    db.session.commit()

    comments = []
    comments.append(Comment(
        user_id=2,
        live_streaming_id=ls.id,
        is_question=True,
        comment="How are you today?",
        priority=2,
    ))
    comments.append(Comment(
        user_id=5,
        live_streaming_id=ls.id,
        is_question=True,
        comment="Do you like cat?",
        priority=4,
    ))
    comments.append(Comment(
        user_id=3,
        live_streaming_id=ls.id,
        comment="Do you wanna build a snowman?",
        priority=3,
    ))
    db.session.add_all(comments)
    db.session.commit()