angular.module('repo.ctrl', [
  'repo.service',
  'mq.service'
])
.controller('RepoVersionCtrl', ['$scope', '$state', '$stateParams', '$log', '$filter', 'RepoVersionService', 'MQService', RepoVersionCtrl])
.controller('NewRepoVersionCtrl',['$scope', '$state', '$stateParams', 'RepoVersionService', NewRepoVersionCtrl])
.controller('EditRepoVersionCtrl',['$scope', '$state', '$stateParams', '$mdDialog', '$mdMedia', 'RepoVersionService', EditRepoVersionCtrl]);

function RepoVersionCtrl($scope, $state, $stateParams, $log, $filter, RepoVersionService, MQService) {
  $scope.sortType = 'status';
  $scope.sortReverse = false;
  
  var opts = {
    repo_id: $stateParams.repoId
  };
  RepoVersionService.get(opts.repo_id).then(function successCallback(response) {
    $scope.repo = response.data;
    $scope.nav.repo = response.data;
  }, function errorCallback(response) {
    // TODO: report error
  });
}

// TODO: Abstract to one: NewOrUpdateRepoCtrl()
function NewRepoVersionCtrl($scope, $state, $stateParams, RepoVersionService) {
  $scope.enumVCS = ['git', 'svn', 'hg'];
  $scope.currVCS = $scope.enumVCS[0];
  $scope.repo = {
    component_id : $stateParams.componentId,
    name : null,
    vcs_type : null,
    clone_url : null,
    tree : null,
    inputted_url : null,
    last_commit : null,
    repo_meta_cmt : null,
    repo_cmt : null,
    user_languages: null
  };

  $scope.saveRepoVersion = function() {
    $scope.repo.vcs_type = $scope.currVCS;
    $scope.repo.user_languages = $scope.repo.user_languages.split(',');
    RepoVersionService.create($scope.repo).then(function successCallback(response) {
      $state.go('components.show', {componentId: $stateParams.componentId}, {reload: true});
    }, function errorCallback(response) {
      // TODO: report error
    });
  };
}

function EditRepoVersionCtrl($scope, $state, $stateParams, $mdDialog, $mdMedia, RepoVersionService) {
  $scope.enumVCS = ['git', 'svn', 'hg'];
  $scope.currVCS = $scope.enumVCS[0];

  RepoVersionService.get($stateParams.repoId).then(function successCallback(response) {
    $scope.repo = {
      rv_id : response.data.id,
      name : response.data.meta.name,
      vcs_type : response.data.meta.vcs_type,
      clone_url : response.data.meta.clone_url,
      tree : response.data.tree,
      last_commit : response.data.last_commit,
      repo_meta_cmt : response.data.meta.cmt,
      repo_cmt : response.data.cmt,
      user_languages: response.data.user_languages
    };
  }, function errorCallback(response) {
    // TODO: report error
  });

  $scope.editRepoVersion = function() {
    $scope.repo.vcs_type = $scope.currVCS;
    $scope.repo.user_languages = $scope.repo.user_languages;
    RepoVersionService.update($scope.repo).then(function successCallback(response) {
      $state.go('components.show', {componentId: $stateParams.componentId}, {reload: true});
    }, function errorCallback(response) {
      // TODO: report error
    });
  };

  $scope.deleteRepoVersion = function(ev, repo){
    var confirm = $mdDialog.confirm()
            .title('Warning')
            .textContent('Would you like to delete "' + repo.name + '"?')
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
}