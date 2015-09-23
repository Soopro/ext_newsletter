angular.module "newsletterApp"


.factory "requestInterceptor", [
  "$q"
  "$location"
  "Auth"
  "Config"
  (
    $q
    $location
    Auth
    Config
  ) ->
    request: (request) ->
      request.headers = request.headers or {}
      if Auth.get_token()
        request.headers.Authorization = Auth.get_token()
      request

    response: (response) ->
      response or $q.when(response)

    responseError: (rejection) ->
      if rejection.status is 401
        console.log(401)
        $location.path Config.path.auth
      $q.reject rejection
]

.config [
  "$httpProvider"
  (
    $httpProvider
  ) ->
    $httpProvider.interceptors.push "requestInterceptor"

]