from . import TestCase

from flask import url_for, session

from .. import db
from ...models import Admin


class AuthTest(TestCase):
    render_templates = False

    def test_login(self):
        self._create_admin()

        with self.client as c:
            data = {"email": "user@example.com", "password": "Password"}
            c.post(url_for("auth.login"), data=data)

            self.assertTrue('user_id' in session)
            self.assertEqual(1, session['user_id'])

    def test_login_wrong_email(self):
        self._create_admin()

        with self.client as c:
            data = {"email": "csacsa@example.com", "password": "Password"}
            c.post(url_for("auth.login"), data=data)

            self.assertFalse('user_id' in session)

    def test_login_wrong_password(self):
        self._create_admin()

        with self.client as c:
            data = {"email": "user@example.com", "password": "Passwordacscas"}
            c.post(url_for("auth.login"), data=data)

            self.assertFalse('user_id' in session)

    def test_logout(self):
        self._create_admin()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1
                sess['_fresh'] = True
            c.get(url_for("auth.logout"))

            self.assertFalse('user_id' in session)

    def test_settings(self):
        u = self._create_admin()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1
                sess['_fresh'] = True

            data = {"current": "Password", "password": "passwordnew"}
            c.post(url_for("auth.settings"), data=data)

            self.assertTrue(u.check_password('passwordnew'))

    def test_settings_wrong_current_password(self):
        u = self._create_admin()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1
                sess['_fresh'] = True

            data = {"current": "paassword", "password": "passwordnew"}
            c.post(url_for("auth.settings"), data=data)

            self.assertFalse(u.check_password('passwordnew'))

    def _create_admin(self):
        u = Admin()
        u.email = "user@example.com"
        u.password = "Password"
        db.session.add(u)

        return u
