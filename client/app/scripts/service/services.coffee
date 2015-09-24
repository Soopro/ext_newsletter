angular.module "newsletterClient"

# AUTH
.service "Auth", [
  "$cookieStore"
  (
    $cookieStore
  ) ->
    @set_token = (token) ->
      $cookieStore.put "newsletter_token", token

    @get_token = ->
      $cookieStore.get "newsletter_token"

    @set_user = (user) ->
      $cookieStore.put "newsletter_open_id", user

    @get_user = ->
      $cookieStore.get "newsletter_open_id"

    @clean_auth = ->
      $cookieStore.remove "newsletter_token"
      $cookieStore.remove "newsletter_open_id"

    return @	# don"t forget!
]

.factory "restAPI", [
  "supResource"
  "Config"
  (
    supResource
    Config
  ) ->
    ext_api = "#{Config.api}/newsletter"
    auth_api = "#{Config.api}/user"

    profile: do ->
      supResource "#{ext_api}/profile"

    posts: do ->
      supResource "#{ext_api}/posts"

    post: do ->
      supResource "#{ext_api}/post/:post_id",
        "post_id":"@id"

    send_test_post: do ->
      supResource "#{ext_api}/post/:post_id/send_test"

    send_post: do ->
      supResource "#{ext_api}/post/:post_id/send"

    ext_token: do ->
      supResource "#{auth_api}/ext_token/:open_id"

    sup_auth: do ->
      supResource "#{auth_api}/sup_auth"

    token_check: do ->
      supResource "#{auth_api}/token_check"

    role_list: do ->
      supResource "#{ext_api}/member_role"
]