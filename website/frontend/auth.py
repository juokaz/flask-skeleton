from flask import Blueprint
from flask import request, flash, redirect, url_for
from flask.ext.login import login_user as _login_user, logout_user, \
    current_user, LoginManager, login_required
from ..utils import templated, handle_404

from .forms import LoginForm, RegisterForm, PasswordForm, PasswordResetForm

from ..services import users_service, security_service

from functools import wraps

bp = Blueprint('auth', __name__)


def init(app):
    lm = LoginManager()
    lm.login_view = "auth.login"
    lm.login_message = False
    lm.user_callback = users_service.get
    lm.setup_app(app)

    @app.before_request
    def before_request():
        # if user is logged in or no endpoint is set allow the request
        if current_user.is_authenticated():
            return

        endpoint = request.endpoint or ''

        criteria = [
            endpoint.find('auth') == -1,
            endpoint.find('static') == -1
        ]

        if all(criteria):
            return app.login_manager.unauthorized()


def anonymous_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated():
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


def check_token(check):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.args.get("token")
            status = check(token)
            expired, invalid, user_id = status

            if invalid or expired:
                flash("Invalid token.")
                return redirect(url_for('auth.login'))

            user = handle_404(users_service, user_id)

            return f(user, *args, **kwargs)
        return decorated_function
    return decorator


@bp.route('/register', methods=['GET', 'POST'])
@anonymous_required
@templated()
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = users_service.create(**form.data)

        flash("Registered successfully.")

        return login_user(user)
    return dict(form=form)


@bp.route('/login', methods=['GET', 'POST'])
@anonymous_required
@templated()
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.user
        return login_user(user)
    return dict(form=form)


@bp.route('/forgot', methods=['GET', 'POST'])
@anonymous_required
@templated()
def password_reset():
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = form.user

        security_service.send_password_reset_email(user)

        flash("Password reset link has been emailed.")
        return redirect(url_for("auth.login"))
    return dict(form=form)


@bp.route("/password", methods=['GET', 'POST'])
@anonymous_required
@check_token(security_service.reset_password_token_status)
@templated()
def password(user):
    form = PasswordForm(user)
    del form.current

    if form.validate_on_submit():
        users_service.update(user, password=form.password.data)

        flash("Password updated.")
        return login_user(user)
    return dict(form=form, user=user)


@bp.route('/confirm')
@check_token(security_service.confirm_email_token_status)
@templated()
def confirm_email(user):
    users_service.update(user, confirmed=True)

    if user.id != current_user.get_id():
        logout_user()
        login_user(user)

    flash("Email confirmed.")
    return redirect(url_for("index"))


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


def login_user(user):
    if users_service.can_login(user):
        _login_user(user, remember=True)
        return redirect(request.args.get("next") or url_for("index"))
    else:
        flash("Inactive user.")
        return redirect(url_for("auth.login"))
