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
    
    $scope.post_id = $routeParams.post_id;
    var all_roles = {alias: 'all', title: 'Send To All'}
    var role_list;
    
    function init(){
      role_list = restNL.memberRoles.query();
      $scope.selected_role = all_roles;
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
    $scope.is_sended = false;
    $scope.password = '';
    $scope.test_email = '';
    
    $scope.send_func = [
      {
        name: "Send Test Post",
        is_published: false
      },
      {
        name: "Send Post by Role",
        is_published: true
      },
    ];
    
    $scope.selected_func = $scope.send_func[0];
    
    $scope.send = function(){
      if($scope.selected_func.is_published){
        send_post($scope.selected_role, $scope.password);
      } else {
        send_test_post($scope.test_email, $scope.password);
      }
    };
    
    var send_test_post = function(email, password) {
      if (fsv($scope.mail_form, ['test_email', 'password'])){
        $scope.is_sended = true;
        restNL.mailTest.send({
          post_id: $scope.post_id
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
    
    var send_post = function(roles, password) {
      if (fsv($scope.mail_form, ['password'])){
        var selected_roles;
        if (roles.alias === "all"){
          selected_roles = (function() {
            var _i, _results;
            _results = [];
            for (_i = 0, _len = role_list.length; _i < _len; _i++) {
              _results.push(role_list[_i].alias);
            }
            return _results;
          })();
        } else {
          selected_roles = [roles.alias];
        }
      
      
        $scope.is_sended = true;
        restNL.mail.send({
          post_id: $scope.post_id
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
        extManager.flash('Roles have refreshed.')
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