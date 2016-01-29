#coding=utf-8
from __future__ import absolute_import

from flask import Blueprint, request, current_app
from .models import NewsletterProfile, NewsletterPost, NewsletterHistory
from .routes import urlpatterns
from errors.base_errors import APIError
from utils.base_utils import make_json_response, route_inject
from utils.request import verify_token


bp_name = "newsletter"

blueprint = Blueprint(bp_name, __name__)

route_inject(blueprint, urlpatterns)

model_list = [NewsletterProfile, NewsletterPost, NewsletterHistory]


@blueprint.before_app_first_request
def before_first_request():
    current_app.mongodb_database.register(model_list)


@blueprint.before_request
def before_request():
    verify_token(current_app.config.get("DEBUG"))


@blueprint.errorhandler(APIError)
def blueprint_api_err(err):
    return make_json_response(err)