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

from ehc_e2e.workflow import BaseWorkflow
from ehc_e2e.utils.context.model import YAMLData

def __main__():
    import os

    _cd = os.path.dirname(os.path.realpath(__file__))
    _parent_dir = os.path.abspath(os.path.join(_cd, os.pardir))
    _global = os.path.join(_parent_dir, r'../conf/generic.yaml')
    _wf = [
        os.path.join(_parent_dir, r'../conf/E2EWF-1-LC1S.config.yaml'),
    ]
    wf = BaseWorkflow()
    wf.apply_settings_from_files(_global, *_wf)
    wf.user_opens_browser()
    wf.cloud_administrator_login()
    #wf.cloud_administrator_adds_backup_service_level()
    wf.cloud_administrator_adds_backup_service_level_for_deploy_vm()
    wf.cloud_administrator_adds_backup_service_level_for_set_vm()
    wf.user_logout()

main = __main__

if __name__ == '__main__':
    __main__()
