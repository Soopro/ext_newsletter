angular.module('newsletter')

.config([
  '$routeProvider',
  
  function(
    $routeProvider
  ){
    var bp = "newsletter";
    var dir = "blueprints/newsletter/views";

    $routeProvider
    
    .when('/' + bp + '/', {
      redirectTo: '/' + bp + '/posts'
    })
    
    .when('/' + bp + '/profile', {
      templateUrl: dir + "/profile.html",
      controller: "profileCtrl"
    })
    
    .when('/' + bp + '/posts', {
      templateUrl: dir + "/posts.html",
      controller: "postsCtrl"
    })
    
    .when('/' + bp + '/edit_post/:post_id', {
      templateUrl: dir + "/edit.html",
      controller: "postCtrl"
    });
  }
]);