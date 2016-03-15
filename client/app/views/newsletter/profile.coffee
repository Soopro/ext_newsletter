angular.module "newsletter"

.controller "profileCtrl", [
  "$scope"
  "restAPI"
  (
    $scope
    restAPI
  ) ->

    $scope.profile = restAPI.profile.get()

    $scope.update_profile = ()->
      console.log 'update'
      console.log $scope.profile
      $scope.profile.$save()
]