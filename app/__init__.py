# app/__init__.py

import sys

# 3rd-party imports
from flask import Flask, render_template, abort
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
# from flask.ext.cache import Cache
from flask_caching import Cache

from rediscluster import StrictRedisCluster

# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()

# Flask database migration management

# Flask Login Manager initialization
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    cache_configuration = {
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_HOST': app.config['REDIS_HOST'],
        'CACHE_REDIS_PORT': app.config['REDIS_PORT'],
        'CACHE_REDIS_PASSWORD': app.config['REDIS_PASSWORD'],
        'CACHE_REDIS_DB': 0,
        'CACHE_DEFAULT_TIMEOUT': app.config['REDIS_EXPIRATION'],
        'CACHE_KEY_PREFIX': '__xray__python__',
        'CACHE_ARGS': [1, 2, 3, 4, 5],
        'CACHE_OPTIONS': {'foo': 'bar', 'Age': 7}
        # 'CACHE_REDIS_URL':'redis://localhost:6379'
    }
    # Check Configuring Flask-Cache section for more details
    # app.cache = Cache(app, config={'CACHE_TYPE': 'simple'})
    app.cache = Cache(config=cache_configuration)

    startup_nodes = [
        {'host': '127.0.0.1', 'port': 6379},
        {'host': '127.0.0.1', 'port': 6380}
    ]
    try:
        app.redisconn = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)
        app.redisconn.set('name', 'admin')
        app.redisconn.set('age', 18)
    except Exception, e:
        app.logger.error('What the fuck is going on , the StrictRedisCluster Connect Error, app will exit')
        #sys.exit(1)

    # initialize the flask objects
    Bootstrap(app)
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"

    migrate = Migrate(app, db)

    from app import models

    # Register the Blueprints
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint)

    # Custom Error Handling
    # existing code remains

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html', title='Forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        logError(True)
        return render_template('errors/404.html', title='Page Not Found'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        logError(True)
        return render_template('errors/500.html', title='Server Error'), 500

    @app.route('/500')
    def error():
        logError(True)
        abort(500)

    def logError(start):
        # explicitely Prints error to the errorlog. @/var/log/apache2/error.log
        assert start
        import traceback, sys, StringIO
        err = sys.stderr
        buffer = sys.stderr = StringIO.StringIO()
        traceback.print_exc()
        sys.stderr = err
        print buffer.getvalue()

    return app
