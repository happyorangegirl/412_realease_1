angular.module('bug.service', [])
  .factory('BugService', ['$http', 'EnvironmentConfig', BugService]);

function BugService($http, EnvironmentConfig) {
  var api = EnvironmentConfig.api + '/bugs';
  return {
    /**
     * @param opts {entity_id: Integer, entity_type: String(pack|repo|license)}
     */
    query: function (opts) {
      var config = {
        params: opts
      };
      return $http.get(api, config);
    },
    get: function (id) {
      var uri = api + '/' + id;
      return $http.get(uri);
    },
    create: function(bug) {
      return $http.post(api, bug);
    },
    remove: function(id){
      var uri = api + '/' + id;
      return $http.delete(uri);
    },

    // Swagger-doc should have followed Angular's Array encoding
    //stat: function(component_ids) {
    //  var config = {
    //    params: {
    //      'component_ids[]': component_ids
    //    }
    //  };
    //  var uri = api + '/stat';
    //  return $http.get(uri, config);
    //},
  };
}