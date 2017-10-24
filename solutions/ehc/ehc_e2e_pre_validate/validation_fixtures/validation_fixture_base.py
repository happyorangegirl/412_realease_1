#  Copyright 2016 EMC GSE SW Automation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import logging
import time
from ehc_e2e_pre_validate.rest_utilities import (VRARestEx, VROApiExtension, VRA_CATALOG_ITEM_REST_RELATIVE_URL)
from ehc_e2e_pre_validate.validation_controllers import ValidationController
from ehc_e2e_pre_validate.validators.vra_rest_validators import VRAHealthValidator
from ehc_e2e_pre_validate.validators.vro_action_validators import VROVCenterValidator
from ehc_e2e_pre_validate.validators.vro_api_validators import \
    (VROEHCFoundationPluginValidator, VROEHCPackagesValidator, VROHealthValidator, VROViprPluginValidator)


class ValidationFixtureBase(object):
    def __init__(self, validation_fixture_name='EHC E2E Prevalidation', **kwargs):
        self._kwargs = kwargs
        self._validation_controller = ValidationController(validator_sequence_name=validation_fixture_name)

    def setUp(self):
        # extracting those values from config file.
        vra_rest_ext = VRARestEx('vra-vip.vlab.local', 'dev110', 'ehc_sysadmin', 'Password123!')
        vro_api_ext = VROApiExtension('192.168.3.110', 'xiongb2@vlab', 'Password123!')
        vcenter_fqdns_to_check = ['vcs01.vlab.local']

        vro_health_validator = VROHealthValidator('vRO Health Validator', vro_api_ext, 'healthstatus')
        vra_health_validator = VRAHealthValidator(
            'vRA Health Validator', vra_rest_ext, VRA_CATALOG_ITEM_REST_RELATIVE_URL)
        vro_ehc_packages_validator = VROEHCPackagesValidator('vRO EHC Packages Validator', vro_api_ext, 'packages')
        vro_vipr_plugin_validator = VROViprPluginValidator('vRO Vipr Plugin Validator', vro_api_ext, 'plugins')
        vro_ehc_foundation_plugin_validator = VROEHCFoundationPluginValidator(
            'vRO EHC Foundation Plugin Validator', vro_api_ext, 'plugins')
        vro_vcenter_svr_validator = VROVCenterValidator(
            'vRO VCenter Servers Validator', vro_api_ext, 'getAllVCenters', **{'vcenter_fqdns': vcenter_fqdns_to_check})

        vro_validators = [vro_health_validator, vro_ehc_packages_validator, vro_ehc_foundation_plugin_validator,
                          vro_vipr_plugin_validator, vro_vcenter_svr_validator]
        vra_validators = [vra_health_validator]
        self._validation_controller.add_validators(vro_validators + vra_validators)
        if self._kwargs.get('validators_to_extend', []):
            self._validation_controller.add_validators(self._kwargs['validators_to_extend'])

    def run_fixture(self):
        try:
            self.setUp()
            logging.info('Waiting until all requests complete...')
            time.sleep(3)
            self._validation_controller.process_validators()
        finally:
            self.tearDown()

    def tearDown(self):
        self._validation_controller.print_results()

if __name__ == '__main__':
    validation_fixture = ValidationFixtureBase()
    validation_fixture.run_fixture()
