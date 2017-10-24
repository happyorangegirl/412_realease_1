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

from uiacore.modeling.webui.controls import (WebTextBox, WebButton,
                                             WebLabel)
from ehc_e2e.auc.uimap.shared.basepage import BasePage


class DeleteVcenterRelationshipPage(BasePage):
    def __init__(self):
        super(DeleteVcenterRelationshipPage, self).__init__()
        self.txt_description = WebTextBox(id='description')
        self.txt_reasons = WebTextBox(id='reasons')
        self.btn_next = WebButton(id='next')
        self.select_parent_element = WebLabel(xpath='//div[@class="popupContent"]/div[@class="listBoxEx"]/div/table')
        self.lab_select_operation = WebLabel(xpath='//div[@title="Action:"]')
        self.btn_select_the_operation = WebButton(xpath='//table[@id="provider-mainAction"]/tbody/tr/td[1]')

        self.lab_protected_vcenter_name = WebLabel(xpath='//div[@title="Protected vCenter:"]')
        self.btn_protected_vcenter_name = WebButton(xpath='//*[@id="provider-ProtectedVCenterDTName"]/tbody/tr/td[1]')
        self.btn_recovery_vcenter_name = WebButton(xpath='//table[@id="provider-RecoveryVCenterDTName"]/tbody/tr/td[1]')
        self.lab_action_chosen = WebLabel(xpath='//div[@title="Review the inputs and submit :"]')

        self.btn_submit = WebButton(id='submit')
        self.lab_confirmation_success = WebLabel(xpath='//div[text()="The request has been submitted successfully."]')
        self.btn_ok = WebButton(id='CONFIRMATION_OK_BUTTON')
        self.ehc_configure = WebButton(xpath='//div[text()="EHC Configuration"]')
        self.btn_cancel = WebButton(id='cancel')
        self.btn_save = WebButton(id="save")

        self.btn_confirm_to_del = WebButton(xpath="//table[@id='provider-confirmation']/tbody/tr/td[2]")
        self.lbl_confirmlist = WebLabel(xpath='//div[@class="popupContent"]/div[@class="listBoxEx"]/div/table')
