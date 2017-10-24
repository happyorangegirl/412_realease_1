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

import time
from .mainpage import MainPage
from .basepage import BasePage
from ..specific.operatevmpage import OperateVMPage
from .loadingwindow import LoadingWindow

from robot.api import logger


class ItemPage(object):
    frame_onload = 'https://com.vmware.csp.core.cafe.catalog.plugin.vproxy//item/ItemGadget.gadget.xml'

    def __init__(self, current_browser):
        self.current_browser = current_browser
        self.browser = current_browser.instance._browser.current

    def enter_frame(self):
        self.browser.switch_to.frame(None)

        if MainPage().btn_items.exists():
            MainPage().btn_items.click()
            time.sleep(3)
        else:
            raise AssertionError('Can not found `items` navigator tab/button')
        _frame_id = self.frame_id()
        self.browser.switch_to.frame(_frame_id)
        return _frame_id

    def frame_id(self):
        _frame_id = BasePage().get_accurate_frameid(self.current_browser, ItemPage.frame_onload)
        return _frame_id

    def enter_vm_frame(self, vm_name):
        page = OperateVMPage(vm_name)

        if page.btn_machine.exists():
            page.btn_machine.click()
            LoadingWindow().wait_loading(self.current_browser)
        else:
            raise AssertionError('the button Machine does not exist.')

        # got_element = lambda
        seconds = 60
        while seconds > 0:
            if not page.lnk_test_vm.exists():
                page.btn_refresh_item.click()
                seconds -= 10
                time.sleep(10)
            else:
                logger.debug('Found VM: {}'.format(vm_name))
                page.lnk_test_vm.click()
                LoadingWindow().wait_loading2(self.current_browser, 30)
                return True

        raise AssertionError("Target VM: {} does not exists".format(vm_name))

    @staticmethod
    def get_vm_status(current_browser, vm_name):
        """
        TODO: get status from items list table, do not click and enter VM detail page
        Returns (str):
            Any one of ['TurningOn', 'TurningOff', 'Rebooting', 'On', 'Off', 'UnprovisionMachine']
        """
        items_page = ItemPage(current_browser)
        if not items_page.enter_frame():
            raise AssertionError('Failed to switch to items page')
        time.sleep(3)
        items_page.enter_vm_frame(vm_name)

        vm_page = VMPage(current_browser)
        vm_page.enter_inner_frame()
        logger.debug("Getting the vm's status")

        operatevm_page = OperateVMPage(vm_name)
        if operatevm_page.lbl_vm_status.exists():
            vm_status = operatevm_page.lbl_vm_status.value
            logger.info('The status of vm {0} is: {1}.'.format(vm_name, vm_status))
        else:
            raise AssertionError('the label Status does not exist.')

        items_page.enter_frame()
        if operatevm_page.btn_cancel.exists():
            operatevm_page.btn_cancel.click()
        else:
            raise AssertionError('the Cancel button does not exist.')

        return vm_status


class VMPage(object):

    inner_frame_id = 'innerFrame'

    outer_frame_onload = 'https://com.vmware.csp.iaas.ui.vproxy//forms-gadget.xml'

    def __init__(self, current_browser):
        self.current_browser = current_browser
        self.browser = current_browser.instance._browser.current

    def _enter_outer_frame(self):
        outer_frame_id = BasePage().get_accurate_frameid(
            self.current_browser, VMPage.outer_frame_onload, from_top_document=False)
        self.browser.switch_to.frame(outer_frame_id)
        return outer_frame_id

    def enter_inner_frame(self):
        if self._enter_outer_frame():
            self.browser.switch_to.frame(VMPage.inner_frame_id)
            logger.debug('Switched to inner frame')
            return True
