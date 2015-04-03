from flask import current_app

from itsdangerous import URLSafeTimedSerializer
from itsdangerous import BadSignature, SignatureExpired

import hashlib

from ..utils import send_mail


class Security:
    def send_confirmation_email(self, user):
        token = self.generate_confirmation_token(user)
        confirmation_link = "/confirm?token=%s" % token

        send_mail('Welcome!', user.email, 'confirmation_instructions',
                  user=user, confirmation_link=confirmation_link)

    def send_password_reset_email(self, user):
        token = self.generate_reset_password_token(user)
        reset_link = "/password?token=%s" % token

        send_mail('Password Reset', user.email, 'password_reset_instructions',
                  user=user, reset_link=reset_link)

    def generate_confirmation_token(self, user):
        """Generates a unique confirmation token for the specified user.
        :param user: The user to work with
        """
        data = [str(user.id), self.md5(user.email)]
        return self.get_token('confirmation', data)

    def confirm_email_token_status(self, token):
        """Returns the expired status, invalid status, and user of a confirmation
        token. For example::
            expired, invalid, user = confirm_email_token_status('...')
        :param token: The confirmation token
        """
        return self.get_token_status('confirmation', token, 3600)

    def generate_reset_password_token(self, user):
        """Generates a unique reset password token for the specified user.
        :param user: The user to work with
        """
        password = user.password if user.password is not None else user.email
        data = [str(user.id), self.md5(password)]
        return self.get_token('password_reset', data)

    def reset_password_token_status(self, token):
        """Returns the expired status, invalid status, and user of a password reset
        token. For example::
            expired, invalid, user = reset_password_token_status('...')
        :param token: The password reset token
        """
        return self.get_token_status('password_reset', token, 3600)

    def get_token(self, token_name, data):
        serializer = self._get_serializer(token_name)
        return serializer.dumps(data)

    def get_token_status(self, token_name, token, max_age=None):
        """Get the status of a token.
        :param token: The token to check
        :param max_age: The seconds token is valid form
        """
        serializer = self._get_serializer(token_name)
        user, data = None, None
        expired, invalid = False, False

        try:
            data = serializer.loads(token, max_age=max_age)
        except SignatureExpired:
            d, data = serializer.loads_unsafe(token)
            expired = True
        except (BadSignature, TypeError, ValueError):
            invalid = True

        if data:
            user = data[0]

        expired = expired and (user is not None)
        return expired, invalid, user

    def md5(self, data):
        return hashlib.md5(self.encode_string(data)).hexdigest()

    def encode_string(self, string):
        """Encodes a string to bytes, if it isn't already.
        :param string: The string to encode"""

        string = string.encode('utf-8')
        return string

    def _get_serializer(self, token_name):
        app = current_app
        secret_key = app.config.get('SECRET_KEY')
        salt = app.config['SECURITY_%s_SALT' % token_name.upper()]
        return URLSafeTimedSerializer(secret_key=secret_key, salt=salt)
