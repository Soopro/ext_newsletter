# coding=utf-8
from __future__ import absolute_import

from mongokit import Document
from utils.helpers import now


class User(Document):
    __collection__ = 'users'

    STATUS_INACTIVATED = 0
    STATUS_ACTIVATED = 1

    use_dot_notation = True

    structure = {
        "open_id": unicode,
        "alias": unicode,
        "display_name": unicode,
        "access_token": unicode,
        "refresh_token": unicode,
        "token_type": unicode,
        "expires_in": int,
        "random_string": unicode,
        "ext_token": unicode,
        "status": int,
        "updated": int,
        "creation": int,
    }

    required_fields = ["open_id", "alias"]

    default_values = {
        "updated": now,
        "creation": now,
        "display_name": u'',
        "access_token": u'',
        "refresh_token": u'',
        "token_type": u'',
        "random_string": u'',
        "ext_token": u'',
        "expires_in": 0,
        "status": STATUS_INACTIVATED,
    }

    def find_one_by_open_id(self, open_id):
        return self.find_one({
            "open_id": open_id
        })

    def find_one_by_alias(self, alias):
        return self.find_one({
            "alias": alias
        })
