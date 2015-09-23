angular.module "newsletterApp"

.constant "Config",
  base_url: newsletter.server.host
  api: newsletter.server.api

  path:
    default: "/posts"
    auth: "/auth"
    notify: "notify"
    login: "/login"

  sup_auth_uri: newsletter.server.sup_auth