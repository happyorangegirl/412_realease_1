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

from ehc_e2e.entity.datastore import Datastores


class GetDatastoreFromvRO(object):
    """
        Get datastore from vRO by HWI and cluster name
    """
    _vco_inventory_datastores_end_point = 'https://{}:8281/vco/api/inventory/DynamicTypes/DynamicNamespaceDefinition/EHC/EHC.DatastoreFolder/Datastores/'

    def get_datastore_from_vro(self, vro, hwi_name, cluster_name):
        from requests.auth import HTTPBasicAuth
        self.auth = HTTPBasicAuth(
            vro.username,
            vro.password
        )
        logger.debug(self._vco_inventory_datastores_end_point.format(vro.address), False)
        datastores = []
        try:
            requests.packages.urllib3.disable_warnings()
            response = requests.get(self._vco_inventory_datastores_end_point.format(vro.address), auth=self.auth,
                                    headers=self.__get_headers_for_vCO_REST(), verify=False)
            all_datastores = Datastores(response.text).get_datastore_list()
            logger.debug('{} Datastores are found in total'.format(len(all_datastores)), False)

            for datastore in all_datastores:
                if datastore.hardware_island == hwi_name and datastore.cluster_name == cluster_name:
                    datastores.append(datastore)
                    # self.datastore_names.append(datastore.name)
            return datastores
        except:
            ex = sys.exc_info()
            logger.error('Get datastore from vRO encounters error:{}'.format(ex), False)

        return datastores

    def get_datastore_names_from_vro(self, vro, hwi_name, cluster_name):
        datastore_names = []
        try:
            datastores = self.get_datastore_from_vro(vro, hwi_name, cluster_name)
            for datastore in datastores:
                datastore_names.append(datastore.name)

            return datastore_names
        except:
            ex = sys.exc_info()
            logger.error('get_datastore_names_from_vro encounters error:{}'.format(ex), False)

        return datastore_names

    def get_srps_from_vro(self, vro, hwi_name, cluster_name):
        datastore_srps = []
        try:
            datastores = self.get_datastore_from_vro(vro, hwi_name, cluster_name)
            for datastore in datastores:
                datastore_srps.append(datastore.srp)

            return datastore_srps
        except:
            ex = sys.exc_info()
            logger.error('get_srps_from_vro encounters error:{}'.format(ex), False)

        return datastore_srps

    def __get_headers_for_vCO_REST(self):
        headers = {
            'Accept': "application/xml",
            'Content-Type': "application/xml;charset=UTF-8"
        }
        return headers

    def filter_latest_storage(self, vro, hwi_name, cluster_name):

        try:
            datastores = self.get_datastore_from_vro(vro, hwi_name, cluster_name)
            if not datastores:
                logger.error('There is no datastore in vRO.', False)
                return None, None
            final_result = sorted(
                datastores, key=lambda datastore: int(datastore.id))[-1]

            return final_result.name, final_result.srp
        except:
            ex = sys.exc_info()
            logger.error('filter_latest_storage encounters error:{}'.format(ex), False)

        return None, None
