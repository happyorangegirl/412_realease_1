angular.module('component.ctrl', [
  'component.service',
  'repo.service',
  'mq.service'
])
  .controller('ComponentCtrl', ['$scope', '$state', '$stateParams', '$log', '$filter', '$mdDialog', '$mdMedia', 'ComponentService',
    'RepoVersionService', 'MQService', '$uibModal', ComponentCtrl]);

function ComponentCtrl($scope, $state, $stateParams, $log, $filter, $mdDialog, $mdMedia, ComponentService,
                       RepoVersionService, MQService, $uibModal) {
  $scope.nav = {
    repo: {},
    component: {},
    pack: {}
  };

  $scope.sortType = 'id';
  $scope.sortReverse = false;

  // FIXME: with true data
  $scope.stackedBar = [ { value: 10, type: 'success' }, { value: 27, type: 'warning' } ];

  var opts = {
    component_id: $stateParams.componentId
  };

  ComponentService.get(opts.component_id).then(function successCallback(response) {
    $scope.component = response.data;
    $scope.nav.component = response.data;
  }, function errorCallback(response) {
    // TODO: report error
  }).then(function() {
    var ids = [];
    angular.forEach($scope.component.repos, function(v,k) {
      ids.push(v.id);
    });

    /// TODO: move to RepoVersionService
    if (!ids.length) return;

    RepoVersionService.stat(ids).then(function(response) {
      var stat = response.data;
      angular.forEach($scope.component.repos, function(v,k) {
        var id = $scope.component.repos[k].id;
        var stacked = genProgressBarStacked(stat[id]);
        //var stacked = [ { value: 10, type: 'success' }, { value: 57, type: 'warning' } ];
        $scope.component.repos[k].stacked = stacked;
      });
    }, function(response) {});
  });

  $scope.deleteRepoVersion = function(ev, repo){
    var confirm = $mdDialog.confirm()
            .title('Warning')
            .textContent('Would you like to delete "' + repo.meta.name + '"?')
            .ariaLabel('Lucky day')
            .targetEvent(ev)
            .ok('Please do it!')
            .cancel('Cancel');

    $scope.RemoveRepoVersionID = repo.id;
    $mdDialog.show(confirm).then(function() {
      RepoVersionService.remove($scope.RemoveRepoVersionID).then(function successCallback(response) {
        $state.go($state.current, {}, {reload: true});
      }, function errorCallback(response) {
        // TODO: report error
      });
    }, function() {
      //cancel.
    });
  };

  $scope.runRepoTask = function(repoId) {
    var repo_ids = [repoId];
    MQService.enqueueRepos(repo_ids).then(function successCallback(response) {
      var modalInstance = $uibModal.open({
        animation: $scope.animationsEnabled,
        templateUrl: 'runRepoTaskOk.html',
        controller: ['$scope', '$uibModalInstance', function($scope, $uibModalInstance) {
          $scope.ok = function () {
            $uibModalInstance.close();
          }
        }],
        size: 'sm',
        resolve: {
          nav: function () {
            return $scope.nav;
          }
        }
      });
    }, function errorCallback(response) {
      var modalInstance = $uibModal.open({
        animation: $scope.animationsEnabled,
        templateUrl: 'runRepoTaskError.html',
        controller: ['$scope', '$uibModalInstance', function($scope, $uibModalInstance) {
          $scope.ok = function () {
            $uibModalInstance.close();
          }
        }],
        size: 'sm',
        resolve: {
          nav: function () {
            return $scope.nav;
          }
        }
      });
    });
  };

  $scope.runPackTask = function(packId) {
    var pack_ids = [packId];
    MQService.enqueuePacks(pack_ids).then(function successCallback(response) {
      //TODO
      console.log(response.data.success[0])
    }, function errorCallback(response) {
      // TODO: report error
      alert(response.status)
    });
  };
}

/**
 * Generate
 * @param stat {Object}
     {
      "entity": "pack",
      "total": 101,
      "details": {
        "10": 1,
        "40": 100
      }
 * @return {Array} [
 *                   {"value":62.5,"type":"success","amount":5},
 *                   {"value":12.5,"type":"warning","amount":1},
 *                   {"value":25,"type":"danger","amount":2}
 *                 ]
 */
function genProgressBarStacked(stat) {
  if (stat.total === 0) {
    return [];
  }
  var exist = false;
  var types = {
    success: exist,
    warning: exist,
    danger: exist
  };
  var success = { value: 0, type: 'success', amount: 0 },
    warning = { value: 0, type: 'warning', amount: 0 },
    danger = { value: 0, type: 'danger', amount: 0 };

  angular.forEach(stat.details, function(v,k) {
    if (k >= 40) {
      types.success = true;
      success.amount += v;
      // 100% based: eg. 10%, 20%, ...
      success.value = success.amount / stat.total * 100;
    }
    if (k >= 30 && k < 40) {
      types.warning = true;
      warning.amount += v;
      warning.value = warning.amount / stat.total * 100;
    }
    if (k >= 10 && k < 30) {
      types.danger = true;
      danger.amount += v;
      danger.value = danger.amount / stat.total * 100;
    }
  });
  // TODO: Clean code
  var stacked = [];
  if (types.success) stacked.push(success);
  if (types.warning) stacked.push(warning);
  if (types.danger) stacked.push(danger);
  return stacked;
}