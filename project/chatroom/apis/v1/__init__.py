from flask import Blueprint
from flask_restful import Api
from flask_cors import CORS

api_v1 = Blueprint('api_v1', __name__)
CORS(api_v1)
api = Api(api_v1)

# lm = LoginManager(api_v1)
# lm.login_message = 'please login'
#
#
# @lm.user_loader
# def load_user(id):
#     return User.query.get(id)

from chatroom.apis.v1.resources import UserAPI, MessageAPI, RoomAPI, UserListAPI, MessageListAPI, \
    RoomListAPI, IndexAPI, AuthTokenAPI, VerifyCodeAPI

api.add_resource(IndexAPI, '/', endpoint='index')
api.add_resource(UserAPI, '/user/<int:id>', endpoint='user')
api.add_resource(MessageAPI, '/message/<string:id>', endpoint='message')
api.add_resource(RoomAPI, '/room/<string:id>', endpoint='room')
api.add_resource(UserListAPI, '/user/', endpoint='users')
api.add_resource(MessageListAPI, '/message/', endpoint='messages')
api.add_resource(RoomListAPI, '/room/', endpoint='rooms')
api.add_resource(AuthTokenAPI, '/auth/token/', endpoint='token')
api.add_resource(VerifyCodeAPI, '/auth/verify_code/', endpoint='verify_code')
