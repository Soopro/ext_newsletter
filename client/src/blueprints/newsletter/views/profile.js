angular.module("newsletter")

.controller("profileCtrl", [
  "$scope", 
  "restNL", 
  "$location",
  "extManager",
  "fsv",
  
  function(
    $scope, 
    restNL,
    $location,
    extManager,
    fsv
  ) {
    $scope.is_saved = false;
    
    $scope.profile = restNL.profile.get();
    $scope.save_profile = function() {
      if (fsv($scope.profile_form, ['host', 'port', 'email', 'use_tls'])){
        $scope.is_saved = true;
        $scope.profile.$save().then(function(data){
          extManager.flash('Settings have been saved.')
        }).finally(function(){
          $scope.is_saved = false;
        });
      }
    };
    
    $scope.jump_to = function(route){
      $location.path(route);
    };
  }
]);

