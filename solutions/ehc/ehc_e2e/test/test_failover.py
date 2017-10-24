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
from ehc_e2e.workflow import AvamarFailActionWorkflow


def main():
    _cd = os.path.dirname(os.path.realpath(__file__))
    _parent_dir = os.path.abspath(os.path.join(_cd, os.pardir))
    _global = os.path.join(_parent_dir, 'conf/generic.yaml')
    _wf = [
        os.path.join(_parent_dir, 'conf/E2EWF-102-RP4VM-DP.config.yaml'),
    ]
    # E2EWF-2 MP3S
    wf = AvamarFailActionWorkflow()
    wf.apply_settings_from_files(_global, *_wf)
    wf.cloud_administrator_opens_browser()

    wf.cloud_administrator_login()
    # wf.cloud_administrator_gets_ASRs_from_vRO()
    # wf.cloud_administrator_gets_ARRs_from_vRO()
    # wf.cloud_administrator_gets_datastores_from_vRO()
    wf.cloud_administrator_creates_reservation_policy()
    wf.cloud_administrator_logout()
    wf.cloud_administrator_login()
    wf.cloud_administrator_deletes_reservation_policy()
    #wf.cloud_administrator_logout()


    # wf.cloud_administrator_adds_rp4vm_policy()
    # wf.cloud_administrator_deletes_rp4vm_policy()


#     #CG1
#     wf.cloud_administrator_provisions_rp4vm_using_new_cg()
#     wf.cloud_administrator_provisions_rp4vm_using_existing_cg()
#
#     # CG2
#     wf.cloud_administrator_provisions_vm_without_rp4vm()
#     wf.cloud_administrator_protects_vm_using_new_cg()
#
#     # CG2
#     wf.cloud_administrator_provisions_vm_without_rp4vm()
#     wf.cloud_administrator_protects_vm_using_existing_cg()
#
#     # CG2-->CG1,failover
#     wf.cloud_administrator_changes_to_an_existing_cg()
#     wf.cloud_administrator_changes_boot_sequence()
#
#     # CG1
#     wf.cloud_administrator_provisions_rp4vm_using_existing_cg()
#
#     # CG1
#     wf.cloud_administrator_provisions_vm_without_rp4vm()
#     wf.cloud_administrator_protects_vm_using_existing_cg()
#
#     # CG1-->CG2
#     wf.cloud_administrator_changes_to_an_existing_cg()
#     wf.cloud_administrator_changes_boot_sequence()
#
#     wf.cloud_administrator_unprotects_vm()
#     wf.cloud_administrator_unprotects_vm()
#     wf.cloud_administrator_unprotects_vm()
#     wf.cloud_administrator_unprotects_vm()
#
#     wf.cloud_administrator_unprotects_all_vms()
#
# =======
    # wf.cloud_administrator_adds_site()
    # wf.cloud_administrator_adds_vcenter()
    # wf.cloud_administrator_adds_hwi()
    # wf.cloud_administrator_adds_vcenter_relationship()
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
    # wf.cloud_administrator_deletes_cluster()
    # wf.cloud_administrator_deletes_vcenter_relationship()
    # wf.cloud_administrator_deletes_hwi()
    # wf.cloud_administrator_deletes_vcenter()
    # wf.cloud_administrator_deletes_site()
    # wf.cloud_administrator_deletes_reservation()
    # wf.cloud_administrator_deletes_reservation_policy()

    # # E2EWF-1 MP3S
    # wf = BaseWorkflow()
    # wf.cloud_administrator_opens_browser()
    # wf.cloud_administrator_login()
    # wf.cloud_administrator_adds_site()
    # wf.cloud_administrator_adds_vcenter()
    # wf.cloud_administrator_adds_hwi()
    # wf.cloud_administrator_adds_vcenter_relationship()
    # wf.cloud_administrator_onboard_cluster()
    # wf.cloud_administrator_adds_avamar_grid()
    # wf.cloud_administrator_adds_avamar_site_relationship()
    # wf.cloud_administrator_adds_an_avamar_replication_relationship()
    # wf.cloud_administrator_associates_cluster_to_asr()
    # wf.cloud_administrator_associates_avamar_proxies_with_cluster()
    # wf.cloud_administrator_adds_backup_service_level()
    # wf.cloud_administrator_provisions_cloud_storage()
    # wf.cloud_administrator_creates_reservation_policy()
    # wf.cloud_administrator_creates_reservation()
    # wf.cloud_administrator_assigns_reservation_policy_to_reservation()
    # wf.cloud_administrator_assigns_reservation_policy_to_blueprint()
    # wf.cloud_administrator_deploys_vm()
    # wf.cloud_administrator_operates_vm()
    # wf.cloud_administrator_sets_backup_service_level()
    # wf.cloud_administrator_on_demand_backup_vm()
    # # on demand restore here
    # wf.cloud_administrator_destroy_vms()
    # wf.cloud_administrator_deletes_backup_service_level()
    # wf.cloud_administrator_deletes_datastore()
    # wf.cloud_administrator_deletes_an_avamar_replication_relationship()
    # wf.cloud_administrator_deletes_an_avamar_site_relationship()
    # wf.cloud_administrator_deletes_avamar_grid()
    # wf.cloud_administrator_deletes_cluster()
    # wf.cloud_administrator_deletes_vcenter_relationship()
    # wf.cloud_administrator_deletes_hwi()
    # wf.cloud_administrator_deletes_vcenter()
    # wf.cloud_administrator_deletes_site()
    # wf.cloud_administrator_deletes_reservation()
    # wf.cloud_administrator_deletes_reservation_policy()

    wf.cloud_administrator_closes_browser()
    wf.reset_settings()


if __name__ == '__main__':
    main()