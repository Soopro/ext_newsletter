angular.module('newsletter')

.constant('Config', {
  'baseURL': {
    'api': sup_ext_newsletter.server.api
  },
  
  'debug': sup_ext_newsletter.is_debug,
  
  'route': {
    portal: '/newsletter',
    auth: '/auth',
    error: '/404',
  },

});
