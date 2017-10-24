angular.module('pack.ctrl', [
  'pack.service',
  'license.service',
  'bug.service'
])
  .controller('PackCtrl', ['$scope', '$state', '$stateParams', 'PackService', 'BugService', PackCtrl])
  .controller('PackSearchCtrl', ['$scope', '$state', '$stateParams', 'PackService', '$location', PackSearchCtrl])
  .controller('NewPackCtrl', ['$scope', '$state', '$stateParams', '$mdDialog', '$mdMedia', 'PackService', NewPackCtrl]);


function PackCtrl($scope, $state, $stateParams, PackService, BugService) {
  PackService.get($stateParams.packId).then(function(response) {
    $scope.nav.pack = response.data;
  }, function() {
    // TODO: error
  }).then(function() {
      PackService.availableOpts().then(function(response) {
        $scope.availableOpts = response.data;
        angular.forEach($scope.availableOpts.status, function(v, k) {
          if (v.code == $scope.nav.pack.status) {
            $scope.currStatus = $scope.availableOpts.status[k];
          }
        });
      }, function() {
        // TODO: error
      })
  }).then(function() {
    // Fill in bugs
    BugService.query({
      entity_type: 'pack',
      entity_id: $scope.nav.pack.id
    }).then(function(response) {
      $scope.nav.pack.bugs = response.data;
    }, function() {
      $scope.nav.pack.bugs = []
    });
  });

  // Save this pack
  $scope.save = function() {
    $scope.nav.pack.status = $scope.currStatus.code;
    PackService.update($scope.nav.pack).then(function(response) {
      var showParams =  $state.params;
      $state.go('^.show', showParams);
    }, function() {
      // TODO:
      //   * Conflict
    });
  };
}

function NewPackCtrl($scope, $state, $stateParams, $mdDialog, $mdMedia, PackService) {
  $scope.newpack = {
    name : null,
    language : null,
    uuid : null,
    version : null,
    repo_id : $stateParams.repoId,
    group : null,
    source_url : null,
    project_url : null,
    status : null,
    version_cmt : null,
    homepage : null
  };

  $scope.savePackVersion = function(){
    $scope.newpack.status = $scope.currStatus.code;
    $scope.newpack.language = $scope.currLanguages;
    PackService.create($scope.newpack).then(function(response) {
      var packId = response.data.id;
      $state.go('^.show', {packId: packId});
    }, function() {
      // TODO:
      //   * Conflict
    });
  };
}

function PackSearchCtrl($scope, $state, $stateParams, PackService, $location) {
  $scope.sortType = 'status';
  $scope.sortReverse = false;

  //var searchObj = $location.search();
  //$scope.status = searchObj.status;
  $scope.status = '';


  $scope.packs = [];

  $scope.search_packs = function(){
    var conditions = {
      status: $scope.status,
      release_id: 1
    };
    $location.search('status', $scope.status);
    PackService.query(conditions).then(function(response) {
      $scope.packs = response.data;
    }, function() {
      // TODO: error
    });
  };
}