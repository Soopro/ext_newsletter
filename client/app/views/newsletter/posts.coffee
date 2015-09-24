angular.module "newsletterClient"

.controller "postsCtrl", [
  "$rootScope"
  "$scope"
  "$route"
  "$location"
  "restAPI"
  (
    $rootScope
    $scope
    $route
    $location
    restAPI
  ) ->
    $scope.posts = restAPI.posts.query()

    $scope.open_post = (post_id) ->
      $location.path("/edit_post/#{post_id}")
]