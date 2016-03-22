angular.module("newsletter")

.controller("profileCtrl", [
  "$scope", 
  "restNL", 
  "$location",
  "fsv",
  
  function(
    $scope, 
    restNL,
    $location,
    fsv
  ) {
    $scope.profile = restNL.profile.get();
    $scope.save_profile = function() {
      if (fsv($scope.profile_form, ['host', 'port', 'email', 'use_tls'])){
        $scope.profile.$save();
      }
    };
    
    $scope.jump_to = function(route){
      $location.path(route);
    };
  }
]);

