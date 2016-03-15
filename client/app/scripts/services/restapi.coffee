angular.module 'newsletter'
.factory 'restAPI', 
  (
    $resource, Config
  ) ->
    api = Config.api
    auth_api = Config.auth_api
    
    profile: do ->
      $resource api+"/profile"
    posts: do ->
      $resource api+"/posts/:post_id"
    mail: do ->
      $resource api+"/posts/:post_id/mail"
    mailTest: do ->
      $resource api+"/posts/:post_id/mail_test"
    memberRoles: do ->
      $resource api+"/member_roles"

    ext_token: do -> 
      $resource auth_api+"/ext_token/:open_id"
    sup_auth: do -> 
      $resource auth_api+"/sup_auth"
    token_check: do -> 
      $resource auth_api+"/token_check"
