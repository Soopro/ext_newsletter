# coding=utf-8
from __future__ import absolute_import

from flask import current_app, g
from .errors import *
from utils.api_utils import output_json
from utils.request import get_param
from datetime import datetime
from services.mail import MailSender


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
    if not post:
        raise PostNotFound

    post["title"] = title
    post["content"] = content
    post["update_time"] = datetime.utcnow()
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
    role_id = get_param('selected_role', required=True)
    password = get_param('password', required=True)

    profile = current_app.mongodb_conn.Profile.\
        find_one_by_open_id(g.curr_user["open_id"])
    if not profile:
        raise ProfileNotFound

    post = current_app.mongodb_conn.Post.\
        find_one_by_id_and_open_id(post_id, g.curr_user["open_id"])
    if not post:
        raise PostNotFound

    members = _get_member_by_roles(role_id)
    print "members:", members
    to = []
    for member in members:
        to.append(member.get('email'))
    # get email addresses and send emails
    # todo get emails from member ids

    _send_mail(post, profile, password, to)
    # todo send history

    return output_post(post)


@output_json
def send_test_post(post_id):
    test_email = get_param('test_mail', required=True)
    password = get_param('password', required=True)

    profile = current_app.mongodb_conn.Profile.\
        find_one_by_open_id(g.curr_user["open_id"])
    if not profile:
        raise ProfileNotFound

    post = current_app.mongodb_conn.Post.\
        find_one_by_id_and_open_id(post_id, g.curr_user["open_id"])
    if not post:
        raise PostNotFound

    _send_mail(post, profile, password, test_email)

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


def _send_mail(post, profile, password, to_email):
    smtp_host = profile["host"]
    smtp_port = profile["port"]
    smtp_user = profile["username"]
    from_email = profile["username"]
    is_with_tls = profile["use_tls"]
    to_email = to_email if isinstance(to_email, list)\
        else [email.strip() for email in to_email.split(',')]
    sender = MailSender(smtp_host, smtp_user, password,
                        smtp_port=smtp_port, is_with_tls=is_with_tls)

    subject = post["title"]
    body = post["content"]
    try:
        sender.send(from_email,
                    to_email,
                    subject,
                    body)
    except Exception as e:
        current_app.logger.error(e)
        raise MailFailed


def output_profile(profile):
    return {
        "id": profile["_id"],
        "open_id": profile["open_id"],
        "host": profile["host"],
        "port": profile["port"],
        "username": profile["username"],
        "use_tls": profile["use_tls"],
    } if profile else {
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
        "update_time": post["update_time"]
    }
