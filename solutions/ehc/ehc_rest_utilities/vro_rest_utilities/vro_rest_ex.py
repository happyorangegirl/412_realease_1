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
from vro_rest_base import VRORestBase
from ehc_rest_utilities.parameters.vro_rest_apis import CATALOG_VCAC_API, CATALOG_VCACCAFE_API, PLATFORM_TYPE_API, \
    CREDENTIAL_API, PREFIX_API, ENDPOINT_API, BUSINESS_GROUP_API


class VRORestEx(VRORestBase):

    def get_vra_host(self, vra_url, tenant):
        json = self.vro_session.call_api_json(
            'GET', '{host}/{api}'.format(host=self.host, api=CATALOG_VCACCAFE_API), 200)
        if not (json and json.get('relations')):
            return None

        for vcaccafe_host in json['relations'].get('link', []):
            vcac_attributes = self.name_value_pairs_to_dict(vcaccafe_host.get('attributes', {}))
            if vra_url == vcac_attributes.get('url') and tenant == vcac_attributes.get('tenant'):
                vcac_attributes['href'] = vcaccafe_host['href']
                return vcac_attributes

        logging.info('vRA host not found. URL={0}, tenant={1}'.format(vra_url, tenant))
        return None

    def get_vra_host_by_name(self, vra_host_name):
        json = self.vro_session.call_api_json(
            'GET', '{host}/{api}'.format(host=self.host, api=CATALOG_VCACCAFE_API), 200)
        if not (json and json.get('relations')):
            return None

        for vcaccafe_host in json['relations'].get('link', []):
            vcac_attributes = self.name_value_pairs_to_dict(vcaccafe_host.get('attributes', {}))
            if vra_host_name == vcac_attributes.get('name'):
                vcac_attributes['href'] = vcaccafe_host['href']
                return vcac_attributes

        logging.info('vRA host {0} not found.'.format(vra_host_name))
        return None

    def get_iaas_host(self, iaas_url):
        json = self.vro_session.call_api_json('GET', '{host}/{api}'.format(host=self.host, api=CATALOG_VCAC_API), 200)
        if not (json and json.get('relations')):
            return None

        for vcac_host in json['relations'].get('link', []):
            vcac_attributes = self.name_value_pairs_to_dict(vcac_host.get('attributes', {}))
            if iaas_url == vcac_attributes.get('url'):
                vcac_attributes['href'] = vcac_host['href']
                return vcac_attributes

        logging.info('IaaS host not found. URL={0}'.format(iaas_url))
        return None

    def get_iaas_host_by_name(self, iaas_host_name):
        json = self.vro_session.call_api_json('GET', '{host}/{api}'.format(host=self.host, api=CATALOG_VCAC_API), 200)
        if not (json and json.get('relations')):
            return None

        for vcac_host in json['relations'].get('link', []):
            vcac_attributes = self.name_value_pairs_to_dict(vcac_host.get('attributes', {}))
            if iaas_host_name == vcac_attributes.get('name'):
                vcac_attributes['href'] = vcac_host['href']
                return vcac_attributes

        logging.info('IaaS {0} host not found.'.format(iaas_host_name))
        return None

    def add_vra_host(self, **kwargs):
        input_template = self.create_input_template()
        for k, v in kwargs.iteritems():
            if k == 'authPassword':
                self.append_parameter(input_template, k, v, 'SecureString')
            else:
                self.append_parameter(input_template, k, v)

        return self.execute_workflow('Add a vRA host', input_template)

    def add_iaas_host(self, **kwargs):
        input_template = self.create_input_template()
        for k, v in kwargs.iteritems():
            if k == 'authPassword':
                self.append_parameter(input_template, k, v, 'SecureString')
            else:
                self.append_parameter(input_template, k, v)

        return self.execute_workflow('Add an IaaS host', input_template)

    def remove_vra_host(self, vra_url, tenant):
        vcaccafe = self.get_vra_host(vra_url, tenant)
        if not vcaccafe:
            return None
        vcaccafe_sdk_object = {'sdk-object': {'href': vcaccafe['href'], 'id': vcaccafe['id']}}

        input_template = self.create_input_template()
        self.append_parameter(input_template, 'host', vcaccafe_sdk_object)
        return self.execute_workflow('Remove a vRA host', input_template)

    def remove_vra_host_by_name(self, vra_host_name):
        vcaccafe = self.get_vra_host_by_name(vra_host_name)
        if not vcaccafe:
            return None
        vcaccafe_sdk_object = {'sdk-object': {'href': vcaccafe['href'], 'id': vcaccafe['id']}}

        input_template = self.create_input_template()
        self.append_parameter(input_template, 'host', vcaccafe_sdk_object)
        return self.execute_workflow('Remove a vRA host', input_template)

    def remove_iaas_host(self, iaas_url):
        vcac = self.get_iaas_host(iaas_url)
        if not vcac:
            return None
        vcac_sdk_object = {'sdk-object': {'href': vcac['href'], 'id': vcac['id']}}

        input_template = self.create_input_template()
        self.append_parameter(input_template, 'host', vcac_sdk_object)
        return self.execute_workflow('Remove an IaaS host', input_template)

    def remove_iaas_host_by_name(self, iaas_host_name):
        vcac = self.get_iaas_host_by_name(iaas_host_name)
        if not vcac:
            return None
        vcac_sdk_object = {'sdk-object': {'href': vcac['href'], 'id': vcac['id']}}

        input_template = self.create_input_template()
        self.append_parameter(input_template, 'host', vcac_sdk_object)
        return self.execute_workflow('Remove an IaaS host', input_template)

    def get_platform_type(self, platform_name):
        json = self.vro_session.call_api_json('GET', '{host}/{api}'.format(host=self.host, api=PLATFORM_TYPE_API), 200)
        if not json:
            return None

        for pf_type in json.get('link', []):
            pf_attributes = self.name_value_pairs_to_dict(pf_type.get('attributes', {}))
            if platform_name == pf_attributes.get('displayName'):
                pf_attributes['href'] = pf_type['href']
                return pf_attributes

        logging.info('Platform type {0} not found'.format(platform_name))
        return None

    def get_credential(self, credential_name):
        json = self.vro_session.call_api_json('GET', '{host}/{api}'.format(host=self.host, api=CREDENTIAL_API), 200)
        if not json:
            return None

        for cred in json.get('link', []):
            cred_attributes = self.name_value_pairs_to_dict(cred.get('attributes', {}))
            if credential_name == cred_attributes.get('displayName'):
                cred_attributes['href'] = cred['href']
                return cred_attributes

        logging.info('Credential {0} not found'.format(credential_name))
        return None

    def get_machine_prefix(self, prefix_name):
        json = self.vro_session.call_api_json('GET', '{host}/{api}'.format(host=self.host, api=PREFIX_API), 200)
        if not json:
            return None

        for prefix in json.get('link', []):
            prefix_attributes = self.name_value_pairs_to_dict(prefix.get('attributes', {}))
            if prefix_name == prefix_attributes.get('name'):
                prefix_attributes['href'] = prefix['href']
                return prefix_attributes

        logging.info('Machine prefix {} not found'.format(prefix_name))
        return None

    def update_vro_config(self, vra_host_name, **kwargs):
        vcaccafe = self.get_vra_host_by_name(vra_host_name)
        if not vcaccafe:
            return None
        vcaccafe_sdk_object = {'sdk-object': {'href': vcaccafe['href'], 'id': vcaccafe['id']}}

        input_template = self.create_input_template()
        self.append_parameter(input_template, 'cafeHost', vcaccafe_sdk_object)
        for k, v in kwargs.iteritems():
            if k == 'password':
                self.append_parameter(input_template, k, v, 'SecureString')
            else:
                self.append_parameter(input_template, k, v)

        return self.execute_workflow('Update orchestrator server configuration', input_template)

    def create_credential(self, iaas_host_name, **kwargs):
        vcac = self.get_iaas_host_by_name(iaas_host_name)
        if not vcac:
            return None
        vcac_sdk_object = {'sdk-object': {'href': vcac['href'], 'id': vcac['id']}}

        input_template = self.create_input_template()
        self.append_parameter(input_template, 'vcacHost', vcac_sdk_object)
        for k, v in kwargs.iteritems():
            if k == 'password':
                self.append_parameter(input_template, k, v, 'SecureString')
            else:
                self.append_parameter(input_template, k, v)

        return self.execute_workflow('Create a Connection Credential', input_template)

    def create_endpoint(self, iaas_host_name, platform_name, credential_name, **kwargs):
        vcac = self.get_iaas_host_by_name(iaas_host_name)
        if not vcac:
            return None
        vcac_sdk_object = {'sdk-object': {'href': vcac['href'], 'id': vcac['id']}}

        platform = self.get_platform_type(platform_name)
        if not platform:
            return None
        platform_sdk_object = {'sdk-object': {'href': platform['href'], 'id': platform['id']}}

        credential = self.get_credential(credential_name)
        if not credential:
            return None
        credential_sdk_object = {'sdk-object': {'href': credential['href'], 'id': credential['credentialId']}}

        input_template = self.create_input_template()
        self.append_parameter(input_template, 'vcacHost', vcac_sdk_object)
        self.append_parameter(input_template, 'interfaceType', platform_sdk_object)
        self.append_parameter(input_template, 'credentials', credential_sdk_object)

        for k, v in kwargs.iteritems():
            self.append_parameter(input_template, k, v)

        return self.execute_workflow('Create a Management Endpoint', input_template)

    def get_endpoint(self, endpoint_name):
        json = self.vro_session.call_api_json('GET', '{host}/{api}'.format(host=self.host, api=ENDPOINT_API), 200)
        if not json:
            return None

        for endpoint in json.get('link', []):
            endpoint_attributes = self.name_value_pairs_to_dict(endpoint.get('attributes', {}))
            if endpoint_name == endpoint_attributes.get('displayName'):
                endpoint_attributes['href'] = endpoint['href']
                return endpoint_attributes

        logging.info('Endpoint {0} does not exists'.format(endpoint_name))
        return None

    def create_machine_prefix(self, iaas_host_name, **kwargs):
        vcac = self.get_iaas_host_by_name(iaas_host_name)
        if not vcac:
            return None
        vcac_sdk_object = {'sdk-object': {'href': vcac['href'], 'id': vcac['id']}}

        input_template = self.create_input_template()
        self.append_parameter(input_template, 'vcacHost', vcac_sdk_object)

        for k, v in kwargs.iteritems():
            self.append_parameter(input_template, k, v)

        return self.execute_workflow('Create a Machine Prefix', input_template)

    def create_business_group(self, vra_host_name, prefix_name, **kwargs):
        vcaccafe = self.get_vra_host_by_name(vra_host_name)
        if not vcaccafe:
            return None
        vcaccafe_sdk_object = {'sdk-object': {'href': vcaccafe['href'], 'id': vcaccafe['id']}}

        prefix = self.get_machine_prefix(prefix_name)
        if not prefix:
            return None
        prefix_sdk_object = {'sdk-object': {'href': prefix['href'], 'id': prefix['id']}}

        input_template = self.create_input_template()
        self.append_parameter(input_template, 'host', vcaccafe_sdk_object)
        self.append_parameter(input_template, 'defaultMachinePrefix', prefix_sdk_object)

        for k, v in kwargs.iteritems():
            self.append_parameter(input_template, k, v)

        return self.execute_workflow('Create a business group', input_template)

    def get_business_group(self, bg_name):
        json = self.vro_session.call_api_json('GET', '{host}/{api}'.format(host=self.host, api=BUSINESS_GROUP_API), 200)
        if not json:
            return None

        for bgroup in json.get('link', []):
            bgroup_attributes = self.name_value_pairs_to_dict(bgroup.get('attributes', {}))
            if bg_name.lower() == bgroup_attributes.get('name').lower():
                bgroup_attributes['href'] = bgroup['href']
                return bgroup_attributes

        logging.info('Business Group {0} does not exists'.format(bg_name))
        return None
