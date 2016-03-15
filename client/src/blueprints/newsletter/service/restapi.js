angular.module('newsletter')

.factory('restNL', [
  'supResource',
  'Config',

  function (
    supResource,
    Config
  ){
    'use strict';
  
    var api = Config.baseURL.api;
    

    var res = {
      profile: supResource(api+"/profile"),
      posts: supResource(api+"/posts/:post_id"),
      mail: supResource(api+"/posts/:post_id/mail"),
      mailTest: supResource(api+"/posts/:post_id/mail_test"),
      memberRoles: supResource(api+"/member_roles")
    };
  
    return res;
  }
])
