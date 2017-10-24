angular.module('license.service', [])
  .factory('LicenseService', ['$http', 'EnvironmentConfig', LicenseService]);

function LicenseService($http, EnvironmentConfig) {
  var api = EnvironmentConfig.api + '/licenses';
  return {
    get: function (license_id) {
      var uri = api + '/' + license_id;
      return $http.get(uri);
    },
    delete: function (license_id) {
      var uri = api + '/' + license_id;
      return $http.delete(uri);
    },
    createOrUpdate: function(license) {
      if (license.id) {
        var uri = api + '/' + license.id;
        return $http.put(uri, license);
      } else {
        return $http.post(api, license);
      }
    },
    fetchRemoteLicenseText: function(license_url) {
      var config = {
        params: {
          license_url: license_url
        }
      };
      var uri = api + '/remote-text';
      return $http.get(uri, config);
    }
  };
}