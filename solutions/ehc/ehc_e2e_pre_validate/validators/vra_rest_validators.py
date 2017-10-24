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
from .vra_rest_validator_base import VRARestValidator


class VRAHealthValidator(VRARestValidator):

    def response_validation(self, response_data):
        if response_data:
            count = len(response_data['content']) if response_data.get('content', None) else 0
            logging.info('vRA Catalog item count is :{}'.format(count))
            return count > 0, 'vRA is running ok and catalog page has items.'
        else:
            return False, 'vRA is having problem, failed to get catalog items, catalog page may not have any items.'
