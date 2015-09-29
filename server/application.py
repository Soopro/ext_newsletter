from __future__ import absolute_import
from flask import Flask, current_app, request
import traceback
from mongokit import Connection
from utils.base_utils import make_json_response, make_cors_headers
from errors.general_errors import (NotFound,
                                   ErrUncaughtException,
                                   MethodNotAllowed)
from config import config as CONFIG_NAME
from utils.sup_ext_oauth import SupAuth
from redis import Redis
from utils.encoders import Encoder
from mail import MailQueuePusher

def create_app(config_name='dev'):
    app = Flask(__name__)
    config = CONFIG_NAME[config_name]
    app.config.from_object(config)
    app.mongodb_database = Connection(host=app.config.get("DB_HOST"),
                                      port=app.config.get("DB_PORT"))
    app.mongodb_conn = app.mongodb_database[app.config.get("DB_DBNAME")]

    app.sup_auth = SupAuth(app_key=app.config.get("APP_KEY"),
                           app_secret=app.config.get("APP_SECRET"),
                           grant_type=app.config.get("GRANT_TYPE"),
                           secret_key=app.config.get("SECRET_KEY"),
                           redirect_uri=app.config.get("REDIRECT_URI"),
                           expired_in=app.config.get("EXPIRED_IN"))

    app.json_encoder = Encoder
    app.redis = Redis()
    app.mail_pusher = MailQueuePusher(app.redis, True)
    
    from blueprints.user import blueprint as user_module
    app.register_blueprint(user_module, url_prefix="/newsletter/user")

    from blueprints.newsletter import blueprint as newsletter_module
    app.register_blueprint(newsletter_module, url_prefix="/newsletter")

    # register error handlers
    @app.errorhandler(404)
    def app_error_404(error):
        current_app.logger.warn("Error: 404\n{}".format(traceback.format_exc()))
        return make_json_response(NotFound())

    @app.errorhandler(405)
    def app_error_405(error):
        current_app.logger.warn("Error: 405\n{}".format(traceback.format_exc()))
        return make_json_response(MethodNotAllowed())

    @app.errorhandler(Exception)
    def app_error_500(error):
        current_app.logger.warn("Error: 500\n{}".format(traceback.format_exc()))
        return make_json_response(ErrUncaughtException(repr(error)))

    @app.before_request
    def app_before_request():
        # cors response
        if request.method == "OPTIONS":
            resp = current_app.make_default_options_response()
            cors_headers = make_cors_headers()
            resp.headers.extend(cors_headers)
            return resp
        return

    return app
