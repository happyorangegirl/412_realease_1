# -*- coding: utf-8 -*-

# import logging
# import os
# import json
# from json_schema_generator import SchemaGenerator
# import yaml
# import sys
#
#
# _current_dir = os.path.dirname(os.path.realpath(__file__))
# _parent_dir = os.path.abspath(os.path.join(_current_dir, os.pardir))
# _config_path = os.path.join(_current_dir, 'config\E2EWF-1-LC1S.config.yaml')
#
# YAML_KEY_NAME_TO_EXTRACT = ''
#
#
# def deserialize_yaml_config(configfile, key_to_extract):
#     if not configfile and not os.path.isfile(_config_path):
#         return
#
#     try:
#         with open(configfile, 'rb') as yml:
#             raw_yaml = yaml.load(yml)
#             for k, v in raw_yaml.iteritems():
#                 if k.lower() == key_to_extract.lower():
#                     json_obj = json.JSONEncoder().encode(v)
#                     generator = SchemaGenerator.from_json(json_obj)
#                     # generator.to
#     except IOError as ex:
#         logging.error('Open file: {} encounters error: {}'.format(configfile, ex.message))
#     except:
#         raise
#
#
# def serialize_to_file(obj, filepath):
#     if obj:
#         try:
#             with open(filepath, 'wb') as outyaml:
#                 yaml.safe_dump(obj, outyaml)
#         except:
#             logging.error('Serializing obj to file:{} encounters exception:'.format(sys.exc_info()))
#     else:
#         logging.warning('The giving obj to serialize is None.')
#
# def pretty_print_json(jsondata):
#     print json.dumps(jsondata, sort_keys=True, indent=4,
#                      separators=(',', ':'))
#
#
# if __name__ == '__main__':
#     deserialize_yaml_config(_config_path, YAML_KEY_NAME_TO_EXTRACT)