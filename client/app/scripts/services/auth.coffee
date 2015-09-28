angular.module "newsletterClient"

# AUTH
.service "Auth", [
  "$cookies"
  (
    $cookies
  ) ->
    @setToken = (token) ->
      $cookies.put "token", token

    @getToken = ->
      $cookies.get "token"

    @setOpenId = (open_id) ->
      $cookies.put "open_id", open_id

    @getOpenId = ->
      $cookies.get "open_id"

    @cleanAuth = ->
      $cookies.remove "token"
      $cookies.remove "open_id"

    return @	# don"t forget!
]
