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


class DeleteDataStorePage(BasePage):
    def __init__(self):
        super(DeleteDataStorePage, self).__init__()
        self.txt_reasons = WebTextBox(id='reasons')
        self.txt_description = WebTextBox(id='description')
        self.btn_next = WebButton(id='next')
        self.txt_password = WebTextBox(xpath='//input[@id="provider-password"]')
        self.btn_select_datastore_to_delete = WebButton(
            xpath='//table[@id="provider-selectedDatastore"]/tbody/tr/td[2]')
        self.lbl_active_value = WebLabel(xpath='//div[@class="popupContent"]'
                                               '/div[@class="listBoxEx"]/div/table')
        self.btn_open_confirm_dropdownlist = WebButton(
            xpath='//*[@id="provider-confirm"]/tbody/tr/td[2]')
        self.btn_submit = WebButton(id="submit")
        self.lbl_confirmation_success = WebLabel(xpath='//div[text()="The request has been submitted successfully."]')
        self.btn_ok = WebButton(id="CONFIRMATION_OK_BUTTON")
        self.btn_cloud_storage = WebButton(xpath='//div[text()="Cloud Storage"]')
        self.lbl_submit_request = WebLabel(xpath='//div[text()="Submit Request"]')
        self.btn_save = WebButton(id='save')
