# coding=utf-8
from __future__ import absolute_import

from flask import Blueprint, request, current_app
from .models import User
from .routes import urlpatterns
from errors.base_errors import APIError
from utils.base_utils import make_json_response, route_inject
from utils.request import verify_token


bp_name = "user"

user_api_endpoints = [
    "{}.delete_token".format(bp_name)
]

blueprint = Blueprint(bp_name, __name__)

route_inject(blueprint, urlpatterns)


@blueprint.before_app_first_request
def before_first_request():
    current_app.mongodb_database.register(model_list)
    return


@blueprint.before_request
def before_request():
    if request.endpoint in user_api_endpoints:
        verify_token()
    return


@blueprint.errorhandler(APIError)
def blueprint_api_err(err):
    return make_json_response(err)