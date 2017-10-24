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

from uiacore.modeling.webui.controls import WebButton, WebTextBox
from ehc_e2e.auc.uimap.extension import WebComboEx, WebFrame
from ehc_e2e.auc.uimap.shared.basepage import BasePage


class DeployVMCommonPage(BasePage):
    def __init__(self, bp_name):
        super(DeployVMCommonPage, self).__init__()
        # this element is not in deploy vm page
        self.btn_bp_entitlement = WebButton(xpath='//div[text()="{}"]'.format(bp_name))

        # this element is not in deploy vm page
        self.btn_bp_request = WebButton(
            xpath='.//div[@id="CATALOG_ITEM_{}"]//div[@id="CATALOG_ITEM_REQUEST_BUTTON"]'.format(bp_name))

        self.btn_save = WebButton(xpath='//*[@id="save"]')
        self.btn_submit = WebButton(xpath='//*[@id="submit"]')
        self.btn_cancel = WebButton(xpath='//*[@id="cancel"]')
        self.btn_ok = WebButton(xpath='//*[@id="CONFIRMATION_OK_BUTTON"]')

        self.iframe_bp = WebFrame(onload='gadget.xml', extensionid='com.vmware.vcac.core.design.blueprints.requestForm')
        self.iframe_catalog = WebFrame(onload='selfservice/SelfServiceGadget.gadget.xml')

        self.txt_description = WebTextBox(
            xpath='//span[text()="Description:"]/parent::label/following-sibling::div/div/div/textarea')

        self.txt_cg_xpath = '//label[@data-qtip="EHC RP4VM CG"]/following-sibling::div/div/div/input'
        self.txt_cg = WebTextBox(xpath=self.txt_cg_xpath)
        self.txt_boot_priority_xpath = \
            '//label[@data-qtip="EHC RP4VM Boot Priority"]/following-sibling::div/div/div/input'
        self.txt_boot_priority = WebTextBox(xpath=self.txt_boot_priority_xpath)
        self.cb_policy_xpath = '//label[@data-qtip="EHC RP4VM Policy"]/following-sibling::div'
        self.cb_policy = WebComboEx(xpath=self.cb_policy_xpath)
        self.cb_backup_service_xpath = '//label[@data-qtip="Set Backup Service Level"]/following-sibling::div'
        self.cb_backup_service = WebComboEx(xpath=self.cb_backup_service_xpath)
