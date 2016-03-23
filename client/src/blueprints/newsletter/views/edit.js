angular.module("newsletter")

.controller("postCtrl", [
  "$rootScope", 
  "$scope", 
  "restNL", 
  "$route", 
  "$routeParams", 
  "$location", 
  "$mdDialog",
  "fsv",
  
  function(
    $rootScope, 
    $scope, 
    restNL, 
    $route,
    $routeParams, 
    $location,
    $mdDialog,
    fsv
  ) {
    var post_id = $routeParams.post_id;
    
    $scope.is_submitted = false;
    
    if(post_id === 'new'){
      $scope.is_new = true;
      post_id = null;
      $scope.post = new restNL.posts();
    } else {
      $scope.is_new = false;
      $scope.post = restNL.posts.get({post_id: post_id});
    }
    
    $scope.save_post = function() {
      if (fsv($scope.post_form, ['title', 'content'])){
        $scope.post.$save({post_id: $scope.post.id}).then(function(data){
          $scope.is_submitted = true;
          if($scope.is_new){
            $location.path("/newsletter/edit_post/" + data.id);
          }
        }).finally(function(){
          $scope.is_submitted = false;
        });
      }
    };
    
    $scope.delete_post = function() {
      $scope.post.$delete({post_id: $scope.post.id});
      $location.path("/newsletter/posts");
    };
    
    $scope.jump_to = function(route){
      console.log("jump to:" + route);
      $location.path(route);
    };

  }
]);
