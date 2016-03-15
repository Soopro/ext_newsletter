# coding=utf-8
from __future__ import absolute_import

from flask import Blueprint, request, current_app

from apiresps import APIError

from utils.helpers import route_inject
from utils.api_utils import make_json_response

from .models import User
from .routes import urlpatterns

from ..helpers import verify_token

bp_name = "user"

open_api_endpoints = [
    "{}.get_new_ext_token".format(bp_name),
    "{}.get_sup_token".format(bp_name),
    "{}.token_check".format(bp_name)
]

blueprint = Blueprint(bp_name, __name__)

route_inject(blueprint, urlpatterns)


@blueprint.before_app_first_request
def before_first_request():
    current_app.mongodb_database.register(User)


@blueprint.before_request
def before_request():
    if request.endpoint in open_api_endpoints:
        pass
    else:
        verify_token()


@blueprint.errorhandler(APIError)
def blueprint_api_err(err):
    return make_json_response(err)
