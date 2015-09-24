angular.module "newsletterClient"


.controller "NotifyCtrl", [
  "$scope"
  "restAPI"
  "$routeParams"
  "$location"
  "Auth"
  "Config"
  (
    $scope
    restAPI
    $routeParams
    $location
    Auth
    Config
  ) ->
    console.log("notifyCtrl Start！")
    console.log Auth.get_user()
    if $routeParams.code and $routeParams.state
      params =
        code: $routeParams.code
        open_id: Auth.get_user()
        state: $routeParams.state
      restAPI.sup_auth.post {}
      ,  params
      .$promise
      .then (cb_data) ->
        Auth.set_token cb_data.ext_token
        $location.url Config.path.default
      .catch (cb_data) ->
        console.log cb_data
    else
      alert "code and state is required!"


]