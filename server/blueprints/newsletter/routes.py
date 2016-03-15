# coding=utf-8
from __future__ import absolute_import
from .controllers import *


urlpatterns = [
    ("/profile", get_profile, "GET"),
    ("/profile", create_profile, "POST"),
    ("/profile", update_profile, "PUT"),
    ("/post", get_posts, "GET"),
    ("/post", create_post, "POST"),
    ("/post/<post_id>", get_post, "GET"),
    ("/post/<post_id>", update_post, "PUT"),
    ("/post/<post_id>", delete_post, "DELETE"),
         
    ("/posts/<post_id>/mail", send_post, "POST"),
    ("/posts/<post_id>/mail_test", send_test_post, "POST"),

    ("/member_roles", get_member_role, "GET")
]
