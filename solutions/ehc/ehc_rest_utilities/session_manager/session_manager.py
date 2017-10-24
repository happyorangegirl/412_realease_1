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

from xml.etree import ElementTree
import logging
import requests
from requests.auth import HTTPBasicAuth
from requests.sessions import Session
from ehc_rest_utilities.parameters.vra_rest_apis import AUTH_API
from ehc_rest_utilities.parameters.vipr_rest_apis import LOGIN_API, LOGOUT_API
requests.packages.urllib3.disable_warnings()


class BaseSession(Session):

    # assume host accepts and returns json
    def call_api_json(self, method, url, expected_status, json=None):
        response = self.request(method, url, json=json)
        if response.status_code != expected_status:
            logging.error('Failed to request URL: {0}. REST method: {1}. HTTP status: {2}. Response content: {3}'
                          .format(url, method, response.status_code, response.content))
            return None
        return response.json() if response.content else {}


class VRASession(BaseSession):

    def __init__(self, host, tenant, username, password):
        super(VRASession, self).__init__()

        self.verify = False     # disable SSL
        self.host = host
        self.tenant = tenant

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '}

        body = {
            'username': username,
            'password': password,
            'tenant': tenant}

        # request auth token.
        response = self.post(url='https://{host}/{api}'.format(host=self.host, api=AUTH_API),
                             headers=headers, json=body)
        if response.status_code == 200:
            headers['Authorization'] += response.json()['id']
        else:
            raise RuntimeError('Failed to authenticate: ' + response.json()['errors'][0]['systemMessage'])

        # save header to session
        self.headers.update(headers)


class VROSession(BaseSession):

    def __init__(self, host, username, password):
        super(VROSession, self).__init__()

        self.verify = False
        self.auth = HTTPBasicAuth(username, password)
        self.host = host
        self.port = 8281    # temporarily hard coded
        self.headers = {'Accept': "application/json",
                        'Content-Type': "application/json"}


class ViPRSession(BaseSession):

    def __init__(self, host, username, password):
        super(ViPRSession, self).__init__()

        self.verify = False
        self.auth = HTTPBasicAuth(username, password)
        self.port = 4443
        self.host = host
        self.headers = {'Accept': "application/json",
                        'Content-Type': "application/json"}

        response = self.get('https://{host}:{port}/{api}'.format(host=self.host, port=self.port, api=LOGIN_API))
        if response.status_code == 200:
            self.auth = None
            self.headers['X-SDS-AUTH-TOKEN'] = response.headers['X-SDS-AUTH-TOKEN']
        else:
            root = ElementTree.fromstring(response.content)
            # not support json while login
            raise RuntimeError('Failed to authenticate: ' + root.find('head/title').text)
        self.logged_in = True

    def logout(self):
        if self.logged_in:
            self.get('https://{host}:{port}/{api}'.format(host=self.host, port=self.port, api=LOGOUT_API))
        self.logged_in = False
