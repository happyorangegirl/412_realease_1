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
        os.path.join(_parent_dir, 'conf/E2EWF-2-CA2S.config.yaml'),
    ]

    wf = BaseWorkflow()
    wf.apply_settings_from_files(_global, *_wf)
    wf.cloud_administrator_opens_browser()
    wf.cloud_administrator_login()
    wf.cloud_administrator_adds_site()
    # wf.cloud_administrator_adds_vcenter()
    wf.cloud_administrator_adds_hwi()
    # wf.cloud_administrator_onboard_cluster()
    # wf.cloud_administrator_provisions_cloud_storage()
    # wf.cloud_administrator_creates_reservation_policy()
    # wf.cloud_administrator_creates_reservation()
    # wf.cloud_administrator_assigns_reservation_policy_to_reservation()
    # wf.cloud_administrator_assigns_reservation_policy_to_blueprint()
    # wf.cloud_administrator_deploys_vm()
    # wf.cloud_administrator_operates_vm()
    # wf.cloud_administrator_destroy_vms()
    # wf.cloud_administrator_deletes_datastore()
    # wf.cloud_administrator_edits_cluster_hwi()
    # wf.cloud_administrator_deletes_cluster()
    # wf.cloud_administrator_edits_hwi()
    # wf.cloud_administrator_deletes_hwi()
    wf.cloud_administrator_edits_vcenter()
    wf.cloud_administrator_deletes_vcenter()
    wf.cloud_administrator_edits_site()
    wf.cloud_administrator_deletes_site()
    wf.cloud_administrator_removes_reservation_policy_from_reservation()
    wf.cloud_administrator_deletes_reservation()
    wf.cloud_administrator_removes_reservation_policy_from_blueprint()
    wf.cloud_administrator_deletes_reservation_policy()
    wf.cloud_administrator_logout()
    wf.cloud_administrator_closes_browser()
    wf.reset_settings()

main = __main__

if __name__ == '__main__':
    __main__()
