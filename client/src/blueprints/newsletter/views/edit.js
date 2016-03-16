angular.module("newsletter")

.controller("postCtrl", [
  "$rootScope", 
  "$scope", 
  "restNL", 
  "$route", 
  "$routeParams", 
  "$location", 
  "$mdDialog",
  function(
    $rootScope, 
    $scope, 
    restNL, 
    $route,
    $routeParams, 
    $location,
    $mdDialog
  ) {
    var post_id = $routeParams.post_id;
    if(post_id === 'new'){
      $scope.is_new = true;
      post_id = null;
      $scope.post = new restNL.posts();
    } else {
      $scope.is_new = false;
      $scope.post = restNL.posts.get({post_id: post_id});
    }

    $scope.role_list = restNL.memberRoles.query();
    $scope.save_post = function() {
      $scope.post.$save({post_id: $scope.post.id}).then(function(data){
        if($scope.is_new){
          $location.path("/newsletter/edit_post/" + data.id);
        }
      });
    };
    $scope.delete_post = function() {
      $scope.post.$delete({post_id: $scope.post.id});
      $location.path("/newsletter/posts");
    };
    $scope.send_test_post = function() {
      restNL.mailTest.send({
        post_id: $scope.post.id
      }, {
        test_mail: $scope.test_email,
        password: $scope.password
      });
    };
    $scope.send_post = function() {
      restNL.mail.send({
        post_id: $scope.post.id
      }, {
        selected_role: $scope.selected_role,
        password: $scope.password
      });
    };
    $scope.jump_to = function(route){
      $location.path(route);
    };

  }
]);
