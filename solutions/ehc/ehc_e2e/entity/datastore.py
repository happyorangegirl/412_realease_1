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


class Datastores(object):
    def __init__(self, xml_str):
        xmldoc = minidom.parseString(xml_str)
        datastores = xmldoc.getElementsByTagName('relations')
        if len(datastores) != 1:
            raise ValueError('Unexpected format in returned payload!')
        datastore_list = datastores[0].getElementsByTagName('attributes')
        self.datastores = []
        for datastore in datastore_list:
            self.datastores.append(Datastore(datastore))

    def get_datastore_list(self):
        return self.datastores


class Datastore(object):
    def __init__(self, xmldoc):
        datastore_attributes = xmldoc.getElementsByTagName('attribute')
        for attribute in datastore_attributes:
            setattr(self, attribute.attributes['name'].value, attribute.attributes['value'].value)
