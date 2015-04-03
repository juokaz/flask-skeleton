import os
from flask import Flask, render_template
from flask.ext.assets import Environment
from flask.ext.mail import Mail
from ..models import db
from ..utils import jinja_init, babel_init

from . import auth, users

app = Flask(__name__)

env = os.environ.get('ENV', 'dev')
app.config.from_object('website.settings.%sConfig' % env.capitalize())
app.config['SECRET_KEY'] = __name__ + app.config['SECRET_KEY']

jinja_init(app)
babel_init(app)
auth.init(app)

db.init_app(app)
assets = Environment(app)
mail = Mail(app)

app.register_blueprint(auth.bp)
app.register_blueprint(users.bp, url_prefix='/users')


@app.route("/")
def index():
    return render_template("index.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
