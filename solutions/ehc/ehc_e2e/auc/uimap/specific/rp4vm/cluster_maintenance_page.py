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

from uiacore.modeling.webui.controls import WebTextBox

from ehc_e2e.auc.uimap.extension import WebCombo
from ehc_e2e.auc.uimap.shared.generic import (
    RequestInfoTab, NavigationBar, SelectOperationTab, RequestResult)


class ClusterMaintenancePage(RequestInfoTab, SelectOperationTab,
                             NavigationBar, RequestResult,):

    def __init__(self):
        super(ClusterMaintenancePage, self).__init__()

        self.cbo_hardware_island = WebCombo(id='provider-Local_hwIslandSelected')
        self.cbo_unprepared_cluster = WebCombo(id='provider-Local_clusterName')
        self.cbo_hardware_island_for_rp4vm = WebCombo(id='provider-Local_rp4vmHwi')
        self.cbo_partner_cluster_for_rp4vm = WebCombo(id='provider-Local_rp4vmCluster')

        self.cbo_confirm = WebCombo(id='provider-deleteConfirmation')

        self.txt_primary_cluster_ip = WebTextBox(id='provider-primaryVrpaClusterIp')
        self.txt_primary_cluster_admin = WebTextBox(id='provider-primaryVrpaClusterUsername')
        self.txt_primary_cluster_password = WebTextBox(id='provider-primaryVrpaClusterPassword')
        self.txt_secondary_cluster_ip = WebTextBox(id='provider-secondaryVrpaClusterIp')
        self.txt_secondary_cluster_admin = WebTextBox(id='provider-secondaryVrpaClusterUsername')
        self.txt_secondary_cluster_password = WebTextBox(id='provider-secondaryVrpaClusterPassword')
        self.txt_secondary_cluster_name = WebTextBox(id='provider-secondaryVrpaClusterToDelete')

        self.cbo_hardware_island_vsan = WebCombo(id='provider-vsan_hwIslandSelected')
        self.cbo_unprepared_cluster_vsan = WebCombo(id='provider-vsan_clusterName')
        self.cbo_hardware_island_for_rp4vm_vsan = WebCombo(id='provider-vsan_rp4vmHwi')
        self.cbo_partner_cluster_for_rp4vm_vsan = WebCombo(id='provider-vsan_rp4vmCluster')
