from flask import current_app, abort, url_for, request, render_template
from flask.ext.mail import Message

from functools import wraps

import os
from jinja2 import Environment, FileSystemLoader
from premailer import Premailer

from urllib.parse import urlencode, parse_qs, unquote

import re
from jinja2 import evalcontextfilter, Markup, escape

from sqlalchemy.orm import exc

from flask.ext.babel import Babel


def handle_404(service, *args, **kwargs):
    _abort = current_app.abort if hasattr(current_app, 'abort') else abort
    try:
        return service.get(*args, **kwargs)
    except (exc.NoResultFound, exc.MultipleResultsFound):
        return _abort(404)


def templated(template=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template
            if template_name is None:
                template_name = request.endpoint.replace('.', '/') + '.html'
            ctx = f(*args, **kwargs)
            if not isinstance(ctx, dict):
                return ctx
            if 'template' in ctx:
                template_name = ctx['template']
                del ctx['template']
            return render_template(template_name, **ctx)
        return decorated_function
    return decorator


def send_mail(subject, recipient, template, force=False, **context):
    """Send an email via the Flask-Mail extension.
    :param subject: Email subject
    :param recipient: Email recipient
    :param template: The name of the email template
    :param context: The context to render the template with
    """
    mail = current_app.extensions.get('mail')
    base_url = current_app.config['BASE_URL']

    if mail.suppress and not force:
        return

    msg = Message(subject, recipients=[recipient])

    body = render_email_template(template, base_url=base_url, **context)

    body = inline_css(body)

    msg.html = body

    mail.send(msg)


def render_email_template(template, **context):
    base = os.path.dirname(__file__)
    path = "%s/frontend/templates/" % base

    env = Environment(loader=FileSystemLoader(path))
    template = env.get_template("email/%s.html" % template)
    return template.render(**context)


def inline_css(body):
    m = Premailer(body, include_star_selectors=True, remove_classes=False)
    body = m.transform()
    return body


def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page

    query_string = request.query_string

    query = parse_qs(query_string)
    query.pop('page', None)

    if query:
        query = urlencode(query, True)
        return url_for(request.endpoint, **args) + "?" + query
    else:
        return url_for(request.endpoint, **args)


def format_currency(value):
    if value is None:
        return ''
    return "${:,.2f}".format(value)


_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')


@evalcontextfilter
def nl2br(eval_ctx, value):
    if value is None:
        return ''
    result = u'\n\n'.join(u'%s<br />' % p.replace('\n', '<br>\n')
                          for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result


def jinja_init(app):
    app.jinja_env.globals['url_for_other_page'] = url_for_other_page
    app.jinja_env.filters['format_currency'] = format_currency
    app.jinja_env.filters['nl2br'] = nl2br

    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True


def babel_init(app):
    babel = Babel()
    babel.init_app(app)

    @babel.timezoneselector
    def get_timezone():
        timezone = request.cookies.get('timezone')
        if timezone is not None:
            timezone = unquote(timezone)
            return timezone
