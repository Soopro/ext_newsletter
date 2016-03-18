angular.module('newsletter')

.controller('authRedirectCtrl', [
  '$routeParams',
  '$location',
  'Auth',
  'restUser',
  'Config',

  function(
    $routeParams,
    $location,
    Auth,
    restUser,
    Config
  ){
    'use strict';

    if ($routeParams.code && $routeParams.state) {
      console.log($routeParams.code)
      console.log($routeParams.state)
      var params = {
        code: $routeParams.code,
        open_id: Auth.get_open_id(),
        state: $routeParams.state
      }
      var auth = new restUser.auth(params)
      
      auth.$access()
      .then(function (data) {
        console.log(data);
        Auth.set_token(data.ext_token);
        $location.path(Config.route.index);
      })
    } else {
      console.error("code and state is required!")
      $location.path(Config.route.error)
    }
  }
])
