angular.module('newsletter')

.service('Auth', [
  '$cookies',
  'Config',
  
  function(
    $cookies,
    Config
  ){
    'use strict';

    var ext_token = $cookies.get('token') ? $cookies.get('token') : null;

    var hanlder = {
      is_logged: function() {
        return ext_token? true : false;
      },
      set_token: function(token) {
        $cookies.put('token',token)
      },
      get_token: function() {
        if (Config.debug){
          return 'token_for_debug'
        }
        return $cookies.get('token')
      },
      set_open_id: function(open_id) {
        $cookies.put('open_id', open_id);
      },
      get_open_id: function() {
        return $cookies.get('open_id')
      },
      clean: function() {
        $cookies.remove('token')
  			$cookies.remove('open_id')
      }
    }
    return hanlder;
  }
])
