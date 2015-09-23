angular.module "newsletterApp"

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