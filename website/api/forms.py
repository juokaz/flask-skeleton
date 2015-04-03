from website.frontend.forms import UserForm

import wtforms_json
from flask import request

from .common import handle_validation_error

# monkey patch wtforms for better json support
wtforms_json.init()


class JsonForm():
    def get_formdata(self):
        """Override the default flask wtform get_formdata method to load data
        stricly from json instead of trying get/post first"""
        formdata = request.json
        return wtforms_json.MultiDict(
            wtforms_json.flatten_json(self.__class__, formdata)
        ) if formdata else None

    def validate_on_submit(self):
        if super().validate_on_submit():
            return True

        for field, errors in self.errors.items():
            for error in errors:
                handle_validation_error(field, error)


class UserForm(JsonForm, UserForm):
    pass
