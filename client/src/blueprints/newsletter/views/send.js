angular.module("newsletter")

.controller("sendCtrl", [
  "$scope", 
  "restNL", 
  "$location",
  "$routeParams", 
  "fsv",
  
  function(
    $scope, 
    restNL,
    $location,
    $routeParams,
    fsv
  ) {
    $scope.is_published = false;
    $scope.is_sended = false;
    $scope.password = '';
    
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