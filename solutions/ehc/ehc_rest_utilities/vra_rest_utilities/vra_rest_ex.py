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

from vra_rest_base import VRARestBase
from ehc_rest_utilities.parameters.vra_rest_apis import CATALOG_ITEM_API


class VRARestEx(VRARestBase):

    def get_blueprint_names(self):
        json_data = self.vra_session.call_api_json('GET', '{host}/{api}'
                                                   .format(host=self.host, api=CATALOG_ITEM_API), 200)
        if not json_data:
            return None
        return [catalog_item['name'] for catalog_item in json_data['content']
                if catalog_item['catalogItemTypeRef']['label'] == 'Composite Blueprint']
