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

import string

from ehc_e2e.utils.dir import get_e2e_workflow_conf_path
from ehc_e2e.workflow import SRMDRWorkflow

WF_SETTINGS = 'E2EWF-9-C6-MP3S.config.yaml'


def workflow():
    _global_settings = get_e2e_workflow_conf_path('generic.yaml')
    _wf_settings = get_e2e_workflow_conf_path(WF_SETTINGS)
    wf = SRMDRWorkflow()

    wf.apply_settings_from_files(_global_settings, _wf_settings)
    return wf


def gen_aucs():
    wf = workflow()
    aucs = (
        wf.cloud_administrator_opens_browser,
        wf.cloud_administrator_login,

        wf.cloud_administrator_adds_site,
        wf.cloud_administrator_adds_vcenter,
        wf.cloud_administrator_adds_hwi,
        wf.cloud_administrator_adds_vcenter_relationship,
        wf.cloud_administrator_onboard_cluster,

        wf.cloud_administrator_adds_avamar_grid,
        wf.cloud_administrator_adds_avamar_site_relationship,
        wf.cloud_administrator_gets_ASRs_from_vRO,
        wf.cloud_administrator_associates_cluster_to_asr,
        wf.cloud_administrator_associates_avamar_proxies_with_cluster,
        wf.cloud_administrator_adds_an_avamar_replication_relationship,
        wf.cloud_administrator_gets_ARRs_from_vRO,

        wf.cloud_administrator_provisions_cloud_storage,
        wf.cloud_administrator_creates_reservation_policy,
        wf.cloud_administrator_creates_reservation,
        wf.cloud_administrator_assigns_reservation_policy_to_reservation,
        wf.cloud_administrator_assigns_reservation_policy_to_blueprint,

        wf.cloud_administrator_adds_backup_service_level_for_deploy_vm,
        wf.cloud_administrator_adds_backup_service_level_for_set_vm,
        # AUC#22 Request a VM from specific blueprint with DP build profile
        wf.cloud_administrator_deploys_vm,
        wf.cloud_administrator_operates_vm,
        wf.cloud_administrator_sets_backup_service_level,
        wf.cloud_administrator_sets_no_protection_backup_service_level,
        wf.cloud_administrator_sets_origin_backup_service_level,
        wf.cloud_administrator_on_demand_backup_vm,
        wf.cloud_administrator_on_demand_restore_vm,

        # Fail over
        wf.cloud_administrator_prepares_for_srm_dp_failover,
        wf.cloud_administrator_validates_protection_for_srm_dr_workloads,
        wf.cloud_administrator_performs_srm_dr_recovery,
        wf.cloud_administrator_performs_srm_dr_reprotect,
        wf.cloud_administrator_remediate_manages_srm_dr_protected_workloads,

        # wf.cloud_administrator_deploys_vm,
        wf.cloud_administrator_sets_backup_service_level,
        wf.cloud_administrator_on_demand_backup_vm,
        wf.cloud_administrator_on_demand_restore_vm,

        # Fail back
        wf.cloud_administrator_prepares_for_srm_dp_failover,
        wf.cloud_administrator_validates_protection_for_srm_dr_workloads,
        wf.cloud_administrator_performs_srm_dr_recovery,
        wf.cloud_administrator_performs_srm_dr_reprotect,
        wf.cloud_administrator_remediate_manages_srm_dr_protected_workloads,

        wf.cloud_administrator_adds_backup_service_level_for_set_vm,
        wf.cloud_administrator_deploys_vm,
        wf.cloud_administrator_sets_backup_service_level,
        wf.cloud_administrator_on_demand_backup_vm,
        wf.cloud_administrator_on_demand_restore_vm,
        wf.cloud_administrator_displays_backup_service_level_all,
        wf.cloud_administrator_run_admin_report,

        wf.cloud_administrator_destroy_vms,
        wf.cloud_administrator_deletes_backup_service_level_all,
        wf.cloud_administrator_removes_reservation_policy_from_blueprint,
        wf.cloud_administrator_removes_reservation_policy_from_reservation,
        wf.cloud_administrator_deletes_reservation,
        wf.cloud_administrator_deletes_reservation_policy,

        wf.cloud_administrator_deletes_datastore,
        wf.cloud_administrator_deletes_an_avamar_replication_relationship,
        wf.cloud_administrator_deletes_an_avamar_site_relationship,
        wf.cloud_administrator_deletes_avamar_grid,

        wf.cloud_administrator_deletes_cluster,
        wf.cloud_administrator_deletes_vcenter_relationship,
        wf.cloud_administrator_deletes_hwi,
        wf.cloud_administrator_deletes_vcenter,
        wf.cloud_administrator_deletes_site,

        wf.cloud_administrator_logout,
        wf.cloud_administrator_closes_browser,
        wf.clean_up_environment
    )
    return aucs


def gen_keywords():
    aucs = gen_aucs()
    for i in aucs:
        name = i.__name__
        print ' '.join([string.capitalize(j) for j in name.split('_')])


def main():
    wf = workflow()
    aucs = gen_aucs()
    for i in aucs:
        func = getattr(wf, i.__name__)
        func()


if __name__ == '__main__':
    main()
    # gen_keywords()
