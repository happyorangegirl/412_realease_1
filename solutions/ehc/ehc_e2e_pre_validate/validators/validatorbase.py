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


from ..validate_result import  ValidationResult, Result

class ValidatorBase(object):

    def __init__(self, name):
        self.name = name
        self.validation_result = ValidationResult(self.name, Result.FAIL, '')

    def validate(self):
        """
        return an instance of ValidationResult
        :return: an instance of ValidationResult
        """
        raise NotImplementedError

    def response_validation(self, response_data):

        pass

    def __str__(self):
        return self.name
