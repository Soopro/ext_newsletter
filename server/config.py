class Config(object):
    DEBUG = True
    
    HOST = "127.0.0.1"
    PORT = 5001

    DB_HOST = '127.0.0.1'
    DB_PORT = 27017
    DB_DBNAME = 'ext_newsletter'
    REDIRECT_URL_DOMAIN = 'http://url4.cc'

    SECRET_KEY = 'secret_key'

    ALLOW_ORIGINS = ['*']
    ALLOW_CREDENTIALS = False

    REMOTE_OAUTH_URL = 'http://d.sup.farm/#/oauth'
    
    TOKEN_URL = 'http://api.sup.farm/oauth/token'

    APP_KEY = 'url4-1443411015'
    APP_SECRET = '230275dd-063b-4c8e-bc36-a6c045d2f410'
    GRANT_TYPE = 'code'

    REDIRECT_URI = 'http://127.0.0.1:9527/#/redirect'
    EXPIRED_IN = 36000
    
class ProductionConfig(Config):
    DEBUG = False


config = {
    'dev': Config,
    'production': ProductionConfig
}
