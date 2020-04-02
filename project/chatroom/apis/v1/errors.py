from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

from chatroom.apis.v1 import api_v1


def api_abort(code, message=None, **kwargs):
    if message is None:
        message = HTTP_STATUS_CODES.get(code, '')

    response = jsonify(status=code, message=message, **kwargs)
    response.status_code = code
    return response


# def invalid_token():
#     response = api_abort(401, error='invalid_token', error_description='Either the token was expired or invalid.')
#     response.headers['WWW-Authenticate'] = 'Bearer'
#     return response


def token_missing():
    response = api_abort(401)
    response.headers['WWW-Authenticate'] = 'Bearer'
    return response


class NoCurrentUser(Exception):
    pass


@api_v1.errorhandler(NoCurrentUser)
def no_user():
    return api_abort(401, 'no current user')


class InvalidTokenError(Exception):
    pass


@api_v1.errorhandler(InvalidTokenError)
def invalid_token():
    return api_abort(401, 'Either the token was expired or invalid')


# @api_v1.errorhandler(BaseException)
# def base_error(e):
#     return api_abort(500, e.args[0])


class VerifyCodeError(Exception):
    pass


@api_v1.errorhandler(VerifyCodeError)
def invalid_verify_code():
    return api_abort(400, 'wrong verify code')


class ParamError(Exception):
    pass


@api_v1.errorhandler(ParamError)
def param_error(e):
    return api_abort(400, e.args[0])
