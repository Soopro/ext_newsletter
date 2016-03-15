angular.module('newsletter')

.config([
  '$routeProvider',
  
  function(
    $routeProvider
  ){
    var bp = "newsletter";
    var dir = "blueprints/newsletter/views";

    $routeProvider
    
    .when('/' + bp + '/profile', {
      templateUrl: "views/newsletter/profile.html",
      controller: "profileCtrl"
    })
    
    .when('/' + bp + '/posts', {
      templateUrl: "views/newsletter/posts.html",
      controller: "postsCtrl"
    })
    
    .when('/' + bp + '/edit_post/:post_id', {
      templateUrl: "views/newsletter/edit.html",
      controller: "postCtrl"
    });
  }
]);