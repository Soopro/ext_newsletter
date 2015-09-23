#coding=utf-8
from __future__ import absolute_import
from .controllers import (newsletter_get_profile, newsletter_set_profile, newsletter_get_post_list,
                          newsletter_get_post, newsletter_add_post, newsletter_update_post,
                          newsletter_delete_post, newsletter_send_post, newsletter_send_test_post,
                          newsletter_get_member_role)


urlpatterns = [
    ("/profile", newsletter_get_profile, "GET"),
    ("/profile", newsletter_set_profile, "POST"),
    ("/posts", newsletter_get_post_list, "GET"),
    ("/post", newsletter_add_post, "POST"),
    ("/post/<post_id>", newsletter_get_post, "GET"),
    ("/post/<post_id>", newsletter_update_post, "PUT"),
    ("/post/<post_id>", newsletter_delete_post, "DELETE"),
    ("/post/<post_id>/send", newsletter_send_post, "POST"),
    ("/post/<post_id>/send_test", newsletter_send_test_post, "POST"),
    ("/member_role", newsletter_get_member_role, "GET")
]