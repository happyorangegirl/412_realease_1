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

from uiacore.modeling.webui.controls import (WebTextBox, WebButton, WebLabel)
from ehc_e2e.auc.uimap.shared.basepage import BasePage


class AddHwiPage(BasePage):
    def __init__(self):
        super(AddHwiPage, self).__init__()
        self.txt_reasons = WebTextBox(id='reasons')
        self.txt_description = WebTextBox(id='description')
        self.btn_next = WebButton(id='next')
        self.lbl_action_to_performed = WebLabel(xpath='//div[@title="Action to be performed :"]')
        self.lbl_provideName_for_hwi = WebLabel(
            xpath='//div[@title="Please provide the name for the new Hardware Island:"]')

        self.btn_performed_tab = WebButton(xpath='//table[@id="provider-HIAction"]/tbody/tr/td[1]')
        self.lbl_active_value = WebLabel(xpath='//div[@class="popupContent"]/div[@class="listBoxEx"]/div/table')

        self.lbl_active_checkbox = WebLabel(xpath='//div[@id ="provider-hIslandVArrays"]/div/table')
        self.txt_hwi_name = WebTextBox(
            xpath='//input[@id="provider-hIsnaldName" and @class="gwt-TextBox" and @style="width: 182px;"]')
        self.btn_provider_vcenter = WebButton(xpath='//table[@id="provider-hIslandVCenter"]/tbody/tr/td[1]')
        self.btn_provider_site = WebButton(xpath='//table[@id="provider-hIslandSite"]/tbody/tr/td[1]')
        self.btn_provider_vipr_to_add = WebButton(xpath='//table[@id="provider-ViPRInstanceToAdd"]/tbody/tr/td[1]')
        self.btn_submit = WebButton(id="submit")
        self.lbl_confirmation_success = WebLabel(xpath='//div[text()="The request has been submitted successfully."]')
        self.btn_ok = WebButton(id="CONFIRMATION_OK_BUTTON")
        self.contains_text = ".//*[contains(text(), '{}')]"
        self.btn_cancel = WebButton(id="cancel")
        self.btn_ehc_configure = WebButton(xpath='//div[text()="EHC Configuration"]')
        self.btn_save = WebButton(id="save")
