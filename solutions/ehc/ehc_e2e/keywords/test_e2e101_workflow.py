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

from ehc_e2e.workflow import RP4VMWorkflow


if __name__ == '__main__':
    _cd = os.path.dirname(os.path.realpath(__file__))
    _parent_dir = os.path.abspath(os.path.join(_cd, os.pardir))
    _global = os.path.join(_parent_dir, 'conf/generic.yaml')
    _wf = [
        os.path.join(_parent_dir, 'conf/E2EWF-101-RP4VM.config.yaml'),
    ]

    rp4vm = RP4VMWorkflow()
    rp4vm.apply_settings_from_files(_global, *_wf)
    rp4vm.cloud_administrator_opens_browser()
    rp4vm.cloud_administrator_login()

    rp4vm.cloud_administrator_adds_site()
    rp4vm.cloud_administrator_adds_vcenter()
    rp4vm.cloud_administrator_adds_hwi()
    rp4vm.cloud_administrator_adds_rp4vm_vcenter_relationship()
    rp4vm.cloud_administrator_onboards_local_cluster()
    rp4vm.cloud_administrator_provisions_cloud_storage()
    rp4vm.cloud_administrator_adds_vRPA_clusters()
    rp4vm.cloud_administrator_adds_rp4vm_policy()

    rp4vm.cloud_administrator_creates_reservation_policy()
    rp4vm.cloud_administrator_creates_reservation()
    rp4vm.cloud_administrator_assigns_reservation_policy_to_reservation()
    rp4vm.cloud_administrator_assigns_reservation_policy_to_blueprint()

    # RP4VM AUCs
    # rp4vm.cloud_administrator_deploys_vm()
    # rp4vm.cloud_administrator_protects_vm_using_new_cg()
    #
    # rp4vm.cloud_administrator_provisions_rp4vm_using_new_cg()
    #
    # rp4vm.cloud_administrator_provisions_rp4vm_using_existing_cg()
    # rp4vm.cloud_administrator_changes_to_an_existing_cg()
    # rp4vm.cloud_administrator_changes_boot_sequence()
    #
    # rp4vm.cloud_administrator_performs_failover_on_protected_vms()
    # rp4vm.cloud_administrator_adds_post_failover_synchronization()
    # rp4vm.cloud_administrator_deploys_vm()
    #
    # rp4vm.cloud_administrator_performs_failover_on_protected_vms()
    # rp4vm.cloud_administrator_adds_post_failover_synchronization()
    # rp4vm.cloud_administrator_protects_vm_using_existing_cg()
    #
    # rp4vm.cloud_administrator_changes_to_a_new_cg()
    #
    # rp4vm.cloud_administrator_unprotects_all_vms()
    # rp4vm.cloud_administrator_destroy_vms()
    #
    # rp4vm.cloud_administrator_deletes_rp4vm_policy()
    # rp4vm.cloud_administrator_deletes_vRPA_clusters()
    rp4vm.cloud_administrator_deletes_datastore()

    rp4vm.cloud_administrator_deletes_cluster()
    rp4vm.cloud_administrator_deletes_rp4vm_vcenter_relationship()
    rp4vm.cloud_administrator_deletes_hwi()
    rp4vm.cloud_administrator_deletes_vcenter()
    rp4vm.cloud_administrator_deletes_site()

    rp4vm.cloud_administrator_removes_reservation_policy_from_blueprint()
    rp4vm.cloud_administrator_removes_reservation_policy_from_reservation()
    rp4vm.cloud_administrator_deletes_reservation()
    rp4vm.cloud_administrator_deletes_reservation_policy()

    rp4vm.cloud_administrator_closes_browser()
    rp4vm.reset_settings()
