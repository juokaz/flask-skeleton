from ...tests import TestCase
from ...admin import app


class TestCase(TestCase):
    def create_app(self):
        app.config.from_object('website.settings.TestConfig')
        return app
