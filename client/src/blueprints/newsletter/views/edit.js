// Generated by CoffeeScript 1.10.0
(function() {
  angular.module("newsletter").controller("postCtrl", [
    "$rootScope", "$scope", "restAPI", "$route", "$routeParams", "$location", function($rootScope, $scope, restAPI, $route, $routeParams, $location) {
      var post_id;
      post_id = $routeParams.post_id;
      $scope.is_new = post_id === 'new' ? true : false;
      post_id = null;
      if (!$scope.is_new) {
        post_id = $routeParams.post_id;
        $scope.post = restAPI.posts.get({
          post_id: post_id
        });
      } else {
        $scope.post = new restAPI.posts();
      }
      $scope.role_list = restAPI.memberRoles.query();
      $scope.send_test_post = function() {
        return restAPI.mailTest.save({
          post_id: post_id
        }, {
          test_mail: $scope.test_email
        });
      };
      $scope.send_post = function() {
        console.log($scope.selected_role);
        return restAPI.mail.save({
          post_id: post_id
        }, {
          selected_role: $scope.selected_role
        });
      };
      $scope.save_post = function() {
        $scope.post.$save();
        return $location.path("/posts");
      };
      return $scope.delete_post = function() {
        $scope.post.$delete();
        return $location.path("/posts");
      };
    }
  ]);

}).call(this);
