'use strict';

/**
 * Route configuration for the RDash module.
 */
angular.module('RDash').config(['$stateProvider', '$urlRouterProvider',
  setupRDashState
])
.run(['$rootScope', '$state', '$stateParams', '$cookieStore', 'AuthService', function ($rootScope, $state, $stateParams, $cookieStore, AuthService) {
  $rootScope.$state = $state;
  $rootScope.$stateParams = $stateParams;

  AuthService.LoadCredentials();


}]);

function setupRDashState($stateProvider, $urlRouterProvider) {
  // For unmatched routes
  $urlRouterProvider.otherwise('/');

  var index = {
      url: '/',
      templateUrl: 'templates/dashboard.html',
      controller: 'DashboardCtrl'
  };

  var auth_login = {
    url: '/login',
    templateUrl: 'templates/auth/login.html',
    controller: 'AuthCtrl'
  };

  var auth_profile = {
    url: '/profile',
    templateUrl: 'templates/auth/profile.html',
    controller: 'ProfileCtrl'
  };

  var auth_github = {
    url: '/authgithub',
    templateUrl: 'templates/auth/github.html',
    controller: 'OAuthGithubCtrl'
  };

  var free_trivial = {
    url: '/try',
    templateUrl: 'templates/repos/free_trivial.html',
    controller: 'FreeTrivialCtrl'
  };

  var support = {
      url: '/support',
      templateUrl: 'templates/support.html'
  };

  // DOC: https://github.com/angular-ui/ui-router/wiki/Nested-States-and-Nested-Views#abstract-states
  var products = {
      abstract: true,
      url: '/products',
      template: '<div ui-view></div>'
  };

  var products_index = {
      url: '/index',
      templateUrl: 'templates/products/index.html',
      controller: 'TableCtrl'
  };

  var products_show = {
      url: '/{productId:[0-9]{1,8}}',
      templateUrl: 'templates/products/show.html',
      controller: 'ProductNavCtrl'
  };
  var products_show_releases = {
      abstract: true,
      url: '/releases',
      template: '<ui-view/>'
  };
  var products_show_releases_show = {
      abstract: true,
      url: '/:releaseId',
      template: '<ui-view/>'
  };

  var sub_products = {
      abstract: true,
      url: '/subs',  // Aka subproducts
      template: '<ui-view/>'
  };

  var sub_products_index = {
      url: '/index',
      templateUrl: 'templates/sub_products/index.html',
      controller: 'SubProductCtrl'
  };

  var components = {
    abstract: true,
    url: '/components',
    template: '<ui-view/>'
  };
  var components_show = {
    url: '/:componentId',
    templateUrl: 'templates/components/show.html',
    controller: 'ComponentCtrl'
  };

  var repos = {
    abstract: true,
    url: '/repos',
    template: '<ui-view/>'
  };
  var repos_show = {
    url: '/{repoId:int}',
    templateUrl: 'templates/repos/show.html',
    controller: 'RepoVersionCtrl'
  };
  var repos_new = {
    url:'/new',
    templateUrl: 'templates/repos/new.html',
    controller: 'NewRepoVersionCtrl'
  };
  var repos_edit = {
    url: '/:repoId/edit',
    templateUrl: 'templates/repos/edit.html',
    controller: 'EditRepoVersionCtrl'
  };

  var packs = {
    url: '/packs',
    templateUrl: 'templates/packs/base.html',
    controller: 'LicenseCtrl'
  };
  var packs_show = {
    url: '/{packId:[0-9]+}',
    templateUrl: 'templates/packs/show.html',
    controller: 'PackCtrl'
  };
  var packs_new = {
    url: '/new',
    templateUrl: 'templates/packs/new.html',
    controller: 'NewPackCtrl'
  };
  var packs_edit = {
    url: '/:packId/edit',
    templateUrl: 'templates/packs/edit.html',
    controller: 'PackCtrl'
  };

  var packs_search = {
    url: '/packs/search',
    templateUrl: 'templates/packs/search.html',
    controller: 'PackSearchCtrl'
  };

  var email = {
    abstract: true,
    url: '/email',
    template: '<ui-view/>'
  };

  var email_subproducts = {
    url: '/subproducts/:subproductId&stage=:stage',
    templateUrl: 'templates/misc/email_finished.html',
    controller:  function($scope, SubProductsService, $stateParams) {
      $scope.subproductName = null;
      SubProductsService.get($stateParams.subproductId).then(function(response) {
        $scope.subproductName = response.data.name;
        $scope.GoogleSheetSharedLink = null;
      });

    }
  };

  var demo = {
    url: '/editor',
    abstract: true,
    template: '<ui-view/>',
    // controller: 'DemoCtrl'
  };

  var demo_base = {
    url: '',
    templateUrl: 'templates/demo/base.html',
    controller: 'DemoCtrl'
  };

  var demo_show = {
    url: '/show',
    templateUrl: 'templates/demo/show.html',
    controller: 'DemoShowCtrl'
  };

  var demo_edit = {
    url: '/edit',
    templateUrl: 'templates/demo/edit.html',
    controller: 'DemoEditCtrl'
  };

  var run = {
    url: '/run',
    abstract: true,
    template: '<ui-view/>'
  };

  var run_wrokflow = {
    url: '/workflow',
    templateUrl: 'templates/run/workflow.html',
    controller: 'WorkflowCtrl'
  };

  var run_wrokflow_log = {
    url: '/:id',
    templateUrl: 'templates/run/workflow.log.html',
    controller: 'WorkflowLogCtrl'
  };

  // Application routes
  $stateProvider

    .state('demo', demo)
    .state('demo.base', demo_base)
    .state('demo.base.show', demo_show)
    .state('demo.base.edit', demo_edit)

    .state('run', run)
    .state('run.wf', run_wrokflow)
    .state('run.log', run_wrokflow_log)
    
    .state('index', index)

    .state('login', auth_login)
    .state('profile', auth_profile)
    .state('authgithub', auth_github)

    .state('email', email)
    .state('email.subproducts', email_subproducts)

    // TODO: Implement try page: Live data roll with WebSocket
    .state('free_trivial', free_trivial)

    .state('packs_search', packs_search)

    .state('support', support)
    .state('products', products)
    .state('products.index', products_index)
    .state('products.show', products_show)
    .state('products.show.releases', products_show_releases)
    .state('products.show.releases.show', products_show_releases_show)

    .state('products.show.releases.show.subs', sub_products)
    .state('products.show.releases.show.subs.index', sub_products_index)

    .state('components', components)
    .state('components.show', components_show)

    .state('components.show.rv', repos)
    .state('components.show.rv.show', repos_show)
    .state('components.show.rv.new', repos_new)
    .state('components.show.rv.edit',repos_edit)

    .state('components.show.rv.show.pv', packs)
    .state('components.show.rv.show.pv.new', packs_new)
    .state('components.show.rv.show.pv.show', packs_show)
    .state('components.show.rv.show.pv.edit', packs_edit);

}