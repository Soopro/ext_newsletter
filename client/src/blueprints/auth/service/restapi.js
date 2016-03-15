angular.module('newsletter')

.factory('restUser', [
  '$resource',
  'Config',

  function (
    $resource,
    Config
  ){
    var api = Config.baseURL.auth_api;
    
    var res = {
      ext_token: $resource(api+"/ext_token/:open_id"),
      sup_auth: $resource(api+"/sup_auth"),
      check: $resource(api+"/check", null, {
        "check": {method: "POST"}
      })
    };
  
    return res;
  }
]);
