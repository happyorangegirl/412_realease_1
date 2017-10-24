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

from robot.api import logger
from uiacore.modeling.webui.controls import (WebButton, WebLabel)
from ehc_e2e.auc.uimap.shared.basepage import BasePage
from ehc_e2e.auc.uimap.shared.mainpage import MainPage


class DestroyVMsPage(BasePage):
    def __init__(self, destroy_vm_name):
        super(DestroyVMsPage, self).__init__()
        self.btn_destroy = WebButton(xpath='//div[text()="Destroy"]')
        self.gadget_2_frame_label = WebLabel(id='__gadget_2')
        self.gadget_2_frame_id = '__gadget_2'
        self.service_destroy_lab = WebLabel(xpath='//div[text()="Are you sure you wish to continue?"]')
        self.destroy_vm_item = WebButton(xpath='//a[@title="{item}"]'.format(item=destroy_vm_name))
        self.btn_close = WebButton(id='cancel')

        self.btn_submit = WebButton(id='submit')
        self.lab_confirmation_success = WebLabel(xpath='//div[text()="The request has been submitted successfully."]')
        self.btn_ok = WebButton(id='CONFIRMATION_OK_BUTTON')

        self.btn_item_page_table_refresh = WebButton(xpath='//div[@id="RESOURCES_TABLE_REFRESH_ICON"]')
        self.item_page_iframe_url = 'https://com.vmware.csp.core.cafe.catalog.plugin.vproxy//item/ItemGadget.gadget.xml'
        self.btn_machines = WebButton(id='Infrastructure.Machine')
        self.machines_xpath = '//*[@id="Infrastructure.Machine"]'

    def navigate_to_items_page(self, current_browser):
        _browser = current_browser.instance._browser.current
        _browser.switch_to.frame(None)

        if MainPage().btn_items.exists():
            MainPage().btn_items.click()
            BasePage().wait_for_loading_complete(3)
            return True
        else:
            return False

    def switch_to_target_frame(self, current_browser, go_inner_frame=False, target_frame_id=''):

        _browser = current_browser.instance._browser.current
        if not go_inner_frame:
            _browser.switch_to.default_content()

        if target_frame_id:
            _browser.switch_to.frame(target_frame_id)
            logger.info(
                'Switch to frame {}'.format(target_frame_id),
                False, True)
        else:
            logger.error('Looking for target iframe failed.')

        if go_inner_frame:
            iframes = _browser.find_elements_by_tag_name('iframe')
            iframe_id_exist = False
            for iframe in iframes:
                iframe_id = iframe.get_attribute('id')

                if iframe_id == 'innerFrame':
                    iframe_id_exist = True
                    _browser.switch_to.frame(iframe_id)
                    logger.info('Switch to innerFrame.')
                    break
            if not iframe_id_exist:
                logger.error('Looking for innerFrame failed.')
