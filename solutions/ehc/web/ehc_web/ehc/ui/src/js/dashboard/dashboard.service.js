angular.module('dashboard.service', [])
  .factory('DashboardService', ['$http', 'EnvironmentConfig', DashboardService]);

function DashboardService($http, EnvironmentConfig) {
  var api = EnvironmentConfig.api + '/dashboard';
  return {
    stat: function() {
      var uri = api + '/stat';
      return $http.get(uri);
    }
  };
}