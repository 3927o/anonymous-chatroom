from flask_sqlalchemy import SQLAlchemy
from flask_avatars import Avatars
from flask_socketio import SocketIO

db = SQLAlchemy()
avatars = Avatars()
socketio = SocketIO()
