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
from ehc_rest_utilities.parameters.vro_rest_apis import WORKFLOW_API, ACTION_API
from ehc_rest_utilities.session_manager import VROSession


class VRORestBase(object):

    def __init__(self, vro_session):
        assert isinstance(vro_session, VROSession), 'VRORestBase accepts VROSession instance only'
        self.vro_session = vro_session
        self.host = 'https://{host}:{port}'.format(host=vro_session.host, port=vro_session.port)

    # workflow execution does not return any specific information. just returns execution resource URL in this method
    def execute_workflow(self, wf_name, input_template=None, **kwargs):
        if not input_template:
            input_template = self.create_input_template()
            for k, v in kwargs.iteritems():
                self.append_parameter(input_template, k, v)
        json_data = self.vro_session.call_api_json('GET', '{host}/{api}'.format(host=self.host, api=WORKFLOW_API), 200)
        if not json_data:
            return None

        for workflow in json_data.get('link', []):
            wf_attributes = self.name_value_pairs_to_dict(workflow.get('attributes', {}))
            if wf_name == wf_attributes.get('name'):
                response = self.vro_session.post(url=wf_attributes['itemHref'] + 'executions', json=input_template)
                if response.status_code != 202:
                    logging.error('Failed to POST workflow execution request. HTTP status = {0}. Response content = {1}'
                                  .format(response.status_code, response.content))
                    return None
                return response.headers['Location']

        logging.warning('Workflow {0} not found'.format(wf_name))
        return None

    def get_wf_execution(self, exec_url):
        return self.vro_session.call_api_json('GET', exec_url, 200)

    def check_wf_execution_status(self, exec_url, timeout=600, interval=10):
        while timeout > 0:
            timeout -= interval
            time.sleep(interval)

            wf_exec = self.get_wf_execution(exec_url)
            exec_status = wf_exec.get('state')
            if exec_status == 'completed':
                return True
            elif exec_status == 'failed':
                logging.warning('Workflow {0} failed with message: {1}'
                                .format(exec_url, wf_exec.get('content-exception')))
                return False

        logging.warning('Timed out to check workflow execution status')
        return False

    def execute_action(self, action_name, input_template=None, **kwargs):
        if not input_template:
            input_template = self.create_input_template()
            for k, v in kwargs.iteritems():
                self.append_parameter(input_template, k, v)

        json_data = self.vro_session.call_api_json('GET', '{host}/{api}'.format(host=self.host, api=ACTION_API), 200)
        if not json_data:
            return None

        for action in json_data.get('link', []):
            action_attributes = self.name_value_pairs_to_dict(action.get('attributes', {}))
            if action_name == action_attributes.get('name'):
                return self.vro_session.call_api_json('POST', action['href'] + 'executions', 200, json=input_template)
        logging.warning('Action {0} not found'.format(action_name))
        return None

    @staticmethod
    def name_value_pairs_to_dict(nv_pairs):
        return {nv_pair['name']: nv_pair.get('value', '') for nv_pair in nv_pairs if 'name' in nv_pair}

    def extract_sdk_objects(self, action_execution_result):
        sdk_objects = []
        try:
            for obj in action_execution_result['value']['array']['elements']:
                json_data = self.vro_session.call_api_json('GET', obj['sdk-object']['href'], 200)
                if json_data:
                    sdk_objects.append(self.name_value_pairs_to_dict(json_data.get('attributes', {})).get('name'))
        except:
            logging.error('Failed to read sdk-objects from action execution result. Please verify the output format')
            return None
        return sdk_objects

    @staticmethod
    def create_input_template():
        return {'parameters': []}

    @staticmethod
    def append_parameter(input_template, param_name, param_value, param_type=None):
        # if you see any error like 'type can not be null'
        # please help investigate the correct input type and put it into template
        basic_type_mapping = {
            str: 'string',
            int: 'number',
            bool: 'boolean'}

        if isinstance(param_value, list):
            value_to_append = {'array': {'elements': []}}
            for value in param_value:
                if isinstance(value, dict):
                    value_to_append['array']['elements'].append(value)
                elif type(value) in basic_type_mapping:
                    value_to_append['array']['elements'].append(
                        {basic_type_mapping[type(value)]: {'value': value}})
                else:
                    logging.warning('Failed to append parameter: Type {0} not supported yet'.format(type(value)))

        elif isinstance(param_value, dict):
            value_to_append = param_value

        elif type(param_value) in basic_type_mapping:
            basic_type = basic_type_mapping[type(param_value)]
            value_to_append = {basic_type: {'value': param_value}}
            if param_type is None:
                param_type = basic_type

        else:
            logging.warning('Failed to append parameter: Type {0} not supported yet'.format(type(param_value)))
            return

        param_to_append = {
            'name': param_name,
            'value': value_to_append
        }
        if param_type:
            param_to_append['type'] = param_type

        input_template['parameters'].append(param_to_append)
