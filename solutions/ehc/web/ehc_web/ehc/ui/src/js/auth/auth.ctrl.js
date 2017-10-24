angular.module('auth.ctrl', [])
  .controller('AuthCtrl', ['$scope', '$state', '$location', 'AuthService', 'EnvironmentConfig', AuthCtrl])
.controller('ProfileCtrl', ['$scope', '$state', '$location', 'AuthService', ProfileCtrl]);

function AuthCtrl($scope, $state, $location, AuthService, EnvironmentConfig) {
  $scope.error = false;
  $scope.errorMessage = '';
  $scope.cliendID = EnvironmentConfig.cliendID;
  $scope.username = 'stub_admin';
  $scope.password = 'admin';
  $scope.login = function () {
    $scope.dataLoading = true;
    if (AuthService.Login() === true) {
      AuthService.SetCredentials($scope.username, $scope.password);
      $location.path('/');
    }
    /*
    AuthService.Login($scope.username, $scope.password)
      .then(function(response) {
        AuthService.SetCredentials($scope.username, $scope.password);
        $location.path('/');
      }, function(response) {
        $scope.error = response.data.error;
        $scope.dataLoading = false;
      }); */
  };
}

function ProfileCtrl($scope, $state, $location, AuthService) {
  var host = $location.host();

  $scope.admin_uis = {
    'Supervisor Admin UI': 'http://' + host + ':9001',
    'RabbitMQ Admin UI': 'http://' + host + ':15672'
  };

  $scope.logout = function () {
    AuthService.ClearCredentials();
    $state.go('login');
  };
}