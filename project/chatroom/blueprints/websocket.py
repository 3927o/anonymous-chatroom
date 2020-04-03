from flask import g
from flask_socketio import join_room, leave_room, emit

from chatroom.extensions import socketio
from chatroom.models import Message, Room

message_room1 = []
message_room2 = []


@socketio.on('new message')
def new_message(data):
    room = data['room']
    message = str(data['username'] + ' : ' + data['content'])
    if room == 'room1':
        message_room1.append(message)
    else:
        message_room2.append(message)
    emit('new message', message, room=room)


@socketio.on('join')
def join_room(data):
    username = data['username']
    room = data['room']
    join_room(room)
    emit('join_succeed', username+' joined '+room, room=room)


@socketio.on('leave')
def leave_room(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    emit('leave_succeed', username+' leaved '+room, room=room)
