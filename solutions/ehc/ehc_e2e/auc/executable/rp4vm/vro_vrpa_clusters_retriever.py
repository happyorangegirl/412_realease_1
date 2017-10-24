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
from ehc_e2e.entity.vrpacluster import vRPAClusters


class VROvRPAClustersRetriever(BaseUseCase):
    """
        Get vRPA Clusters from vRO by HWI and cluster name
    """
    _vco_inventory_vrpa_clusters_end_point = \
        'https://{}:8281/vco/api/inventory/DynamicTypes/DynamicNamespaceDefinition/EHC/' \
        'EHC.vRPAClusterFolder/vRPAClusters/'

    def test_get_vrpa_clusters_from_vro(self):
        from requests.auth import HTTPBasicAuth
        self.auth = HTTPBasicAuth(
            self.vro_username,
            self.vro_password
        )
        logger.info(self._vco_inventory_vrpa_clusters_end_point.format(self.vro_address), False, True)
        try:
            requests.packages.urllib3.disable_warnings()
            response = requests.get(self._vco_inventory_vrpa_clusters_end_point.format(self.vro_address),
                                    auth=self.auth, headers=self.__get_headers_for_vCO_REST(), verify=False)
            self.matched_vrpa_clusters = vRPAClusters(response.text).get_matched_rp4vm_vrpa_cluster_list(self.ips)
            logger.info('Totally {} vRPA Clusters are found'.format(len(self.matched_vrpa_clusters)), False, True)
        except:
            ex = sys.exc_info()[0]
            logger.error('Error:{}'.format(ex), False)
            self.fail('Running on step: "Cloud Administrator Gets vRPA CLusters"-FAILED.')

    def __get_headers_for_vCO_REST(self):
        headers = {
            'Accept': "application/xml",
            'Content-Type': "application/xml;charset=UTF-8"
        }
        return headers

    def runTest(self):
        self.test_get_vrpa_clusters_from_vro()

    def _validate_input_args(self, vro_address, vro_username, vro_password, pri_ip, sec_ip):
        self.vro_address = vro_address
        self.vro_username = vro_username
        self.vro_password = vro_password
        self.ips = [pri_ip, sec_ip]
        self.matched_vrpa_clusters = []
        assert self.vro_address is not None, 'vRO address is not provided!'
        assert self.vro_username is not None, 'vRO username is not provided!'
        assert self.vro_password is not None, 'vRO password is not provided!'
        assert len(self.ips) > 1, 'Both primary and secondary VRPA cluster IP addresses are required.'

    def _finalize_output_params(self):
        if self.matched_vrpa_clusters:
            self._output.extend(self.matched_vrpa_clusters)
