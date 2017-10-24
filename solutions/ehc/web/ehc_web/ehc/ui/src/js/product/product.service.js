angular.module('product.service', ['RDash.config'])
.factory('ProductService', ['$http', 'EnvironmentConfig', function ($http, EnvironmentConfig) {
  var uri = EnvironmentConfig.api + '/products';
  return {
    // TODO: opts for search
    query: function (params) {
      return $http.get(uri, params);
    },
    create: function(product) {
      product.user_id = 1;
      return $http.post(uri, product);
    }
  };
}]);

