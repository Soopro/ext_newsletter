#coding=utf-8
from __future__ import absolute_import
from .controllers import (newsletter_get_profile, newsletter_set_profile, newsletter_get_post_list,
                          newsletter_get_post, newsletter_add_post, newsletter_update_post,
                          newsletter_delete_post, newsletter_send_post, newsletter_send_test_post,
                          newsletter_get_member_role)


urlpatterns = [
    ("/profiles", newsletter_get_profile, "GET"),
    ("/profiles", newsletter_set_profile, "POST"),
    ("/posts", newsletter_get_post_list, "GET"),
    ("/posts", newsletter_add_post, "POST"),
    ("/posts/<post_id>", newsletter_get_post, "GET"),
    ("/posts/<post_id>", newsletter_update_post, "PUT"),
    ("/posts/<post_id>", newsletter_delete_post, "DELETE"),
    
    ("/posts/<post_id>/mail", newsletter_send_post, "POST"),
    ("/posts/<post_id>/mail_test", newsletter_send_test_post, "POST"),

    ("/member_roles", newsletter_get_member_role, "GET")
]