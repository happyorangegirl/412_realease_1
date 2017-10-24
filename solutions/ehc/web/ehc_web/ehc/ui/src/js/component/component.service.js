angular.module('component.service', [])
  .factory('ComponentService', ['$http', 'EnvironmentConfig', ComponentService]);

function ComponentService($http, EnvironmentConfig) {
  var api = EnvironmentConfig.api + '/components';
  return {
    // TODO: opts for search
    query: function (opts) {
      //var uri = api + '/' + opts.component_id;
      //return $http.get(uri, opts);
    },
    get: function (component_id) {
      var uri = api + '/' + component_id;
      return $http.get(uri);
    },
    create: function(product) {
      return $http.post(api, product);
    },
    remove: function(component_id){
      var uri = api + '/' + component_id;
      return $http.delete(uri);
    },

    // Swagger-doc should have followed Angular's Array encoding
    stat: function(component_ids) {
      var config = {
        params: {
          'component_ids[]': component_ids
        }
      };
      var uri = api + '/stat';
      return $http.get(uri, config);
    },
  };
}