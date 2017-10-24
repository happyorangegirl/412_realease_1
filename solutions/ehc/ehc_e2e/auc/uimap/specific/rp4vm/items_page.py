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

from uiacore.modeling.webui.controls import WebLink, WebCombo, WebButton

from ehc_e2e.auc.uimap.shared.generic import ItemsTab


class ItemVMPage(ItemsTab):
    def __init__(self, vmname):
        super(ItemVMPage, self).__init__()

        self.cbo_vms = WebCombo(id='RESOURCES_TABLE_DATA')

        self.lnk_vm = WebLink(xpath='//table[@id="RESOURCES_TABLE_DATA"]'
                              '//a[@title="%s"]' % vmname)

        self.lnk_machines = WebLink(id='Infrastructure.Machine')

        self.lnk_change_boot_priority = WebLink(
            xpath='//div[contains(text(), "RP4VM Change Boot Priority")]')

        self.lnk_change_cg = WebLink(
            xpath='//div[contains(text(), "RP4VM Change CG")]')

        self.lnk_protect_vm = WebLink(
            xpath='//div[contains(text(), "RP4VM Protect VM")]')

        self.lnk_unprotect_vm = WebLink(
            xpath='//div[contains(text(), "RP4VM Unprotect VM")]')

        self.lnk_destroy = WebLink(
            xpath='//div[contains(text(), "Destroy")]')

        self.btn_close = WebButton(id='cancel')
