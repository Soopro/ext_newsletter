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
      $scope.post = restAPI.post.get post_id:post_id
    else
      $scope.post = new restAPI.post()

    $scope.role_list = restAPI.role_list.query()

    $scope.send_test_post = () ->
      restAPI.send_test_post.post post_id:post_id
        , {test_mail:$scope.test_email}

    $scope.send_post = () ->
      console.log $scope.selected_role
      restAPI.send_post.post post_id:post_id
        , {selected_role:$scope.selected_role}

    $scope.save_post = () ->
      $scope.post.$save()
      $location.path("/posts")

    $scope.delete_post = () ->
      $scope.post.$delete()
      $location.path("/posts")
]