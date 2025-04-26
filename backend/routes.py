from flask import Blueprint
from controller.user import login, register
from controller.live_streaming import create_ls, end_ls, check_ls

bp_user = Blueprint('bp_user', __name__)
bp_ls = Blueprint('bp_ls', __name__)

bp_user.route('/login', methods=["POST"])(login)
bp_user.route('/register', methods=["POST"])(register)

bp_ls.route('/create', methods=["POST"])(create_ls)
bp_ls.route('/end/<id>', methods=["PATCH"])(end_ls)
bp_ls.route('/check', methods=["GET"])(check_ls)
