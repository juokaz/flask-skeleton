from . import TestCase

from flask import url_for


class IndexTest(TestCase):
    def test_index(self):
        response = self.client.get(url_for('index'))

        self.assert200(response)
        self.assertEquals({'hello': 'world'}, response.json)
        json = 'application/hal+json'
        self.assertEquals(json, response.headers['Content-Type'])

    def test_index_links(self):
        response = self.as_user('get', url_for('index'))

        self.assertTrue('users' in response.json['_links'])

    def test_unsupported_mimetype(self):
        response = self.client.post(url_for('index'), content_type='text/xml')

        self.assertStatus(response, 415)
        json = 'application/vnd.error+json'
        self.assertEquals(json, response.headers['Content-Type'])
        message = 'This endpoint only supports Content-Type: ' \
            + 'application/json requests, not text/xml.'
        self.assertEquals(message, response.json['message'])
