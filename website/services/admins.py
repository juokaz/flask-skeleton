from ..models import Admin
from .base import Service


class Admins(Service):
    __model__ = Admin
