var RDashModule = angular.module('RDash');
RDashModule.controller('TableCtrl', ['$scope', '$state', '$log', '$mdDialog', '$mdMedia', '$rootScope', '$filter',
  function ($scope, $state,  $log, $mdDialog, $mdMedia, $rootScope, $filter) {
    $scope.nav = {
      productName: 'dd',
      releaseVersion: '',
      subProductName: ''
    };
    //$scope.$on('updateProductName', function(event) {
    //  event.currentScope.navBar.productName = event.targetScope.productName;
    //});

    $scope.currentPage = 1;
    $scope.numPages = 5;
    $scope.pageSize = 5;
    $scope.pages = [];
    $scope.status = ' ';
    $scope.customFullscreen = $mdMedia('xs')||$mdMedia('sm');
    $scope.allData = null;
    $scope.allProduct = null;

    $scope.onSelectPage = function (page) {
      /*ProductService.query().then(function successCallback(response) {
        $scope.numPages = Math.ceil(response.data.length/$scope.pageSize);
        $scope.products = response.data.slice((page - 1)* $scope.pageSize, (page - 1)* $scope.pageSize + $scope.pageSize);
      }, function errorCallback(response) {
        // TODO: report error
      });*/
      $scope.currentPage = page;
      $scope.numPages = Math.ceil($scope.allData.length/$scope.pageSize);
      $scope.products = $scope.allData.slice((page - 1)* $scope.pageSize, (page - 1)* $scope.pageSize + $scope.pageSize);
    };

    $scope.sortType = 'id';
    $scope.sortReverse = false;
    $scope.searchProduct = {name: ''};
    $scope.filteredItems = null;

    $scope.printState = function () {
      console.log($state.current == 'tables');
    };

    $scope.gotoDashbarod = function () {
      $state.go('index');
    };

    var searchMatch = function (haystack, needle) {
        if (!needle) {
            return true;
        }
        var haystackString;

        if (typeof(haystack) !== "string") {
            haystackString = toString(haystack);
        } else {
            haystackString = haystack;
        }
        return haystackString.toLowerCase().indexOf(needle.toLowerCase()) !== -1;
    };

    $scope.search = function(){
      $scope.filteredItems = $filter('filter')($scope.allProduct, function (item) {
        for(var attr in item) {
          if (searchMatch(item[attr], $scope.searchProduct.name))
            return true;
        }
        return false;
      });
      $scope.currentPage = 1;
      $scope.groupToPages();
    };

    $scope.groupToPages = function () {
      $scope.allData = $scope.filteredItems;
      $scope.numPages = Math.ceil($scope.allData.length/$scope.pageSize);
      $scope.products = $scope.filteredItems.slice(0, $scope.pageSize);
    };

    $scope.addProduct = function(ev) {
      // Appending dialog to document.body to cover sidenav in docs app
      // Modal dialogs should fully cover application
      // to prevent interaction outside of dialog
      var useFullScreen = ($mdMedia('sm') || $mdMedia('xs'))  && $scope.customFullscreen;

      $mdDialog.show({
        controller: DialogController,
        templateUrl: 'dialog1.tmpl.html',
        parent: angular.element(document.getElementById("popupContainer")),
        targetEvent: ev,
        clickOutsideToClose: true,
        fullscreen: useFullScreen
      })
      .then(function() {
        //$scope.status = 'saved';
      }, function() {
        $scope.status = 'You cancelled the dialog.';
      });

      $scope.$watch(function() {
        return $mdMedia('xs') || $mdMedia('sm');
      }, function(wantsFullScreen) {
        $scope.customFullscreen = (wantsFullScreen === true);
      });
    };

    $scope.delete = function(ev, id, p){
      // Appending dialog to document.body to cover sidenav in docs app
      var confirm = $mdDialog.confirm()
            .title('Warning')
            .textContent('Would you like to delete "' + p.name + '"?')
            .ariaLabel('Lucky day')
            .targetEvent(ev)
            .ok('Please do it!')
            .cancel('Cancel');

      $mdDialog.show(confirm).then(function() {
        var index=$scope.allData.indexOf(p);
        if(index > -1) $scope.allData.splice(index,1);
        $scope.products = $scope.allData.slice(($scope.currentPage - 1)* $scope.pageSize, ($scope.currentPage - 1)* $scope.pageSize + $scope.pageSize);
        $scope.status = 'Delete!'
      }, function() {
        $scope.status = 'Cancel.';
      });
    };

    $scope.activeProduct = {
      name: null,
      cmt: null,
      user_id: null
    };
    $scope.edit = function(ev, product) {
      var useFullScreen = ($mdMedia('sm') || $mdMedia('xs'))  && $scope.customFullscreen;
      $scope.activeProduct = product;
      $mdDialog.show({
        controller: UpdateDialogController,
        templateUrl: 'updatedialog.tmpl.html',
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
        $scope.status = 'You cancelled the dialog.';
      });

      $scope.$watch(function() {
        return $mdMedia('xs') || $mdMedia('sm');
      }, function(wantsFullScreen) {
        $scope.customFullscreen = (wantsFullScreen === true);
      });
    };

    $scope.addRelease = function(ev, id) {
      var useFullScreen = ($mdMedia('sm') || $mdMedia('xs'))  && $scope.customFullscreen;
      $scope.addReleaseProID = id;
      $mdDialog.show({
        controller: AddReleaseDialogController,
        templateUrl: 'addrelease.tmpl.html',
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
        $scope.status = 'You cancelled the dialog.';
      });

      $scope.$watch(function() {
        return $mdMedia('xs') || $mdMedia('sm');
      }, function(wantsFullScreen) {
        $scope.customFullscreen = (wantsFullScreen === true);
      });

    };
  }]
)
.controller('UpdateDialogController', ['$scope', '$state', '$mdDialog',  'ProductService',  DialogController])
.controller('UpdateDialogController', ['$scope', '$state', '$mdDialog', 'ProductService',  UpdateDialogController])
.controller('AddReleaseDialogController', ['$scope', '$state', '$mdDialog', AddReleaseDialogController]);

function DialogController($scope, $state, $mdDialog, ProductService) {
  $scope.fields = {
    name: null,
    cmt: null,
    user_id: null
  };
  $scope.hide = function() {
    $mdDialog.hide();
  };

  $scope.cancel = function() {
    $mdDialog.cancel();
  };

  $scope.save = function() {
    ProductService.create($scope.fields).then(function successCallback(response) {
      $mdDialog.hide();
      $state.go($state.current, {}, {reload: true});
      //$state.go('products.show.releases.show.subs.index', {productId: response.data.id, releaseVersion: 'v2.3.1'});
      // TODO: clear $scope.fields;
    }, function errorCallback(response) {
      // TODO: report error
    });

  };
}

function UpdateDialogController($scope, $state, $mdDialog, ProductService) {
  $scope.hide = function() {
    $mdDialog.hide();
  };

  $scope.cancel = function() {
    $mdDialog.cancel();
  };

  $scope.save = function() {
    $mdDialog.hide();
  };
}

function AddReleaseDialogController($scope, $state, $mdDialog) {
  $scope.activeRelease = {
    product_id: $scope.addReleaseProID,
    version: null,
    cmt: null
  };
  $scope.hide = function() {
    $mdDialog.hide();
  };

  $scope.cancel = function() {
    $mdDialog.cancel();
  };

  $scope.save = function() {
  };
}

RDashModule.directive('paging',function () {
  return {
    restrict: 'EA',
    template: '',
    replace: true,
    link: function($scope, $element, $attrs) {
      $scope.$watch(function() {
        var newValue = $scope.currentPage + ' ' + $scope.numPages;
        return newValue;
      }, function() {
        $scope.pages = [];
        //if ($scope.currentPage > $scope.numPages) {
          //$scope.selectPage($scope.numPages);
        //}
        $scope.pagesLength = 9 ;
        if($scope.numPages <= $scope.pagesLength) {
          for(var i = 1; i <= $scope.numPages; i++) {
            $scope.pages.push(i);
          }
        } else {
          var offset = ($scope.pagesLength -1)/2;
          if($scope.currentPage <= offset) {
            for(var i = 1; i <= offset + 1; i++) {
              $scope.pages.push(i);
            }
            $scope.pages.push('...');
            $scope.pages.push($scope.numPages);
          } else if ($scope.currentPage > $scope.numPages - offset) {
            $scope.pages.push(1);
            $scope.pages.push('...');
            for(var i = offset + 1; i >= 1; i--) {
              $scope.pages.push($scope.numPages - i);
            }
            $scope.pages.push($scope.numPages);
          } else {
            $scope.pages.push(1);
            $scope.pages.push('...');
            for(var i = offset/2; i >= 1; i--) {
              $scope.pages.push($scope.currentPage - i);
            }
            $scope.pages.push($scope.currentPage);
            for(var i = 1; i <= offset/2; i++) {
              $scope.pages.push($scope.currentPage + i);
            }
            $scope.pages.push('...');
            $scope.pages.push($scope.numPages);
          }
        }

      });
      $scope.isActive = function (page) {
        return $scope.currentPage === page;
      };
      $scope.noPrevious = function () {
        return $scope.currentPage == 1;
      };
      $scope.noNext = function () {
        return $scope.currentPage == $scope.numPages;
      };
      $scope.selectPage = function (page) {
        if (page == '...') {
          return;
        }else {
          if (!$scope.isActive(page)) {
            $scope.currentPage = page;
            $scope.onSelectPage(page);
          }
        }
        
      };
      $scope.selectPrevious = function () {
        if (!$scope.noPrevious()) {
          $scope.selectPage($scope.currentPage - 1);
        }
      };
      $scope.selectNext = function () {
        if (!$scope.noNext()) {
          $scope.selectPage($scope.currentPage + 1);
        }
      };
    }
  };
});