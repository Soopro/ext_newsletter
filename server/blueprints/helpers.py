# coding=utf-8
from __future__ import absolute_import

from flask import current_app, request, g
from apiresps.errors import AuthFailed


def verify_token():
    User = current_app.mongodb_conn.User
    if current_app.debug:
        user = User.find_one()
        if not user:
            user = User()
            user.save()
        g.curr_user = user
    else:
        ext_token = request.headers.get('Authorization')
        if ext_token is None:
            raise AuthFailed('Authorization header was missing')

        open_id = current_app.sup_auth.parse_ext_token(ext_token)

        if not open_id:
            raise AuthFailed('invalid open id')

        current_user = User.find_one_by_open_id(open_id)
        if current_user is None:
            raise AuthFailed("User Not Exist")

        g.curr_user = current_user
