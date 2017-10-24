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

import os

from ehc_e2e.workflow import SRMDRWorkflow
from ehc_e2e.workflow import RP4VMWorkflow
from ehc_e2e.workflow import AvamarFailActionWorkflow


if __name__ == '__main__':
    _cd = os.path.dirname(os.path.realpath(__file__))
    _parent_dir = os.path.abspath(os.path.join(_cd, os.pardir))
    _global = os.path.join(_parent_dir, 'conf/generic.yaml')

    _wf = [
        os.path.join(_parent_dir, 'conf/E2EWF-8-C2-CA2S.config.yaml'),
    ]
    # _wf = [
    #     os.path.join(_parent_dir, 'conf/E2EWF-101-RP4VM.config.yaml'),
    # ]

    srm = AvamarFailActionWorkflow()
    srm.apply_settings_from_files(_global, *_wf)
    srm.cloud_administrator_opens_browser()
    srm.cloud_administrator_login()
    srm.cloud_administrator_adds_site()
    srm.cloud_administrator_adds_vcenter()
    srm.cloud_administrator_adds_hwi()
    srm.cloud_administrator_onboard_cluster()
    srm.cloud_administrator_adds_avamar_grid()
    srm.cloud_administrator_adds_avamar_site_relationship()
    srm.cloud_administrator_associates_cluster_to_asr()
    srm.cloud_administrator_associates_avamar_proxies_with_cluster()
    srm.cloud_administrator_adds_an_avamar_replication_relationship()
    srm.cloud_administrator_adds_backup_service_level_for_deploy_vm()
    srm.cloud_administrator_adds_backup_service_level_for_set_vm()
    srm.cloud_administrator_provisions_cloud_storage()
    srm.cloud_administrator_creates_reservation_policy()
    srm.cloud_administrator_creates_reservation()
    srm.cloud_administrator_assigns_reservation_policy_to_reservation()
    srm.cloud_administrator_assigns_reservation_policy_to_blueprint()
    srm.cloud_administrator_deploys_vm()
    srm.cloud_administrator_operates_vm()
    srm.cloud_administrator_sets_backup_service_level()
    srm.cloud_administrator_on_demand_backup_vm()
    # srm.cloud_administrator_on_demand_restore_vm()
    srm.cloud_administrator_failovers_avamar_grids_after_site_failure()

    srm.cloud_administrator_adds_backup_service_level_for_set_vm()
    srm.cloud_administrator_deploys_vm()
    srm.cloud_administrator_sets_backup_service_level()
    srm.cloud_administrator_on_demand_backup_vm()
    # srm.cloud_administrator_on_demand_restore_vm()
    srm.cloud_administrator_failbacks_avamar_policies_after_site_restoration()

    srm.cloud_administrator_adds_backup_service_level_for_set_vm()
    srm.cloud_administrator_deploys_vm()
    srm.cloud_administrator_sets_backup_service_level()
    srm.cloud_administrator_on_demand_backup_vm()
    # srm.cloud_administrator_on_demand_restore_vm()
    srm.cloud_administrator_displays_backup_service_level()
    srm.cloud_administrator_run_admin_report()

    srm.cloud_administrator_destroy_vms()
    srm.cloud_administrator_deletes_backup_service_level_all()
    srm.cloud_administrator_removes_reservation_policy_from_blueprint()
    srm.cloud_administrator_removes_reservation_policy_from_reservation()
    srm.cloud_administrator_deletes_reservation()
    srm.cloud_administrator_deletes_reservation_policy()
    srm.cloud_administrator_deletes_datastore()
    srm.cloud_administrator_deletes_an_avamar_replication_relationship()
    srm.cloud_administrator_deletes_an_avamar_site_relationship()
    srm.cloud_administrator_deletes_avamar_grid()
    srm.cloud_administrator_deletes_cluster()
    srm.cloud_administrator_deletes_hwi()
    srm.cloud_administrator_deletes_vcenter()
    srm.cloud_administrator_deletes_site()
    srm.cloud_administrator_logout()
    srm.cloud_administrator_closes_browser()
    srm.reset_settings()

