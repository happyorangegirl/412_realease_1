//subProduct Module Test
describe('subProduct Module Test', function () {
  var module = angular.module('subProduct');

  it('should exist', function() {
    expect(module).not.toBeNull();
  });

});

//subProduct.service Module Test
describe('subProduct.service Module Test', function () {
  var module = angular.module('subProduct.service');

  it('should exist', function() {
    expect(module).not.toBeNull();
  });

});

//SubProductsService Factory Test
describe('SubProductsService Factory Test', function() {
  //load module mq.service
  beforeEach(module('subProduct.service'));
  //load module RDash.config
  beforeEach(module('RDash.config'));

  it('should have SubProductsService Factory', inject(function(SubProductsService) {
    expect(SubProductsService).toBeDefined();

    var id = 0;
    promise = SubProductsService.create(id);
    expect(promise).not.toBeNull();

    promise = SubProductsService.remove(id);
    expect(promise).not.toBeNull();
  }));

});