/* -------------------------------
 * Server Conf: sup ext newsletter 
/* ------------------------------- */

if (sup_ext_newsletter == 'undefined' || !sup_ext_newsletter){
   var sup_ext_newsletter = {}
}


var test = {
  'api': "http://127.0.0.1:5001/newsletter",
  'auth_api': "http://127.0.0.1:5001/user",
};

var dev = {
  'api': "http://127.0.0.1:5001/newsletter",
  'auth_api': "http://127.0.0.1:5001/user",
};

var prd = {
  'api': "http://ext.soopro.com/newsletter/server/newsletter",
  'auth_api': "http://ext.soopro.com/newsletter/server/user",
};


sup_ext_newsletter.server = dev
sup_ext_newsletter.cookie_domain = ".sup.local"
sup_ext_newsletter.is_debug = true;
