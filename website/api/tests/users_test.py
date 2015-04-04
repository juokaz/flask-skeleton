from . import TestCase

from flask import url_for

from .. import db
from ...models import User


class UsersTest(TestCase):
    render_templates = False

    def test_list_users(self):
        self._create_user()

        response = self.as_user('get', url_for("users"))

        self.assertEquals(1, len(response.json['_embedded']['users']))

    def test_view_user(self):
        self._create_user()

        response = self.as_user('get', url_for("user", id=1))

        self.assertEquals("user@example.com", response.json['email'])

    def test_add_user(self):
        data = {'email': 'user@example.com'}

        self.as_user('post', url_for("users"), data=data)

        u = User.query.get(1)

        self.assertEquals('user@example.com', u.email)

    def test_add_user_invalid(self):
        data = {}
        response = self.as_user('post', url_for("users"), data=data)

        self.assert400(response)
        message = "Error in the email field - This field is required."
        self.assertEquals(message, response.json['message'])

    def test_edit_user(self):
        u = self._create_user()

        data = {'email': 'user@example.com', 'first_name': 'Fist Name'}

        self.as_user('put', url_for("user", id=1), data=data)

        self.assertEquals('Fist Name', u.first_name)

    def test_delete_user(self):
        u = self._create_user()

        self.as_user('delete', url_for("user", id=1))

        self.assertEqual(False, u.active)

    def _create_user(self):
        u = User()
        u.id = 1
        u.email = "user@example.com"
        u.password = "Password"
        u.type = "manufacturer"
        u.manufacturer_id = 1
        db.session.add(u)

        return u
