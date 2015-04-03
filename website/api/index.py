from flask import url_for
from flask.ext.restful import Resource
from .auth import current_user


class Index(Resource):
    def get(self):
        response = {'hello': 'world'}
        if current_user.is_authenticated():
            links = {}
            links['users'] = {'href': url_for('users')}
            response['_links'] = links
        return response
