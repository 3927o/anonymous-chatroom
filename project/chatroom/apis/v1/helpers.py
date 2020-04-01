from flask import g
from datetime import datetime

from chatroom.models import User, db, VerifyCode
from chatroom.apis.v1.errors import api_abort, NoCurrentUser, VerifyCodeError
from chatroom.apis.v1.schemas import *


def signup(data):
    if User.query.filter_by(username=data['username']).first() is not None:
        return api_abort(401, 'username already exit')
    if User.query.filter_by(phone=data['phone']).first() is not None:
        return api_abort(401, 'phone already register')
    if not validate_code(data['phone'], data['verify_code'], 'create'):
        raise VerifyCodeError
    user = User(data['username'], data['password'], data['phone'])
    db.session.add(user)
    db.session.commit()
    g.current_user = user
    return user_schema(user)


# def login(data):
#     user = User.query.filter_by(username=data['username']).one()
#     if user is None:
#         return api_abort(401, 'user do not exit')
#     if not user.validate_password(data['password']):
#         return api_abort(401, 'wrong password')
#     # login_user(user, remember=data['remember'])
#     g.current_user = user


# @login_required
# def logout():
#     user = current_user
#     logout_user()
#     return user_schema(user)

def user_put(data):  # phone verify
    if g.current_user is None:
        raise NoCurrentUser
    user = g.current_user
    if data['verify_code'] is not None and not validate_code(user.phone, data['verify_code'], 'put'):
        raise VerifyCodeError
    if data['username'] is not None:
        user.username = data['username']
    if data['password'] is not None:
        user.set_password(data['password'])
    if data['phone'] is not None:
        user.phone = data['phone']
    db.session.commit()
    return user_schema(user)


def user_delete(code):  # phone verify
    if g.current_user is None:
        raise NoCurrentUser
    user = g.current_user
    if not validate_code(user.phone, code, 'delete'):
        raise VerifyCodeError
    data = user_schema(user)
    db.session.delete(user)
    db.session.commit()
    return data


def send_message(tel, code):
    from aliyunsdkcore.client import AcsClient
    from aliyunsdkcore.request import CommonRequest
    client = AcsClient('LTAI4Fc1e4iqFFsgt6YRcA1u', 'ON5xaXsAJeiAjWiUlnNVAgdLQZLcx6', 'cn-hangzhou')

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', str(tel))
    request.add_query_param('SignName', "狂野男孩聊天室")
    request.add_query_param('TemplateCode', "SMS_186947418")
    request.add_query_param('TemplateParam', str({'code': code}))

    response = client.do_action_with_exception(request)
    print(str(response, encoding='utf-8'))


def check_time_interval(phone_or_code, interval):
    if type(phone_or_code) is str:
        exit_code = VerifyCode.query.filter_by(phone=phone_or_code).first()
    else:
        exit_code = phone_or_code

    if exit_code is not None:
        time_now = datetime.utcnow()
        if time_now.utcnow().timestamp() - exit_code.create_time.timestamp() > interval:
            return False
    return True


def validate_code(phone, code, type):
    real = VerifyCode.query.filter_by(phone=phone).first()
    if not check_time_interval(real, 300):
        print("TLE")
        return False
    if real is None or real.code != int(code) or real.type != type:
        print(real.code)
        print(code)
        return False
    db.session.delete(real)
    db.session.commit()
    return True
