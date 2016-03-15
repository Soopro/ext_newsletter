# coding=utf-8
from __future__ import absolute_import

from flask import Blueprint, current_app
from .models import Profile, Post, History
from .routes import urlpatterns
from apiresps import APIError
from utils.api_utils import make_json_response
from utils.helpers import route_inject
from ..helpers import verify_token


bp_name = "newsletter"

blueprint = Blueprint(bp_name, __name__)

route_inject(blueprint, urlpatterns)

model_list = [Profile, Post, History]


@blueprint.before_app_first_request
def before_first_request():
    current_app.mongodb_database.register(model_list)


@blueprint.before_request
def before_request():
    verify_token()


@blueprint.errorhandler(APIError)
def blueprint_api_err(err):
    return make_json_response(err)
