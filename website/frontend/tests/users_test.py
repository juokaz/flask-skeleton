from . import TestCase

from flask import url_for

from .. import db
from ...models import User


class UsersTest(TestCase):
    render_templates = False

    def test_list_users(self):
        u = User()
        u.id = 2
        u.email = "user2@example.com"
        db.session.add(u)

        self.as_user('get', url_for("users.index"))

        users = self.get_context_variable("users")
        self.assertEqual(2, users.total)
        self.assertEqual(u, users.items[0])

    def test_add_user(self):
        data = {"email": "user2@example.com"}
        self.as_user('post', url_for("users.add"), data=data)

        user = User.query.get(2)

        self.assertEqual("user2@example.com", user.email)
        self.assertEqual(True, user.active)
        self.assertEqual(False, user.confirmed)

    def test_add_user_duplicate_email(self):
        data = {"email": "user@example.com"}
        self.as_user('post', url_for("users.add"), data=data)

        user = User.query.get(2)

        self.assertEqual(None, user)

    def test_edit_user(self):
        data = {"email": "usernew@example.com"}
        self.as_user('post', url_for("users.edit", id=1), data=data)

        user = User.query.get(1)

        self.assertEqual("usernew@example.com", user.email)

    def test_delete_user(self):
        self.as_user('post', url_for("users.delete", id=1))

        user = User.query.get(1)

        self.assertEqual(False, user.active)

    def test_settings_user(self):
        data = {"email": "usernew@example.com", "update_user": ''}
        self.as_user('post', url_for("users.settings"), data=data)

        user = User.query.get(1)

        self.assertEqual("usernew@example.com", user.email)

    def test_settings_password(self):
        data = {"current": "password", "password": "passwordnew",
                "change_password": ''}
        self.as_user('post', url_for("users.settings"), data=data)

        user = User.query.get(1)

        self.assertTrue(user.check_password("passwordnew"))

    def test_settings_password_wrong_current(self):
        data = {"current": "p2323assword", "password": "passwordnew",
                "change_password": ''}
        self.as_user('post', url_for("users.settings"), data=data)

        user = User.query.get(1)

        self.assertFalse(user.check_password("passwordnew"))
