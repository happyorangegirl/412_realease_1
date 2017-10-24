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
from ehc_e2e.entity.datastore import Datastores


class GetDatastoreFromvRO(BaseUseCase):
    """
        Get datastore from vRO by HWI and cluster name
    """
    _vco_inventory_datastores_end_point = \
        'https://{}:8281/vco/api/inventory/DynamicTypes/DynamicNamespaceDefinition/EHC/EHC.DatastoreFolder/Datastores/'

    def test_get_datastore_from_vro(self):
        from requests.auth import HTTPBasicAuth
        self.auth = HTTPBasicAuth(
            self.vro_username,
            self.vro_password
        )
        logger.info(self._vco_inventory_datastores_end_point.format(self.vro_address), False, True)
        try:
            requests.packages.urllib3.disable_warnings()
            response = requests.get(self._vco_inventory_datastores_end_point.format(self.vro_address), auth=self.auth,
                                    headers=self.__class__.get_headers_for_vco_rest(), verify=False)
            all_datastores = Datastores(response.text).get_datastore_list()
            logger.info('Totally {} Datastores are found'.format(len(all_datastores)), False, True)
            for datastore in all_datastores:
                if datastore.hardware_island == self.hwi_name and datastore.cluster_name == self.cluster_name:
                    self.datastore_names.append(datastore.name)
        except:
            ex = sys.exc_info()
            logger.error('Error:{}'.format(ex), False)
            self.fail(msg='Running on step: "Cloud Administrator Gets Datastores"-FAILED.')

    @staticmethod
    def get_headers_for_vco_rest():
        headers = {
            'Accept': "application/xml",
            'Content-Type': "application/xml;charset=UTF-8"
        }
        return headers

    def runTest(self):
        self.test_get_datastore_from_vro()

    def _validate_context(self):
        if self.ctx_in:
            self.vro_address = self.ctx_in.vro.address
            self.vro_username = self.ctx_in.vro.username
            self.vro_password = self.ctx_in.vro.password
            self.hwi_name = self.ctx_in.added_cloud_storage[0].hwi_name
            self.cluster_name = self.ctx_in.added_cloud_storage[0].cluster_name
            assert self.vro_address is not None, 'vRO address is not provided!'
            assert self.vro_username is not None, 'vRO username is not provided!'
            assert self.vro_password is not None, 'vRO password is not provided!'
            assert self.hwi_name is not None, 'Datastore filter criteria - HWI name is not provided!'
            assert self.cluster_name is not None, 'Datastore filter criteria - Cluster name is not provided!'
        self.datastore_names = []

    def _finalize_context(self):
        self.ctx_out.added_cloud_storage[0].name = self.datastore_names
