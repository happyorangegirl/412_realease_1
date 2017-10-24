angular.module('auth.github', [])
  .controller('OAuthGithubCtrl', ['$scope', '$rootScope', '$state', '$location','AuthService', 'EnvironmentConfig', OAuthGithubCtrl]);

function OAuthGithubCtrl($scope, $rootScope, $state, $location, AuthService, EnvironmentConfig) {
  $scope.code = $location.absUrl().split("code=")[1].split("#")[0];
  //test
  $scope.username = 'test';
  $scope.password = 'test';
  //test

  AuthService.GetGithubUserInfo($scope.code).then(function(response) {
    AuthService.SetCredentials($scope.username, $scope.password);
    $location.path('/');
  }, function() {
      // TODO:
      //   * Conflict
  });
}