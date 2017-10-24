angular.module('subProduct.ctrl', [

])
  .controller('SubProductCtrl', ['$scope', '$stateParams', '$mdDialog', '$mdMedia', 'SubProductsService', '$state', 'ComponentService', SubProductCtrl])
  .controller('AddComptController', ['$scope', '$state', '$mdDialog', 'ComponentService', AddComptController]);

function SubProductCtrl($scope, $stateParams, $mdDialog, $mdMedia, SubProductsService, $state, ComponentService) {
  $scope.release = {};
  $scope.subProjects = [];
  ReleaseService.get({
    release_id: $stateParams.releaseId
  }).then(function successCallback(response) {
      $scope.release = response.data;
      /* Nav override */
      $scope.nav.product = response.data.product;
      $scope.nav.release = response.data;
    },
    function errorCallback(response) {
    }
  ).then(function() {
    var component_ids = [];
    angular.forEach($scope.nav.release.subproducts, function(subproduct, i) {
      angular.forEach(subproduct.components, function (component, j) {
        var id = $scope.nav.release.subproducts[i].components[j].id;
        component_ids.push(id);
      })
    });

    ComponentService.stat(component_ids).then(function successCallback(response) {
      angular.forEach($scope.nav.release.subproducts, function(subproduct, i) {
        angular.forEach(subproduct.components, function(component, j) {
          var id = $scope.nav.release.subproducts[i].components[j].id;
          var stacked = genProgressBarStacked(response.data[id]);
          $scope.nav.release.subproducts[i].components[j].stacked = stacked;
        });
      });
    }, function failCallback() {});
  });

  $scope.addComponent = function(ev, id){
    var useFullScreen = ($mdMedia('sm') || $mdMedia('xs'))  && $scope.customFullscreen;
      $scope.addComptSubID = id;
      $mdDialog.show({
        controller: AddComptController,
        templateUrl: 'addcomponent.tmpl.html',
        parent: angular.element(document.getElementById("popupContainer")),
        targetEvent: ev,
        clickOutsideToClose: true,
        fullscreen: useFullScreen,
        scope: $scope,
        preserveScope: true
      })
      .then(function() {
        //$scope.status = 'saved';
      }, function() {
        //$scope.status = 'You cancelled the dialog.';
      });

      $scope.$watch(function() {
        return $mdMedia('xs') || $mdMedia('sm');
      }, function(wantsFullScreen) {
        $scope.customFullscreen = (wantsFullScreen === true);
      });
  };

  $scope.delete = function(ev, sub){
    // Appending dialog to document.body to cover sidenav in docs app
      var confirm = $mdDialog.confirm()
            .title('Warning')
            .textContent('Would you like to delete "' + sub.name + '"?')
            .ariaLabel('Lucky day')
            .targetEvent(ev)
            .ok('Please do it!')
            .cancel('Cancel');

      $scope.RemoveSubproductID = sub.id;
      $mdDialog.show(confirm).then(function() {
        SubProductsService.remove($scope.RemoveSubproductID).then(function successCallback(response) {
          $state.go($state.current, {}, {reload: true});
        }, function errorCallback(response) {
          // TODO: report error
        });
      }, function() {
        //cancel.
      });
  };

  $scope.deleteComponent = function(ev, component){
    var confirm = $mdDialog.confirm()
            .title('Warning')
            .textContent('Would you like to delete "' + component.name + '"?')
            .ariaLabel('Lucky day')
            .targetEvent(ev)
            .ok('Please do it!')
            .cancel('Cancel');

    $scope.RemoveComponentID = component.id;
    $mdDialog.show(confirm).then(function() {
      ComponentService.remove($scope.RemoveComponentID).then(function successCallback(response) {
        $state.go($state.current, {}, {reload: true});
      }, function errorCallback(response) {
        // TODO: report error
      });
    }, function() {
      //cancel.
    });
  };
}

function AddComptController($scope, $state, $mdDialog, ComponentService){
  $scope.cmpt = {
    subproduct_id: $scope.addComptSubID,
    name: null,
    cmt: null
  };
  $scope.hide = function() {
    $mdDialog.hide();
  };

  $scope.cancel = function() {
    $mdDialog.cancel();
  };

  $scope.save = function() {
    ComponentService.create($scope.cmpt).then(function successCallback(response) {
      $mdDialog.hide();
      $state.go($state.current, {}, {reload: true});
    }, function errorCallback(response) {
      // TODO: report error
    });
  };
}