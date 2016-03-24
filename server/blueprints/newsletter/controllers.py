# coding=utf-8
from __future__ import absolute_import

from flask import current_app, g
from .errors import *
from utils.api_utils import output_json
from utils.request import get_param
from utils.helpers import now
from services.mail import MailSender
from apiresps.validations import Struct


@output_json
def get_profile():
    profile = current_app.mongodb_conn.Profile.\
        find_one_by_open_id(g.curr_user["open_id"])

    return output_profile(profile)


@output_json
def create_profile():
    host = get_param("host", Struct.Domain, required=True)
    port = get_param("port", Struct.Int, required=True)
    username = get_param("username", Struct.Email, required=True)
    use_tls = get_param("use_tls", Struct.Bool, default=False)

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
    host = get_param("host", Struct.Domain, required=True)
    port = get_param("port", Struct.Int, required=True)
    username = get_param("username", Struct.Email, required=True)
    use_tls = get_param("use_tls", Struct.Bool, default=False)

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
    posts = [output_post(post) for post in posts]
    return posts


@output_json
def create_post():
    user = g.curr_user
    open_id = user.get('open_id')

    title = get_param('title', Struct.Attr, required=True)
    content = get_param('content', Struct.Text, required=True)

    post = current_app.mongodb_conn.Post()
    post["open_id"] = open_id
    post["title"] = title
    post["content"] = content
    post.save()
    return output_post(post)


@output_json
def get_post(post_id):
    Struct.ObjectId(post_id)
    post = current_app.mongodb_conn.Post.\
        find_one_by_id_and_open_id(post_id, g.curr_user["open_id"])
    if not post:
        raise PostNotFound

    return output_post(post)


@output_json
def update_post(post_id):
    Struct.ObjectId(post_id)
    title = get_param('title', Struct.Attr, required=True)
    content = get_param('content', Struct.Text, required=True)

    post = current_app.mongodb_conn.Post.\
        find_one_by_id_and_open_id(post_id, g.curr_user["open_id"])
    if not post:
        raise PostNotFound

    post["title"] = title
    post["content"] = content
    post["update_time"] = now()
    post.save()

    return output_post(post)


@output_json
def delete_post(post_id):
    Struct.ObjectId(post_id)
    post = current_app.mongodb_conn.Post.\
        find_one_by_id_and_open_id(post_id, g.curr_user["open_id"])
    if not post:
        raise ErrExtPostNotFound

    post.delete()

    return output_post(post)


@output_json
def send_post(post_id):
    Struct.ObjectId(post_id)
    roles = get_param('selected_roles', Struct.ObjectId, required=True)
    password = get_param('password', Struct.Pwd, required=True)

    profile = current_app.mongodb_conn.Profile.\
        find_one_by_open_id(g.curr_user["open_id"])
    if not profile:
        raise ProfileNotFound

    post = current_app.mongodb_conn.Post.\
        find_one_by_id_and_open_id(post_id, g.curr_user["open_id"])
    if not post:
        raise PostNotFound

    to = []
    for role in roles:
        to.extend(_get_member_email_by_role(role))

    if to:
        _send_mail(post, profile, password, to)

    return output_post(post)


@output_json
def send_test_post(post_id):
    Struct.ObjectId(post_id)
    test_email = get_param('test_mail', Struct.Email, required=True)
    password = get_param('password', Struct.Pwd, required=True)

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
def get_member_roles():
    roles = current_app.mongodb_conn.Role.\
        find_all_by_open_id(g.curr_user["open_id"])

    return [output_role(role) for role in roles]


@output_json
def update_member_roles():
    open_id = g.curr_user["open_id"]

    roles = _get_all_roles()
    # print roles
    if isinstance(roles, list):
        Role = current_app.mongodb_conn.Role

        local_roles = Role.find_all_by_open_id(open_id)
        for role in local_roles:
            role.delete()

        for role in roles:
            r = Role()
            r["open_id"] = open_id
            r["alias"] = role["alias"]
            r["title"] = role["title"]
            r.save()
    else:
        raise RoleGetFailed

    members = _get_all_members()
    # print members
    Member = current_app.mongodb_conn.Member
    for member in members:
        m = Member.find_all_by_oid_and_login(open_id, login)
        if not m:
            m = Member()
            m["open_id"] = open_id
            m["login"] = member["login"]
        m["name"] = member["login"]
        m["email"] = member["email"]
        m["mobile"] = member["mobile"]
        m["avatar"] = member["avatar"]
        m["role"] = member["role"]
        m.save()

    return {
        "roles": [output_role(role) for role in roles]
    }


def _get_all_roles():
    try:
        roles = current_app.sup_oauth.get_roles(g.curr_user["access_token"])
    except:
        raise RoleGetFailed
    return roles


def _get_all_members():
    offset = 0
    ONCE_AMOUNT = 100
    members = []

    while True:
        member_list = _get_members(offset)
        if not member_list:
            break
        members.extend(member_list)
        offset += ONCE_AMOUNT

    return members


def _get_members(offset, retry=0):
    try:
        members = current_app.sup_oauth.get_members(
            g.curr_user["access_token"], offset=offset)
    except:
        if retry < 3:
            members = _get(offset, retry+1)
        else:
            raise MemberGetFailed
    return members


def _get_member_email_by_role(role):
    members = current_app.mongodb_conn.Member.\
        find_all_by_oid_and_role(g.curr_user["open_id"], role)
    emails = []
    for member in members:
        email = member.get("email")
        if email:
            emails.append(member)
    return emials


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


def output_role(role):
    return {
        "alias": role["alias"],
        "title": role["title"],
    }


# def output_member(member):
#     return {
#         'login': member.get('login'),
#         'name': member.get('name'),
#         'email': member.get('email'),
#         'mobile': member.get('mobile'),
#         'avatar': member.get('avatar'),
#         'role_id': member.get('role_id')
#     }
