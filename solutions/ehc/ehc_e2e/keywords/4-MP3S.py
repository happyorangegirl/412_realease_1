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
from ehc_e2e.utils.dir import get_e2e_workflow_conf_path

WF_SETTINGS = 'E2EWF-4-MP3S.config.yaml'


def main():
    wf = BaseWorkflow()

    _global_settings = get_e2e_workflow_conf_path('generic.yaml')
    _wf_settings = get_e2e_workflow_conf_path(WF_SETTINGS)
    wf.apply_settings_from_files(_global_settings, _wf_settings)

    wf.cloud_administrator_opens_browser()
    wf.cloud_administrator_login()

    wf.cloud_administrator_opens_browser()
    wf.cloud_administrator_login()
    wf.cloud_administrator_deploys_vm()
    wf.cloud_administrator_operates_vm()
    # wf.cloud_administrator_destroy_vms()
    # wf.cloud_administrator_logout()
    # wf.cloud_administrator_closes_browser()
    # wf.reset_settings()

if __name__ == '__main__':
    main()
