'use strict';

/**
 * @ngdoc function
 * @name url4Client.controller:RedirectCtrl
 * @description
 * # RedirectCtrl
 * Controller of the url4Client
 */
angular.module('newsletter')
  .controller('RedirectCtrl', function ($routeParams, Auth, restAPI, $location) {
    if ($routeParams.code && $routeParams.state) {
      var params = {
        code: $routeParams.code,
        open_id: Auth.getOpenId(),
        state: $routeParams.state
      };
      console.log(params)

      restAPI.sup_auth.save({},params)
        .$promise
        .then(function (data) {
          console.log(data);
          Auth.setToken(data.ext_token);
          $location.url("/")
        })
    }
    else {
      alert("code and state is required!")
    }
  });
