angular.module('repo.service', [])
  .factory('RepoVersionService', ['$http', 'EnvironmentConfig', RepoVersionService]);

function RepoVersionService($http, EnvironmentConfig) {
  var api = EnvironmentConfig.api + '/repos';
  return {
    // TODO: opts for search

    get: function (repo_id) {
      var uri = api + '/' + repo_id;
      return $http.get(uri);
    },

    // Swagger-doc should have followed Angular's Array encoding
    stat: function(repo_ids) {
      var config = {
        params: {
        'repo_ids[]': repo_ids
        }
      };
      var uri = api + '/stat';
      return $http.get(uri, config);
    },
    create: function(repo) {
      return $http.post(api, repo);
    },
    update: function(repo) {
      var uri = api + '/' + repo.rv_id;
      return $http.put(uri, repo);
    },

    remove: function(repo_id) {
      var uri = api + '/' + repo_id;
      //return $http.delete(uri);
    }
  };
}