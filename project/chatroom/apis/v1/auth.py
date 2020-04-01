from functools import wraps

from flask import g, current_app, request
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from chatroom.models import User
from chatroom.apis.v1.errors import api_abort, token_missing, InvalidTokenError


def generate_token(user):
    expiration_access = 3600
    expiration_refresh = 3600 * 24 * 7

    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration_access)
    access_token = s.dumps({'id': user.id, 'type': 'access_token'}).decode('ascii')

    # even if the action is 'refresh', generate new refresh token
    s_refresh = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration_refresh)
    refresh_token = s_refresh.dumps({'id': user.id, 'type': 'refresh_token'}).decode('ascii')

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'expiration_access': expiration_access,
        'expiration_refresh': expiration_refresh
    }


def validate_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.load(token)
    except (BadSignature, SignatureExpired):
        return False
    user = User.query.get(data['id'])
    if user is None:
        return False
    g.current_user = user
    return True


def get_token():
    if 'Authorization' in request.headers:
        try:
            token_type, token = request.headers['Authorization'].split(None, 1)
        except ValueError:
            # The Authorization header is either empty or has no token
            token_type = token = None
    else:
        token_type = token = None
    return token_type, token


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token_type, token = get_token()

        # Flask normally handles OPTIONS requests on its own, but in the
        # case it is configured to forward those to the application, we
        # need to ignore authentication headers and let the request through
        # to avoid unwanted interactions with CORS.
        if request.method != 'OPTIONS':
            if token_type is None:
                return api_abort(400, 'token missing')
            if token_type.lower() != 'bearer':
                return api_abort(400, 'The token type must be bearer.')
            if token is None:
                return token_missing()
            if not validate_token(token):
                raise InvalidTokenError
        return f(*args, **kwargs)

    return decorated
