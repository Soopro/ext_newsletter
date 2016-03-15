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
    restApi,
    Config
  ){
    'use strict';
    
    var open_id = $routeParams.open_id;
    
    $scope.open_id = open_id

    // get remote redirect info from ext server.
    function get_token () {
      if (open_id) {
        
        Auth.clean();
        Auth.set_open_id(open_id);

        var token = new restApi.ext_token({open_id: open_id})
        
        token.$get()
        .then(function (data) {
          if (data.state) {
            var redirect_uri = encodeURIComponent(data.redirect_uri)
              
            $window.location = data.auth_uri +
            '?open_id=' + open_id +
            '&state=' + data.state +
            '&ext_key=' + data.ext_key +
            '&response_type=' + data.response_type +
            '&redirect_uri=' + redirect_uri;
          }
        })
				.catch(function (data) {
					console.error(data)
				})
      }
    };
    
    // get current token from cookie
    var ext_token = Auth.get_token();

    if (!ext_token) {
      get_token()
    } else {
      var token = new restApi.check({
        ext_token: ext_token
      })
      token.$check()
      .then(function (data){
        if (data.error) {
          get_token()
        } else {
          $location.url('/newsletter')
        }
      })
    }
  }
])
