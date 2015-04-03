from ...tests import TestCase
from .. import app, db
from ...models import Admin


class TestCase(TestCase):
    def create_app(self):
        app.config.from_object('website.settings.TestConfig')
        return app

    def as_admin(self, method_name, *args, **kwargs):
        if Admin.query.get(1) is None:
            u = Admin()
            u.email = "user@example.com"
            u.password = "Password"
            db.session.add(u)

        return self._get(method_name, *args, **kwargs)
