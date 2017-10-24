angular.module('dashboard.ctrl', [
    'dashboard.service',
    'chart.js'
  ])
  .controller('DashboardCtrl', ['$scope', '$state', '$stateParams', 'DashboardService', '$location', '$anchorScroll',
    DashboardCtrl])
  .controller("PieCtrl", ['$scope', PieCtrl]);

function DashboardCtrl($scope, $state, $stateParams, DashboardService, $location, $anchorScroll) {
  $scope.releases = [];
}

function PieCtrl($scope) {
  $scope.labels = ["Success", "Failed", "Running"];
  $scope.data = [500, 200, 100];
  $scope.colors = ['#32CD32', '#FF4500', '#FFD700'];
}