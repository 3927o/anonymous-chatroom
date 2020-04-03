from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template("socket_test.html")


def ack():
    print('message was received!')


# @socketio.on('connect')
# def connect():
#     print('connected')
#     i = 0
#     # while True:
#     #     time.sleep(1)
#     #     i += 1
#     emit('response', "connected", namespace='/')
#
#
# @socketio.on('disconnect')
# def test_disconnect():
#     print('Client disconnected')


message_room1 = []
message_room2 = []


@socketio.on('new message')
def new_message(data):
    # if type(data) is str:
    #     data = eval(data)
    # print(data['username'])
    print(data)
    print(type(data))
    room = data['room']
    message = str(data['username'] + ' : ' + data['content'])
    if room == 'room1':
        message_room1.append(message)
    else:
        message_room2.append(message)
    emit('new message', message, room=room)


@socketio.on('join')
def join(data):
    print(data)
    print(type(data))
    username = data['username']
    room = data['room']
    join_room(room)
    emit('join_succeed', username+' joined '+room, room=room)


@socketio.on('leave')
def leave(data):
    print(data)
    print(type(data))
    username = data['username']
    room = data['room']
    leave_room(room)
    emit('leave_succeed', username+' leaved '+room, room=room)


if __name__ == '__main__':
    socketio.run(app, port=80, debug=True)
