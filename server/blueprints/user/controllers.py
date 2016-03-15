# coding=utf-8
from __future__ import absolute_import

from flask import current_app, g

import uuid
from utils.helpers import now
from utils.api_utils import output_json
from utils.request import get_param

from apiresps.validations import Struct

from .errors import (RequestAccessTokenFailed,
                     RemoteAPIFailed,
                     UserStateInvalid,
                     UserNotFound)


@output_json
def get_new_ext_token(open_id):
    Struct.ObjectId(open_id)

    User = current_app.mongodb_conn.User

    user = User.find_one_by_open_id(open_id)

    if not user:
        user = User()
        user['open_id'] = open_id
        user['status'] = User.STATUS_INACTIVATED
        # user['alias'] = open_id # TODO alias

    ext_key = current_app.config.get('EXT_KEY')
    state = unicode(uuid.uuid4())

    user['random_string'] = state
    user['expires_in'] = 0
    user.save()

    oauth_uri = current_app.config.get('OAUTH_PAGE_URI')
    redirect_uri = current_app.config.get('OAUTH_REDIRECT_URI')

    # print user
    return {
        'state': state,
        'auth_uri': oauth_uri,
        'ext_key': ext_key,
        'response_type': 'code',
        'redirect_uri': redirect_uri
    }


@output_json
def get_sup_token():
    open_id = get_param('open_id', Struct.ID, True)
    state = get_param('state', Struct.Attr, True)
    code = get_param('code', Struct.Attr, True)

    user = current_app.mongodb_conn.User.find_one_by_open_id(open_id)
    if not user:
        raise UserNotFound

    if user.get('random_string') != state:
        raise UserStateInvalid

    if not user['access_token']:
        try:
            resp = current_app.sup_auth.get_access_token(code)
        except Exception:
            raise RequestAccessTokenFailed
    else:
        if user['expires_in'] < now():
            try:
                resp = current_app.sup_auth.\
                            refresh_access_token(user['refresh_token'])
                if 'access_token' not in resp:
                    resp = current_app.sup_auth.get_access_token(code)
            except Exception:
                raise RequestAccessTokenFailed

    if 'access_token' not in resp:
        raise RemoteAPIFailed

    user['access_token'] = resp['access_token']
    user['refresh_token'] = resp['refresh_token']
    user['expires_in'] = resp['expires_in']
    user['display_name'] = u''  # TODO display name
    user['ext_token'] = current_app.sup_auth.generate_ext_token(open_id)
    user.save()

    return {
        "id": user['_id'],
        "display_name": user['display_name'],
        "alias": user['alias'],
        "status": user['status'],
        "ext_token": user['ext_token']
    }


@output_json
def get_alias():
    user = g.curr_user
    return {
        "open_id": user['open_id'],
        "alias": user['alias']
    }


@output_json
def set_alias():
    alias = get_param("alias", Struct.Alias, True)

    user = g.curr_user

    user = current_app.mongodb_conn.User.find_one_by_alias(alias)
    if not user:
        raise UserNotFound

    user["alias"] = alias
    user.save()

    return {
        "open_id": user['open_id'],
        "alias": user['alias']
    }


@output_json
def token_check():
    ext_token = get_param('ext_token', Struct.Token, True)

    open_id = current_app.sup_auth.parse_ext_token(ext_token)
    user = current_app.mongodb_conn.User.find_one_by_open_id(open_id)

    return {
        'result': bool(user)
    }
