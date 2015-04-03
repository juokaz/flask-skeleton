from . import TestCase

from flask import url_for


class IndexTest(TestCase):
    def test_index(self):
        response = self.as_user('get', url_for('index'))

        self.assert200(response)

    def test_not_found(self):
        response = self.as_user('get', '/index-missing')

        self.assert404(response)

    def test_not_found_as_anonymous(self):
        response = self.client.get('/index-missing')

        url = url_for("auth.login") + "?next=%2Findex-missing"
        self.assertRedirects(response, url)
