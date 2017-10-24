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


class CloudStorageObject(object):
    """
        Entity class for holding provisioned cloud storage properties.
    """
    def __init__(self, datastore_name, srp, hwi_name, cluster_name):
        self.name = datastore_name if datastore_name else []
        self.srp = srp if srp else []
        self.hwi_name = hwi_name
        self.cluster_name = cluster_name

    def __str__(self):
        return 'name: {} srp: {}'.format(' '.join(self.name), ' '.join(self.srp))
