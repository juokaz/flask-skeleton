from wtforms import TextField, validators

from ..forms import FilterForm


class UsersForm(FilterForm):
    email = TextField('Email',
                      validators=[validators.Optional()])
