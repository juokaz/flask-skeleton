from ..utils import url_for_other_page
from flask import request, url_for
from flask.ext.restful import fields, marshal

from werkzeug.exceptions import default_exceptions, HTTPException
from flask import abort as original_abort, json
from flask import make_response

from urllib.parse import urlparse, urlunparse


def paginate(entities, fields, name, links={}):
    page = int(request.args.get("page", 1))

    view_name = request.url_rule.endpoint
    args = request.view_args
    _links = {'self': {'href': url_for(view_name, **args)}}
    links = dict(list(links.items()) + list(_links.items()))

    try:
        paginated = entities.paginate(page, 25)
        items = paginated.items
        total = paginated.total
        per_page = paginated.per_page
        count = len(items)
        _links = paginated_links(paginated)
        links = dict(list(links.items()) + list(_links.items()))
    except AttributeError:
        items = entities
        total = per_page = count = len(items)

    response = {}
    response['_embedded'] = {name: marshal(items, fields)}
    response['_links'] = links
    response['total'] = total
    response['per_page'] = per_page
    response['count'] = count

    return response


def paginated_links(paginated):
    _links = {}
    if paginated.pages > 0:
        if paginated.page != paginated.pages:
            _links['last'] = {'href': url_for_other_page(paginated.pages)}
    if paginated.has_next:
        _links['next'] = {'href': url_for_other_page(paginated.next_num)}
    if paginated.has_prev:
        _links['previous'] = {'href': url_for_other_page(paginated.prev_num)}
    return _links


def content_created(entity, fields):
    response = marshal(entity, fields)
    return response, 201, {'location': response['_links']['self']['href']}


def content_updated(entity):
    return "", 204


def content_deleted():
    return "", 204


def handle_validation_error(field, error):
    msg = u"Error in the %s field - %s" % (
        field,
        error
    )
    abort(400, message=msg)


class IdUrl(fields.Url):
    def __init__(self, endpoint=None, attribute='id', key='id'):
        super(IdUrl, self).__init__(endpoint)
        self.attribute = attribute
        self.key = key

    def output(self, key, obj):
        data = self._get_data(obj)
        data[self.key] = getattr(obj, self.attribute)
        endpoint = self.endpoint or request.endpoint
        # parse the url to remove the query string
        o = urlparse(url_for(endpoint, **data))
        return urlunparse(("", "", o.path, "", "", ""))

    def _get_data(self, obj):
        """Get all model properties"""
        columns = obj.__table__.columns.keys()
        return dict((col, getattr(obj, col)) for col in columns)


def abort(status_code, body=None, headers=None, **kwargs):
    """Same as :func:`flask.abort` but with a JSON response."""
    bases = [JSONHTTPException]
    # Add Werkzeug base class.
    if status_code in default_exceptions:
        bases.insert(0, default_exceptions[status_code])
    error_cls = type('JSONHTTPException', tuple(bases), dict(code=status_code))
    exception = error_cls(body)
    if len(kwargs):
        exception.data = kwargs
    original_abort(make_response(exception, status_code, headers or {}))


class JSONHTTPException(HTTPException):
    """A base class for HTTP exceptions with ``Content-Type:
    application/json``.
    The ``description`` attribute of this class must set to a string (*not* an
    HTML string) which describes the error.
    """

    def get_body(self, environ):
        """Overrides :meth:`werkzeug.exceptions.HTTPException.get_body` to
        return the description of this error in JSON format instead of HTML.
        """
        try:
            data = self.data
        except AttributeError:
            data = dict(message=self.description, code=self.code)
        return json.dumps(data)

    def get_headers(self, environ):
        """Returns a list of headers including ``Content-Type:
        application/json``.
        """
        return [('Content-Type', 'application/vnd.error+json')]
