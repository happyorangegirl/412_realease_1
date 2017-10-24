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

import time
import logging
from ehc_rest_utilities.parameters.vra_rest_apis import CATALOG_ITEM_API, CATALOG_REQUEST_API, TENANT_API, \
    PRINCIPAL_API, USER_ROLE_API, DIRECTORY_API, FILTER
from ehc_rest_utilities.parameters.vra_payload_templates import CREATE_TENANT_TEMPLATE, ADD_USER_TEMPLATE, \
    ADD_DIRECTORY_TEMPLATE, ALL_ROLES_TEMPLATE
from ehc_rest_utilities.session_manager import VRASession


class VRARestBase(object):

    def __init__(self, vra_session):
        assert isinstance(vra_session, VRASession), 'VRARestBase accepts VRASession instance only'
        self.vra_session = vra_session
        self.host = 'https://{host}'.format(host=vra_session.host)

    def get_vra_session(self):
        return self.vra_session

    def set_vra_session(self, vra_session):
        assert isinstance(vra_session, VRASession), 'set_vra_session accepts VRASession instance only'
        self.vra_session = vra_session

    def request_catalog_item(self, catalog_item_name, **kwargs):
        # find catalog item resource
        json_data = self.vra_session.call_api_json(
            'GET', '{host}/{api}{filter}'.format(host=self.host, api=CATALOG_ITEM_API,
                                                 filter=FILTER.format(key='name', value=catalog_item_name)), 200)
        if not json_data:
            logging.error('Failed to retrieve catalog item resources from vRA host')
            return None

        if json_data['metadata']['totalElements'] < 1:
            logging.error('Cannot find catalog item {0}'.format(catalog_item_name))
            return None

        get_request_template_url = json_data['content'][0]['links'][0]['href']
        post_request_url = json_data['content'][0]['links'][1]['href']

        # get request template
        json_data = self.vra_session.call_api_json('GET', get_request_template_url, 200)
        if not json_data:
            logging.error('Failed to get request template resource from vRA')
            return None

        # update request template then post it
        json_data['data'].update((k, kwargs[k]) for k in json_data['data'].viewkeys() & kwargs.viewkeys())
        return self.vra_session.call_api_json('POST', post_request_url, 201, json=json_data)

    def get_catalog_item_request(self, request_id):
        return self.vra_session.call_api_json('GET', '{host}/{api}/{id}'
                                              .format(host=self.host, api=CATALOG_REQUEST_API, id=request_id), 200)

    def get_current_request_by_filter(self, filter_key=None, filter_value=None):
        """   this method is to filter request according to key and value.
        match_key = {'description': 'description',
                      'item': 'catalog item'
                      'request': 'requestNumber'
                      }
        :param filter_key: item name in rest about request info
        :param filter_value: the value for filter key
        :return: request dict info
        """
        if not (filter_key and filter_value):
            logging.error('Please provide key and value to filter request.')
            return None

        json_data = self.vra_session.call_api_json(
            'GET', '{host}/{api}{filter}&$orderby=requestNumber desc'.format(
                host=self.host, api=CATALOG_REQUEST_API, filter=FILTER.format(
                    key=filter_key, value=filter_value)), 200)

        if not json_data:
            return None

        if json_data['metadata']['totalElements'] < 1:
            logging.error('Cannot find the request')
            return None

        return json_data['content'][0]

    def check_request_status(self, rid, timeout=600, interval=10):
        while timeout > 0:
            timeout -= interval
            time.sleep(interval)

            request = self.get_catalog_item_request(rid)
            request_status = request.get('stateName')
            if request_status == 'Successful':
                return True
            elif request_status == 'Failed':
                logging.warning('Request No.{0} failed with message {1}'
                                .format(request['requestNumber'], request['requestCompletion']['completionDetails']))
                return False

        logging.warning('Timed out to check request status')
        return False

    def create_tenant(self, **kwargs):
        input_template = CREATE_TENANT_TEMPLATE
        input_template.update(kwargs)
        return self.vra_session.call_api_json('PUT', '{host}/{api}/{tenant_id}'.format(
            host=self.host, api=TENANT_API, tenant_id=input_template['urlName']), 200, json=input_template)

    def get_tenant(self, tenant_id):
        return self.vra_session.call_api_json('GET', '{host}/{api}/{tenant_id}'.format(
            host=self.host, api=TENANT_API, tenant_id=tenant_id), 200)

    def if_tenant_exists(self, tenant_id):
        response = self.vra_session.get(url='{host}/{api}/{id}'.format(host=self.host, api=TENANT_API, id=tenant_id))
        return True if response.status_code == 200 else False

    def add_local_user(self, tenant, **kwargs):
        input_template = ADD_USER_TEMPLATE
        self.update_template(input_template, kwargs)
        return self.vra_session.call_api_json('POST', '{host}/{api}'.format(
            host=self.host, api=PRINCIPAL_API.format(tenant=tenant)), 200, json=input_template)

    def assign_role(self, tenant, user, role):
        return self.vra_session.call_api_json('PUT', '{host}/{api}/{role}'.format(
            host=self.host, api=USER_ROLE_API.format(tenant=tenant, user=user), role=role), 204)

    def assign_multi_roles(self, tenant, user, role_list=ALL_ROLES_TEMPLATE):
        return self.vra_session.call_api_json('PUT', '{host}/{api}'.format(
            host=self.host, api=USER_ROLE_API.format(tenant=tenant, user=user)), 204, json=role_list)

    def add_directory(self, tenant, **kwargs):
        input_template = ADD_DIRECTORY_TEMPLATE
        input_template.update(kwargs)
        return self.vra_session.call_api_json('POST', '{host}/{api}'.format(
            host=self.host, api=DIRECTORY_API.format(tenant=tenant)), 201, json=input_template)

    def get_directory(self, tenant):
        return self.vra_session.call_api_json('GET', '{host}/{api}'.format(
            host=self.host, api=DIRECTORY_API.format(tenant=tenant)), 200)

    @staticmethod
    def update_template(left, right):
        for k, v in right.iteritems():
            if isinstance(v, dict) and isinstance(left.get(k), dict):
                VRARestBase.update_template(left[k], v)
            else:
                left[k] = v

    @staticmethod
    def timestamp():
        return time.strftime('%y%m%d%I%M%p', time.localtime())
