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

import logging

from robot.api import logger
from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.auc.reusable import PageNavigator, LoadingPopupWaiter
from ehc_e2e.auc.uimap.specific.rp4vm import ItemVMPage, RP4VMOperationPage


class RP4VMOperationManager(BaseUseCase):
    class Func(object):
        PROTECT_VM, UNPROTECT_VM, CHANGE_CG, CHANGE_BOOT_PRIORITY = (
            'test_protecting_vm',
            'test_unprotecting_vm',
            'test_changing_cg',
            'test_changing_boot_priority'
        )

    def __init__(self, name=None, method_name=Func.PROTECT_VM, **kwargs):
        super(RP4VMOperationManager, self).__init__(
            name, method_name, **kwargs)

    def setUp(self):
        self._request_page = RP4VMOperationPage()
        self.wait_loading = LoadingPopupWaiter(
            self, browser=self._browser.instance._browser)

        self._item_page = ItemVMPage(vmname=self.vm_name)

    def test_protecting_vm(self):
        self._start_new_service_request()
        self._fill_out_request_info()
        # self._protect_vm()
        self._submit_request()

    def test_changing_cg(self):
        self._start_new_service_request()
        self._fill_out_request_info()
        # self._change_cg()
        self._submit_request()

    def test_changing_boot_priority(self):
        self._start_new_service_request()
        self._fill_out_request_info()
        # self._change_boot_sequence()
        self._submit_request()

    def test_unprotecting_vm(self):
        self._start_new_service_request()
        self._fill_out_request_info()
        self._submit_request()

    def _start_new_service_request(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        PageNavigator(self).go_to_items_page()

        self.wait_loading.wait_for_popup_loading_finish()

        with self._item_page.frm_items:
            self._item_page.lnk_machines.click()

            self.wait_loading.wait_for_popup_loading_finish()

            self.assertTrue(self._item_page.lnk_vm.exists(),
                            msg=_formatter(step='Display VM Link'))
            self._item_page.lnk_vm.click()

        self.wait_loading.wait_for_popup_loading_finish()
        with self._item_page.frm_items:
            self.assertTrue(self._item_page.lnk_protect_vm.exists(),
                            msg=_formatter(step='Display PROTECT VM Link'))
            if self._testMethodName == self.Func.PROTECT_VM:
                self._item_page.lnk_protect_vm.click()
            if self._testMethodName == self.Func.UNPROTECT_VM:
                self._item_page.lnk_unprotect_vm.click()
            if self._testMethodName == self.Func.CHANGE_CG:
                self._item_page.lnk_change_cg.click()
            if self._testMethodName == self.Func.CHANGE_BOOT_PRIORITY:
                self._item_page.lnk_change_boot_priority.click()
        from ehc_e2e.auc.uimap.shared import LoadingWindow
        LoadingWindow().wait_loading2(self._browser)

    def _fill_out_request_info(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        with self._request_page.frm_items:
            self.assertTrue(
                self._request_page.txt_description.exists(),
                msg=_formatter(step='Display Description text box')
            )

            self._request_page.txt_description.set(self._testMethodName)
            self._request_page.txt_reasons.set(self._name)
            logger.info("Filled description: {0} and reason: {1}".format(self._testMethodName, self._name))
            # self._request_page.btn_next.click()

    def _submit_request(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        with self._request_page.frm_items:
            self.assertTrue(self._request_page.btn_submit.exists(),
                            msg=_formatter(step='Click submit button'))
            self._request_page.btn_submit.click()
            logger.info("Request submitted.")

        with self._request_page.frm_items:
            self.assertTrue(self._request_page.lbl_success_msg.exists(),
                            msg='Failed to submit request')
            self._request_page.btn_ok.click()
            logger.info("Request submitted.")

    def _protect_vm(self):
        self.__rp4vm_operation(self._request_page.cbo_protect_create, self._request_page.txt_protect_cg)

    def _change_cg(self):
        self.__rp4vm_operation(self._request_page.cbo_change_create, self._request_page.txt_change_cg)

    def __rp4vm_operation(self, cbo_operation, txt_new_cg):
        _formatter = 'Running on step: "{step}" - FAILED'.format
        with self._request_page.frm_items:

            if bool(self.rp4vm_info['is_new_cg']):
                txt_new_cg.set(self.rp4vm_info['cg'])
                self._request_page.cbo_policy_name.select(by_visible_text=self.rp4vm_info['policy'])
                self.wait_loading.wait_for_popup_loading_finish()
            else:
                cbo_operation.select(by_visible_text='No')
                self.wait_loading.wait_for_popup_loading_finish()

                if not self._request_page.cbo_exist_cg.current.get_attribute('aria-hidden'):
                    self.assertTrue(self._request_page.cbo_exist_cg.exists(),
                                    msg=_formatter(step='Display combox exist cg'))
                    self._request_page.cbo_exist_cg.select(by_visible_text=self.rp4vm_info['cg'])
                    self.wait_loading.wait_for_popup_loading_finish()

            self._request_page.cbo_boot_sequence.select(by_visible_text=self.rp4vm_info['sequence'])
            self._request_page.btn_next.click()

    def _change_boot_sequence(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        with self._request_page.frm_items:
            self.assertTrue(self._request_page.cbo_boot_sequence.exists(),
                            msg=_formatter(step='Display combox boot sequence'))
            current_sequence = self._request_page.cbo_current_boot_sequence.current.text
            choice_sequence = map(str, self._request_page.cbo_boot_sequence.items())
            self.assertNotIn(current_sequence, self._request_page.cbo_boot_sequence.items(),
                             msg=_formatter(step='Current sequence NOT in choice sequence'))
            from random import choice
            select_sequence = choice(choice_sequence)
            self._request_page.cbo_boot_sequence.select(by_visible_text=select_sequence)
            self._request_page.btn_next.click()

    def _validate_input_args(self, **kwargs):
        self.__validate_args_of_rp4vm_operation(**kwargs)

    def _finalize_output_params(self):
        pass

    def __validate_args_of_rp4vm_operation(self, browser=None, **rp4vm_info):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        self.assertIsNotNone(rp4vm_info, msg=_formatter(step='Validate RP4VM operation info'))
        self.rp4vm_info = rp4vm_info
        self.vm_name = rp4vm_info.get('vm', '')
        self._browser = browser

    def tearDown(self):
        with self._item_page.frm_items:
            if self._item_page.btn_close.exists():
                self._item_page.btn_close.click()

        with self._request_page.frm_items:
            if self._request_page.btn_save.exists():
                self._request_page.btn_save.click()
