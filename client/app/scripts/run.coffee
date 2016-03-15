angular.module "newsletter"

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