from flask.ext.wtf import Form

from flask import request


class Form(Form):
    def __init__(self, *args, **kwargs):
        if hasattr(self, 'get_formdata'):
            kwargs['formdata'] = self.get_formdata()

        super().__init__(*args, **kwargs)


class FilterForm(Form):
    def __init__(self, csrf_enabled=False, *args, **kwargs):
        formdata = request.args
        super().__init__(csrf_enabled=csrf_enabled, formdata=formdata,
                         *args, **kwargs)

    def is_submitted(self):
        """
        Checks if form has been submitted. The default case is if the HTTP
        method is **GET**.
        """

        # check if at least one field is in the request
        one_field = False
        for field in self:
            if field.name in request.args:
                one_field = True
                break

        return request and request.method == "GET" and one_field

    @property
    def data(self):
        if self.validate_on_submit():
            return super(FilterForm, self).data
        return {}
