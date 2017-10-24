angular.module('workflow.ctrl', [
  'demo.service',
])
.controller('WorkflowCtrl', ['$scope', '$state', '$stateParams', '$log', '$filter', 'DemoService', WorkflowCtrl])
.controller('WorkflowLogCtrl', ['$scope', '$state', '$stateParams', '$log', '$filter', 'DemoService', WorkflowLogCtrl]);

function WorkflowCtrl($scope, $state, $stateParams, $log, $filter, DemoService) {
  $scope.workflows = [];
  
  DemoService.getWorkflows().then(function successCallback(response) {
    $scope.workflows = response.data;
    console.log($scope.workflows)
  }, function errorCallback(response) {
    // TODO: report error
  });

  $scope.run = function(wf_id) {
    alert('Started Workflow: ' + wf_id);
  };
}

function WorkflowLogCtrl($scope, $state, $stateParams, $log, $filter) {
  $scope.workflow = $stateParams['id'];

  $scope.curr_date = new Date();
  $scope.text = "INFO  Started workflow: " + $scope.workflow;
}