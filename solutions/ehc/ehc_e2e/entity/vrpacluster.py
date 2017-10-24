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


class vRPAClusters(object):
    def __init__(self, xml_str):
        xmldoc = minidom.parseString(xml_str)
        vrpa_clusters = xmldoc.getElementsByTagName('relations')
        if len(vrpa_clusters) != 1:
            raise ValueError('Unexpected format in returned payload!')
        vrpa_cluster_list = vrpa_clusters[0].getElementsByTagName('attributes')
        self.vrpa_clusters = []
        self.rp4vm_vrpa_clusters = []
        for vrpa_cluster in vrpa_cluster_list:
            vrpa = vRPACluster(vrpa_cluster)
            self.vrpa_clusters.append(vrpa)

    def get_matched_rp4vm_vrpa_cluster_list(self, ip_list):
        for each_cluster in self.vrpa_clusters:
            if each_cluster.cluster_mgmt_ip in ip_list:
                self.rp4vm_vrpa_clusters.append(each_cluster)
        return self.rp4vm_vrpa_clusters


class vRPACluster(object):
    def __init__(self, xmldoc):
        datastore_attributes = xmldoc.getElementsByTagName('attribute')
        for attribute in datastore_attributes:
            setattr(self, attribute.attributes['name'].value, attribute.attributes['value'].value)
