from flask import url_for

# 可尝试使用filed


def make_resp(data, status=200, message='succeed'):
    return {
        'status': status,
        'message': message,
        'data': data
    }


def user_schema(user, tel=True):
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
    return data


def users_schema(users):  # 分页功能
    return {
        'self': url_for('.users'),
        'kind': 'UserList',
        'count': len(users),
        'users': [user_schema(user, tel=False) for user in users]
    }
