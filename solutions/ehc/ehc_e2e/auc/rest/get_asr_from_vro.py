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

import sys

import requests
from robot.api import logger

from ehc_e2e.entity.asr import ASRs
from .constants import REST_HEADER


class GetASRFromvRO(object):
    """
        Get all ASRs from vRO
    """
    _vco_inventory_asr_end_point = \
        'https://{}:8281/vco/api/inventory/DynamicTypes/DynamicNamespaceDefinition/EHC/EHC.ASRFolder/ASRs/'

    def get_asr_from_vro(self, vro):
        from requests.auth import HTTPBasicAuth
        self.auth = HTTPBasicAuth(
            vro.username,
            vro.password
        )
        logger.info(self._vco_inventory_asr_end_point.format(vro.address), False, True)
        try:
            requests.packages.urllib3.disable_warnings()
            response = requests.get(self._vco_inventory_asr_end_point.format(vro.address), auth=self.auth,
                                    headers=REST_HEADER, verify=False)
            if response.status_code == 200:
                all_asrs = ASRs(response.text).get_asr_list()
                logger.info('Totally {} ASRs are found'.format(len(all_asrs)), False, True)
                self.asrs = all_asrs
                return self.asrs
            else:
                logger.error(
                    'Requesting vro resource:{} failed.'.format(self._vco_inventory_asr_end_point.format(vro.address)))
        except:
            logger.error('Error:{}'.format(sys.exc_info()), False)
            return None
