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

from ehc_e2e.workflow import RP4VMWorkflow


def __main__():
    import os
    _cd = os.path.dirname(os.path.realpath(__file__))
    _parent_dir = os.path.abspath(os.path.join(_cd, os.pardir))
    _global = os.path.join(_parent_dir, 'conf/generic.yaml')
    _wf = [
        os.path.join(_parent_dir,
                     'conf/Basic-LC1S-Deployment-with-DP-and-Existing-VC-Relationship.yaml'),
    ]

    wf = RP4VMWorkflow()
    wf.apply_settings_from_files(_global, *_wf)
    wf.cloud_administrator_opens_browser()
    # wf.login_to_vra_as_config_admin()
    # wf.cloud_administrator_adds_site()
    # wf.cloud_administrator_adds_vcenter()
    # wf.cloud_administrator_adds_hwi()
    wf.site_with_same_name_exists()
    wf.vcenter_with_same_name_exists()
    wf.hwi_with_same_name_exists()
    wf.vcenter_relationship_with_same_name_exists()
    wf.login_to_vra_as_config_admin()
    # wf.cloud_administrator_onboards_local_cluster()
    # wf.cloud_administrator_logout()
    # wf.login_to_vra_as_backup_admin()
    # wf.cloud_administrator_adds_avamar_grid_unselect_proxy()
    # wf.cloud_administrator_adds_avamar_site_relationship()
    # wf.cloud_administrator_adds_an_avamar_replication_relationship()
    wf.cloud_administrator_associates_cluster_to_asr()
    wf.cloud_administrator_adds_backup_service_level()
    wf.cloud_administrator_logout()
    wf.login_to_vra_as_storage_admin()
    wf.cloud_administrator_provision_multiple_cloud_storage()
    wf.cloud_administrator_logout()
    wf.login_to_vra_as_config_admin()
    # wf.cloud_administrator_creates_reservation()
    wf.cloud_administrator_creates_reservation_policy()
    wf.cloud_administrator_assigns_datastores_and_reservation_policy_to_reservation()
    wf.cloud_administrator_assigns_reservation_policy_to_reservation()
    wf.cloud_administrator_assigns_reservation_policy_to_blueprint()
    wf.cloud_administrator_logout()
    wf.login_to_vra_as_backup_admin()
    #wf.login_to_vra_as_tenant_bg_user()
        # #Keyword should be login_to_vra_as_tenant_bg_user, no bg user usable, replaced with backup admin
    wf.cloud_administrator_deploys_vm_parallel()
    # wf.cloud_administrator_adds_avamar_proxy()
    wf.reset_settings()

main = __main__

if __name__ == '__main__':
    __main__()