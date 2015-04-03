from . import TestCase

from ..auth import current_user


class AuthTest(TestCase):
    render_templates = False
    protected = '/protected'

    def test_protected(self):
        response = self.client.get(self.protected)

        self.assert401(response)

    def test_login(self):
        auth_headers = self.get_auth_header('usr:psw')

        with self.client as c:
            response = c.get(self.protected, headers=auth_headers)

            self.assert200(response)
            self.assertTrue(current_user.is_authenticated())

    def test_wrong_api_key(self):
        auth_headers = self.get_auth_header('csanslcka:666')

        response = self.client.get(self.protected, headers=auth_headers)

        self.assert401(response)
