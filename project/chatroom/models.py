from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid1
from datetime import datetime

from chatroom.extensions import db

assist_table = db.Table('association',
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                        db.Column('room_id', db.String(36), db.ForeignKey('room.id')))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    username = db.Column(db.String(10), unique=True, index=True)
    register_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated = db.Column(db.DateTime, default=datetime.utcnow())
    password_hash = db.Column(db.String(128))
    phone = db.Column(db.String(30), unique=True)  # 添加短信验证和格式验证
    messages = db.relationship('Message', back_populates='author', cascade='all')
    # rooms_owned = 1
    avatar = 1
    rooms = db.relationship('Room',
                            secondary=assist_table,
                            back_populates='users')

    def set_avatar(self, file):
        pass

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, username, password, phone):
        self.username = username
        self.set_password(password)
        # if validate_phone(phone):
        #     self.phone = phone
        self.phone = phone


class Room(db.Model):
    id = db.Column(db.String(36), primary_key=True, index=True)
    name = db.Column(db.String(20), unique=True, index=True)
    introduce = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    updated = db.Column(db.DateTime, default=datetime.utcnow())
    messages = db.relationship('Message', back_populates='room', cascade='all')
    # owner_id = 1
    # owner = 1
    users = db.relationship('User',
                            secondary=assist_table,
                            back_populates='rooms')
    avatar = 1

    def set_avatar(self, file):
        pass

    def __init__(self, name, introduce=None):
        self.id = str(uuid1())
        self.name = name
        if introduce is None:
            self.introduce = ' '
        else:
            self.introduce = introduce


class Message(db.Model):
    id = db.Column(db.String(36), primary_key=True, index=True)
    content = db.Column(db.Text, index=True)
    timestamp = db.Column(db.DateTime)
    updated = db.Column(db.DateTime, default=datetime.utcnow())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    room_id = db.Column(db.String(36), db.ForeignKey('room.id'), index=True)
    author = db.relationship('User', back_populates='messages')
    room = db.relationship('Room', back_populates='messages')

    def __init__(self, content, author_id, room_id):
        self.id = str(uuid1())
        self.content = content
        self.author_id = author_id
        self.room_id = room_id
        self.timestamp = datetime.utcnow()
        # self.author_id = g.user.id


class VerifyCode(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    code = db.Column(db.Integer)
    phone = db.Column(db.String(30))
    type = db.Column(db.String(10))
    create_time = db.Column(db.DateTime, default=datetime.utcnow())
    expiration = db.Column(db.Integer, default=300)

    def __init__(self, code, phone, type):
        self.id = str(uuid1())
        self.phone = phone
        self.type = type
        self.code = code


# @db.event.listens_for(Room, 'set')
# @db.event.listens_for(Message, 'set')
# @db.event.listens_for(User, 'set')
def update_time(target, value, oldvalue, initiator):
    target.updated = datetime.utcnow()


db.event.listen(Room.name, 'set', update_time)
db.event.listen(Room.introduce, 'set', update_time)
db.event.listen(User.username, 'set', update_time)
db.event.listen(User.password_hash, 'set', update_time)
db.event.listen(User.phone, 'set', update_time)
db.event.listen(Message.content, 'set', update_time)
