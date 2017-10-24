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


class DeleteAvamarGridPage(BasePage):
    def __init__(self):
        super(DeleteAvamarGridPage, self).__init__()
        self.txt_description = WebTextBox(id='description')
        self.btn_next = WebButton(id='next')
        self.lbl_provideName_for_hwi = WebLabel(
            xpath='//div[@title="Please provide the name for the new Hardware Island:"]')
        self.btn_operation_type = WebButton(xpath='//table[@id="provider-operationType"]/tbody/tr/td[1]')
        self.lbl_active_value = WebLabel(xpath='//div[@class="popupContent"]'
                                               '/div[@class="listBoxEx"]/div/table')

        self.btn_provider_del_avamar_grid = WebButton(xpath='//table[@id="provider-delAvamarGrid"]/tbody/tr/td[1]')
        self.btn_provider_confirmation = WebButton(xpath='//table[@id="provider-delCon"]/tbody/tr/td[1]')
        self.btn_submit = WebButton(id="submit")
        self.lbl_confirmation_success = WebLabel(xpath='//div[text()="The request has been submitted successfully."]')
        self.btn_ok = WebButton(id="CONFIRMATION_OK_BUTTON")
        self.contains_text = ".//*[contains(text(), '{}')]"
        self.btn_cancel = WebButton(id="cancel")
        self.btn_data_protection_services = WebButton(xpath='//div[text()="Data Protection Services"]')
        self.btn_click = WebButton(xpath='//div[@title="Enter new Avamar Grid Name:"]')
        self.btn_save = WebButton(id="save")
