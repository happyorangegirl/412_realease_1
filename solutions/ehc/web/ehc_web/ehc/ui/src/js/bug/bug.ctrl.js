angular.module('bug.ctrl', [
])
  .controller('BugReportModalCtrl', ['$scope', '$uibModalInstance', '$location', 'nav', BugReportModalCtrl]);

function BugReportModalCtrl($scope, $uibModalInstance, $location, nav) {
  $scope._nav = nav;

  $scope.bug = {
    entity_id: $scope._nav.pack.id,
    entity_type: 'pack',
    why: null,
    html_url: $location.absUrl(),
    status: 10,
    assigned_id: null
  };

  $scope.summitTheBug = function () {
    $uibModalInstance.close($scope.bug);
  };

  $scope.cancelBugReportModal = function () {
    $uibModalInstance.dismiss('cancel');
  };
};
