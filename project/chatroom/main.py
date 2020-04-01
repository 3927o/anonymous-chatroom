from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template("socket_test.html")


def ack():
    print
    'message was received!'


@socketio.on('connect')
def connect():
    print('connected')
    i = 0
    while True:
        time.sleep(1)
        i += 1
        emit('response', str(i), namespace='/', callback=ack)


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, port=80, debug=True)
