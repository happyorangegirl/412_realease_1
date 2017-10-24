'use strict';

/**
 * AngularJS Basic HTTP Authentication Example.
 * Homepage:  https://github.com/cornflourblue/angular-authentication-example
 */

angular.module('auth.service', [])
  .factory('Base64', Base64)
  .factory('AuthService',
    ['Base64', '$http', '$cookieStore', '$rootScope', '$timeout', 'EnvironmentConfig', '$state', AuthService]);


function AuthService(Base64, $http, $cookieStore, $rootScope, $timeout, EnvironmentConfig, $state) {
  var service = {};
  var api = EnvironmentConfig.api;
  var globalsCookieKey = 'globals';

  service.Login = function (username, password) {
    /* Dummy authentication for testing, uses $timeout to simulate api call
     ----------------------------------------------*/
    /*$timeout(function(){
      var response = { success: checkAuthInfo(username, password) };
      if(!response.success) {
        response.message = 'Username or password is incorrect';
      }
      callback(response);
    }, 1000);*/

    // TODO:
    /* Use this for real authentication
     ----------------------------------------------*/
    var uri = api + '/auth/basic';
    return true;
    // return $http.post(uri, { username: username, password: password });
  };

  service.SetCredentials = function (username, password) {
    var authdata = Base64.encode(username + ':' + password);

    $rootScope.globals = {
      currentUser: {
        username: username,
        authdata: authdata
      }
    };

    $http.defaults.headers.common['Authorization'] = 'Basic ' + authdata; // jshint ignore:line
    $cookieStore.put('globals', $rootScope.globals);
  };

  // TODO:
  service.LoadCredentials = function () {
    //$rootScope.globals
    var globals = $cookieStore.get(globalsCookieKey);
    globals = globals ? globals : {};
    $cookieStore.put(globalsCookieKey, globals);
    $rootScope.globals = globals;

    if ($rootScope.globals.currentUser !== undefined) {
      $http.defaults.headers.common['Authorization'] = 'Basic ' + $rootScope.globals.currentUser.authdata; // jshint ignore:line
    }

    $rootScope.$on('$stateChangeStart', function(event, toState, fromState) {
      if (toState.name == 'support') {;}
      else if (toState.name !== 'login' && $rootScope.globals.currentUser === undefined && toState.name !== 'authgithub') {
        event.preventDefault();
        $state.go('login');
      }
    });
  };

  service.ClearCredentials = function () {
    var globals = $cookieStore.get(globalsCookieKey);
    delete globals.currentUser;
    $cookieStore.put(globalsCookieKey, globals);
    $rootScope.globals = globals;
    $http.defaults.headers.common.Authorization = 'Basic ';
  };

  service.GetGithubUserInfo = function (code) {
    //var cliend_id = EnvironmentConfig.cliendID;
    //var cliend_secret = EnvironmentConfig.cliendSecret;
    var data = {
      code : code
    };
    var uri = api + '/githuboauth/getuser';
    //return $http.post('https://github.com/login/oauth/access_token&cliend_id='+cliend_id+'&cliend_secret='+cliend_secret+'&code='+code);
    return $http.post(uri, data);
  };

  return service;
}

function checkAuthInfo(username, password) {
  return username === 'test' && password === 'test'
}

function Base64() {
  /* jshint ignore:start */

  var keyStr = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';

  return {
    encode: function (input) {
      var output = "";
      var chr1, chr2, chr3 = "";
      var enc1, enc2, enc3, enc4 = "";
      var i = 0;

      do {
        chr1 = input.charCodeAt(i++);
        chr2 = input.charCodeAt(i++);
        chr3 = input.charCodeAt(i++);

        enc1 = chr1 >> 2;
        enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
        enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
        enc4 = chr3 & 63;

        if (isNaN(chr2)) {
          enc3 = enc4 = 64;
        } else if (isNaN(chr3)) {
          enc4 = 64;
        }

        output = output +
          keyStr.charAt(enc1) +
          keyStr.charAt(enc2) +
          keyStr.charAt(enc3) +
          keyStr.charAt(enc4);
        chr1 = chr2 = chr3 = "";
        enc1 = enc2 = enc3 = enc4 = "";
      } while (i < input.length);

      return output;
    },

    decode: function (input) {
      var output = "";
      var chr1, chr2, chr3 = "";
      var enc1, enc2, enc3, enc4 = "";
      var i = 0;

      // remove all characters that are not A-Z, a-z, 0-9, +, /, or =
      var base64test = /[^A-Za-z0-9\+\/\=]/g;
      if (base64test.exec(input)) {
        window.alert("There were invalid base64 characters in the input text.\n" +
          "Valid base64 characters are A-Z, a-z, 0-9, '+', '/',and '='\n" +
          "Expect errors in decoding.");
      }
      input = input.replace(/[^A-Za-z0-9\+\/\=]/g, "");

      do {
        enc1 = keyStr.indexOf(input.charAt(i++));
        enc2 = keyStr.indexOf(input.charAt(i++));
        enc3 = keyStr.indexOf(input.charAt(i++));
        enc4 = keyStr.indexOf(input.charAt(i++));

        chr1 = (enc1 << 2) | (enc2 >> 4);
        chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);
        chr3 = ((enc3 & 3) << 6) | enc4;

        output = output + String.fromCharCode(chr1);

        if (enc3 != 64) {
          output = output + String.fromCharCode(chr2);
        }
        if (enc4 != 64) {
          output = output + String.fromCharCode(chr3);
        }

        chr1 = chr2 = chr3 = "";
        enc1 = enc2 = enc3 = enc4 = "";

      } while (i < input.length);

      return output;
    }
  };

  /* jshint ignore:end */
}