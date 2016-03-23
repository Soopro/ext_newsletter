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
    $scope.user = null;
    $scope.users = null;
    $scope.loadUsers = function() {
      // Use timeout to simulate a 650ms request.
      return $timeout(function() {
        $scope.users =  $scope.users  || [
          { id: 1, name: 'Scooby Doo' },
          { id: 2, name: 'Shaggy Rodgers' },
          { id: 3, name: 'Fred Jones' },
          { id: 4, name: 'Daphne Blake' },
          { id: 5, name: 'Velma Dinkley' }
        ];
      }, 650);
    };
    
    
    
    
    
    $scope.is_published = false;
    $scope.is_sended = false;
    $scope.password = '';
    
    $scope.role_list = restNL.memberRoles.query();
    console.log($scope.role_list)
    
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