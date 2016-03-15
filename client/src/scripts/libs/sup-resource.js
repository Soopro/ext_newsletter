// Generated by CoffeeScript 1.10.0

/*
 supResource

 Author : Redy Ru
 Email : redy.ru@gmail.com
 License : 2014 MIT
 Version 1.0.0

 ---- Usage ----
 A warp of ng-resource, add 'update' 'save' and 'create'
 and provider service warp $q.defer().promise, for chain request only
 */

(function() {
  angular.module('supResource', ['ngResource']).factory("supResource", [
    '$resource', function($resource) {
      return function(url, paramDefaults, actions) {
        var _actions, restapi;
        _actions = {
          update: {
            method: "PUT",
            isArray: false
          },
          trigger: {
            method: "POST"
          },
          create: {
            method: "POST"
          },
          post: {
            method: "POST"
          }
        };
        actions = angular.extend({}, _actions, actions);
        restapi = $resource(url, paramDefaults, actions);
        restapi.prototype.$save = function(params, success, error) {
          if (!this.id) {
            return this.$create(params, success, error);
          } else {
            return this.$update(params, success, error);
          }
        };
        return restapi;
      };
    }
  ]).factory("supChain", [
    '$q', function($q) {
      return function(object) {
        var deferred;
        if (!object) {
          deferred = $q.defer();
          deferred.resolve();
          return deferred.promise;
        } else if (typeof object.then === "function") {
          return object;
        } else if (object.$promise) {
          return object.$promise;
        } else {
          throw "Error: Invalid parameter in 'supChain'. - Object must have" + " Promise or $promise. [SupResource]";
        }
      };
    }
  ]).factory("supParallel", [
    '$q', function($q) {
      return function(list) {
        var count, deferred, failure, index, limit, obj, pms, results, start_then, success;
        deferred = $q.defer();
        if (list instanceof Array) {
          results = [];
          count = 1;
          limit = list.length;
          start_then = function(pms, index) {
            return pms.then(function(data) {
              results[index] = data;
              if (count < limit) {
                return count++;
              } else {
                return success(results);
              }
            })["catch"](function(error) {
              return failure(error);
            });
          };
          for (index in list) {
            obj = list[index];
            if (typeof obj.then === "function") {
              pms = obj;
            } else if (obj.$promise) {
              pms = obj.$promise;
            }
            start_then(pms, index);
          }
          success = function(results) {
            return deferred.resolve(results);
          };
          failure = function(error) {
            return deferred.reject(error);
          };
          return deferred.promise;
        } else {
          throw "Error: Invalid parameter in 'supParallel'. - " + "Objst must be Array, each item must be a promise " + "[SupResource]";
        }
      };
    }
  ]);

}).call(this);
