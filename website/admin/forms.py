from flask_wtf import Form
from wtforms import TextField, BooleanField, PasswordField, validators

from ..services import users_service, admins_service


class LoginForm(Form):
    email = TextField(u'Email', validators=[validators.required(),
                                            validators.Email()])
    password = PasswordField(u'Password', validators=[validators.required()])
    remember_me = BooleanField('Remember Me', default=False)

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = admins_service.first(email=self.email.data)
        if user is None:
            self.email.errors.append(u'Unknown email')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append(u'Invalid password')
            return False

        self.user = user
        return True


class UserForm(Form):
    email = TextField('Email', validators=[validators.Required(),
                                           validators.Email()])
    first_name = TextField('First Name')
    last_name = TextField('Last Name')
    confirmed = BooleanField('Email Confirmed')
    active = BooleanField('Active')

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(obj=user, *args, **kwargs)
        self.user = user

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = users_service.first(email=self.email.data)
        if user is not None and (self.user is None or user.id != self.user.id):
            error = 'There is already a user with the same email address'
            self.email.errors.append(error)
            return False

        return True


class PasswordForm(Form):
    current = PasswordField('Current Password',
                            validators=[validators.Required()])
    password = PasswordField('Password', validators=[validators.Required()])

    def __init__(self, user, *args, **kwargs):
        super(PasswordForm, self).__init__(obj=user, *args, **kwargs)
        self.user = user

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        if self.current and not self.user.check_password(self.current.data):
            self.current.errors.append('Current password is incorrect')
            return False

        return True
