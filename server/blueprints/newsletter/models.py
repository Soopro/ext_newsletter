# coding=utf-8
from mongokit import Document, ObjectId
from datetime import datetime


NewsletterDeactivated, NewsletterActivated = xrange(2)


class Post(Document):
    __collection__ = "post"

    structure = {
        "open_id": unicode,
        "title": unicode,
        "content": unicode,
        "update_time": datetime,
    }

    required_fields = [
        "open_id",
        "title",
        "content",
        "update_time"
    ]
    default_values = {
        "update_time": datetime.utcnow
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
