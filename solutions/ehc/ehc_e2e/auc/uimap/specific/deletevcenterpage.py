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
                                             WebLabel, WebLink)
from ehc_e2e.auc.uimap.shared.basepage import BasePage


class DeleteVcenterPage(BasePage):
    def __init__(self):
        super(DeleteVcenterPage, self).__init__()
        self.lbl_calalog = WebLabel(xpath="//div[@class='gwt-Label GJPN4V0DODD GJPN4V0DJ3C']")

        self.lbl_vcenter_title = WebLabel(xpath="//a[@title='vCenter Endpoint Maintenance']")
        self.lnk_vcenter_request = WebLink(id="CATALOG_ITEM_REQUEST_BUTTON")
        self.txt_description = WebTextBox(id="description")
        self.txt_reasons = WebTextBox(id="reasons")
        self.btn_next = WebButton(id="next")

        self.lbl_select_operation = WebLabel(xpath="//div[@title='Action:']")

        self.btn_provider_vcenter_action = WebLink(xpath="//table[@id='provider-vCenterAction']/tbody/tr/td[1]")
        self.lbl_select_actionlist_value = WebLabel(
            xpath='//div[@class="popupContent"]/div[@class="listBoxEx"]/div/table')

        self.lbl_delete_vcenter = WebLabel(xpath="//div[@title='vCenter Object:']")

        self.btn_provider_vcenter_to_delete = WebButton(xpath="//table[@id='provider-vCenterToDelete']/tbody/tr/td[1]")
        self.lbl_select_vcenterlist_value = WebLabel(
            xpath='//div[@class="popupContent"]/div[@class="listBoxEx"]/div/table')
        self.btn_provider_confirm_to_delete = WebButton(xpath="//table[@id='provider-confirmToDelete']/tbody/tr/td[1]")
        self.lbl_select_confirmlist_value = WebLabel(
            xpath='//div[@class="popupContent"]/div[@class="listBoxEx"]/div/table')
        self.btn_submit = WebButton(id="submit")
        self.btn_cancel = WebButton(id="cancel")
        self.lbl_confirmation_success = WebLabel(xpath='//div[text()="The request has been submitted successfully."]')
        self.btn_ok = WebButton(id="CONFIRMATION_OK_BUTTON")
