# coding=utf-8
from mongokit import Document, ObjectId
from utils.helpers import now


NewsletterDeactivated, NewsletterActivated = xrange(2)


class Post(Document):
    __collection__ = "post"

    structure = {
        "open_id": unicode,
        "title": unicode,
        "content": unicode,
        "update_time": int,
    }

    required_fields = [
        "open_id",
        "title",
        "content",
        "update_time"
    ]
    default_values = {
        "update_time": now
    }

    def find_all_by_open_id(self, open_id):
        return self.find({
            "open_id": open_id
        })

    def find_one_by_id_and_open_id(self, id, open_id):
        return self.find_one({
            "_id": ObjectId(id),
            "open_id": open_id
        })


HistoryProcessUnsent, HistoryProcessSending,\
    HistoryProcessSent = xrange(3)


class History(Document):
    __collection__ = "history"

    structure = {
        "open_id": ObjectId,
        "send_history": [
            {
                "member": unicode,
                "send_time": int,
                "process": int,
            }
        ]
    }

    def one_by_post_id(self, post_id):
        return self.one({
            "post_id": post_id
        })


class Profile(Document):
    __collection__ = "profile"

    structure = {
        "open_id": unicode,
        "host": unicode,
        "port": int,
        "username": unicode,
        "use_tls": bool,
    }

    required_fields = ["host", "port", "username", "use_tls"]

    indexes = [
        {
            "fields": ["open_id"],
            "unique": True
        }
    ]

    def find_one_by_open_id(self, open_id):
        return self.find_one({
            "open_id": open_id
        })


class Role(Document):
    __collection__ = "role"

    structure = {
        "open_id": unicode,
        "alias": unicode,
        "title": unicode
    }

    required_fields = ["open_id", "alias", "title"]

    def find_all_by_open_id(self, open_id):
        return self.find({
            "open_id": open_id
        })

    def find_one_by_oid_and_id(self, open_id, id):
        return self.find_one({
            "open_id": open_id,
            "_id": ObjectId(id)
        })

    def find_one_by_oid_and_alias(self, open_id, alias):
        return self.find_one({
            "open_id": open_id,
            "alias": alias
        })


class Member(Document):
    __collection__ = "member"

    structure = {
        "open_id": unicode,
        "login": unicode,
        "name": unicode,
        "email": unicode,
        "mobile": unicode,
        "avatar": unicode,
        "role": unicode
    }

    required_fields = [
        "open_id",
        "login",
        "name",
        "email",
        "mobile",
        "avatar",
        "role"
    ]

    def find_all_by_open_id(self, open_id):
        return self.find({
            "open_id": open_id
        })

    def find_all_by_oid_and_role(self, open_id, role):
        return self.find({
            "open_id": open_id,
            "role": role
        })

    def find_all_by_oid_and_login(self, open_id, login):
        return self.find({
            "open_id": open_id,
            "login": login
        })

    def find_one_by_id(self, id):
        return self.find_one({
            "_id": ObjectId(id)
        })
