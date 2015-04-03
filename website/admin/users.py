from flask import Blueprint
from flask import flash, redirect, url_for
from ..utils import templated, handle_404

from .forms import UserForm
from .filters import UsersForm

from ..services import users_service

bp = Blueprint('users', __name__)


@bp.route("/", defaults={'page': 1})
@bp.route('/<int:page>')
@templated()
def index(page):
    filter_form = UsersForm()
    users = users_service.get_users(**filter_form.data)
    users = users.paginate(page, 100)
    return dict(users=users, filter_form=filter_form)


@bp.route('/add', methods=['GET', 'POST'])
@templated()
def add():
    form = UserForm()
    del form.active
    del form.confirmed
    if form.validate_on_submit():
        user = users_service.create(active=True, confirmed=True, **form.data)

        flash("User created with a password '%s'." % user.generated_password)
        return redirect(url_for("users.index"))
    return dict(form=form)


@bp.route('/edit/<id>', methods=['GET', 'POST'])
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

    users_service.delete(user)

    flash("User deleted.")
    return redirect(url_for("users.index"))
