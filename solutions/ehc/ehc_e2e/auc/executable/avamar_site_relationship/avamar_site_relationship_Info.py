"""
 Copyright 2016 EMC GSE SW Automation

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""


class AvamarSiteRelationshipInfo(object):
    """
    Object class used to store information for the newly added ASR.
    """
    def __init__(self, asr_name, backup_env_type, *sites):
        self.asr_name = asr_name
        self.backup_env_type = backup_env_type
        self.sites = []
        for site in sites:
            if site and site != '':
                self.sites.append(site)

    def __str__(self):
        return 'asr_name:{0}, backup_env_type:{1}, sites:{2}'.format(
            self.asr_name, self.backup_env_type, self.sites)
