angular.module "newsletterApp"

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

    get_token = ->
      if $routeParams.open_id
        $scope.open_id = $routeParams.open_id
        Auth.clean_auth()
        restAPI.ext_token.get
          open_id: $scope.open_id
        .$promise
        .then (cb_data) ->
          if cb_data.state
            Auth.set_user $scope.open_id
            redirect_uri = encodeURIComponent(cb_data.redirect_uri)

            $window.location = Config.sup_auth_uri +
              '?open_id=' + $scope.open_id +
              '&state=' + cb_data.state +
              '&app_key=' + cb_data.app_key +
              '&response_type=' + cb_data.response_type +
              '&redirect_uri=' + redirect_uri
        .catch (cb_data) ->
          console.error(cb_data)
      else
        alert "open_id is required!"

    ext_token = Auth.get_token()
    if !ext_token
      get_token()
    else
      console.log("isLogin")
      restAPI.token_check.post {}
        ,ext_token: ext_token
      .$promise
      .then (cb_data) ->
        if cb_data.error
            get_token()
        else
          $location.url Config.path.default
]