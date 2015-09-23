import os

class Config(object):
    # path
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # DATABASES
    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017

    # Other
    SECRET_KEY = 'secret_key'

    ALLOW_ORIGINS = ['*']
    ALLOW_CREDENTIALS = False


class DevelopmentConfig(Config):
    PORT = 5001
    MONGODB_DATABASE = 'ext_newsletter_dev'

    AUTH_URL = 'http://localhost:9002/#/oauth2'
    TOKEN_URL = 'http://localhost:5000/auth2/token'
    ROLE_URL = "http://localhost:5000/crm/role"
    MEMBER_URL = "http://localhost:5000/crm/member"

    APP_KEY = 'newsletter-1427872426'
    APP_SECRET = '77bf3b8f-9781-4cbc-b704-6e6e740f2795'
    GRANT_TYPE = 'code'

    REDIRECT_URI = 'http://localhost:9000/#/notify'
    EXPIRED_IN = 36000

    # develop


class TestingConfig(Config):
    PORT = 20001
    MONGODB_DATABASE = 'ext_newsletter_testing'

    AUTH_URL = 'http://manage.sup.farm/#/oauth2'
    TOKEN_URL = 'http://api.sup.farm/auth2/token'
    ROLE_URL = "http://api.sup.farm/crm/role"
    MEMBER_URL = "http://api.sup.farm/crm/member"

    APP_KEY = 'newsletter-1428916145'
    APP_SECRET = '8b1b62fd-2894-4675-8be3-bb7137602102'
    GRANT_TYPE = 'code'

    REDIRECT_URI = 'http://ext.sup.farm/newsletter/#/notify'
    EXPIRED_IN = 36000


class ProductionConfig(Config):
    PORT = 20001
    MONGODB_DATABASE = 'ext_newsletter_production'

    AUTH_URL = 'http://manage.soopro.com/#/oauth2'
    TOKEN_URL = 'http://api.soopro.com/auth2/token'
    ROLE_URL = "http://api.soopro.com/crm/role"
    MEMBER_URL = "http://api.soopro.com/crm/member"

    APP_KEY = 'newsletter-1429007027'
    APP_SECRET = '0a22b469-a58f-4b4a-b619-718b24e13912'
    GRANT_TYPE = 'code'

    REDIRECT_URI = 'http://ext.soopro.com/newsletter/#/notify'
    EXPIRED_IN = 36000
