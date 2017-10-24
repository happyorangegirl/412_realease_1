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
from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.entity.asr import ASRs


class GetASRFromvRO(BaseUseCase):
    """
        Get all ASRs from vRO
    """
    _vco_inventory_asr_end_point = \
        'https://{}:8281/vco/api/inventory/DynamicTypes/DynamicNamespaceDefinition/EHC/EHC.ASRFolder/ASRs/'

    def test_get_asr_from_vro(self):
        from requests.auth import HTTPBasicAuth
        self.auth = HTTPBasicAuth(
            self.vro_username,
            self.vro_password
        )
        logger.info(self._vco_inventory_asr_end_point.format(self.vro_address), False, True)
        try:
            requests.packages.urllib3.disable_warnings()
            response = requests.get(self._vco_inventory_asr_end_point.format(self.vro_address), auth=self.auth,
                                    headers=self.__class__.get_headers_for_vco_rest(), verify=False)
            all_asrs = ASRs(response.text).get_asr_list()
            logger.info('Totally {} ASR are found'.format(len(all_asrs)), False, True)
            self.asrs = all_asrs
        except:
            ex = sys.exc_info()
            logger.error('Error:{}'.format(ex), False)
            self.fail(msg='Running on step: "Cloud Administrator Gets ASRs"-FAILED.')

    @staticmethod
    def get_headers_for_vco_rest():
        headers = {
            'Accept': "application/xml",
            'Content-Type': "application/xml;charset=UTF-8"
        }
        return headers

    def runTest(self):
        self.test_get_asr_from_vro()

    def _validate_context(self):
        if self.ctx_in:
            self.vro_address = self.ctx_in.vro.address
            self.vro_username = self.ctx_in.vro.username
            self.vro_password = self.ctx_in.vro.password
            assert self.vro_address is not None, 'vRO address is not provided!'
            assert self.vro_username is not None, 'vRO username is not provided!'
            assert self.vro_password is not None, 'vRO password is not provided!'
        self.asrs = []

    def _finalize_context(self):
        self.ctx_out.get_asr_from_vro.available_asr = self.asrs
