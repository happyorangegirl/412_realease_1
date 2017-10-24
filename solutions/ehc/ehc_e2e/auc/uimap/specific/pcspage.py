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


class ProvisionCloudStoragePage(BasePage):
    def __init__(self):
        super(ProvisionCloudStoragePage, self).__init__()
        self.hwi_name = None
        self.cluster_name = None
        self.name = None
        self.srp = None
        self.txt_reasons = WebTextBox(id='reasons')
        self.txt_description = WebTextBox(id='description')
        self.btn_next = WebButton(id='next')
        self.txt_password = WebTextBox(xpath='//input[@id="provider-userPassword"]')
        self.lnk_dropdownlist_menu = WebLabel(xpath='//div[@class="popupContent"]/div[@class="listBoxEx"]/div/table')
        self.btn_choose_cluster_name = WebButton(xpath='//table[@id="provider-selectedClusterName"]/tbody/tr/td[1]')
        self.btn_select_hwi_name = WebButton(xpath='//table[@id="provider-selectedHardwareIslandName"]/tbody/tr/td[1]')
        self.btn_choose_storage_type = WebButton(xpath='//table[@id="provider-selectedStorageType"]/tbody/tr/td[1]')
        self.btn_choose_vipr_storage_tier = WebButton(
            xpath='//table[@id="provider-selectedVPoolNameWithCapacity"]/tbody/tr/td[1]')
        self.txt_size_in_gb = WebTextBox(id="provider-dsSize")
        self.btn_submit = WebButton(id="submit")
        self.lbl_confirmation_success = WebLabel(xpath='//div[text()="The request has been submitted successfully."]')
        self.btn_ok = WebButton(id="CONFIRMATION_OK_BUTTON")
        # self.btn_cloud_storage = WebButton(xpath='//div[text()="Cloud Storage"]')
        self.btn_save = WebButton(id="save")
