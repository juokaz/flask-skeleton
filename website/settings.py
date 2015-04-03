class Config(object):
    BASE_URL = "https://example.com"
    CSRF_ENABLED = True
    SECRET_KEY = 'secret key'

    SQLALCHEMY_ECHO = False

    MAIL_DEFAULT_SENDER = 'info@example.com'

    BABEL_DEFAULT_TIMEZONE = 'US/Eastern'

    SECURITY_PASSWORD_RESET_SALT = 'secret key'
    SECURITY_CONFIRMATION_SALT = 'secret key'


class ProdConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    SECRET_KEY = ''

    SQLALCHEMY_DATABASE_URI = ''

    SECURITY_PASSWORD_RESET_SALT = ''
    SECURITY_CONFIRMATION_SALT = ''


class DevConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'mysql://dev:dev@localhost/dev'
    SQLALCHEMY_ECHO = True

    ASSETS_DEBUG = True

    MAIL_SUPPRESS_SEND = True


class TestConfig(Config):
    DEBUG = True
    TESTING = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

    WTF_CSRF_ENABLED = False
