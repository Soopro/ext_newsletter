# coding=utf-8
from __future__ import absolute_import

import traceback

from flask import Flask, current_app, request
from redis import Redis
from mongokit import Connection as MongodbConn

from config import config
from utils.encoders import Encoder
from utils.api_utils import make_json_response, make_cors_headers
from apiresps.errors import (NotFound,
                             MethodNotAllowed,
                             UncaughtException)

from services.sup_oauth import SupOAuth
from services.mail import MailQueuePusher


__version_info__ = ('0', '1', '5')
__version__ = '.'.join(__version_info__)

__artisan__ = ['Majik']


def create_app(config_name='dev'):
    app = Flask(__name__)

    app.version = __version__
    app.artisan = __artisan__

    # config
    app.config.from_object(config[config_name])
    app.json_encoder = Encoder

    # database connections
    app.mongodb_database = MongodbConn(
        host=app.config.get("DB_HOST"),
        port=app.config.get("DB_PORT"))
    app.mongodb_conn = app.mongodb_database[
        app.config.get("DB_DBNAME")]

    app.sup_auth = SupOAuth(ext_key=app.config.get("EXT_KEY"),
                            ext_secret=app.config.get("EXT_SECRET"),
                            grant_type=app.config.get("OAUTH_GRANT_TYPE"),
                            secret_key=app.config.get("SECRET_KEY"),
                            token_uri=app.config.get("OAUTH_TOKEN_API_URI"),
                            redirect_uri=app.config.get("OAUTH_REDIRECT_URI"),
                            expired_in=app.config.get("OAUTH_EXPIRED_IN"))

    app.redis = Redis()
    app.mail_pusher = MailQueuePusher(app.redis, True)

    from blueprints.user.models import User
    app.mongodb_database.register([User])

    # register blueprints
    from blueprints.user import blueprint as user_module
    app.register_blueprint(user_module, url_prefix="/user")

    from blueprints.newsletter import blueprint as newsletter_module
    app.register_blueprint(newsletter_module, url_prefix="/newsletter")

    # register error handlers
    @app.errorhandler(404)
    def app_error_404(error):
        current_app.logger.warn(
            "Error: 404\n{}".format(traceback.format_exc()))
        return make_json_response(NotFound())

    @app.errorhandler(405)
    def app_error_405(error):
        current_app.logger.warn(
            "Error: 405\n{}".format(traceback.format_exc()))
        return make_json_response(MethodNotAllowed())

    @app.errorhandler(Exception)
    def app_error_uncaught(error):
        current_app.logger.warn(
            "Error: Uncaught\n{}".format(traceback.format_exc()))
        return make_json_response(UncaughtException(repr(error)))

    @app.before_request
    def app_before_request():
        # cors response
        if request.method == "OPTIONS":
            resp = current_app.make_default_options_response()
            cors_headers = make_cors_headers()
            resp.headers.extend(cors_headers)
            return resp

    print "-------------------------------------------------------"
    print "Newsletter Extension: {}".format(app.version)
    print "Developers: {}".format(', '.join(app.artisan))
    print "-------------------------------------------------------"

    return app
