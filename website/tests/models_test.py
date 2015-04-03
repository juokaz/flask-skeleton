from . import TestCase

from ..models import User


class UsersTest(TestCase):
    def test_get_full_name(self):
        u = User()
        u.email = 'user@example.com'

        self.assertEquals('user@example.com', u.get_full_name())

        u.first_name = 'User'

        self.assertEquals('User', u.get_full_name())

        u.last_name = 'Last'

        self.assertEquals('User Last', u.get_full_name())
