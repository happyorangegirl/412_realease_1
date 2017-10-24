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


class OperateVMPage(BasePage):
    def __init__(self, test_vm_name=None):
        super(OperateVMPage, self).__init__()
        self.lnk_test_vm = WebLink(xpath='//*[@title="{0}"]'.format(test_vm_name))
        self.btn_poweroff = WebButton(xpath='//div[text()="Power Off"]')
        self.btn_reboot = WebButton(xpath='//div[text()="Reboot"]')
        self.btn_poweron = WebButton(xpath='//div[text()="Power On"]')

        self.btn_submit = WebButton(xpath='//*[@id="submit"]')
        self.btn_ok = WebButton(xpath="//*[@id='CONFIRMATION_OK_BUTTON']")
        self.btn_cancel = WebButton(xpath="//*[@id='cancel']")
        self.btn_save = WebButton(xpath="//*[@id='save']")
        self.btn_next = WebButton(xpath='//button[@id="next"]')
        self.btn_machine = WebButton(xpath='//*[@id="Infrastructure.Machine"]')

        self.lbl_vm_status = WebLabel(id='ctl00_ctl00_MasterContent_MainContentPlaceHolder_MachineRecord_lblStatus')

        self.btn_get_backup_status = WebButton(xpath='//div[text()="Get Backup Status"]')
        self.btn_on_demand_backup = WebButton(xpath='//div[text()="On Demand Backup"]')
        self.btn_on_demand_restore = WebButton(xpath='//div[text()="On Demand Restore"]')

        self.txt_description = WebTextBox(xpath='//input[@id="description"]')
        self.txt_reasons = WebTextBox(xpath='//textarea[@id="reasons"]')
        self.gadget_url_str = 'https://com.vmware.csp.core.cafe.catalog.plugin.vproxy//item/ItemGadget.gadget.xml'
        self.btn_refresh_item = WebButton(xpath='//*[@id="RESOURCES_TABLE_REFRESH_ICON"]')
        self.gadget_url_item_details_str = 'https://com.vmware.csp.iaas.ui.vproxy//forms-gadget.xml'
