angular.module "newsletterClient"

.config [
  "$routeProvider"
  ($routeProvider) ->
    $routeProvider

    .when "/auth",
      templateUrl: "views/user/auth.html"
      controller: "AuthCtrl"
    .when "/notify",
      templateUrl: "views/user/notify.html"
      controller: "NotifyCtrl"
    .when "/login",
      templateUrl: "views/user/login.html"
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
			templateUrl: "views/404.html"
    .otherwise redirectTo: "/404"

]
