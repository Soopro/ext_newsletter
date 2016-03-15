angular.module('newsletter')

.constant('Config', {
  'baseURL': {
    'api': sup_ext_newsletter.server.api,
    'auth_api': sup_ext_newsletter.server.auth_api,
  },
  'cookie_domain': sup_ext_newsletter.cookie_domain,
  'debug': sup_ext_newsletter.is_debug,

});
