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
from ehc_rest_utilities.parameters.vipr_rest_apis import ORDER_API, CATALOG_SERVICE_API, PROJECT_API, \
    PROJECT_ACL_API, CURRENT_TENANT_API, CREATE_PROJECT_API, FILTER
from ehc_rest_utilities.session_manager import ViPRSession


# need try catch block to close session on exception
class ViPRRestBase(object):

    def __init__(self, vipr_session):
        assert isinstance(vipr_session, ViPRSession), 'ViPRRestBase accepts ViPRSession instance only'
        self.vipr_session = vipr_session
        self.host = 'https://{host}:{port}'.format(host=vipr_session.host, port=vipr_session.port)

    def close_vipr_session(self):
        self.vipr_session.logout()

    def get_tenant_id(self):
        json = self.vipr_session.call_api_json('GET', '{host}/{api}'.format(host=self.host, api=CURRENT_TENANT_API), 200)
        return json.get('id')

    def create_project(self, name):
        curr_tenant = self.get_tenant_id()
        return self.vipr_session.call_api_json('POST', '{host}/{api}'.format(
            host=self.host, api=CREATE_PROJECT_API.format(id=curr_tenant)), 200, {'name': name})

    def update_project(self, project_id, name=None, owner=None):
        json_input = {}
        if name:
            json_input['name'] = name
        if owner:
            json_input['owner'] = owner
        if not json_input:
            logging.warning('Missing name or owner information. Updating aborted.')
            return None

        return self.vipr_session.call_api_json(
            'PUT', '{host}/{api}/{id}'.format(host=self.host, api=PROJECT_API, id=project_id), 200, json=json_input)

    def add_acl(self, project_id, name, user_type, access='ALL'):
        user_type = user_type.lower()
        add_dict = {}
        if user_type == 'user':
            add_dict['subject_id'] = name
        elif user_type == 'group':
            add_dict['group'] = name
        add_dict['privilege'] = [access]
        json_input = {'add': [add_dict]}
        return self.vipr_session.call_api_json('PUT', '{host}/{api}'.format(
            host=self.host, api=PROJECT_ACL_API.format(id=project_id)), 200, json=json_input)

    def order_catalog_service(self, catalog_service_name, **kwargs):
        json_data = self.vipr_session.call_api_json(
            'GET', '{host}/{api}/{filter}'.format(host=self.host, api=CATALOG_SERVICE_API, filter=FILTER
                                                  .format(key='name', value=catalog_service_name)), 200)
        if not json_data:
            return None

        for catalog_service in json_data.get('resource', []):
            if catalog_service_name == catalog_service.get('match'):
                json_input = self.generate_parameters_input(**kwargs)
                json_input['catalog_service'] = catalog_service['id']

                return self.vipr_session.call_api_json(
                    'POST', '{host}/{api}'.format(host=self.host, api=ORDER_API), 200, json=json_input)

        logging.warn('Catalog service {0} not found'.format(catalog_service_name))
        return None

    def get_order(self, oid):
        return self.vipr_session.call_api_json('GET', '{host}/{api}/{id}'.format(host=self.host, api=ORDER_API, id=oid), 200)

    def check_order_status(self, order_id, timeout=600, interval=10):
        while timeout > 0:
            timeout -= interval
            time.sleep(interval)

            order = self.get_order(order_id)
            order_status = order.get('order_status')
            if order_status == 'SUCCESS':
                return True
            elif order_status == 'ERROR':
                logging.warning('Order {0} failed with message: {1}'.format(order_id, order.get('message')))
                return False

        logging.warning('Timed out to check order status')
        return False

    @staticmethod
    def generate_parameters_input(**kwargs):
        template = {'parameters': []}
        for k, v in kwargs.iteritems():
            attr_dict = dict()
            attr_dict['label'] = str(k)
            attr_dict['value'] = str(v)
            template['parameters'].append(attr_dict)
        return template
