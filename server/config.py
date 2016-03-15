# coding=utf-8
from __future__ import absolute_import


class Config(object):
    DEBUG = True
    SECRET_KEY = 'newsletter_999'

    DB_HOST = '127.0.0.1'
    DB_PORT = 27017

    CURL_BASE_URL = 'http://127.0.0.1/newsletter'

    ALLOW_ORIGINS = ['*']
    ALLOW_CREDENTIALS = False

    OAUTH_GRANT_TYPE = 'code'
    OAUTH_EXPIRED_IN = 36000

    EXT_KEY = 'url4cc-1453895893'
    EXT_SECRET = '38a6daf0-a718-4456-938f-c6ab2ad03456'

    OAUTH_PAGE_URI = 'http://sup.local:9527/#/oauth'
    OAUTH_TOKEN_API_URI = 'http://localhost:5000/oauth/token'
    OAUTH_REDIRECT_URI = 'http://localhost:8888/#/auth/redirect'

    MEMBER_URL = "http://api.soopro.com/crm/member"
    ROLE_URL = "http://api.soopro.com/crm/role"


class DevelopmentConfig(Config):
    DB_DBNAME = 'ext_newsletter_dev'


class TestCaseConfig(Config):
    DB_DBNAME = 'ext_newsletter_testcase'

    CURL_BASE_URL = 'http://127.0.0.1/newsletter'


class TestingConfig(Config):
    DB_DBNAME = 'ext_newsletter_test'

    EXT_KEY = 'url4cc-1453895893'
    EXT_SECRET = '38a6daf0-a718-4456-938f-c6ab2ad03456'

    OAUTH_PAGE_URI = 'http://d.sup.farm/#/oauth'
    OAUTH_TOKEN_API_URI = 'http://api.sup.farm/oauth/token'
    OAUTH_REDIRECT_URI = 'http://ext.sup.farm/url4/client/#/auth/redirect'


class ProductionConfig(Config):
    DEBUG = False
    DB_DBNAME = 'ext_newsletter_prd'

    EXT_KEY = 'url4cc-1453895893'
    EXT_SECRET = '38a6daf0-a718-4456-938f-c6ab2ad03456'

    OAUTH_PAGE_URI = 'http://d.soopro.com/#/oauth'
    OAUTH_TOKEN_API_URI = 'http://api.soopro.com/oauth/token'
    OAUTH_REDIRECT_URI = 'http://ext.soopro.com/url4/client/#/auth/redirect'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    "testcase": TestCaseConfig,
    'default': DevelopmentConfig
}
