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
from ehc_e2e.scenario import BaseScenario

if __name__ == '__main__':
    _cd = os.path.dirname(os.path.realpath(__file__))
    _parent_dir = os.path.abspath(os.path.join(_cd, os.pardir))
    _global = os.path.join(_parent_dir, 'conf/generic.yaml')

    _wf = [
        os.path.join(_parent_dir, 'test/test_data/test_scenario_conf/E2ESN-3-RP4VM.config.yaml')
    ]

    bs = BaseScenario()
    bs.apply_settings_from_files(_global, *_wf)
    bs.initialize_workflow_relation_mapping()
    bs.cloud_administrator_opens_browser()
    bs.cloud_administrator_login()
    # bs.cloud_administrator_adds_site()
    # bs.cloud_administrator_adds_vcenter()
    # bs.cloud_administrator_adds_hwi()
    # bs.cloud_administrator_adds_rp4vm_vcenter_relationship()
    # bs.cloud_administrator_onboards_local_cluster()
    # bs.cloud_administrator_adds_vRPA_clusters()
    # bs.cloud_administrator_adds_rp4vm_policy()
    # bs.cloud_administrator_adds_avamar_grid_unselect_proxy()
    # bs.cloud_administrator_adds_avamar_site_relationship()
    # bs.cloud_administrator_adds_an_avamar_replication_relationship()
    # bs.cloud_administrator_associates_cluster_to_asr()
    # bs.cloud_administrator_adds_avamar_proxy()
    # bs.cloud_administrator_adds_backup_service_level()
    # bs.cloud_administrator_provision_multiple_cloud_storage()
    # bs.cloud_administrator_creates_reservation_policy_with_mapping()
    # bs.cloud_administrator_assigns_datastores_and_reservation_policy_to_reservation_with_mapping()
    # bs.split_rp4vm_mapping_relation_for_workflow()
    # bs.cloud_administrator_assigns_reservation_policy_to_blueprint_with_mapping()

    # rp4vm AUCs
    bs.cloud_administrator_deploys_vm_parallel()

    bs.write_workflow_relation_mappings_from_current_workflow_to_scenario()
    print 'End'
