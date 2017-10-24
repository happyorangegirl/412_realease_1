#  Copyright 2016 EMC HCE SW Automation
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


import os
import re
import sys

from compat import text_type, binary_type
from util import r_replace

# ---For testing purpose---.
PACKAGE_ROOT_PATH, FILE_NAME = os.path.split(os.path.abspath(__file__))
TESTDATA_FOLDER = 'testdata'
ORIGINAL_YAML = os.path.join(PACKAGE_ROOT_PATH, TESTDATA_FOLDER,
                             'E2EWF-2-CA1S.config.yaml')
SIT_YAML = os.path.join(PACKAGE_ROOT_PATH, TESTDATA_FOLDER,
                        'sit-E2EWF-2-CA1S.config.yaml')
OUT_YAML = os.path.join(PACKAGE_ROOT_PATH, TESTDATA_FOLDER, 'out_4.yaml')
# ---For testing purpose---.


class YamlLineContent(object):
    def __init__(self, is_key, variable_name, anchor_name, key_value,
                 plain_text, need_update=False):
        self._is_key = is_key
        self._key_name = variable_name
        self._anchor_name = anchor_name
        self._key_value = key_value
        self._plain_text = plain_text
        self._need_update = need_update

    @property
    def plain_text(self):
        return self._plain_text

    @plain_text.setter
    def plain_text(self, value):
        self._plain_text = value

    @property
    def is_key(self):
        return self._is_key

    @is_key.setter
    def is_key(self, value):
        self._is_key = value

    @property
    def anchor_name(self):
        return self._anchor_name

    @anchor_name.setter
    def anchor_name(self, value):
        self._anchor_name = value

    @property
    def key_value(self):
        return self._key_value

    @key_value.setter
    def key_value(self, value):
        self._key_value = value

    @property
    def need_update(self):
        return self._need_update

    @need_update.setter
    def need_update(self, value):
        self._need_update = value


class YamlReader(object):
    ANCHOR_EXISTENCE_REG_PATTERN = r'\s+&\w+[-|\w]*'
    ANCHOR_NAME_REG_PATTERN = r'&\w+[-|\w]*'
    KEY_NAME_REG_PATTERN = r'\w+[-|\w]*:'
    MANDATORY_KEY_NAME = 'mandatory:'
    OPTIONAL_KEY_NAME = 'optional:'

    def walk_yaml(self, stream):
        """
        walk through the given yaml stream to produce a list of content lines.
        :param stream:
        :return:
        """
        yaml_content_lines = []
        try:
            if isinstance(stream, text_type):
                yaml_str = stream
            elif isinstance(stream, binary_type):
                yaml_str = stream.decode(
                    'utf-8')  # most likely, but the Reader checks BOM for this
            else:
                yaml_str = stream.read()
        except:
            print '[ERROR]Reading Yaml file encounters error, error details:' \
                  ' {}'.format(sys.exc_info()[:])
            raise

        # Currently, we only update mandatory section.
        is_line_need_update = False
        for yaml_line in yaml_str.splitlines():
            rline = yaml_line.rstrip()
            lline = rline.lstrip()
            if not yaml_line.startswith('#') \
                    and self.MANDATORY_KEY_NAME in yaml_line.lower():
                is_line_need_update = True

            if not yaml_line.startswith('#') \
                    and self.OPTIONAL_KEY_NAME in yaml_line.lower():
                is_line_need_update = False
            if lline.startswith('#'):
                # this is a comment, just set its plain text.
                # yaml_line.is_variable = False
                yaml_content_lines.append(
                    YamlLineContent(False, None, None, None, yaml_line))
            elif lline.endswith(':'):
                yaml_content_lines.append(
                    YamlLineContent(True, lline[:-1], None, None, yaml_line))
            elif re.findall(self.ANCHOR_EXISTENCE_REG_PATTERN, lline,
                            flags=re.IGNORECASE):
                anchor_result = re.findall(self.ANCHOR_NAME_REG_PATTERN, lline,
                                           flags=re.IGNORECASE)
                # there can be &xxx within the actual key value, but the first
                # occurrence of regular expression result should be the anchor.
                anchor_name = anchor_result[0]
                anchor_value = lline[lline.find(anchor_name) + len(
                    anchor_name):].lstrip()

                # the key name should precede anchor name.
                key_name = lline[:lline.find(anchor_name)].rstrip()
                yaml_content_lines.append(
                    YamlLineContent(True, key_name, anchor_name, anchor_value,
                                    yaml_line, is_line_need_update))
            elif re.findall(self.KEY_NAME_REG_PATTERN, lline,
                            flags=re.IGNORECASE):
                # if we use this pattern to find the key value, then the first
                # occurrence of reg expression result should be the key, don't
                # forget to remove the last character ':' when constructing
                # YamlLineContent object at last.
                key_name = re.findall(self.KEY_NAME_REG_PATTERN, lline,
                                      flags=re.IGNORECASE)[0]
                key_value = lline[len(key_name):].lstrip()
                yaml_content_lines.append(
                    YamlLineContent(True, key_name[:-1], None, key_value,
                                    yaml_line))
            else:
                # This is most likely for blank lines
                yaml_content_lines.append(
                    YamlLineContent(False, None, None, None, yaml_line))

        return yaml_content_lines


def build_anchors_dict(content_lines):
    """
    building a dict of anchor_name:anchor_value,
     list.
    :param content_lines:
    :return:
    """
    anchors_dict = {}
    for anchor_line in [x for x in content_lines if x.is_key and x.anchor_name]:
        if anchors_dict.get(anchor_line.anchor_name):
            print '[ERROR]Anchor: {} already found and added, it should not ' \
                  'appear again!'.format(anchor_line.anchor_name)
        else:
            print '[INFO]Anchor: {} found, its value is: {}'.format(
                anchor_line.anchor_name, anchor_line.key_value)
            anchors_dict.update(
                {anchor_line.anchor_name: anchor_line.key_value})

    return anchors_dict


def update_anchor_values(referred_anchors_dict, target_yaml_content_lines):
    target_yaml_anchor_lookup_table = {}
    # build lookup table with item anchor:index, index is based on the
    # content_lines list.
    for i, item in enumerate(target_yaml_content_lines):
        # We only cares about anchors and currenly
        # only those anchors under mandatory key.
        if item.anchor_name and item.need_update:
            if target_yaml_anchor_lookup_table.get(item.anchor_name):
                print '[WARN]Duplicate anchor found, there is already an ' \
                      'anchor:{} found and stored!!'.format(item.anchor_name)
            else:
                print '[DEBUG]Building anchor lookup table by adding ' \
                      'anchor:{}'.format(item.anchor_name)
                target_yaml_anchor_lookup_table.update({item.anchor_name: i})

    for anchor_name, index in target_yaml_anchor_lookup_table.iteritems():
        anchor_value = referred_anchors_dict.get(anchor_name)
        if anchor_value:
            # if the value of anchor is same as referenced, no need to update.
            if anchor_value != target_yaml_content_lines[index].key_value:
                print '[INFO]Will update value for anchor: {}'.format(anchor_name)
                print '[INFO]Will update value for anchor: {}'.format(anchor_name)
                original_text = target_yaml_content_lines[index].plain_text
                search_text = target_yaml_content_lines[index].key_value
                target_yaml_content_lines[index].plain_text = r_replace(
                    original_text, search_text, anchor_value)
                target_yaml_content_lines[index].key_value = anchor_value

    return target_yaml_content_lines


def update_single_yaml(original_yaml, reference_yaml, output_yaml):
    if not os.path.isfile(original_yaml):
        print '[WARN]{} is not a valid file, stop further operation!'.format(
            original_yaml)
    if not os.path.isfile(reference_yaml):
        print '[WARN]{} is not a valid file, stop further operation!'.format(
            original_yaml)

    try:
        with open(original_yaml) as f_original_yaml:
            target_result_collection = YamlReader().walk_yaml(f_original_yaml)
        with open(reference_yaml) as f_site_yaml:
            sit_result_collection = YamlReader().walk_yaml(f_site_yaml)
    except:
        print '[ERROR]Opening file: {} and {} encounters error:{}.'.format(
            original_yaml, reference_yaml, sys.exc_info()[:])
        raise

    sit_anchors_dict = build_anchors_dict(sit_result_collection)
    result = update_anchor_values(sit_anchors_dict, target_result_collection)

    with open(output_yaml, 'w') as out_f:
        for line in result:
            out_f.write('{}\n'.format(line.plain_text))


if __name__ == '__main__':
    # TEST
    update_single_yaml(ORIGINAL_YAML, SIT_YAML, OUT_YAML)
