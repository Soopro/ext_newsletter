angular.module "newsletter"

.config [
  "$routeProvider"
  (
    $routeProvider
  ) ->
    $routeProvider
    
    .when "/",
      redirectTo: "/posts"

    .when "/auth",
      templateUrl: "views/auth/auth.html"
      controller: "AuthCtrl"
    .when "/redirect",
      templateUrl: "views/auth/redirect.html"
      controller: "RedirectCtrl"
    .when "/notify",
      templateUrl: "views/auth/notify.html"
      controller: "NotifyCtrl"
    .when "/profile",
      templateUrl: "views/newsletter/profile.html"
      controller: "profileCtrl"
    .when "/posts",
      templateUrl: "views/newsletter/posts.html"
      controller: "postsCtrl"
    .when "/edit_post/:post_id",
      templateUrl: "views/newsletter/edit.html"
      controller: "postCtrl"
    .when "/404",
      template: "<h1>No cookies here, puppy!</h1>"
    .otherwise redirectTo: "/404"

]
