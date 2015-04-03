from flask import Blueprint
from flask import request
from flask import flash, redirect, url_for
from flask.ext.login import login_user, logout_user, \
    current_user, login_required, LoginManager
from ..utils import templated, handle_404

from .forms import LoginForm, PasswordForm

from ..services import admins_service

bp = Blueprint('auth', __name__)


def init(app):
    lm = LoginManager()
    lm.login_view = "auth.login"
    lm.login_message = False
    lm.user_callback = admins_service.get
    lm.setup_app(app)

    @app.before_request
    def before_request():
        # if user is logged in or no endpoint is set allow the request
        if current_user.is_authenticated():
            return

        endpoint = request.endpoint or ''

        criteria = [
            endpoint.find('auth.login') == -1,
            endpoint.find('static') == -1
        ]

        if all(criteria):
            return app.login_manager.unauthorized()


@bp.route("/settings", methods=['GET', 'POST'])
@templated()
def settings():
    admin = handle_404(admins_service, current_user.id)

    form = PasswordForm(admin)

    if form.validate_on_submit():
        admins_service.update(admin, password=form.password.data)

        flash("Password updated.")
        return redirect(url_for("auth.settings"))
    return dict(form=form, admin=admin)


@bp.route('/login', methods=['GET', 'POST'])
@templated()
def login():
    if current_user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.user, remember=form.remember_me.data)
        return redirect(request.args.get("next") or url_for("index"))
    return dict(form=form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
