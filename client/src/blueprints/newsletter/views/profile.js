angular.module("newsletter")

.controller("profileCtrl", [
  "$scope", 
  "restNL", 
  "$location",
  function(
    $scope, 
    restNL,
    $location
  ) {
    $scope.profile = restNL.profile.get();
    $scope.save_profile = function() {
      console.log('save profile');
      console.log($scope.profile);
      $scope.profile.$save();
    };
    
    $scope.jump_to = function(route){
      $location.path(route);
    };
  }
]);

