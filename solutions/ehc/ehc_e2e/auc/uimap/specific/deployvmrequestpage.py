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

from uiacore.modeling.webui.controls import WebButton, WebLink, WebLabel

from ehc_e2e.auc.uimap.extension import WebFrame


class DeployVmRequestPage(object):
    def __init__(self):
        super(DeployVmRequestPage, self).__init__()

        self.frm_request_details = WebFrame(
            onload='request/RequestGadget.gadget.xml',
            extensionid='csp.catalog.request')
        self.btn_ok = WebButton(id='cancel')

        self.frm_blueprint_request = WebFrame(
            onload='gadget.xml',
            extensionid='com.vmware.vcac.core.design.blueprints.requestDetailsForm')
        self.lnk_execution_info = WebLink(xpath='//a[@data-qtip="Execution Information"]')

        self.lnk_exe_info = WebLink(xpath='//span[text()="Execution Information"]')
        self.deployed_vms = []

    @staticmethod
    def get_provision_details_cells(bp_filter=False, bp_list=None):
        _grid_container = WebLabel(xpath='//div[starts-with(@id,"vcac")]/div[2]/div/div')
        _items = _grid_container.current.parent.find_elements_by_xpath('//div[starts-with(@id,"vcac")]/div[2]/div/div/table')

        _details_cells = [_item.find_elements_by_tag_name('td')[2]
                          for _item in _items if 'Provision' in _item.text and
                          (not bp_filter or any(bp in _item.text.split('\n')[0] for bp in bp_list))]

        return [WebLabel(element=cell) for cell in _details_cells]

    def get_deployed_vms(self, bp_filter=False, bp_list=None):
        with self.frm_request_details:
            with self.frm_blueprint_request:
                if self.lnk_execution_info.exists():
                    self.lnk_execution_info.click()
                    self.deployed_vms.extend(
                        [cell.value.split()[-1].strip('.')
                         for cell in self.__class__.get_provision_details_cells(bp_filter=bp_filter, bp_list=bp_list)
                         if 'Request succeeded.' in cell.value])
        with self.frm_request_details:
            self.btn_ok.click()

        return self.deployed_vms
