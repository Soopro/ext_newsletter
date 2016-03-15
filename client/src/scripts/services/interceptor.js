angular.module('newsletter')

.factory('interceptor', [
  '$q',
  '$location',
  'Auth',
  'Config',

  function(
    $q,
    $location,
    Auth,
    Config
  ){
    'use strict';

    var interceptor = {
      request: function (request) {
        request.headers = request.headers || {};
        var token = Auth.get_token()
        if (token) {
          request.headers.Authorization = 'Bearer '+token
        }
        return request;
      },
      response: function (response) {
        return response ? response : $q.when(response)
      },
      responseError: function (rejection) {
        var reject_url = rejection.config.url;
        var is_api_reject = reject_url.indexOf(Config.baseURL.api) == 0;
        if (!is_api_reject){
          console.log ('Request is rejected by remote.')
        } else {
          if (rejection.status == 0 && rejection.data == null){
            $location.path('/404');
            console.error('Error! No connection to server.')
          }
          if (rejection.status == 401) {
            Auth.clean();
            $location.path('/auth');
          }
          if (rejection.data && rejection.data.errmsg
                             && rejection.status != 200){
            console.error(rejection.data)
          }
        }

        
        return $q.reject(rejection);
      }
    };
    return interceptor
  }
])

.config([
  '$httpProvider',

  function(
    $httpProvider
  ){
    $httpProvider.interceptors.push('interceptor');
  }
])
