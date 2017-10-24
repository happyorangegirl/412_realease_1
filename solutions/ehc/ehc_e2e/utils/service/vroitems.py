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

from robot.api import logger
from ehc_rest_utilities.session_manager.session_manager import VROSession
from ehc_rest_utilities.vro_rest_utilities.vro_rest_base import VRORestBase
import ehc_e2e.constants.vro_vra_constants as vro_vra_constants


class VroItems(object):
    def __init__(self, wf_context):
        vro = wf_context.vro
        self.vro_session = VROSession(host=vro.address, username=vro.username, password=vro.password)
        self.vro_rest_base = VRORestBase(self.vro_session)

    def get_specific_item_by_name_from_vro(self, item_name, item_api):
        """
        Args:
          item_name: specific item name(STRING)
          item_api: item api to get(STRING)

        Returns: REST request response, vro_rest_base
        """
        (vro_response_dict, vro_rest_base) = self.get_all_items_from_vro(item_api)
        if vro_response_dict:
            for item in vro_response_dict.get('relations', {}).get('link', []):
                item_attr = vro_rest_base.name_value_pairs_to_dict(item.get('attributes', {}))
                if item_name == item_attr.get('name'):
                    logger.info("Item: {} already exist".format(item_name))
                    return True
        else:
            return False

    def get_all_items_from_vro(self,item_api):
        """
        Args:
          item_api: item api to get(STRING)

        Returns: REST request response, vro_rest_base
        """

        # https://192.168.3.166:8281/vco/api/inventory/DynamicTypes/DynamicNamespaceDefinition/EHC/EHC.vCenterFolder/vCenters/
        url = r"https://{0}:{1}{2}{3}".format(
            self.vro_session.host, self.vro_session.port, vro_vra_constants.DYNAMIC_TYPES_API, item_api)
        try:
            logger.info("Start to check get request using: {}".format(url))
            response = self.vro_session.get(
                url, auth=self.vro_session.auth, headers=self.vro_session.headers, verify=False)
            if response.status_code != vro_vra_constants.HTTP_SUCCESS_RESPONSE:
                logger.error("Request: {0} response from vro {1} is not OK.".format(url, self.vro_session.host))
                return None, None
            return response.json(), self.vro_rest_base
        except Exception as e:
            logger.error(
                "Exception {0}, occurs when trying to get response from target URL: {1}.".format(e, url))
            raise
