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

from urlparse import urljoin
import logging

from ehc_rest_utilities.session_manager.session_manager import VRASession
from ehc_rest_utilities.vra_rest_utilities.vra_rest_base import VRARestBase


class VRARestEx(VRARestBase):
    def __init__(self, host, tenant, username, password):
        super(VRARestEx, self).__init__(VRASession(host, tenant, username, password))
        self.vra_rest_url_base = 'https://' + host + '/'

    def request_resource(self, relative_url):
        vra_rest_request_url = urljoin(self.vra_rest_url_base, relative_url)
        logging.info('Start Requesting vRA resource by url:{}'.format(vra_rest_request_url))
        response = self.vra_session.get(vra_rest_request_url)
        if response.status_code == 200:
            logging.info('Request succeeded to get resource from url:{}'.format(vra_rest_request_url))
            return response.json()
        else:
            logging.error('Request failed to get resource from url:{}'.format(vra_rest_request_url))
            return response