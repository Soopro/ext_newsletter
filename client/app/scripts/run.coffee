angular.module "newsletterClient"

.run [
  "$rootScope"
  "$location"
  "Auth"
  "Config"
  "restAPI"
  (
    $rootScope
    $location
    Auth
    Config
    restAPI
  ) ->

]