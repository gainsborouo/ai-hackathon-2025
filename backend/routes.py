from flask import Blueprint
from controller.user import login, register
from controller.watch_time import start_watching, stop_watching
from controller.comment import post_comment, fetch_comments
from controller.live_streaming import create_ls, end_ls, check_ls

bp_user = Blueprint('bp_user', __name__)
bp_ls = Blueprint('bp_ls', __name__)

bp_user.route('/login', methods=["POST"])(login)
bp_user.route('/register', methods=["POST"])(register)
bp_watch = Blueprint('bp_watch', __name__)
bp_comment = Blueprint('bp_comment', __name__)

bp_ls.route('/create', methods=["POST"])(create_ls)
bp_ls.route('/end/<id>', methods=["PATCH"])(end_ls)
bp_ls.route('/check', methods=["GET"])(check_ls)

bp_watch.route('/<int:live_stream_id>/start', methods=["POST"])(start_watching)
bp_watch.route('/<int:live_stream_id>/stop', methods=["POST"])(stop_watching)
bp_comment.route('/<int:live_stream_id>', methods=["POST"])(post_comment)
bp_comment.route('/<int:live_stream_id>', methods=["GET"])(fetch_comments)
