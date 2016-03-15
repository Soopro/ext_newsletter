angular.module "newsletter"
.factory "interceptor", [
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
      if Auth.getToken()
        request.headers.Authorization = Auth.getToken()
      return request

    response: (response) ->
      return response or $q.when(response)

    responseError: (rejection) ->
      # if rejection.status is 0 and rejection.data is null
      #   $location.path '/404'
      if rejection.status is 401
        $location.path '/auth'
      return $q.reject rejection
]

.config [
  "$httpProvider"
  (
    $httpProvider
  ) ->
    $httpProvider.interceptors.push "interceptor"

]