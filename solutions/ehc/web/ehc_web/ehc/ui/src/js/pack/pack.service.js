angular.module('pack.service', [])
  .factory('PackService', ['$http', 'EnvironmentConfig', PackService]);

function PackService($http, EnvironmentConfig) {
  var api = EnvironmentConfig.api + '/packs';
  return {
    // TODO: opts for search
    query: function (params) {
      var uri = api + '/search';
      var config = {
        params: params
      };
      return $http.get(uri, config);
    },
    get: function (pack_id) {
      var uri = api + '/' + pack_id;
      return $http.get(uri);
    },
    create: function(data) {
      return $http.post(api, data);
    },
    update: function (data) {
      var uri = api + '/' + data.id;
      return $http.put(uri, data);
    },
    availableOpts: function (data) {
      var uri = api + '/opts';
      return $http.get(uri, data);
    },
  };
}