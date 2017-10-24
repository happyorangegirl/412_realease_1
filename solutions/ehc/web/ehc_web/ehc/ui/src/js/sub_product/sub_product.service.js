angular.module('subProduct.service', [])
.factory('SubProductsService', ['$http', 'EnvironmentConfig', SubProductsService]);

function SubProductsService($http, EnvironmentConfig) {
  var api = EnvironmentConfig.api + '/subproducts';
  return {
    get: function(subproductId) {
      return $http.get([api, subproductId].join('/'));
    },
    create: function(subproduct) {
      return $http.post(api, subproduct);
    },
    remove: function(id){
      var uri = api + '/' + id;
      return $http.delete(uri);
    }
  };
}