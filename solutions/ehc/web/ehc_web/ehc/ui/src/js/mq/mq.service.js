 angular.module('mq.service', [])
  .factory('MQService', ['$http', 'EnvironmentConfig', MQService]);
function MQService($http, EnvironmentConfig) {
  var api = EnvironmentConfig.api + '/mq/db/packs';
  var uri = EnvironmentConfig.api + '/mq/db/repos';
  return {
    // TODO: opts for search
    enqueuePacks: function (pack_ids) {
      var param = {
        pack_ids: pack_ids
      };
      return $http.post(api, param);
    },

    enqueueRepos: function(repo_ids) {
      var param = {
        repo_ids: repo_ids
      };
      return $http.post(uri, param);
    }
  };
}