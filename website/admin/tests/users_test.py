from . import TestCase

from flask import url_for

from .. import db
from ...models import User


class UsersTest(TestCase):
    render_templates = False

    def test_list_users(self):
        u = self._create_user()

        self.as_admin('get', url_for("users.index"))

        users = self.get_context_variable("users")
        self.assertEqual(1, users.total)
        self.assertEqual(u, users.items[0])

    def test_edit_user(self):
        u = self._create_user()

        data = {"email": "usernew@example.com"}
        self.as_admin('post', url_for("users.edit", id=u.id), data=data)

        self.assertEquals("usernew@example.com", u.email)

    def test_add_user(self):
        data = {"email": "user@example.com"}
        self.as_admin('post', url_for("users.add"), data=data)

        user = User.query.get(1)

        self.assertEqual("user@example.com", user.email)
        self.assertTrue(user.confirmed)
        self.assertTrue(user.active)
        self.assertTrue(user.password is not None)

    def test_add_user_duplicate_email(self):
        self._create_user()

        data = {"email": "user@example.com"}
        self.as_admin('post', url_for("users.add"), data=data)

        user = User.query.get(2)

        self.assertEqual(None, user)

    def test_delete_user(self):
        self._create_user()

        self.as_admin('post', url_for("users.delete", id=1))

        self.assertEquals(None, User.query.get(1))

    def _create_user(self):
        u = User()
        u.id = 1
        u.email = "user@example.com"
        db.session.add(u)

        return u
