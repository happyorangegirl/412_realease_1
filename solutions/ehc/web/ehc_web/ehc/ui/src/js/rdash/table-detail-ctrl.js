angular.module('RDash')
.controller('TableDetailCtrl'), ['$scope', '$stateParams', '$state', function ($scope, $stateParams, $state) {
  
  var id = $stateParams.tableId;
  $scope.id = id;
  console.log(id);
  $scope.name = 'foo';
  $state.go('tables.detail.grid');
  // $scope.items = [1, 2];
}];