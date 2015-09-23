#coding=utf-8
from flask import current_app, g, request
from mongokit import ObjectId
import requests

from errors.bp_newsletter_errors import *
from errors.bp_users_errors import SooproAPIError
from utils.base_utils import output_json
from utils.request import parse_json


@output_json
def newsletter_get_profile():
    user = g.current_user
    open_id = user.get("open_id")
    profile = current_app.mongodb_conn.NewsletterProfile.find_one_by_open_id(open_id)
    if profile is None:
        profile = current_app.mongodb_conn.NewsletterProfile()

    return profile


@output_json
def newsletter_set_profile():
    req = parse_json()
    host, port, username, passwd, use_tls = req.get_params("host", "port", "username", "passwd", "use_tls")
    user = g.current_user
    open_id = user.get('open_id')

    if not use_tls:
        use_tls = False

    profile = current_app.mongodb_conn.NewsletterProfile.find_one_by_open_id(open_id)
    if profile is None:
        profile = current_app.mongodb_conn.NewsletterProfile()
        profile["open_id"] = open_id
    profile["host"] = host
    profile["port"] = port
    profile["username"] = username
    profile["passwd"] = passwd
    profile["use_tls"] = use_tls
    profile.save()
    return profile


@output_json
def newsletter_get_post_list():
    user = g.current_user
    open_id = user.get('open_id')

    posts = current_app.mongodb_conn.NewsletterPost.find({"open_id": open_id})
    out_data = list(posts)
    # histroy
    for post in out_data:
        post["send_history"] = []
    return out_data


@output_json
def newsletter_add_post():
    user = g.current_user
    open_id = user.get('open_id')
    req = parse_json()

    title, content = req.get_required_params("title", "content")
    post = current_app.mongodb_conn.NewsletterPost()
    post["open_id"] = open_id
    post["title"] = title
    post["content"] = content
    try:
        post.save()
    except Exception as e:
        current_app.logger.error(e)
        raise ErrExtNewsletterPostMongoDBErr
    return output_post(post)


@output_json
def newsletter_get_post(post_id):
    user = g.current_user
    open_id = user.get('open_id')

    post_id = ObjectId(post_id)
    post = current_app.mongodb_conn.NewsletterPost.find_one_by_post_id(post_id)
    if post is None:
        raise ErrExtNewsletterPostNotFound
    # history = current_app.mongodb_conn.NewsletterHistory.one_by_post_id(post_id)
    return output_post(post)


@output_json
def newsletter_update_post(post_id):
    user = g.current_user
    open_id = user.get('open_id')
    profile = current_app.mongodb_conn.NewsletterProfile.find_one_by_open_id(open_id)
    if profile is None:
        raise ErrExtNewsletterProfileNotFound

    req = parse_json()
    title, content = req.get_required_params("title", "content")

    post = current_app.mongodb_conn.NewsletterPost.find_one_by_post_id(post_id)
    if post is None:
        raise ErrExtNewsletterPostNotFound

    post["title"] = title
    post["content"] = content
    try:
        post.save()
    except Exception as e:
        current_app.logger.error(e)
        raise ErrExtNewsletterPostMongoDBErr
    return post


@output_json
def newsletter_delete_post(post_id):
    user = g.current_user
    open_id = user.get('open_id')
    profile = current_app.mongodb_conn.NewsletterProfile.find_one_by_open_id(open_id)
    if profile is None:
        raise ErrExtNewsletterProfileNotFound

    post_id = ObjectId(post_id)

    post = current_app.mongodb_conn.NewsletterPost.find_one_by_post_id(post_id)
    if post is None:
        raise ErrExtNewsletterPostNotFound

    try:
        post.delete()
    except Exception as e:
        current_app.logger.error(e)
        raise ErrExtNewsletterPostMongoDBErr
    return {"_id": post_id}


@output_json
def newsletter_send_post(post_id):
    user = g.current_user
    open_id = user.get('open_id')
    print request.json
    profile = current_app.mongodb_conn.NewsletterProfile.find_one_by_open_id(open_id)
    if profile is None:
        raise ErrExtNewsletterProfileNotFound

    post = current_app.mongodb_conn.NewsletterPost.find_one_by_post_id(post_id)
    if post is None:
        raise ErrExtNewsletterPostNotFound

    req = parse_json()
    role_id = req.get_required_params('selected_role').get("id")

    members = _get_member_by_roles(role_id)
    print "members:", members
    to = []
    for member in members:
        print
        to.append(member.get('email'))
    # get email addresses and send emails
    # todo get emails from member ids

    _send_mail(post, profile, to)
    # todo send history

    return post


@output_json
def newsletter_send_test_post(post_id):
    user = g.current_user
    open_id = user.get('open_id')

    post = current_app.mongodb_conn.NewsletterPost.find_one_by_post_id(post_id)
    if post is None:
        raise ErrExtNewsletterPostNotFound

    profile = current_app.mongodb_conn.NewsletterProfile.find_one_by_open_id(open_id)
    print profile
    req = parse_json()
    test_email = [req.get_required_params('test_mail')]
    # get email addresses and send emails
    # if not isinstance(test_emails, list):
    #     raise ErrExtNewsletterInvalidEmailAddresses

    _send_mail(post, profile, test_email)

    return post

@output_json
def newsletter_get_member_role():
    open_id = g.current_user.get('open_id')
    headers={
        "AppKey": current_app.config.get("APP_KEY"),
        "AppSecret": current_app.config.get("APP_SECRET"),
        "Authorization": "Bearer {}".format(g.current_user.get("access_token"))
    }
    get_member_role_url = current_app.config.get("ROLE_URL")
    resp = requests.get(get_member_role_url, headers=headers)
    print resp.json()
    # try:
    #     resp.raise_for_status()
    # except Exception as e:
    #     raise SooproAPIError(e.args[0])

    return resp.json()


def _get_member_by_roles(role_id):
    headers={
        "AppKey": current_app.config.get("APP_KEY"),
        "AppSecret": current_app.config.get("APP_SECRET"),
        "Authorization": "Bearer {}".format(g.current_user.get("access_token"))
    }
    params = {"role_id": role_id}
    get_member_url = current_app.config.get("MEMBER_URL")
    resp = requests.get(get_member_url, headers=headers)
    return resp.json()


def _send_mail(post, profile, to_email_list):
    mail = {
        "host": profile["host"],
        "port": profile["port"],
        "username": profile["username"],
        "passwd": profile["passwd"],
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
        raise ErrExtNewsletterSendErr


def output_post(post):
    return {
        "id": post["_id"],
        "title": post["title"],
        "content": post["content"],
    }