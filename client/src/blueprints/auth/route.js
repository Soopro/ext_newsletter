angular.module('newsletter')

.config([
  '$routeProvider',

  function(
    $routeProvider
  ){
    'use strict';
  
    var bp = "auth"
    var dir = "blueprints/auth/views"

    $routeProvider
    .when('/'+bp, {
      templateUrl: dir+'/auth.html',
      controller: 'authCtrl'
    })
    .when('/'+bp+'/redirect', {
      templateUrl: dir+'/redirect.html',
      controller: 'authRedirectCtrl'
    })
  }
])