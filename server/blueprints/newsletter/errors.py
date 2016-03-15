# coding=utf-8
from __future__ import absolute_import

from apiresps.errors import (InternalServerError, NotFound)


class ProfileNotFound(NotFound):
    status_message = "PROFILE_NOT_FOUND"
    response_code = 400001


class ProfileHasExisted(InternalServerError):
    status_message = "PROFILE_HAS_EXISTED"
    response_code = 400002


class PostNotFound(NotFound):
    status_message = "POST_NOT_FOUND"
    response_code = 400011


class MailFailed(InternalServerError):
    status_message = "SENDING_MAIL_FAILED"
    response_code = 400021
