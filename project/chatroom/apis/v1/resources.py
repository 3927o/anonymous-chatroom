from flask_restful import Api, Resource
from flask import jsonify, request, g
from datetime import datetime
import random

from chatroom.models import User, Message, Room, VerifyCode
# from chatroom.apis.v1 import api_v1
from chatroom.apis.v1.errors import api_abort, InvalidTokenError
from chatroom.apis.v1.schemas import *
from chatroom.apis.v1.reqparses import *
from chatroom.apis.v1.helpers import *
from chatroom.apis.v1.auth import generate_token, auth_required, validate_token


class IndexAPI(Resource):

    def get(self):
        pass


class AuthTokenAPI(Resource):

    def post(self):
        action = request.args.get('action', None)
        # validate password or refresh_token before generate token
        if action == 'get' or action is None:
            data = token_get_reqparse.parse_args()
            user = User.query.filter_by(username=data['username']).first()
            if user is None or not user.validate_password(data['password']):
                return api_abort(code=401, message='Either the username or password was invalid.')
            g.current_user = user
        elif action is 'refresh':  # https://www.jianshu.com/p/25ab2f456904
            data = token_refresh_reqparse.parse_args()
            if not validate_token(data['refresh_token']):
                raise InvalidTokenError
        else:
            return api_abort(401, 'unknown action')

        data = generate_token(g.current_user)

        response = jsonify(data)
        response.headers['Cache-Control'] = 'no-store'
        response.headers['Pragma'] = 'no-cache'
        return response


class UserAPI(Resource):

    decorators = [auth_required]

    def get(self, id):
        user = User.query.get(id)
        if user is None:
            return api_abort(422, 'user do not exit')
        if g.current_user.id != id:
            return api_abort(403, 'permission denied')
        return make_resp(user_schema(user))

    def put(self, id):
        data = user_put_reqparse.parse_args()
        if data['verify_code'] is None:
            if data['password'] is not None or data['phone'] is not None:
                return api_abort(400, 'verify code is needed')
        data = user_put(data)
        return make_resp(data=data)

    def delete(self, id):
        code = request.args.get('verify_code', None)
        data = user_delete(code)
        return make_resp(data)


class UserListAPI(Resource):

    def get(self):
        users = User.query.all()
        data = users_schema(users)
        return make_resp(data)

    def post(self):  # 采用参数确定是注册，登录，登出
        data = signup_reqparse.parse_args()
        code = VerifyCode.query.filter_by(phone=data['phone']).first()
        data = signup(data)
        return make_resp(data)


class MessageAPI(Resource):

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


class MessageListAPI(Resource):  # 采用参数的方式获取某一房间的消息

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


class RoomAPI(Resource):

    def get(self):
        pass

    def put(self):  # 采用装饰器确认是否有权限
        pass

    def delete(self):
        pass


class RoomListAPI(Resource):

    def get(self):
        pass

    def post(self):
        pass


class VerifyCodeAPI(Resource):

    def get(self):
        action = request.args.get('action', None)
        phone = request.args.get('phone', None)
        if action is None or phone is None:
            return api_abort(400, 'action and phone is needed')
        code = random.randint(100001, 999999)

        if not check_time_interval(phone, 60):
            return api_abort(400, 'permission denied')

        send_message(phone, code)
        new_code = VerifyCode(code, phone, action)
        db.session.add(new_code)
        db.session.commit()
        return make_resp({})


# api = Api(api_v1)
# api.add_resource(IndexAPI, '/', endpoint='index')
# api.add_resource(UserAPI, '/user/<int:id>', endpoint='user')
# api.add_resource(MessageAPI, '/message/<string:id>', endpoint='message')
# api.add_resource(RoomAPI, '/room/<string:id>', endpoint='room')
# api.add_resource(UserListAPI, '/user/', endpoint='users')
# api.add_resource(MessageListAPI, '/message/', endpoint='messages')
# api.add_resource(RoomListAPI, '/room/', endpoint='rooms')
# api.add_resource(AuthTokenAPI, '/token/', endpoint='token')
