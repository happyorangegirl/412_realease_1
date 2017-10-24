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
from urlparse import urljoin

from ehc_rest_utilities.vro_rest_utilities.vro_rest_base import VRORestBase
from ehc_rest_utilities.session_manager.session_manager import VROSession


class VROApiExtension(VRORestBase):
    VRO_API_ROOT_URL_FORMATTER = 'https://{host}:8281/vco/api/'.format

    def __init__(self, host, username, password):
        super(VROApiExtension, self).__init__(VROSession(host, username, password))

    def execute_api(self, relative_api_url):
        resource_url = urljoin(
            self.__class__.VRO_API_ROOT_URL_FORMATTER(host=self.vro_session.host), relative_api_url)
        logging.info('The url to request is :{}'.format(resource_url))
        response = self.vro_session.get(resource_url)
        if response.status_code == 200:
            logging.info('Succeeded to GET resources from vro by url:{}'.format(resource_url))
            return response.json()
        else:
            logging.error('Failed to GET resources from vRO by url:{}. HTTP status = {}'.format(
                response.status_code, resource_url))

        return None


if __name__ == '__main__':
    vro_api_extension = VROApiExtension('192.168.3.110', 'xiongb2@vlab.local', 'Password123!')
    print vro_api_extension.execute_action(action_name='getAllViPRVirtualArrays')
    print vro_api_extension.execute_api(relative_api_url='packages')
