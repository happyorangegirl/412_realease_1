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
from ehc_e2e.workflow import SRMDRWorkflow, RP4VMWorkflow
from ehc_e2e.utils.dir import get_e2e_workflow_conf_path

WF_SETTINGS = 'E2EWF-8-C5-MP2S.yaml'


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
        # AUC    # 4 Create SRM DR vCenter relationship - DR/MP related
        # AUC    # 7 Onboard CA1S cluster
        # AUC    # 8 Onboard CA2S cluster
        # AUC    # 9 Onboard MP2S cluster
        # AUC    # 10 Onboard MP3S cluster
        wf.cloud_administrator_adds_avamar_grid,
        wf.cloud_administrator_adds_avamar_site_relationship,
        wf.cloud_administrator_gets_ASRs_from_vRO,
        wf.cloud_administrator_adds_an_avamar_replication_relationship,
        wf.cloud_administrator_gets_ARRs_from_vRO,
        wf.cloud_administrator_associates_cluster_to_asr,
        wf.cloud_administrator_associates_avamar_proxies_with_cluster,
        wf.cloud_administrator_adds_backup_service_level,
        wf.cloud_administrator_provisions_cloud_storage,
        wf.cloud_administrator_creates_reservation_policy,
        wf.cloud_administrator_creates_reservation,
        wf.cloud_administrator_assigns_reservation_policy_to_reservation,
        wf.cloud_administrator_assigns_reservation_policy_to_blueprint,
        # AUC    # 22 Request a VM from specific blueprint with DP build profile
        wf.cloud_administrator_operates_vm,
        wf.cloud_administrator_sets_backup_service_level,
        wf.cloud_administrator_on_demand_backup_vm,
        # AUC    # 27 Day2 Operation - On Demand Restore
        # AUC    # 83 Failover Avamar Grids after Site Failure
        # AUC    # 85 Failover Avamar Policies for offline Avamar Grid
        wf.cloud_administrator_adds_backup_service_level,
        # AUC    # 22 Request a VM from specific blueprint with DP build profile
        wf.cloud_administrator_sets_backup_service_level,
        wf.cloud_administrator_on_demand_backup_vm,
        # AUC    # 27 Day2 Operation - On Demand Restore
        # AUC    # 84 Failback Avamar Policies after Site Restoration
        # AUC    # 86 Failback Avamar Policies after Restoring Avamar Grid
        wf.cloud_administrator_adds_backup_service_level,
        # AUC    # 22 Request a VM from specific blueprint with DP build profile
        wf.cloud_administrator_sets_backup_service_level,
        wf.cloud_administrator_on_demand_backup_vm,
        # AUC    # 27 Day2 Operation - On Demand Restore
        wf.cloud_administrator_displays_backup_service_level,
        wf.cloud_administrator_run_admin_report,
        wf.cloud_administrator_destroy_vms,
        wf.cloud_administrator_deletes_backup_service_level,
        wf.cloud_administrator_gets_datastores_from_vRO,
        wf.cloud_administrator_deletes_datastore,
        wf.cloud_administrator_deletes_an_avamar_replication_relationship,
        wf.cloud_administrator_deletes_an_avamar_site_relationship,
        wf.cloud_administrator_deletes_avamar_grid,
        wf.cloud_administrator_deletes_cluster,
        wf.cloud_administrator_deletes_vcenter_relationship,
        wf.cloud_administrator_deletes_hwi,
        wf.cloud_administrator_deletes_vcenter,
        wf.cloud_administrator_deletes_site,
        wf.cloud_administrator_deletes_reservation,
        wf.cloud_administrator_deletes_reservation_policy,

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
