// Generated by CoffeeScript 1.10.0
(function() {
  var CASE_SENSITIVE, _all_basestring, _trans_key, append, insert, is_exports, load_dict, locale, localizedText, restore, root, self_translate, setLocale, translate, varsion;

  varsion = '1.1.3';

  is_exports = typeof exports !== "undefined" && exports !== null;

  root = is_exports ? exports : this;

  if (!root.sup) {
    root.sup = {};
  }

  sup.localizedDict = {};

  localizedText = {};

  locale = null;

  CASE_SENSITIVE = false;

  _all_basestring = function() {
    var arg, i, len;
    for (i = 0, len = arguments.length; i < len; i++) {
      arg = arguments[i];
      if (typeof arg !== 'string') {
        return false;
      }
    }
    return true;
  };

  _trans_key = function(str) {
    if (!CASE_SENSITIVE) {
      return str.toLowerCase();
    }
    return str;
  };

  insert = function(loc, text_list) {
    return sup.localizedDict[loc] = text_list;
  };

  load_dict = function(loc_texts) {
    var i, len, loc_text_dict, text;
    loc_text_dict = {};
    if (Object.prototype.toString.call(loc_texts) === '[object Array]') {
      for (i = 0, len = loc_texts.length; i < len; i++) {
        text = loc_texts[i];
        if (_all_basestring(text.msgid, text.msgid) && text.msgid) {
          loc_text_dict[_trans_key(text.msgid)] = text.msgstr;
        }
      }
    } else if (loc_texts && typeof loc_texts === 'object') {
      loc_text_dict = loc_texts;
    }
    return loc_text_dict;
  };

  append = function(new_text_list) {
    var i, len, text;
    if (Object.prototype.toString.call(new_text_list) !== '[object Array]') {
      return;
    }
    for (i = 0, len = new_text_list.length; i < len; i++) {
      text = new_text_list[i];
      if (_all_basestring(text.msgid, text.msgid) && text.msgid) {
        localizedText[_trans_key(text.msgid)] = text.msgstr;
      }
    }
  };

  restore = function() {
    setLocale(locale);
  };

  setLocale = function(loc) {
    var k, locale_dict, ref, v;
    if (!loc) {
      loc = '';
    }
    locale = null;
    loc = loc.replace('-', '_');
    ref = sup.localizedDict;
    for (k in ref) {
      v = ref[k];
      if (k.toLowerCase() === loc.toLowerCase()) {
        locale = k;
        break;
      }
    }
    if (locale && sup.localizedDict[locale]) {
      locale_dict = sup.localizedDict[locale];
    } else {
      locale_dict = null;
      locale = loc;
    }
    localizedText = load_dict(locale_dict);
    return locale;
  };

  translate = function(text) {
    var arg, args, i, j, len, len1, ref, trans;
    if (!text || typeof text !== 'string') {
      return text;
    }
    trans = localizedText[_trans_key(text)];
    if (!trans) {
      trans = text;
    }
    args = [];
    for (i = 0, len = arguments.length; i < len; i++) {
      arg = arguments[i];
      args.push(arg);
    }
    ref = args.slice(1);
    for (j = 0, len1 = ref.length; j < len1; j++) {
      arg = ref[j];
      if (arg === void 0) {
        arg = '';
      }
      trans = trans.replace("%s", arg);
    }
    return trans;
  };

  self_translate = function(text) {
    var key, lang, trans_text;
    if (!text || typeof text !== 'object') {
      return text;
    }
    if (locale) {
      lang = locale.split('_')[0] || 'en';
      trans_text = text[locale] || text[lang];
    }
    if (!trans_text) {
      key = Object.keys(text)[0];
      trans_text = text[key];
    }
    return trans_text;
  };

  angular.module('supLocales', ['ngCookies']).run([
    'supLocales', function(supLocales) {
      if (!supLocales.inited) {
        return supLocales.init();
      }
    }
  ]).service("supLocales", [
    '$location', '$rootScope', '$cookies', function($location, $rootScope, $cookies) {
      var default_locale, self;
      default_locale = 'en_US';
      self = this;
      this.version = varsion;
      this.inited = false;
      this.init = function(loc, case_sensitive) {
        var cookieLocale, currLocale, e, error, params, userLang, userLocale;
        this.inited = true;
        CASE_SENSITIVE = Boolean(case_sensitive);
        if (loc) {
          default_locale = loc;
        }
        userLang = navigator.language || navigator.userLanguage;
        userLocale = userLang.replace('-', '_');
        try {
          cookieLocale = $cookies.get('current_locale');
        } catch (error) {
          e = error;
          cookieLocale = null;
        }
        params = $location.search();
        if (params.lang) {
          currLocale = params.lang;
          $location.search("lang", null);
        } else {
          currLocale = cookieLocale ? cookieLocale : userLocale;
        }
        self.set(currLocale);
        $rootScope._ = angular.translate = translate;
        return $rootScope._t = angular.self_translate = self_translate;
      };
      this.load = function(loc, text_list) {
        insert(loc, text_list);
        return setLocale(loc);
      };
      this.translate = function(args) {
        return translate.apply(this, arguments);
      };
      this.set = function(loc) {
        locale = setLocale(loc) || default_locale;
        $rootScope.locale = locale;
        $rootScope.lang = locale.split('_')[0] || 'en';
        if ($cookies.get('current_locale') !== locale) {
          return $cookies.put('current_locale', locale);
        }
      };
      this.append = function(translates) {
        return append(translates);
      };
      this.restore = function() {
        return restore();
      };
      this.get = function() {
        var cookieLocale, e, error;
        try {
          cookieLocale = $cookies.get('current_locale');
        } catch (error) {
          e = error;
          cookieLocale = null;
        }
        return cookieLocale;
      };
      this.match = function(lang1, lang2) {
        if (typeof lang1 !== 'string' || typeof lang2 !== 'string') {
          return false;
        }
        lang1 = lang1.replace('-', '_');
        lang2 = lang2.replace('-', '_');
        return lang1.toLowerCase() === lang2.toLowerCase();
      };
      return this;
    }
  ]);

}).call(this);
