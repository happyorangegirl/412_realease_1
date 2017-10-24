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


def __main__():
    import os

    _cd = os.path.dirname(os.path.realpath(__file__))
    _parent_dir = os.path.abspath(os.path.join(_cd, os.pardir))
    _global = os.path.join(_parent_dir, 'conf/generic.yaml')
    _wf = [
        os.path.join(_parent_dir, 'conf/E2EWF-102-RP4VM-VSAN-DP.config.yaml'),
    ]
    wf = BaseWorkflow()
    wf.apply_settings_from_files(_global, *_wf)
    wf.user_opens_browser()
    wf.login_to_vra_as_backup_admin()
    wf.user_logout()
    wf.login_to_vra_as_config_admin()
    # wf.cloud_administrator_adds_site()
    wf.user_logout()
    wf.login_to_vra_as_storage_admin()
    wf.user_logout()
    wf.login_to_vra_as_tenant_bg_user()
    wf.user_logout()
    wf.cloud_administrator_closes_browser()

main = __main__

if __name__ == '__main__':
    __main__()
