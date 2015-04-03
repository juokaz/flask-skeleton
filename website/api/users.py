from flask.ext.restful import Resource, fields, marshal
from .common import paginate, IdUrl
from .common import content_created, content_updated, content_deleted
from .auth import current_user
from ..utils import handle_404

from .forms import UserForm

from ..services import users_service

user_fields = {
    '_links': {
        'self': {
            'href': IdUrl('user')
        },
    },
    'email': fields.String,
    'firs_name': fields.String,
    'last_name': fields.String,
    'confirmed': fields.Boolean,
}


class Users(Resource):
    def get(self):
        users = users_service.get_all(current_user)
        return paginate(users, user_fields, 'users')

    def post(self):
        form = UserForm()
        if form.validate_on_submit():
            user = users_service.create(current_user, **form.data)

            return content_created(user, user_fields)


class User(Resource):
    def get(self, id):
        user = handle_404(users_service, id, current_user)
        return marshal(user, user_fields)

    def put(self, id):
        user = handle_404(users_service, id, current_user)
        form = UserForm(user)
        if form.validate_on_submit():
            users_service.update(user, **form.patch_data)

            return content_updated(user)

    def delete(self, id):
        user = handle_404(users_service, id, current_user)

        users_service.update(user, active=False)

        return content_deleted()
