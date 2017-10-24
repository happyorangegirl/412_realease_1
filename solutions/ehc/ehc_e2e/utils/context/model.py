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

from robot.api import logger


class YAMLData(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            if hasattr(value, 'iteritems'):
                self.__dict__.__setitem__(key, YAMLData(**value))
            elif hasattr(value, '__iter__'):
                self.__dict__.__setitem__(key, [])

                for item in value:
                    if hasattr(item, 'iteritems'):
                        self.__dict__.__getitem__(key).append(YAMLData(**item))
                    else:
                        self.__dict__.__getitem__(key).append(item)
            else:
                self.__dict__.__setitem__(key, value)

    def __getitem__(self, item):
        return self.__dict__.__getitem__(item)

    def __setitem__(self, key, value):
        # if hasattr(value, 'iteritems'):
        self.__dict__.__setitem__(key, value)

    def __eq__(self, other):
        if not isinstance(self, other.__class__):
            return False

        for key, item in self.__dict__.iteritems():
            if item != other.__getattribute__(key):
                return False

        return True

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        for k, v in self.__dict__.iteritems():
            if isinstance(v, YAMLData):
                return self.__repr__()
        return str(self.__dict__)


def merge_yaml_data(yaml_data, data_to_merged):
    items = data_to_merged.__dict__.iteritems() if hasattr(data_to_merged, '__dict__') else data_to_merged.iteritems()
    for key, value in items:
        logger.debug('Start to merge key: {}'.format(key))
        # not merge web driver( instance)
        not_merged_list = ['mandatory', 'optional', 'instance']
        if key in not_merged_list:
            continue
        if hasattr(value, 'iteritems') or hasattr(value, '__dict__'):
            _add_key(yaml_data, key, YAMLData(**{}))
            merge_yaml_data(_get_key(yaml_data, key), value)
        elif hasattr(value, '__iter__'):
            _add_key(yaml_data, key, [])
            if not isinstance(_get_key(yaml_data, key), list):
                logger.warn('Type of key: {} in data is : {}, change to list.'.format(
                    key, str(type(_get_key(yaml_data, key)))))
                _set_key(yaml_data, key, [])

            for item in value:
                _get_key(yaml_data, key).append(item)
                _set_key(yaml_data, key, list(set(_get_key(yaml_data, key))))
        else:
            _add_key(yaml_data, key, YAMLData(**{}))
            _set_key(yaml_data, key, value)

    return yaml_data


def _has_key(data, key):
    if hasattr(data, 'iteritems'):
        return data.has_key(key)

    elif hasattr(data, '__dict__'):
        return data.__dict__.has_key(key)
    else:
        return False


def _get_key(data, key):
    if hasattr(data, 'iteritems'):
        return data.__getitem__(key)

    elif hasattr(data, '__dict__'):
        return data.__dict__.__getitem__(key)

    else:
        return {}


def _add_key(data, key, default_value):
    if not _has_key(data, key):
        if hasattr(data, 'iteritems'):
            data.__setitem__(key, default_value)
        elif hasattr(data, '__dict__'):
            data.__dict__.__setitem__(key, default_value)
        else:
            return False

    return True


def _set_key(data, key, value):
    if hasattr(data, 'iteritems'):
        data.__setitem__(key, value)
    elif hasattr(data, '__dict__'):
        data.__dict__.__setitem__(key, value)
    else:
        return False

    return True

