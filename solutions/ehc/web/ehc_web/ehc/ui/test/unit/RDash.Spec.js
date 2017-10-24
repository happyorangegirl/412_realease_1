//RDash Module Test
describe('RDash Module Test', function () {
  var module = angular.module('RDash');

  it('should exist', function() {
    expect(module).not.toBeNull();
  });

});

//RDash Route Test
describe('RDash Route Test', function () {
  var $state;
  beforeEach(function() {

    module('RDash');

    inject(function(_$state_) {
      $state = _$state_;
    })
  });

  it('should respond to URL', function() {
    expect($state.href('index')).toEqual('#/');
    expect($state.href('login')).toEqual('#/login');

    expect($state.href('free_trivial')).toEqual('#/try');

    expect($state.href('support')).toEqual('#/support');
    expect($state.href('products')).toEqual('#/products');
    expect($state.href('products.index')).toEqual('#/products/index');
    expect($state.href('products.show', { productId: 1 })).toEqual('#/products/1');
    expect($state.href('products.show.releases', { productId: 1 })).toEqual('#/products/1/releases');
    expect($state.href('products.show.releases.show', { productId: 1, releaseId: 1 })).toEqual('#/products/1/releases/1');

    expect($state.href('products.show.releases.show.subs', { productId: 1, releaseId: 1 })).toEqual('#/products/1/releases/1/subs');
    expect($state.href('products.show.releases.show.subs.index', { productId: 1, releaseId: 1 })).toEqual('#/products/1/releases/1/subs/index');

    expect($state.href('components')).toEqual('#/components');
    expect($state.href('components.show', { componentId: 1 })).toEqual('#/components/1');

    expect($state.href('components.show.rv', { componentId: 1 })).toEqual('#/components/1/repos');
    expect($state.href('components.show.rv.show', { componentId: 1, repoId: 1 })).toEqual('#/components/1/repos/1');
    expect($state.href('components.show.rv.new', { componentId: 1 })).toEqual('#/components/1/repos/new');
    expect($state.href('components.show.rv.edit', { componentId: 1, repoId: 1 })).toEqual('#/components/1/repos/1/edit');

    expect($state.href('components.show.rv.show.pv', { componentId: 1, repoId: 1 })).toEqual('#/components/1/repos/1/packs');
    expect($state.href('components.show.rv.show.pv.new', { componentId: 1, repoId: 1 })).toEqual('#/components/1/repos/1/packs/new');
    expect($state.href('components.show.rv.show.pv.show', { componentId: 1, repoId: 1, packId:1 })).toEqual('#/components/1/repos/1/packs/1');
    expect($state.href('components.show.rv.show.pv.edit', { componentId: 1, repoId: 1, packId:1 })).toEqual('#/components/1/repos/1/packs/1/edit');
  });
});