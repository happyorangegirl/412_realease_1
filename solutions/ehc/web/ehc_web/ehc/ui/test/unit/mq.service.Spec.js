//mq.service Module Test
describe('mq.service Module Test', function () {
  var module = angular.module('mq.service');

  it('should exist', function() {
    expect(module).not.toBeNull();
  });

});

//MQService Factory Test
describe('MQService Factory Test', function() {
  //load module mq.service
  beforeEach(module('mq.service'));
  //load module RDash.config
  beforeEach(module('RDash.config'));

  it('should have MQService Factory', inject(function(MQService) {
    expect(MQService).toBeDefined();

    var pack_ids = [1];
    promisePack = MQService.enqueuePacks(pack_ids);
    expect(promisePack).not.toBeNull();

    var repo_ids = [1];
    promiseRepo = MQService.enqueueRepos(repo_ids);
    expect(promiseRepo).not.toBeNull();
  }));

});