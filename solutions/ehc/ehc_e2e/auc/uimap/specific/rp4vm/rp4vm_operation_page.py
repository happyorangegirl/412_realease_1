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


from uiacore.modeling.webui.controls import WebFrame, WebTextBox
from ehc_e2e.auc.uimap.extension import WebCombo, WebFrame
from ehc_e2e.auc.uimap.shared.generic import (
    RequestInfoTab, SelectOperationTab, NavigationBar, RequestResult)


class RP4VMOperationPage(RequestInfoTab, SelectOperationTab,
                         NavigationBar, RequestResult):
    def __init__(self):
        super(RP4VMOperationPage, self).__init__()

        self.frm_items = WebFrame(onload='item/ItemGadget.gadget.xml')
        self.frm_shell = WebFrame(id='shell')

        self.cbo_protect_create = WebCombo(id='provider-createNewConsistencyGroup')
        self.txt_protect_cg = WebTextBox(id='provider-newConsistencyGroupName')

        self.cbo_change_create = WebCombo(id='provider-createNewConsistencyGrp')
        self.txt_change_cg = WebTextBox(id='provider-newConsistencyGroup')

        self.cbo_exist_cg = WebCombo(id='provider-existingConsistencyGroup')

        self.cbo_policy_name = WebCombo(id='provider-policyName')
        self.cbo_boot_sequence = WebCombo(id='provider-bootSequence')
        self.cbo_current_boot_sequence = WebCombo(id='provider-currentBootSequence')
