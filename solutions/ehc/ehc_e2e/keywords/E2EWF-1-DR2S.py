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
        os.path.join(_parent_dir, 'conf/E2EWF-1-DR2S.config.yaml'),
    ]

    wf = BaseWorkflow()
    wf.apply_settings_from_files(_global, *_wf)
    wf.cloud_administrator_opens_browser()
    wf.cloud_administrator_login()
    # wf.cloud_administrator_adds_site()
    wf.cloud_administrator_adds_vcenter()
    wf.cloud_administrator_adds_vcenter_relationship()
    # wf.cloud_administrator_adds_hwi()
    wf.cloud_administrator_onboard_cluster()
    # wf.cloud_administrator_adds_avamar_grid()
    # wf.cloud_administrator_adds_avamar_site_relationship()
    wf.cloud_administrator_adds_an_avamar_replication_relationship()
    # wf.cloud_administrator_associates_cluster_to_asr()
    # wf.cloud_administrator_associates_avamar_proxies_with_cluster()
    # wf.cloud_administrator_adds_backup_service_level()
    # wf.cloud_administrator_provisions_cloud_storage()
    # wf.cloud_administrator_creates_reservation_policy()
    wf.cloud_administrator_creates_reservation()
    wf.cloud_administrator_assigns_reservation_policy_to_reservation()
    # wf.cloud_administrator_assigns_reservation_policy_to_blueprint()
    # wf.cloud_administrator_deploys_vm()
    # wf.cloud_administrator_operates_vm()
    # wf.cloud_administrator_sets_backup_service_level()
    # wf.cloud_administrator_on_demand_backup_vm()
    # wf.cloud_administrator_on_demand_restore()
    # wf.cloud_administrator_displays_backup_service_level()
    # wf.cloud_administrator_run_admin_report()
    # wf.cloud_administrator_destroy_vms()
    # wf.cloud_administrator_deletes_backup_service_level()
    # # wf.cloud_administrator_deletes_datastore()
    # wf.cloud_administrator_deletes_an_avamar_replication_relationship()
    # wf.cloud_administrator_deletes_an_avamar_site_relationship()
    # wf.cloud_administrator_deletes_avamar_grid()
    # wf.cloud_administrator_deletes_cluster()
    # wf.cloud_administrator_deletes_hwi()
    # wf.cloud_administrator_deletes_vcenter()
    # wf.cloud_administrator_deletes_site()
    # wf.cloud_administrator_removes_reservation_policy_from_reservation()
    # wf.cloud_administrator_deletes_reservation()
    # wf.cloud_administrator_removes_reservation_policy_from_blueprint()
    # wf.cloud_administrator_deletes_reservation_policy()
    # wf.cloud_administrator_logout()
    # wf.cloud_administrator_closes_browser()
    wf.reset_settings()

main = __main__

if __name__ == '__main__':
    __main__()