from flask_sqlalchemy import SQLAlchemy
from flask_avatars import Avatars
from flask_socketio import SocketIO, emit, leave_room
from flask import g, url_for

db = SQLAlchemy()
avatars = Avatars()
socketio = SocketIO()


@socketio.on('disconnect')
def disconnect():
    user = g.current_user
    leave_room(user.room.name)
    emit('leave room', user_schema(user), room=user.room.name)
    user.room = None


def user_schema(user):
    data = {
        'id': user.id,
        'self': url_for('.user', id=user.id, _external=True),
        'kind': 'user',
        'username': user.username,
        'register_at': str(user.register_at),
        'updated': str(user.updated)
    }
    return data
