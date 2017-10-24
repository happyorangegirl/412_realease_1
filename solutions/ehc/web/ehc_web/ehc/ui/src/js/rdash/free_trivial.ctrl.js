/**
 * Master Controller
 */

angular.module('RDash')
  .controller('FreeTrivialCtrl', ['$scope', '$cookieStore', FreeTrivialCtrl]);

function FreeTrivialCtrl($scope) {
  $scope.repo_url = null;

  $scope.tryIt = function() {
    alert('This feature is coming soon...');
  };
}