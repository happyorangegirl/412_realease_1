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

# pylint: disable=too-few-public-methods

from ehc_rest_utilities.session_manager import VRASession
from ehc_rest_utilities.vra_rest_utilities import VRARestBase
from ehc_e2e.constants.vro_vra_constants import DEPLOYED_MACHINE_ITEMS

class VraRestUtil(object):
    def __init__(self, host, tenant, username, password):
        self.vra_session = VRASession(host=host, tenant=tenant, username=username, password=password)
        self.vra_rest_util = VRARestBase(self.vra_session)

    def get_vm_name_by_request_id(self, request_id):
        """
        Return the vm name for the given request id of deploy vm catalog item request.
        :param request_id: the request id of the deploy vm request. this can be obtained from Requests page.
        :return: VM name if the request succeeded, None otherwise.
        """
        vm_url = 'https://{host}/{vm_api}'.format(host=self.vra_session.host, vm_api=DEPLOYED_MACHINE_ITEMS)
        request_result = self.vra_rest_util.get_current_request_by_filter(
            filter_key='requestNumber', filter_value=request_id)
        request_guid = request_result.get('id')

        vm_json_data = self.vra_session.call_api_json('GET', vm_url, 200)
        if not vm_json_data:
            return None

        vm_item = [item for item in vm_json_data.get('content', []) if item.get('requestId') == request_guid]
        vm_name = vm_item[0].get('name') if vm_item else None

        return vm_name


if __name__ == '__main__':
    vra_util = VraRestUtil('vra-vip.vlab.local', 'dev123', 'ehc_sysadmin', 'Password123!')

    vms = vra_util.get_vm_name_by_request_id('1163')
