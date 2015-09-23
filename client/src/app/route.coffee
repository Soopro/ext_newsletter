angular.module "newsletterApp"

.config [
  "$routeProvider"
  (
    $routeProvider
  ) ->
    $routeProvider

    .when "/auth",
      templateUrl: "app/module/user/auth.html"
      controller: "AuthCtrl"
    .when "/notify",
      templateUrl: "app/module/user/notify.html"
      controller: "NotifyCtrl"
    .when "/login",
      templateUrl: "app/module/user/login.html"

    .when "/profile",
      templateUrl: "app/module/newsletter/profile.html"
      controller: "profileCtrl"
    .when "/posts",
      templateUrl: "app/module/newsletter/posts.html"
      controller: "postsCtrl"
    .when "/edit_post/:post_id",
      templateUrl: "app/module/newsletter/edit.html"
      controller: "postCtrl"
    .otherwise redirectTo: "/auth"

]
