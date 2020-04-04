from flask_restful import reqparse

signup_reqparse = reqparse.RequestParser()
signup_reqparse.add_argument('username', type=str, required=True, location='json')
signup_reqparse.add_argument('password', type=str, required=True, location='json')
signup_reqparse.add_argument('phone', type=str, required=True, location='json')
signup_reqparse.add_argument('verify_code', type=str, required=True, location='json')

token_get_reqparse = reqparse.RequestParser()  # 如果action是refresh的话密码是非必要的，在生成token前验证
token_refresh_reqparse = reqparse.RequestParser()
# token_get_reqparse.add_argument('action', type=str, required=True, location='json')
token_get_reqparse.add_argument('username', type=str, required=True, location='json')
token_get_reqparse.add_argument('password', type=str, required=True, location='json')
token_refresh_reqparse.add_argument('refresh_token', type=str, required=True, location='json')

user_put_reqparse = reqparse.RequestParser()
user_put_reqparse.add_argument('username', type=str, location='json')
user_put_reqparse.add_argument('password', type=str, location='json')
user_put_reqparse.add_argument('phone', type=str, location='json')
user_put_reqparse.add_argument('verify_code', type=str, location='json')
user_put_reqparse.add_argument('room', type=dict, location='json')

room_post_reqparse = reqparse.RequestParser()
room_post_reqparse.add_argument('name', type=str, location='json', required=True)
room_post_reqparse.add_argument('introduce', type=str, location='json')

room_put_reqparse = reqparse.RequestParser()
room_put_reqparse.add_argument('name', type=str, location='json')
room_put_reqparse.add_argument('introduce', type=str, location='json')

message_post_reqparse = reqparse.RequestParser()
message_post_reqparse.add_argument('content', type=str, required=True, location='json')

message_put_reqparse = reqparse.RequestParser()
message_put_reqparse.add_argument('content', type=str, required=True, location='json')