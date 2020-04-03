from flask import Flask
import os

from chatroom.extensions import db, avatars, socketio
from chatroom.settings import config
from chatroom.apis.v1 import api_v1


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    db.init_app(app)
    avatars.init_app(app)
    socketio.init_app(app)


def register_blueprints(app):
    app.register_blueprint(api_v1)


app = create_app('testing')
context = app.test_request_context()
context.push()
db.create_all()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
