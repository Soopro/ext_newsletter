from flask import Flask, current_app, request
from mongokit import Connection
import traceback
from redis import Redis
import os
from config import DevelopmentConfig, TestingConfig, ProductionConfig
from utils.encoders import Encoder
from utils.base_utils import make_cors_headers, make_json_response
from utils.sup_ext_oauth import SupAuth
from mail import MailQueuePusher

from errors.general_errors import NotFound, MethodNotAllowed, ErrUncaughtException

ENV_CONFIG_NAME = os.getenv("NEWSLETTER_CONFIG_NAME", 'development')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}


def create_app():
    app = Flask(__name__)
    redis_store = Redis()
    app.config.from_object(config[ENV_CONFIG_NAME])
    app.json_encoder = Encoder
    mongodb_database = Connection(host=app.config.get("MONGODB_HOST"),
                                  port=app.config.get("MONGODB_PORT"))
    mongodb_conn = mongodb_database[app.config.get("MONGODB_DATABASE")]
    app.sup_auth = SupAuth(app_key=app.config.get("APP_KEY"),
                           app_secret=app.config.get("APP_SECRET"),
                           grant_type=app.config.get("GRANT_TYPE"),
                           secret_key=app.config.get("SECRET_KEY"),
                           redirect_uri=app.config.get("REDIRECT_URI"),
                           expired_in=app.config.get("EXPIRED_IN"))

    app.mongodb_database = mongodb_database
    app.mongodb_conn = mongodb_conn
    app.redis = redis_store
    app.mail_pusher = MailQueuePusher(redis_store, True)

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

    from blueprints.user import blueprint as user_module
    app.register_blueprint(user_module, url_prefix="/newsletter/user")

    from blueprints.newsletter import blueprint as newsletter_module
    app.register_blueprint(newsletter_module, url_prefix="/newsletter/newsletter")

    return app
