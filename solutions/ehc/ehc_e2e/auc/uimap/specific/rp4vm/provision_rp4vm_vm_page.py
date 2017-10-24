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

from uiacore.modeling.webui.controls import WebButton, WebTextBox, WebLink

from ehc_e2e.auc.uimap.extension import WebComboEx, WebFrame
from ehc_e2e.auc.uimap.shared.generic import (
    RequestInfoTab, SelectOperationTab, NavigationBar, RequestResult)


class ProvisionRP4VMPage(RequestInfoTab, SelectOperationTab,
                         NavigationBar, RequestResult):

    def __init__(self, blueprint="Blueprints", vsphere_blueprint_id="ABCRP4VM"):
        super(ProvisionRP4VMPage, self).__init__()

        self.frm_shell = WebFrame(id='shell')

        self.btn_RP4VM_blueprint_request = WebButton(
            xpath='.//div[@id="CATALOG_ITEM_%s"]'
                  '//div[@id="CATALOG_ITEM_REQUEST_BUTTON"]' % blueprint)

        self.frm_rp4vm = WebFrame(onload='gadget.xml', extensionid='com.vmware.vcac.core.design.blueprints.requestForm')

        self.lnk_rp4vm_blueprint = WebLink(
            xpath='//span[text()="%s" and contains(@class, "x-tree-node-text")]' % vsphere_blueprint_id)

        self.txt_rp4vm_description = WebTextBox(
            xpath='//span[text()="Description:"]/parent::label/following-sibling::div/div/div/textarea')

        self.txt_rp4vm_cg = WebTextBox(xpath='//label[@data-qtip="EHC RP4VM CG"]/following-sibling::div/div/div/input')
        self.txt_rp4vm_boot_priority = WebTextBox(
            xpath='//label[@data-qtip="EHC RP4VM Boot Priority"]/following-sibling::div/div/div/input')

        self.cbo_rp4vm_policy = WebComboEx(xpath='//label[@data-qtip="EHC RP4VM Policy"]/following-sibling::div')

        self.cbo_backup_service = WebComboEx(
            xpath='//label[@data-qtip="Set Backup Service Level"]/following-sibling::div')
