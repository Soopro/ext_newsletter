angular.module('newsletter')

.config([
  '$routeProvider',
  
  function(
    $routeProvider
  ){
    'use strict';

    $routeProvider
    
    .when('/', {
      redirectTo: '/auth'
    })
    
    .when('/dashboard', {
      redirectTo: '/newsletter'
    })
    
    .when('/404', {
      templateUrl: 'blueprints/404.html'
    })
    
    .otherwise({
      redirectTo: '/404'
    });
  }
]);
