angular.module 'newsletterClient'
	.factory 'restAPI', Config
		return {
			profiles: do ->
				$resource api+"/profiles"
			posts: do ->
				$resource api+"/posts"
			dispatch: do ->
				$resource api+"/profile/dispatch"
			memberRoles: do ->
				$resource api+"/member_roles"
			
			ext_token: do -> 
				$resource auth_api+"/sup_auth"
			up_auth: do -> 
				$resource auth_api+"/sup_auth"
      token_check: do -> 
				$resource auth_api+"/token_check"
		}