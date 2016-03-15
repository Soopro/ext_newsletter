angular.module("newsletter")

.controller("postsCtrl", [
  "$rootScope", 
  "$scope", 
  "$route", 
  "$location", 
  "restNL", 
  function(
    $rootScope, 
    $scope, 
    $route, 
    $location, 
    restNL
  ) {
    $scope.posts = restNL.posts.query();
    console.log($scope.posts)
    $scope.open_post = function(post_id) {
      $location.path("/newsletter/edit_post/" + post_id);
    };
    
    $scope.jump_to = function(route){
      $location.path(route);
    };
  }
]);
