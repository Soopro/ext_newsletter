angular.module('newsletter')

.factory('restFwd', [
  '$resource',
  'Config',

  function (
    $resource,
    Config
  ){
    'use strict';
  
    var api = Config.baseURL.api;
    

    var res = {
      profile: $resource(api+"/profile"),
      posts: $resource(api+"/posts/:post_id"),
      mail: $resource(api+"/posts/:post_id/mail"),
      mailTest: $resource(api+"/posts/:post_id/mail_test"),
      memberRoles: $resource(api+"/member_roles")
    };
  
    return res;
  }
])
