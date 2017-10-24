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

from .validatorbase import ValidatorBase
from ..validate_result import ValidationResult, Result


class VROAPIValidator(ValidatorBase):
    def __init__(self, name, vro_api_extension, api_relative_url):
        super(VROAPIValidator, self).__init__(name)
        self.vro_api_extension = vro_api_extension
        self.api_relative_url = api_relative_url

    def validate(self):
        rest_response = self.vro_api_extension.execute_api(self.api_relative_url)
        if rest_response:
            logging.info(
                'Start validating rest response for vRO relative URI: {}'.format(self.api_relative_url))
            response_validation_ret = self.response_validation(rest_response)
            self.validation_result = ValidationResult(
                self.name, Result.PASS if response_validation_ret[0] else Result.FAIL, response_validation_ret[1])
        else:
            self.validation_result = ValidationResult(
                self.name, Result.FAIL,
                'failed to get rest response for vRO relative URI:{}'.format(self.api_relative_url)
            )
