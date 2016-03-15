angular.module("newsletter")

.controller("postCtrl", [
  "$rootScope", 
  "$scope", 
  "restNL", 
  "$route", 
  "$routeParams", 
  "$location", 
  function(
    $rootScope, 
    $scope, 
    restNL, 
    $route,
    $routeParams, 
    $location
  ) {
    var post_id;
    post_id = $routeParams.post_id;
    $scope.is_new = post_id === 'new' ? true : false;
    post_id = null;
    if (!$scope.is_new) {
      post_id = $routeParams.post_id;
      $scope.post = restNL.posts.get({
        post_id: post_id
      });
    } else {
      $scope.post = new restNL.posts();
    }
    $scope.role_list = restNL.memberRoles.query();
    $scope.send_test_post = function() {
      return restNL.mailTest.save({
        post_id: post_id
      }, {
        test_mail: $scope.test_email
      });
    };
    $scope.send_post = function() {
      console.log($scope.selected_role);
      return restNL.mail.save({
        post_id: post_id
      }, {
        selected_role: $scope.selected_role
      });
    };
    $scope.save_post = function() {
      $scope.post.$save({post_id: $scope.post.id});
      return $location.path("/newsletter/posts");
    };
    $scope.delete_post = function() {
      $scope.post.$delete({post_id: $scope.post.id});
      return $location.path("/newsletter/posts");
    };
    
    $scope.jump_to = function(route){
      $location.path(route);
    };
  }
]);
