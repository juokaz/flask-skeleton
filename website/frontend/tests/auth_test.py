from . import TestCase

from flask import url_for, session

from .. import db
from ...services import security_service
from ...models import User


class AuthTest(TestCase):
    render_templates = False

    def test_login(self):
        self._create_user()

        with self.client as c:
            data = {"email": "user@example.com", "password": "Password"}
            c.post(url_for("auth.login"), data=data)

            self.assertTrue('user_id' in session)
            self.assertEqual(1, session['user_id'])

    def test_login_wrong_email(self):
        self._create_user()

        with self.client as c:
            data = {"email": "csacsa@example.com", "password": "Password"}
            c.post(url_for("auth.login"), data=data)

            self.assertFalse('user_id' in session)

    def test_login_wrong_password(self):
        self._create_user()

        with self.client as c:
            data = {"email": "user@example.com", "password": "Passwordacscas"}
            c.post(url_for("auth.login"), data=data)

            self.assertFalse('user_id' in session)

    def test_login_no_password(self):
        u = self._create_user()
        u._password = None

        with self.client as c:
            data = {"email": "user@example.com", "password": "Password"}
            c.post(url_for("auth.login"), data=data)

            self.assertFalse('user_id' in session)

    def test_login_incomplete_user(self):
        u = self._create_user()
        u.active = False

        with self.client as c:
            data = {"email": "user@example.com", "password": "Password"}
            c.post(url_for("auth.login"), data=data)

            self.assertFalse('user_id' in session)

    def test_logout(self):
        self._create_user()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1
                sess['_fresh'] = True
            c.get(url_for("auth.logout"))

            self.assertFalse('user_id' in session)

    def test_password_reset(self):
        self._create_user()

        url = url_for("auth.password_reset")
        response = self.client.post(url, data={"email": "user@example.com"})

        self.assertRedirects(response, url_for("auth.login"))

    def test_password_reset_wrong_email(self):
        self._create_user()

        url = url_for("auth.password_reset")
        response = self.client.post(url, data={"email": "usercas@example.com"})

        # did not redirect
        self.assert200(response)

    def test_change_password(self):
        u = self._create_user()

        token = security_service.generate_reset_password_token(u)

        url = url_for("auth.password", token=token)
        self.client.post(url, data={"password": "passwordnew"})

        self.assertTrue(u.check_password("passwordnew"))
        # after password reset user gets logged in only if user is complete
        self.assertFalse('user_id' in session)

    def test_register(self):
        url = url_for("auth.register")
        data = {"email": "user@example.com", "password": "password"}
        with self.client as c:
            c.post(url, data=data)

            u = User.query.get(1)

            self.assertEqual("user@example.com", u.email)
            self.assertTrue(u.check_password("password"))
            self.assertFalse(u.confirmed)

    def test_register_authenticated(self):
        self._create_user()

        url = url_for("auth.register")
        data = {"email": "user@example.com", "password": "password"}
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1
                sess['_fresh'] = True
            response = c.post(url, data=data)

            self.assertRedirects(response, url_for("index"))

    def test_register_with_duplicate_email(self):
        """User chooses to use a different email address,
           which already exists as a user"""
        u = self._create_user()

        u = User()
        u.email = "user2@example.com"
        u.password = "Password"
        db.session.add(u)

        url = url_for("auth.register")
        data = {"email": "user2@example.com", "password": "password"}
        with self.client as c:
            c.post(url, data=data)

            self.assertFalse(u.confirmed)

    def test_confirm(self):
        u = self._create_user()

        token = security_service.generate_confirmation_token(u)

        self.client.get(url_for("auth.confirm_email", token=token))

        self.assertTrue(u.confirmed)

    def _create_user(self):
        u = User()
        u.id = 1
        u.email = "user@example.com"
        u.password = "Password"
        db.session.add(u)

        return u
