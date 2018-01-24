import os


class Config(object):
    """
    Common configurations
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    # Put any configurations here that are common across all environments


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

    # APPLICATION_ROOT = None
    ASSETS_DEBUG = True
    # BOOTSTRAP_CDN_FORCE_SSL = False
    # BOOTSTRAP_LOCAL_SUBDOMAIN = None
    # BOOTSTRAP_QUERYSTRING_REVVING = True
    # BOOTSTRAP_SERVE_LOCAL = False
    # BOOTSTRAP_USE_MINIFIED = True
    DATABASE_CONNECT_OPTIONS = {}
    DEBUG = True
    # EXPLAIN_TEMPLATE_LOADING = False
    # JSONIFY_MIMETYPE = 'application/json'
    # JSONIFY_PRETTYPRINT_REGULAR = True
    # JSON_AS_ASCII = True
    # JSON_SORT_KEYS = True
    # LOGGER_HANDLER_POLICY = 'always'
    # LOGGER_NAME = 'app'
    # MAX_CONTENT_LENGTH = None
    # PERMANENT_SESSION_LIFETIME (4451207536) = {timedelta} 31 days, 0:00:00
    # PREFERRED_URL_SCHEME = 'http'
    # PRESERVE_CONTEXT_ON_EXCEPTION = None
    # PROPAGATE_EXCEPTIONS = None
    #SECRET_KEY = None
    CSRF_ENABLED = True
    SECRET_KEY = '123456'
    # SEND_FILE_MAX_AGE_DEFAULT (4451207600) = {timedelta} 12:00:00
    # SERVER_NAME = None
    # SESSION_COOKIE_DOMAIN = None
    # SESSION_COOKIE_HTTPONLY = True
    # SESSION_COOKIE_NAME = 'session'
    # SESSION_COOKIE_PATH = None
    # SESSION_COOKIE_SECURE = False
    # SESSION_REFRESH_EACH_REQUEST = True
    SQLALCHEMY_BINDS = None
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1/notes_db'
    # 'sqlite:///' + os.path.join(basedir, 'instance', 'development.db')
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_MAX_OVERFLOW = None
    SQLALCHEMY_NATIVE_UNICODE = None
    SQLALCHEMY_POOL_RECYCLE = None
    SQLALCHEMY_POOL_SIZE = None
    SQLALCHEMY_POOL_TIMEOUT = None
    SQLALCHEMY_RECORD_QUERIES = None
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    TEMPLATES_AUTO_RELOAD = None
    TESTING = False
    # TRAP_BAD_REQUEST_ERRORS = False
    # TRAP_HTTP_EXCEPTIONS = False
    # USE_X_SENDFILE = False


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False


class TestingConfig(Config):
    """
    Testing configurations
    """

    TESTING = True


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
