describe('Unit test: RDash Module', function() {
  beforeEach(angular.mock.module('product.ctrl'));

  describe('ReleasesCtrl: method', function() {
    var scope, ctrl;

    beforeEach(angular.mock.inject(function($controller) {
      scope = {};
      ctrl = $controller('ReleasesCtrl', {$scope: scope});
    }));

    it('has 5 repos', function () {
      expect(scope.repos.length).toBe(5);
    });

    it('5 equal 5', function () {
      expect(5).toBe(5);
    });
    
  });
});