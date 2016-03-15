# coding=utf-8
from __future__ import absolute_import

from apiresps.errors import (InternalServerError,
                             PermissionDenied,
                             NotFound)


class RequestAccessTokenFailed(InternalServerError):
    status_message = "REQUEST_ACCESS_TOKEN_FAILED"
    response_code = 300001


class RefreshAccessTokenFailed(InternalServerError):
    status_message = "REFRESH_ACCESS_TOKEN_FAILED"
    response_code = 300002


class AccessDenied(InternalServerError):
    status_message = "ACCESS_DENIED"
    response_code = 300003


class RemoteAPIFailed(InternalServerError):
    status_message = "REQUEST_REMOTE_API_FAILED"
    response_code = 300004


class UserNotFound(NotFound):
    status_message = "USER_NOT_FOUND"
    response_code = 300005


class UserStateInvalid(PermissionDenied):
    status_message = "USER_STATE_INVALID"
    response_code = 300006
