from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, WatchTime, LiveStreaming, User
from datetime import datetime
from datetime import timedelta

def calculate_credit(duration: timedelta):
    # 每觀看 1 分鐘給 1 credit
    minutes_watched = duration.total_seconds() // 60
    return int(minutes_watched)

@jwt_required()
def start_watching(live_stream_id):
    current_user_id = get_jwt_identity()

    live_stream = LiveStreaming.query.get(live_stream_id)
    if not live_stream:
        return jsonify({"message": "Live stream not found"}), 404

    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    try:
        new_watch_time = WatchTime(
            user_id=current_user_id,
            live_streaming_id=live_stream_id,
            start_time=datetime.utcnow()
        )
        db.session.add(new_watch_time)
        db.session.commit()

        return jsonify({
            "message": "Successfully started watching",
            "watch_time_id": new_watch_time.id,
            "start_time": new_watch_time.start_time
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"Error starting watching: {e}")
        return jsonify({"message": "Failed to start watching"}), 500


@jwt_required()
def stop_watching(live_stream_id):
    current_user_id = get_jwt_identity()

    watch_time_record = WatchTime.query.filter_by(
        user_id=current_user_id,
        live_streaming_id=live_stream_id,
        end_time=None
    ).order_by(WatchTime.start_time.desc()).first()

    if not watch_time_record:
        return jsonify({"message": "Active watch session not found for this stream"}), 404

    try:
        watch_time_record.end_time = datetime.utcnow()

        duration = watch_time_record.end_time - watch_time_record.start_time
        watch_time_record.credit = calculate_credit(duration)

        user = User.query.filter_by(id=current_user_id).first()
        user.credit = user.credit + watch_time_record.credit
        # print("user " + user.name + " credit + " + str(watch_time_record.credit))

        db.session.commit()

        return jsonify({
            "message": "Successfully stopped watching",
            "watch_time_id": watch_time_record.id,
            "end_time": watch_time_record.end_time,
            "credit": watch_time_record.credit
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error stopping watching: {e}")
        return jsonify({"message": "Failed to stop watching"}), 500
