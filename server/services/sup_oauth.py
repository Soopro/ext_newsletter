# coding=utf-8
from __future__ import absolute_import

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import requests
import json


class SupOAuth(object):
    def __init__(self, ext_key, ext_secret, grant_type, secret_key,
                 token_uri, redirect_uri, expired_in=3600):
        self._s = Serializer(secret_key, expired_in)
        self.ext_key = ext_key
        self.ext_secret = ext_secret
        self.grant_type = grant_type
        self.token_uri = token_uri
        self.redirect_uri = redirect_uri

    def generate_ext_token(self, open_id):
        return self._s.dumps({'open_id': open_id}).decode('utf-8')

    def parse_ext_token(self, token):
        try:
            data = self._s.loads(token)
        except Exception:
            return None
        return data['open_id']

    def get_access_token(self, code):
        payloads = {
            'ext_key': self.ext_key,
            'ext_secret': self.ext_secret,
            'code': code,
            'grant_type': self.grant_type,
            'redirect_uri': self.redirect_uri
        }
        headers = {'content-type': 'application/json'}
        r = requests.post(self.token_uri, 
                          data=json.dumps(payloads),
                          headers=headers)
        return json.loads(r.text)

    def refresh_access_token(self, refresh_token):
        payloads = {
            'ext_key': self.ext_key,
            'ext_secret': self.ext_secret,
            'refresh_token': refresh_token,
            'response_type': "refresh_token",
        }
        headers = {'content-type': 'application/json'}

        r = requests.post(self.token_uri, 
                          data=json.dumps(payloads),
                          headers=headers)
        return json.loads(r.text)
    
    def check_access_token(self, access_token):
        payloads = {
            'ext_key': self.ext_key,
            'ext_secret': self.ext_secret,
            'access_token': access_token,
            'response_type': "access_token",
        }
        headers = {'content-type': 'application/json'}
        r = requests.post(self.token_uri,
                          data=json.dumps(payloads),
                          headers=headers)
        return json.loads(r.text)