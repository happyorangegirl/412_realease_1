angular.module('demo.ctrl', [
  'demo.service',
  'ngSanitize',
  'ui.select'
])
  .controller('DemoShowCtrl', ['$scope', '$state', '$stateParams', 'DemoService', DemoShowCtrl])
  .controller('DemoEditCtrl', ['$scope', '$state', '$stateParams', DemoEditCtrl])
  .controller('ModalInstanceCtrl', ['$scope', '$uibModalInstance', 'actionResult', '$state', /*'originRaw',*/ ModalInstanceCtrl])
  .controller('DemoCtrl', ['$scope', '$state', '$stateParams', '$window', 'DemoService', '$uibModal', DemoCtrl]);


function ModalInstanceCtrl($scope, $uibModalInstance, actionResult, $state) {

  $scope.actionResult = actionResult;

  $scope.ok = function () {
    $uibModalInstance.close($scope.actionResult);
  };

  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };

  // $scope.reload = function() {
  //   $state.go($state.current, {}, {reload: true});
  //   $uibModalInstance.close($scope.actionResult);
  // }
}


function DemoCtrl($scope, $state, $stateParams, $window, DemoService, $uibModal) {
  var self = this;

  self.selected_workflow = {};

  $scope.workflows = [];
  DemoService.getWorkflows().then(function(response) {
    $scope.workflows = response.data;
    console.log($scope.workflows);
  }, function(response) {
      alert('Error: get server data error' + response.data);
  });

  $scope.data = {
    schema: null,
    error: null,
    schema_filename: null
  };
  $scope.schema_filename = '';
  $scope.editor = null;

  $scope.onSelectWorkflow = function($item, $model) {
    console.log($item);
    self.selected_workflow = $item;

    DemoService.getJSONSchema(self.selected_workflow.schema_filename).then(function(response) {

      $scope.data = response.data;
      console.log($scope.data);

      var element_id = 'editor_holder';
      var opts = {
        schema: $scope.data.schema
      };
      if ($scope.editor !== null) {
        $scope.editor.destroy();
        $scope.valid = false;
      }

      $scope.editor = JSONEditorService().new_editor(element_id, opts);
      $scope.editor.on('ready', function() {
        $scope.valid = $scope.editor.validate().length == 0;
      });
      $scope.editor.on('change', function() {
        $scope.valid = $scope.editor.validate().length == 0;
        console.log($scope.valid);
      });
      console.log($scope.editor);
    }, function(response) {
      alert('Error: get server data error');
      console.log(response)
    });
  };

  $scope.exportEditorData = function(schema, schema_filename, editor_data) {
    console.log(editor_data);
    DemoService.export_editor_data(schema, schema_filename, editor_data).then(function(response) {
      $scope.actionResult = response.data;
      $scope.open('sm');
    }, function(response) {
      // alert(response.data);
      $scope.actionResult = response.data;
      $scope.open('lg');
    })

  };
  

  /**
   * size: lg|sm
   */
  $scope.open = function (size, templateUrl='rawTextSaveSuccess.html') {
    var modalInstance = $uibModal.open({
      animation: $scope.animationsEnabled,
      templateUrl: templateUrl,
      controller: 'ModalInstanceCtrl',
      size: size,
      resolve: {
        actionResult: function () {
          return $scope.actionResult;
        }
      }
    });

    modalInstance.result.then(function (selectedItem) {
      $scope.selected = selectedItem;
    }, function () {
      $log.info('Modal dismissed at: ' + new Date());
    });
  };

  $scope.saveRawYAML = function() {
    DemoService.updateRaw($scope.bdl.raw).then(function(response) {
      $scope.actionResult = response.data;
      $scope.open('sm');
    },function(response) {
      $scope.actionResult = response.data;
      $scope.open('lg');
    })
  };

  $scope.saveJSON = function() {
    DemoService.updateJSON($scope.bdl.obj).then(function(response) {
      $scope.actionResult = response.data;
      $scope.open('sm');
    },function(response) {
      $scope.actionResult = response.data;
      $scope.open('lg', templateUrl='rawTextSaveFailed.html');
    })
  };

}


function DemoShowCtrl($scope, $state, $stateParams, DemoService) {
    $scope.active = 1;
    $scope.obj = {};
    $scope.filename = 'foo.yaml';

    $scope.isOptions = function(item) {
      
      return true;
    };

    $scope.isString = function(item) {
      return Object.prototype.toString.call(item) === '[object String]';
    };

    $scope.isArray = function(item) {
      return Object.prototype.toString.call(item) === '[object Array]';
    };

    $scope.isObject = function(item) {
      return Object.prototype.toString.call(item) === '[object Object]';
    };

    $scope.initTopKey = function(key) {
      key.editMode = false;
    }

}

function DemoEditCtrl($scope, $state, $stateParams) {
    $scope.obj = {};
}