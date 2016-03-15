# coding=utf-8
from flask import current_app, g
from mongokit import ObjectId
import requests

from .errors import *
from utils.api_utils import output_json
from utils.request import get_param


@output_json
def get_profile():
    profile = current_app.mongodb_conn.Profile.\
        find_one_by_open_id(g.curr_user["open_id"])

    return output_profile(profile)


@output_json
def create_profile():
    host = get_param("host", required=True)
    port = get_param("port", required=True)
    username = get_param("username", required=True)
    use_tls = get_param("use_tls", default=False)

    Profile = current_app.mongodb_conn.Profile
    profile = Profile.find_one_by_open_id(g.curr_user["open_id"])
    if profile:
        raise ProfileHasExisted
    profile = Profile()
    profile["open_id"] = g.curr_user["open_id"]
    profile["host"] = host
    profile["port"] = port
    profile["username"] = username
    profile["use_tls"] = use_tls
    profile.save()
    return output_profile(profile)


@output_json
def update_profile():
    host = get_param("host", required=True)
    port = get_param("port", required=True)
    username = get_param("username", required=True)
    use_tls = get_param("use_tls", default=False)

    profile = current_app.mongodb_conn.Profile.\
        find_one_by_open_id(g.curr_user["open_id"])
    if not profile:
        raise ProfileNotFound
    profile["host"] = host
    profile["port"] = port
    profile["username"] = username
    profile["use_tls"] = use_tls
    profile.save()
    return output_profile(profile)


@output_json
def get_posts():
    posts = current_app.mongodb_conn.Post.\
        find_all_by_open_id(g.curr_user["open_id"])
    return [output_post(post) for post in posts]


@output_json
def create_post():
    user = g.curr_user
    open_id = user.get('open_id')

    title = get_param('title', required=True)
    content = get_param('content', required=True)

    post = current_app.mongodb_conn.Post()
    post["open_id"] = open_id
    post["title"] = title
    post["content"] = content
    post.save()
    return output_post(post)


@output_json
def get_post(post_id):
    post = current_app.mongodb_conn.Post.\
        find_one_by_id_and_open_id(post_id, g.curr_user["open_id"])
    if not post:
        raise PostNotFound

    return output_post(post)


@output_json
def update_post(post_id):
    title = get_param('title', required=True)
    content = get_param('content', required=True)

    post = current_app.mongodb_conn.Post.\
        find_one_by_id_and_open_id(post_id, g.curr_user["open_id"])
    if post:
        raise PostNotFound

    post["title"] = title
    post["content"] = content
    post.save()

    return output_post(post)


@output_json
def delete_post(post_id):
    post = current_app.mongodb_conn.Post.\
        find_one_by_id_and_open_id(post_id, g.curr_user["open_id"])
    if not post:
        raise ErrExtPostNotFound

    post.delete()

    return output_post(post)


@output_json
def send_post(post_id):
    profile = current_app.mongodb_conn.Profile.\
        find_one_by_open_id(g.curr_user["open_id"])
    if not profile:
        raise ProfileNotFound

    post = current_app.mongodb_conn.Post.\
        find_one_by_id_and_open_id(post_id, g.curr_user["open_id"])
    if not post:
        raise PostNotFound

    req = parse_json()
    role_id = req.get_required_params('selected_role').get("id")

    members = _get_member_by_roles(role_id)
    print "members:", members
    to = []
    for member in members:
        to.append(member.get('email'))
    # get email addresses and send emails
    # todo get emails from member ids

    _send_mail(post, profile, to)
    # todo send history

    return output_post(post)


@output_json
def send_test_post(post_id):
    test_email = get_param('test_mail', required=True)

    profile = current_app.mongodb_conn.Profile.\
        find_one_by_open_id(g.curr_user["open_id"])
    if not profile:
        raise ProfileNotFound

    post = current_app.mongodb_conn.Post.\
        find_one_by_id_and_open_id(post_id, g.curr_user["open_id"])
    if not post:
        raise PostNotFound

    _send_mail(post, profile, test_email)

    return output_post(post)


@output_json
def get_member_role():
    # headers = {
    #     "AppKey": current_app.config.get("APP_KEY"),
    #     "AppSecret": current_app.config.get("APP_SECRET"),
    #     "Authorization": "Bearer {}".format(
    #         g.curr_user.get("access_token"))
    # }
    # get_member_role_url = current_app.config.get("ROLE_URL")
    # resp = requests.get(get_member_role_url, headers=headers)

    return []


def _get_member_by_roles(role_id):
    # headers = {
    #     "AppKey": current_app.config.get("APP_KEY"),
    #     "AppSecret": current_app.config.get("APP_SECRET"),
    #     "Authorization": "Bearer {}".format(
    #         g.curr_user.get("access_token"))
    # }
    # params = {"role_id": role_id}
    # get_member_url = current_app.config.get("MEMBER_URL")
    # resp = requests.get(get_member_url, headers=headers, params=params)

    return []


def _send_mail(post, profile, to_email_list):
    mail = {
        "host": profile["host"],
        "port": profile["port"],
        "username": profile["username"],
        "use_tls": profile["use_tls"],
        "from": profile["username"],
        "to": to_email_list,
        "subject": post["title"],
        "body": post["content"],
    }
    try:
        current_app.mail_pusher.push_single_mail(mail)
    except Exception as e:
        current_app.logger.error(e)
        raise MailFailed


def output_profile(profile):
    if profile:
        return {
            "id": profile["_id"],
            "open_id": profile["open_id"],
            "host": profile["host"],
            "port": profile["port"],
            "username": profile["username"],
            "use_tls": profile["use_tls"],
        }
    else:
        return {
            "id": u'',
            "open_id": u'',
            "host": u'',
            "port": u'',
            "username": u'',
            "use_tls": u'',
        }


def output_post(post):
    return {
        "id": post["_id"],
        "title": post["title"],
        "content": post["content"],
    }
