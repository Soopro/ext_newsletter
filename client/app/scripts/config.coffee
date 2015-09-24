angular.module "newsletterClient"

.constant "Config",
  base_url: "http://127.0.0.1:5001"
  api: newsletter.server.api

  path:
    default: "/posts"
    auth: "/auth"
    notify: "notify"
    login: "/login"

  sup_auth_uri: newsletter.server.sup_auth
  
  
  
  
  
  
  api: "http://127.0.0.1:5001",
  auth_api: "http://127.0.0.1:5001/user"