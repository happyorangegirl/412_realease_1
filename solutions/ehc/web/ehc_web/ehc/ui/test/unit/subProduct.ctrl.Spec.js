//subProduct.ctrl Module Test
describe('subProduct.ctrl Module Test', function () {
  var module = angular.module('subProduct.ctrl');

  it('should exist', function() {
    expect(module).not.toBeNull();
  });

});

//subProduct.ctrl Controller Test
describe('SubProductCtrl controller', function () {
  var scope, stateParams;
  beforeEach(function () {
    module('subProduct.ctrl');
    module('release.service');
    inject(function ($rootScope, $controller) {
      scope = $rootScope.$new();
      $controller('SubProductCtrl', {$scope: scope});
    });
  });

});