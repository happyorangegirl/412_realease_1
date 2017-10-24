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

from ehc_e2e.auc.uimap.extension import WebCombo, WebFrame
from ehc_e2e.auc.uimap.shared.generic import (
    RequestInfoTab, NavigationBar, SelectOperationTab, RequestResult)


class vRPAClusterMaintenancePage(
        RequestInfoTab,
        SelectOperationTab,
        NavigationBar,
        RequestResult
):

    def __init__(self):
        super(vRPAClusterMaintenancePage, self).__init__()

        self.frm_shell = WebFrame(id='shell')
        self.cbo_primary_cluster_name = WebCombo(id='provider-primaryVrpaClusterToDelete')
        self.cbo_force_delete = WebCombo(id='provider-forceDelete')
        self.cbo_confirm = WebCombo(id='provider-deleteConfirmation')
        self.txt_primary_cluster_ip = WebTextBox(id='provider-primaryClusterManagementIp')
        self.txt_primary_cluster_admin = WebTextBox(id='provider-primaryClusterUsername')
        self.txt_primary_cluster_password = WebTextBox(id='provider-primaryClusterPassword')
        self.txt_secondary_cluster_ip = WebTextBox(id='provider-secondaryClusterManagementIp')
        self.txt_secondary_cluster_admin = WebTextBox(id='provider-secondaryClusterUsername')
        self.txt_secondary_cluster_password = WebTextBox(id='provider-secondaryClusterPassword')
        self.txt_secondary_cluster_name = WebTextBox(id='provider-secondaryVrpaClusterToDelete')
