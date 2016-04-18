/* -------------------------------
 * Server Conf: sup ext newsletter
/* ------------------------------- */

if (sup_ext_newsletter == 'undefined' || !sup_ext_newsletter){
   var sup_ext_newsletter = {}
}

var test = {
  'api': 'http://ext.sup.farm/newsletter/server'
}

var dev = {
  'api': 'http://localhost:5003'
}

var prd = {
  'api': 'http://api-nl.exts.soopro.net'
}

sup_ext_newsletter.server = dev
sup_ext_newsletter.is_debug = true;
