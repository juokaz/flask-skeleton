import os
from flask import Flask, request
from flask.ext.mail import Mail
from ..models import db
from .common import abort
from flask.ext.restful import Api, output_json

from . import index, users, auth

app = Flask(__name__)
app.abort = abort

env = os.environ.get('ENV', 'dev')
app.config.from_object('website.settings.%sConfig' % env.capitalize())
app.config['ERROR_404_HELP'] = False

auth.init(app)

db.init_app(app)
mail = Mail(app)

api = Api(app, catch_all_404s=True, default_mediatype='application/hal+json')
api.representations = {'application/hal+json': output_json}


@app.before_request
def validate_mimetype():
    message = "This endpoint only supports Content-Type: %s requests, not %s."
    json = 'application/json'
    if request.method in ['POST', 'PUT']:
        if request.mimetype != json:
            app.abort(415, message=message % (json, request.mimetype))


api.add_resource(index.Index, '/', '/protected', endpoint='index')

api.add_resource(users.Users, '/users', endpoint='users')
api.add_resource(users.User, '/users/<int:id>', endpoint='user')
