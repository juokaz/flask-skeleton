from ..models import User
from .base import Service


class Users(Service):
    __model__ = User

    def __init__(self, security_service):
        self.security_service = security_service

    def get_users(self, user=None, **kwargs):
        return self.get_all(user, **kwargs)

    def create(self, current_user=None, **kwargs):
        user = super().new(**kwargs)

        # if admin is creating a user, populate the password
        if user.confirmed and user.active:
            user.generate_random_password()

        self.save(user)

        if user.confirmed is False:
            self.security_service.send_confirmation_email(user)

        return user

    def can_login(self, user):
        return user.active

    def _add_user_condition(self, query, user):
        query = super()._add_user_condition(query, user)
        query = query.filter_by(active=True)
        return query
