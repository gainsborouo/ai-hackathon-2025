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
import requests
from flask_socketio import SocketIO
from voice.voice import VoiceAssistant

assistant = VoiceAssistant()

class DateTimeFormatter(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, datetime):
            obj = obj + timedelta(hours=8) # deal with timezone
            return obj.strftime("%Y/%m/%d %H:%M:%S")
        return super().default(obj)

load_dotenv()

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*', binary=True)

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

def audio_source(ssml_text):
    # 靜音保活：前 100ms 傳送 20ms 全零 PCM
    silence = b'\x00' * (16000 * 2 * 0.02)
    for _ in range(5):
        yield silence

    stream = assistant.toPolly(ssml_text)
    chunk = stream.read(4096)  # 每次讀 4KB PCM :contentReference[oaicite:4]{index=4}
    while chunk:
        yield chunk
        chunk = stream.read(4096)

@socketio.on('start')
def streaming():
    SIMLI_API_KEY = os.getenv('SIMLI_API_KEY')
    SIMLI_BASE = os.getenv('SIMLI_BASE')
    SIMLI_FACE_ID = os.getenv('SIMLI_FACE_ID')

    question = request.get_json().get('question')
    ssml_output = assistant.toBedrock(data['text'])
    
    headers = {'Authorization': f'Bearer {SIMLI_API_KEY}'}
    requests.post(f"{SIMLI_BASE}/startAudioToVideoSession",
        headers=headers,
        json={'faceId':{SIMLI_FACE_ID},'syncAudio':True}
    ).raise_for_status()
    
    with requests.post(
        f"{SIMLI_BASE}/audioToVideoStream",
        headers=headers,
        data=audio_source(ssml),
        stream=True
    ) as resp:
        resp.raise_for_status()
        for vchunk in resp.iter_content(chunk_size=4096):
            if vchunk:
                socketio.emit('video-chunk', vchunk)  

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        seed_database()
    app.run(port=8000, debug=True)
