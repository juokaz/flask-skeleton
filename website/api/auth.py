from flask import request, Response
from flask import has_request_context, _request_ctx_stack
from werkzeug.local import LocalProxy

current_user = LocalProxy(lambda: get_user())


def init(app):
    @app.before_request
    def validate_authentication():
        # if user is logged in or no endpoint is set allow the request
        if request.endpoint is None or request.path == '/' \
                or request.endpoint.find('static') != -1:
            return

        if not current_user.is_authenticated():
            return authenticate()


def get_user():
    if has_request_context() and not hasattr(_request_ctx_stack.top, 'user'):
        load_user()

    return getattr(_request_ctx_stack.top, 'user', None)


def load_user():
    user = parse_auth()
    if user is not None:
        _request_ctx_stack.top.user = user
    else:
        _request_ctx_stack.top.user = AnonymousUser()


class AnonymousUser(object):
    '''
    This is the default object for representing an anonymous user.
    '''
    def is_authenticated(self):
        return False


class User(object):
    '''
    This is the default object for representing a loggedin user.
    '''
    def is_authenticated(self):
        return True


def parse_auth():
    # TODO: implement actual api key lookup logic
    auth = request.authorization

    if not auth:
        return None

    username = auth.username
    token = auth.password

    if username != 'usr' and token != 'psw':
        return None

    api_key = User()
    return api_key


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})
