angular.module "newsletterClient"

# AUTH
.service "Auth", [
  "$cookie"
  (
    $cookie
  ) ->
    @setToken = (token) ->
      $cookie.put "token", token

    @getToken = ->
      $cookie.get "token"

    @setOpenId = (open_id) ->
      $cookie.put "open_id", open_id

    @getOpenId = ->
      $cookie.get "open_id"

    @cleanAuth = ->
      $cookie.remove "token"
      $cookie.remove "open_id"

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