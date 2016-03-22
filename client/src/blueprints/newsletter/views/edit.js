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
    $scope.is_sended = false;
    
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
    
    $scope.send_test_post = function(email, password) {
      if (fsv($scope.test_mail_form, ['password', 'test_email'])){
        restNL.mailTest.send({
          post_id: $scope.post.id
        }, {
          test_mail: email,
          password: password
        }).$promise.then(function(data){
          $scope.is_sended = true;
        }).finally(function(){
          $scope.is_sended = false;
        });
      }
    };
    
    // $scope.send_post = function(roles, password) {
    //   restNL.mail.send({
    //     post_id: $scope.post.id
    //   }, {
    //     selected_role: $scope.selected_role,
    //     password: $scope.password
    //   });
    // };
    
    $scope.jump_to = function(route){
      $location.path(route);
    };

  }
]);
