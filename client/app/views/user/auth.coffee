angular.module "newsletterClient"

.controller "AuthCtrl", [
  "$scope"
  "restAPI"
  "$route"
  "$routeParams"
  "$location"
  "$window"
  "Auth"
  "Config"
  (
    $scope
    restAPI
    $route
    $routeParams
    $location
    $window
    Auth
    Config

  ) ->

    getToken = ->
      if $routeParams.open_id
        open_id = $routeParams.open_id
        Auth.cleanAuth()
				Auth.setOpenId()
				
        restAPI.ext_token.get({open_id: open_id})
	        .$promise
	        .then (data) ->
	          if data.state
	            redirect_uri = encodeURIComponent(data.redirect_uri)

	            $window.location = data.auth_uri +
	              '?open_id=' + open_id +
	              '&state=' + data.state +
	              '&app_key=' + data.app_key +
	              '&response_type=' + data.response_type +
	              '&redirect_uri=' + redirect_uri
		       .catch (data) ->
	          console.error(data)
      else
        alert "open_id is required!"

    ext_token = Auth.getToken()
		
    if !ext_token
      getToken()
    else
      console.log("isLogin")
      restAPI.token_check.post({},{ext_token: ext_token})
	      .$promise
	      .then (data) ->
	        if data.error
	            getToken()
	        else
	          $location.url('/')
]