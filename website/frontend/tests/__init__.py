from ...tests import TestCase
from .. import app, db
from ...models import User


class TestCase(TestCase):
    def create_app(self):
        app.config.from_object('website.settings.TestConfig')
        return app

    def as_user(self, method_name, *args, **kwargs):
        if User.query.get(1) is None:
            u = User()
            u.id = 1
            u.email = "user@example.com"
            u.password = "password"
            db.session.add(u)

        return self._get(method_name, *args, **kwargs)
