angular.module('demo.service', [])
  .factory('DemoService', ['$http', 'EnvironmentConfig', DemoService])
  .factory('JSONEditorService', [JSONEditorService]);

function DemoService($http, EnvironmentConfig) {
  var api = EnvironmentConfig.api + '/demo';
  return {
    getJSONSchema: function (schema_filename) {
      var params = {
        'schema_filename': schema_filename,
        // 'disable_edit_json': true,
        // 'disable_properties': true,
        'refs': {},
        // 'required_by_default': true
      };
      return $http.get(api, params);
    },

    // TODO: filter parameters
    // Get full list of workflow
    getWorkflows: function () {
      var uri = api + '/workflows/';
      return $http.get(uri);
    },

    export_editor_data: function (schema, schema_filename, editor_data) {
      var uri = api + '/workflows/';
      var data = {
        'schema': schema,
        'schema_filename': schema_filename,
        'editor_data': editor_data
      }
      return $http.post(uri, data);
    },

    // updateJSON: function (text) {
    //   var data = {
    //     'mode': 'JSON',
    //     'text': text
    //   }
    //   return $http.post(api, data);
    // }

  };
}

function JSONEditorService() {
  
  return {
    new_editor: function (element_id, options) {
      var element = document.getElementById(element_id);
      
      var defaults = { 
        theme: 'bootstrap3',
        // ajax: true,
        show_errors: "always",
        iconlib: 'bootstrap3',
        schema: {}
      };
      var actual = window.$.extend({}, defaults, options || {})

      var editor = new window.JSONEditor(element, actual);

      return editor
    }
  };
}

//ddd

