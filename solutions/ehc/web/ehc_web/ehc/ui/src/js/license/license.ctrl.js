angular.module('license.ctrl', [
  'license.service',
  'pack.service',
  'bug.ctrl',
  'bug.service'
])
  .controller('LicenseCtrl', [
    '$scope', '$state', '$stateParams', '$uibModal', 'LicenseService', 'PackService', 'BugService', '$location', '$anchorScroll', LicenseCtrl]);

function LicenseCtrl($scope, $state, $stateParams, $uibModal, LicenseService, PackService, BugService, $location, $anchorScroll) {
  PackService.availableOpts().then(function(response) {
    $scope.availableOpts = response.data;
  }, function() {
    // TODO: error
  });


  $scope.licenseNameChange = function(license) {
    if (license.name.indexOf('Apache') < 0) {
      license.notice = null;
    }
  };

  // New a license view
  $scope.newLicenseView = function() {
    var license = {
      id: null,
      pack_id: $scope.nav.pack.id,
      name: null,
      license_url: null,
      unclear_license: null,
      license_text: null,
      editMode: true,
      sim_ratio: 0,
      is_standard: true
    };
    $scope.nav.pack.licenses.push(license);
    var license_id = 'license-' + ($scope.nav.pack.licenses.length);
    $location.hash(license_id);
    $anchorScroll();
  };

  // Cancel this license view
  $scope.cancelNewLicenseView = function() {
    $scope.nav.pack.licenses.pop();
    $location.hash('page-wrapper');
    $anchorScroll();
  };

  $scope.fetchRemoteLicenseText = function(license) {
    license.fetchingRemoteLicenseText = true;
    LicenseService.fetchRemoteLicenseText(license.license_url).then(function(response) {
      license.fetchingRemoteLicenseText = false;
      license.license_text = response.data;
    }, function() {
      // TODO: error
    });
  };

  $scope.fetchRemoteLicenseTextEventHandle = function($event, license) {
    if ($event.which === 13)
      $scope.fetchRemoteLicenseText(license);
  };

  $scope.createOrUpdateLicense = function(license) {
    if ('UNKNOWN' != license.name) {
      license.unclear_license = null;
    }
    if (license.license_text == null) {
      license.sim_ratio = null;
    }
    LicenseService.createOrUpdate(license).then(function(response) {
      license.nameConflict = false;
      if (license.id && response.status === 200) {
        license.editMode = false;
      }
      else if (!license.id && response.status === 201) {
        var last = $scope.nav.pack.licenses.length - 1;
        $scope.nav.pack.licenses[last] = response.data;
      }
    }, function(response) {
      if (response.status === 600) {
        // TODO: animate The same license already exist
        license.nameConflict = true;
      }

    });
  };

  $scope.deleteLicense = function(license) {
    LicenseService.delete(license.id).then(function(response) {
      // TODO: animate fadeout
      var index = $scope.nav.pack.licenses.indexOf(license);
      if (index > -1) {
        $scope.nav.pack.licenses.splice(index, 1);
      }
    }, function() {
      // TODO: error
    });
  };

  $scope.isLicenseEditOrCreateMode = function(license) {
    var ret = license.editMode === true;
    return ret;
  };


  $scope.openBugReportModal = function(size) {
    var modalInstance = $uibModal.open({
      animation: $scope.animationsEnabled,
      templateUrl: '/templates/bugs/report.html',
      controller: 'BugReportModalCtrl',
      size: size,
      resolve: {
        nav: function () {
          return $scope.nav;
        }
      }
    });

    modalInstance.result.then(function (bug) {
      // TODO: attache bugs here like licenses
      BugService.create(bug).then(function(response) {
        if (response.status == 201 || response.data) {
          $scope.nav.pack.bugs.push(response.data)
        } else {
          alert(response.message);
        }
      }, function(response) {
        alert(response.message);
      })
    }, function () {
      //$log.info('Modal dismissed at: ' + new Date());
    });
  };
}