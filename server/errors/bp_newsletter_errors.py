#coding=utf-8
from __future__ import absolute_import
import httplib
from .base_errors import APIError


class ErrExtNewsletterProfileNotFound(APIError):
    status_code = httplib.NOT_FOUND
    response_code = 100001
    default_message = "extension profile not found"


class ErrExtNewsletterProfileAlreadyActivated(APIError):
    status_code = httplib.BAD_REQUEST
    response_code = 100002
    default_message = "extension already activated"


class ErrExtNewsletterProfileAlreadyDeactivated(APIError):
    status_code = httplib.BAD_REQUEST
    response_code = 100003
    default_message = "extension already deactivated"


class ErrExtNewsletterProfileMongoDBErr(APIError):
    status_code = httplib.INTERNAL_SERVER_ERROR
    response_code = 100004
    default_message = "interval server error"

class ErrExtNewsletterPostMongoDBErr(APIError):
    status_code = httplib.INTERNAL_SERVER_ERROR
    response_code = 100005
    default_message = "internal server error"


class ErrExtNewsletterPostNotFound(APIError):
    status_code = httplib.NOT_FOUND
    response_code = 100006
    default_message = "post not found"


class ErrExtNewsletterSendErr(APIError):
    status_code = httplib.INTERNAL_SERVER_ERROR
    response_code = 100007
    default_message = "internal server error"


class ErrExtNewsletterInvalidEmailAddresses(APIError):
    status_code = httplib.BAD_REQUEST
    response_code = 100008
    default_message = "invalid_email_addresses"

class ErrExtNewsletterSMTPNotFound(APIError):
    status_code = httplib.NOT_FOUND
    response_code = 100009
    default_message = "extension smtp not found"
