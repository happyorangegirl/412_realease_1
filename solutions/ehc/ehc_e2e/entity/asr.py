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
from xml.dom import minidom


class ASRs(object):
    def __init__(self, xml_str):
        xmldoc = minidom.parseString(xml_str)
        asrs = xmldoc.getElementsByTagName('relations')
        if len(asrs) != 1:
            raise ValueError('Unexpected format in returned payload!')
        asr_list = asrs[0].getElementsByTagName('attributes')
        self.asrs = []
        for asr in asr_list:
            self.asrs.append(ASR(asr))

    def get_asr_list(self):
        return self.asrs


class ASR(object):
    def __init__(self, xmldoc):
        asr_attributes = xmldoc.getElementsByTagName('attribute')
        for attribute in asr_attributes:
            setattr(self, attribute.attributes['name'].value, attribute.attributes['value'].value)
