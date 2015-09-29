angular.module "newsletterClient"

.controller "postCtrl",[
  "$rootScope"
  "$scope"
  "restAPI"
  "$route"
  "$routeParams"
  "$location"
  (
    $rootScope
    $scope
    restAPI
    $route
    $routeParams
    $location
  ) ->
    post_id = $routeParams.post_id
    $scope.is_new = if post_id == 'new' then true else false
    post_id = null

    if !$scope.is_new
      post_id = $routeParams.post_id
      $scope.post = restAPI.posts.get post_id:post_id
    else
      $scope.post = new restAPI.posts()

    $scope.role_list = restAPI.memberRoles.query()

    $scope.send_test_post = () ->
      restAPI.mailTest.save post_id:post_id
        , {test_mail:$scope.test_email}

    $scope.send_post = () ->
      console.log $scope.selected_role
      restAPI.mail.save post_id:post_id
        , {selected_role:$scope.selected_role}

    $scope.save_post = () ->
      $scope.post.$save()
      $location.path("/posts")

    $scope.delete_post = () ->
      $scope.post.$delete()
      $location.path("/posts")
]