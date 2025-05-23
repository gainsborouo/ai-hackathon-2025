import os
from flask import Flask
from flask_cors import CORS
from models import db
from routes import bp_user, bp_ls, bp_watch, bp_comment
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from datetime import datetime, timezone, timedelta
from flask.json.provider import DefaultJSONProvider
from seeder import seed_database

class DateTimeFormatter(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, datetime):
            obj = obj + timedelta(hours=8) # deal with timezone
            return obj.strftime("%Y/%m/%d %H:%M:%S")
        return super().default(obj)

load_dotenv()

app = Flask(__name__)
CORS(app)

jwt = JWTManager()
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.json_provider_class = DateTimeFormatter
app.json = app.json_provider_class(app)

db.init_app(app)
jwt.init_app(app)

app.register_blueprint(bp_user, url_prefix='/api/user')
app.register_blueprint(bp_ls, url_prefix='/api/ls')
app.register_blueprint(bp_watch, url_prefix='/api/watch')
app.register_blueprint(bp_comment, url_prefix='/api/comment')

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        seed_database()
    app.run(port=8000, debug=True)
