from flask import Blueprint
from controller.user import login, register

bp_user = Blueprint('bp_user', __name__)

bp_user.route('/login', methods=["POST"])(login)
bp_user.route('/register', methods=["POST"])(register)