# -*- coding: utf-8 -*-

import logging
import os
import json
import re
import yaml
import sys
import urlparse
from django.conf import settings
from ehc_config_adapter.json_schema_generator import SchemaGenerator
from ehc_rest_utilities.session_manager.session_manager import VRASession
from ehc_rest_utilities.session_manager.session_manager import VROSession
from ehc_rest_utilities.vro_rest_utilities.vro_rest_base import VRORestBase
from ehc_rest_utilities.vra_rest_utilities.vra_rest_ex import VRARestEx
from ehc_e2e_common.generic_yaml_file_parser import GenericYamlFileParser

class UISchemaGen(object):
    _current_dir = os.path.dirname(os.path.realpath(__file__))
    _parent_dir = os.path.abspath(os.path.join(_current_dir, os.pardir))
    _config_path = os.path.join(_parent_dir, 'config\E2EWF-1-LC1S.config.yaml')

    YAML_KEY_NAME_TO_EXTRACT = 'mandatory'

    def __init__(self):
        self.__vra = None
        self.__vro = None

        global_context = GenericYamlFileParser.parse_context()

        vra_address_raw = global_context.vra_host
        vra_tenant = global_context.vra_tenant
        vra_username = global_context.config_admin_username
        vra_password = global_context.config_admin_password

        vro_address = global_context.vro_host
        vro_username = global_context.vro_username
        vro_password = global_context.vro_password

        vra_address = urlparse.urlparse(vra_address_raw).netloc
        try:
            vra_session = VRASession(vra_address,
                                     vra_tenant,
                                     vra_username,
                                     vra_password)
            self.__vra = VRARestEx(vra_session)

            vro_session = VROSession(vro_address,
                                     vro_username,
                                     vro_password)
            self.__vro = VRORestBase(vro_session)
        except:
            logging.error("Fail to establish vra/vro connection")


    def yaml_config_to_schema(self,configfile, key_to_extract, to_json=True, sync=False):
        mandatory_value = {}
        optional_value = {}
        '''
        Return the schema for values under 'key_to_extract' key in the given yaml file.
        :param configfile: the yaml file to extract data from.
        :param key_to_extract: the key within that yaml file to inspect values from
        :param to_json: specify if the output schema is in json format
        :return:
        '''

        if not configfile and not os.path.isfile(UISchemaGen._config_path):
            return

        try:
            with open(configfile, 'rb') as yml:
                raw_yaml = yaml.load(yml)
                for level_one_key, level_one_value in raw_yaml.iteritems():
                    if level_one_key.lower() == key_to_extract.lower():
                        if sync:
                            for level_two_key, level_two_value in level_one_value.iteritems():
                                for level_three_key, level_three_value in level_two_value.iteritems():
                                    if self.is_listable(level_three_key):
                                        level_three_value = self.get_workflow_key_enums(level_three_key)
                                        if level_three_value:
                                            level_two_value[level_three_key] = level_three_value
                        mandatory_value = {'mandatory':level_one_value}
                    if level_one_key.lower() == 'optional':
                        optional_value = {'optional':level_one_value}
                if mandatory_value and optional_value:
                    combined_value  = dict(mandatory_value, **optional_value)
                    json_obj = json.dumps(combined_value)
                    generator = SchemaGenerator.from_json(json_obj)
                    if to_json:
                        return generator.to_json()
                    else:
                        return generator.to_dict()
                elif mandatory_value:
                    json_obj = json.dumps(mandatory_value)
                    generator = SchemaGenerator.from_json(json_obj)
                    if to_json:
                        return generator.to_json()
                    else:
                        return generator.to_dict()
                else:
                    logging.error('mandatory should not be empty.')

        except IOError as ex:
            logging.error('Open file: {} encounters error: {}'.format(configfile, ex.message))
        except:
            raise

        return None

    def is_listable(self, key):
        list_pattern = re.compile(
            '(protected_|recovery_)?(vcenter_fqdn|cluster_name|vcenter_datacenter|vipr_varray|blueprint_name)_?([A-Z])?',
            re.I)
        return list_pattern.match(key)

    def get_workflow_key_enums(self, key):
        value_list = []
        if 'vcenter_fqdn' in key.lower():
            value_list = self.get_vcenter_values()
        elif 'vipr_varray' in key.lower():
            value_list = self.get_viprarray_values()
        elif 'cluster_name' in key.lower():
            value_list = self.get_cluster_values()
        elif 'vcenter_datacenter' in key.lower():
            value_list = self.get_datacenter_values()
        elif 'blueprint_name' in key.lower():
            value_list = self.get_blueprint_values()
        return value_list

    def get_vcenter_values(self):

        vcenter_dict_list = self.__vro.execute_action('getAllVCenters')
        vcenter_list = []
        for vcenter_values in vcenter_dict_list['value']['array']['elements']:
            vcenter_list.append(vcenter_values['string']['value'])
        return vcenter_list

    def get_viprarray_values(self):
        vipr_dict_list = self.__vro.execute_action('getAllViPRVirtualArrays')
        vipr_list = []
        for vipr_values in vipr_dict_list['value']['array']['elements']:
            vipr_list.append(vipr_values['string']['value'])
        return vipr_list

    def get_cluster_values(self):
        cluster_list = []
        res = self.__vro.execute_action('getAllClusters')
        cluster_list = self.__vro.extract_sdk_objects(res)
        return cluster_list

    def get_datacenter_values(self):
        datacenter_list = []
        res = self.__vro.execute_action('getAllDatacentersForAllvCenters')
        datacenter_list = self.__vro.extract_sdk_objects(res)
        return datacenter_list

    def get_blueprint_values(self):
        blueprint_list = []
        blueprint_list = self.__vra.get_blueprint_names()
        return blueprint_list

    def serialize_to_file(obj, file_path):
        if obj:
            try:
                with open(file_path, 'wb') as outyaml:
                    yaml.safe_dump(obj, outyaml)
                    logging.info('Serialized object to yaml file: {}'.format(file_path))
            except:
                logging.error('Serializing obj to file:{} encounters exception: {}'.format(file_path, sys.exc_info()))
        else:
            logging.warning('The giving obj to serialize is None.')

    def pretty_print_dict(self,jsondata):
        return json.dumps(jsondata, sort_keys=True, indent=4,
                          separators=(',', ':'))

    def generate(self, config_path,sync):
        import os
        filename = os.path.basename(config_path)
        schema_file = '{}{}.{}'.format('/root/automation/ehc/schema/web/', filename, 'json')
        result = self.yaml_config_to_schema(config_path, self.YAML_KEY_NAME_TO_EXTRACT, False, sync)
        result = self.pretty_print_dict(result)
        with open(schema_file, 'w+') as yml:
            yml.write(str(result))
        return schema_file

