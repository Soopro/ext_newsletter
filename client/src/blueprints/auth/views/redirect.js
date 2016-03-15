angular.module('newsletter')

.controller('authRedirectCtrl', [
  '$routeParams',
  '$location',
  'Auth',
  'restApi',

  function(
    $routeParams,
    $location,
    Auth,
    restApi
  ){
    'use strict';

    if ($routeParams.code && $routeParams.state) {
      var params = {
        code: $routeParams.code,
        open_id: Auth.get_open_id(),
        state: $routeParams.state
      };
      console.log(params)

      restApi.sup_auth.save({},params)
      .$promise
      .then(function (data) {
        console.log(data);
        Auth.set_token(data.ext_token);
        $location.url("/")
      })
    } else {
      alert("code and state is required!")
    }
  }
])
