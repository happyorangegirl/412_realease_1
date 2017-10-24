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

from uiacore.modeling.webui.controls import WebTextBox, WebButton, WebLink

from ehc_e2e.auc.uimap.extension import WebCombo, WebFrame
from ehc_e2e.auc.uimap.shared.generic import (
    RequestInfoTab, SelectOperationTab, NavigationBar, RequestResult)


class PolicyMaintenancePage(RequestInfoTab, SelectOperationTab,
                            NavigationBar, RequestResult):
    def __init__(self):
        super(PolicyMaintenancePage, self).__init__()
        self.frm_shell = WebFrame(id='shell')

        self.txt_async_policy_name = WebTextBox(id='provider-asyncPolicyName')
        self.txt_sync_policy_name = WebTextBox(id='provider-syncPolicyName')
        self.txt_policy_name = WebTextBox(id='provider-policyName')
        self.cbo_type_of_policy = WebCombo(id='provider-policyType')

        self.txt_sync_journal_size = WebTextBox(id='provider-syncJournalSize')
        self.txt_async_journal_size = WebTextBox(id='provider-asyncJournalSize')
        self.txt_rp_number = WebTextBox(id="provider-asyncRpoNumber")
        self.cbo_rp_units = WebCombo(id='provider-asyncRpoUnits')
        self.btn_rp_units_open = WebButton(xpath='//table[@id="provider-asyncRpoUnits"]/tbody/tr[1]/td[2]')
        self.lnk_rp_units_dropdown = WebLink(xpath='//div[@class="popupBoxPopup"]/div[1]/div[1]/div[1]/table/tbody')

        self.cbo_policy_to_delete = WebCombo(id='provider-policyNameToDelete')
        self.cbo_delete_confirm = WebCombo(id='provider-deleteConfirmation')