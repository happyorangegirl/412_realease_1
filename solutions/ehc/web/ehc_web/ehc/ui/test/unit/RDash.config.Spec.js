//RDash.config Module Test
describe('RDash.config Module Test', function () {
  //load module RDash.config
  beforeEach(module('RDash.config'));

  it('should have configured API', inject(function(EnvironmentConfig) {
    expect(EnvironmentConfig.api).toBeDefined();
  }));

});