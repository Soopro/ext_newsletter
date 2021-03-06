# coding=utf-8
from __future__ import absolute_import
from .controllers import *


urlpatterns = [
    ("/profile", get_profile, "GET"),
    ("/profile", create_profile, "POST"),
    ("/profile", update_profile, "PUT"),
    ("/posts", get_posts, "GET"),
    ("/posts", create_post, "POST"),
    ("/posts/<post_id>", get_post, "GET"),
    ("/posts/<post_id>", update_post, "PUT"),
    ("/posts/<post_id>", delete_post, "DELETE"),

    ("/posts/<post_id>/mail", send_post, "POST"),
    ("/posts/<post_id>/mail_test", send_test_post, "POST"),

    ("/member_roles", get_member_roles, "GET"),
    ("/member_roles", update_member_roles, "POST")
]
