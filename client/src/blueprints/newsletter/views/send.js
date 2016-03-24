angular.module("newsletter")

.controller("sendCtrl", [
  "$scope", 
  "restNL", 
  "$timeout",
  "$location",
  "$routeParams", 
  "extManager",
  "fsv",
  
  function(
    $scope, 
    restNL,
    $timeout,
    $location,
    $routeParams,
    extManager,
    fsv
  ) {
    var post_id = $routeParams.post_id;
    var all_roles = {alias: 'all', title: 'Send To All'}
    var role_list;
    
    function init(){
      role_list = restNL.memberRoles.query();
      $scope.select_role = all_roles;
      $scope.roles = null;
    };
    init();
    
    $scope.loadRoles = function() {
      // Use timeout to simulate a 650ms request.
      return $timeout(function() {
        $scope.roles =  $scope.roles || (function() {
          var _i, _results;
          _results = [];
          for (_i = 0, _len = role_list.length; _i < _len; _i++) {
            _results.push(role_list[_i]);
          }
          _results.push(all_roles);
          return _results;
        })();
      }, 650);
    };
    
    
    $scope.is_updating = false;
    $scope.is_published = false;
    $scope.is_sended = false;
    $scope.password = '';
    
    $scope.send_test_post = function(email, password) {
      if (fsv($scope.test_mail_form, ['password', 'test_email'])){
        $scope.is_sended = true;
        restNL.mailTest.send({
          post_id: post_id
        }, {
          test_mail: email,
          password: password
        }).$promise.then(function(data){
          extManager.flash('Successfully. Check it out in your email.')
        }).finally(function(){
          $scope.is_sended = false;
        });
      }
    };
    
    $scope.send_post = function(roles, password) {
      if (fsv($scope.test_mail_form, ['password', 'select_role'])){
        var selected_roles;
        if ($scope.selected_role.alias === "all"){
          selected_roles = (function() {
            var _i, _results;
            _results = [];
            for (_i = 0, _len = role_list.length; _i < _len; _i++) {
              _results.push(role_list[_i].alias);
            }
            return _results;
          })();
        } else {
          selected_roles = [$scope.selected_role.alias];
        }
        
        $scope.is_sended = true;
        restNL.mail.send({
          post_id: post_id
        }, {
          selected_roles: selected_roles,
          password: $scope.password
        }).$promise.then(function(data){
          extManager.flash('Mails are on the way.')
        }).finally(function(){
          $scope.is_sended = false;
        });
      }
    };
    
    $scope.update_roles = function(){
      $scope.is_updating = true;
      restNL.memberRoles.post().$promise.then(function(data){
        init();
      }).finally(function(){
        $scope.is_updating = false;
      });
    };
    
    $scope.jump_to = function(route){
      $location.path(route);
    };
  }
]);