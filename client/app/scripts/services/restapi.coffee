angular.module 'newsletterClient'
.factory 'restAPI', 
  (
    $resource, Config
  ) ->
    api = Config.api
    auth_api = Config.auth_api
    
    profiles: do ->
      $resource api+"/profiles"
    posts: do ->
      $resource api+"/posts/:post_id"
    mail: do ->
      $resource api+"/posts/:post_id/mail"
    mailTest: do ->
      $resource api+"/posts/:post_id/mail_test"
    memberRoles: do ->
      $resource api+"/member_roles"

    ext_token: do -> 
      $resource auth_api+"/sup_auth"
    up_auth: do -> 
      $resource auth_api+"/sup_auth"
    token_check: do -> 
      $resource auth_api+"/token_check"
