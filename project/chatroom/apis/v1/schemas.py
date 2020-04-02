from flask import url_for, jsonify

# 可尝试使用filed


def make_resp(data, status=200, message='succeed'):
    resp = jsonify({
        'status': status,
        'message': message,
        'data': data
    })
    resp.status_code = status
    return resp


def user_schema(user, tel=True, messages=True, rooms=True):
    data = {
        'id': user.id,
        'self': url_for('.user', id=user.id, _external=True),
        'kind': 'user',
        'username': user.username,
        'register_at': str(user.register_at),
        'updated': str(user.updated)
    }
    if tel:
        data['tel'] = user.phone
    if messages:
        data['messages'] = messages_schema(user.messages)
    if rooms:
        data['rooms'] = rooms_schema(user.rooms)
    return data


def users_schema(users):  # 分页功能
    return {
        'self': url_for('.users'),
        'kind': 'UserList',
        'count': len(users),
        'users': [user_schema(user, False, False, False) for user in users]
    }


def room_schema(room, users=True, messages=True):
    data = {
        'id': room.id,
        'self': url_for('.room', id=room.id, _external=True),
        'kind': 'room',
        'name': room.name,
        'introduce': room.introduce,
        'owner': {
            'name': room.owner.username,
            'url': url_for('.user', id=room.owner.id, _external=True)
        },
        'created_at': str(room.timestamp),
        'updated_at': str(room.updated)
    }
    if users:
        data['users'] = users_schema(room.users)
    if messages:
        data['messages'] = messages_schema(room.messages)
    return data


def rooms_schema(rooms):
    return {
        'self': url_for('.rooms'),
        'kind': 'RoomList',
        'count': len(rooms),
        'rooms': [room_schema(room, users=False, messages=False) for room in rooms]
    }


def message_schema(message):
    return {
        'id': message.id,
        'self': url_for('.message', id=message.id, _external=True),
        'kind': "message",
        'content': message.content,
        'author': user_schema(message.author, False, False, False),
        'room': room_schema(message.room, False, False),
        'created_at': str(message.timestamp),
        'updated_at': str(message.updated)
    }


def messages_schema(messages):
    return {
        'self': url_for('.messages'),
        'kind': 'MessageList',
        'count': len(messages),
        'messages': [message_schema(message) for message in messages]
    }
