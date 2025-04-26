import os
from flask import Flask
from models import db
from routes import bp_user
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from datetime import datetime
from flask.json.provider import DefaultJSONProvider
from seeder import seed_database

class DateTimeFormatter(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y/%m/%d %H:%M:%S")
        return super().default(obj)

load_dotenv()

app = Flask(__name__)

jwt = JWTManager()
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.json_provider_class = DateTimeFormatter
app.json = app.json_provider_class(app)

db.init_app(app)
jwt.init_app(app)

app.register_blueprint(bp_user, url_prefix='/api/user')

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        seed_database()
    app.run(port=8000, debug=True)
