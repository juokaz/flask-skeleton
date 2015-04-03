from ..forms import Form
from wtforms import TextField, PasswordField, validators


from ..services import users_service


class UserForm(Form):
    email = TextField('Email', validators=[validators.Required(),
                                           validators.Email()])
    first_name = TextField('First Name')
    last_name = TextField('Last Name')

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


class LoginForm(Form):
    email = TextField('Email', validators=[validators.Required()])
    password = PasswordField('Password', validators=[validators.Required()])

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = users_service.first(email=self.email.data)
        if user is None:
            self.password.errors.append('Invalid email and/or password')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append('Invalid email and/or password')
            return False

        self.user = user
        return True


class RegisterForm(Form):
    email = TextField('Email', validators=[validators.Required(),
                                           validators.Email()])
    password = PasswordField('Password', validators=[validators.Required()])

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = users_service.first(email=self.email.data)
        if user is not None:
            error = 'There is already a user with the same email address'
            self.email.errors.append(error)
            return False

        return True


class PasswordForm(Form):
    current = PasswordField('Current Password',
                            validators=[validators.Required()])
    password = PasswordField('Password', validators=[validators.Required()])

    def __init__(self, user, *args, **kwargs):
        super().__init__(obj=user, *args, **kwargs)
        self.user = user

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        if self.current and not self.user.check_password(self.current.data):
            self.current.errors.append('Current password is incorrect')
            return False

        return True


class PasswordResetForm(Form):
    email = TextField('Email', validators=[validators.Required()])

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = users_service.first(email=self.email.data)
        if user is None:
            self.email.errors.append('Invalid email and/or password')
            return False

        self.user = user
        return True
