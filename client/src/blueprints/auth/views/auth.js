angular.module('newsletter')

.controller('authCtrl', [
  '$scope',
  '$window',
  '$location',
  '$routeParams',
  'Auth',
  'restUser',
  'Config',

  function(
    $scope,
    $window,
    $location,
    $routeParams,
    Auth,
    restUser,
    Config
  ){
    'use strict';

    $scope.open_id = $routeParams.open_id;
    if (!$scope.open_id || typeof($scope.open_id) != 'string'){
      console.error('Open id is required!')
      $location.path(Config.route.error)
      return;
    }

    // get remote redirect info from ext server.
    function get_token (open_id) {
      if (open_id) {
        
        Auth.clean();
        Auth.set_open_id(open_id);
        
        var auth = new restUser.auth({open_id: open_id})
        
        auth.$get()
        .then(function (data) {
          if (data.state) {
            $window.location = data.auth_uri +
            '?open_id=' + open_id +
            '&state=' + data.state +
            '&ext_key=' + data.ext_key +
            '&response_type=' + data.response_type +
            '&redirect_uri=' + encodeURIComponent(data.redirect_uri);
          }
        })
				.catch(function (data) {
					console.error(data)
          $location.path(Config.route.error)
				})
      }
    };
    
    // get current token from cookie
    var ext_token = Auth.get_token();

    if (!ext_token) {
      get_token($scope.open_id)
    } else {
      var token = new restUser.checker({
        open_id: $scope.open_id
      })
      token.$check()
      .then(function (data){
        if (data.result) {
          $location.url(Config.route.index)
        } else {
          get_token()
        }
      })
    }
  }
])
