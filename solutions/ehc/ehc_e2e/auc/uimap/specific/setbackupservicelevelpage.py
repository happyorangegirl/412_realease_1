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

from uiacore.modeling.webui.controls import WebTextBox, WebButton, WebLabel, WebLink
from ehc_e2e.auc.uimap.shared.basepage import BasePage


class SetBackupServiceLevelPage(BasePage):

    def __init__(self, test_vm_name=None):
        super(SetBackupServiceLevelPage, self).__init__()
        self.test_vm_item = WebButton(xpath='//a[@title="{item}"]'.format(item=test_vm_name))
        self.btn_set_backup_service_level = WebButton(xpath='//div[text()="Set Backup Service Level"]')
        self.lbl_desc = WebLabel(xpath='//div[@title="Description:"]')
        self.txt_desc = WebTextBox(id='description')
        self.btn_next = WebButton(xpath='//*[@id="next"]')
        self.btn_submit = WebButton(xpath='//*[@id="submit"]')
        self.btn_ok = WebButton(xpath="//*[@id='CONFIRMATION_OK_BUTTON']")
        self.btn_close = WebButton(xpath="//*[@id='cancel']")
        self.btn_save = WebButton(xpath="//*[@id='save']")
        self.lbl_set_backup_service_level = WebLabel(
            xpath='//div[@title="Select a New Backup Service Level to move the VM into:"]')
        self.lnk_set_backup_service_level_menu = WebLink(
            xpath='//*[@id="provider-newBackupservicelevel"]/tbody/tr/td[@align="right"]')
        self.lnk_set_backup_service_level_dropdownlist = WebLink(
            xpath='//*[@class="listBoxEx"]/div/table/tbody')
        self.lbl_confirmation_success = WebLabel(
            xpath='//div[text()="The request has been submitted successfully."]')
        self.lnk_properties = WebLink(
            xpath='//*[@id="ctl00_ctl00_MasterContent_MainContentPlaceHolder_MachineRecord_T4"]')
        self.lbl_properties_data = WebLabel(
            xpath='//*[@id="ctl00_ctl00_MasterContent_MainContentPlaceHolder_MachineRecord_propBag'
                  '_pnlContent_propertyGrid_DXMainTable"]')
        self.properties_row_xpath_str = '//*[@id="ctl00_ctl00_MasterContent_MainContentPlaceHolder_MachineRecord' \
                                        '_propBag_pnlContent_propertyGrid_DXDataRow'
        self.gadget_url_str = 'https://com.vmware.csp.core.cafe.catalog.plugin.vproxy//item/ItemGadget.gadget.xml'
        self.gadget_url_item_details_str = 'https://com.vmware.csp.iaas.ui.vproxy//forms-gadget.xml'
        self.btn_refresh_item = WebButton(xpath='//*[@id="RESOURCES_TABLE_REFRESH_ICON"]')
        self.btn_machine = WebButton(xpath='//*[@id="Infrastructure.Machine"]')
