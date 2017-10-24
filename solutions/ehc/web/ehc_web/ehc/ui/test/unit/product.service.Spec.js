describe('Unit test: product.service', function() {
  beforeEach(angular.mock.module('product.service'));
  var service;

  beforeEach(inject(function(_ProductService_) {
      service = _ProductService_;
  }));

  describe('ProductService:', function() {
    it('ProductService has been defined', function () {
      expect(service).toBeDefined();
      var products = service.query();
      expect(products.length).not.toBe(0);
    });
  });
});