from flask import Blueprint, request
from flask import flash, redirect, url_for
from flask.ext.login import current_user
from ..utils import templated, handle_404

from .forms import UserForm, PasswordForm

from ..services import users_service

bp = Blueprint('users', __name__)


@bp.route("", defaults={'page': 1})
@bp.route('/<int:page>')
@templated()
def index(page):
    users = users_service.get_users(current_user).paginate(page, 25)
    return dict(users=users)


@bp.route('/add', methods=['GET', 'POST'])
@templated()
def add():
    form = UserForm()
    if form.validate_on_submit():
        users_service.create(current_user, **form.data)

        flash("User created.")
        return redirect(url_for("users.index"))
    return dict(form=form)


@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@templated()
def edit(id):
    user = handle_404(users_service, id)

    form = UserForm(user)
    if form.validate_on_submit():
        users_service.update(user, **form.data)

        flash("User saved.")
        return redirect(url_for("users.index"))
    return dict(form=form, user=user)


@bp.route('/delete/<id>', methods=['POST'])
def delete(id):
    user = handle_404(users_service, id)

    users_service.update(user, active=False)

    flash("User deleted.")
    return redirect(url_for("users.index"))


@bp.route("/settings", methods=['GET', 'POST'])
@templated()
def settings():
    user = handle_404(users_service, current_user.id)

    password_form = PasswordForm(user)

    if 'change_password' in request.form:
        if password_form.validate_on_submit():
            users_service.update(user, password=password_form.password.data)

            flash("Password updated.")
            return redirect(url_for("users.settings"))

    if 'update_user' in request.form:
        user_form = UserForm(user)
        if user_form.validate_on_submit():
            users_service.update(user, **user_form.data)

            flash("User updated.")
            return redirect(url_for("users.settings"))
    else:
        # otherwise after password form submit this form gets empty fields
        user_form = UserForm(user, formdata=None)

    return dict(password_form=password_form, user_form=user_form, user=user)
