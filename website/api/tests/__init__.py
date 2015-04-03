from ...tests import TestCase
from .. import app

import base64
import json


class TestCase(TestCase):
    def create_app(self):
        app.config.from_object('website.settings.TestConfig')
        return app

    def as_user(self, method_name, *args, **kwargs):
        auth = 'user:psw'

        return self._get(auth, method_name, *args, **kwargs)

    def _get(self, auth, method_name, *args, **kwargs):

        if 'data' in kwargs:
            kwargs['data'] = json.dumps(kwargs['data'])
            kwargs['content_type'] = 'application/json'

        method = getattr(self.client, method_name)
        response = method(*args, headers=self.get_auth_header(auth), **kwargs)

        return response

    def get_auth_header(self, auth):
        header = b'Basic ' + base64.b64encode(auth.encode('ascii')),
        auth_headers = {
            'AUTHORIZATION': header
        }

        return auth_headers
