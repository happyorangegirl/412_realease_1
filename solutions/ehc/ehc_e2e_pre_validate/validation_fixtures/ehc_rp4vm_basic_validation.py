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

from ehc_e2e_pre_validate.validation_fixtures.validation_fixture_base import ValidationFixtureBase

from ehc_e2e_pre_validate.rest_utilities import VROApiExtension
from ehc_e2e_pre_validate.validators.vro_api_validators import VRORP4VMPackageValidator


class EhcRP4VMBasiceValidation(ValidationFixtureBase):
    def __init__(self):
        vro_api_ext = VROApiExtension('192.168.3.110', 'xiongb2@vlab', 'Password123!')
        vro_rp4vm_plugin_validator = VRORP4VMPackageValidator('vRO RP4VM Package Validator', vro_api_ext, 'packages')
        super(EhcRP4VMBasiceValidation, self).__init__(
            validation_fixture_name='EHC E2E RP4VM Prevalidation',
            **{'validators_to_extend':[vro_rp4vm_plugin_validator]}
        )


if __name__ == '__main__':
    rp4vm = EhcRP4VMBasiceValidation()
    rp4vm.run_fixture()
