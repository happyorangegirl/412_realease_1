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
from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.auc.reusable import (
    LoadingPopupWaiter, PageNavigator, RequestManager)
from ehc_e2e.auc.uimap.specific.rp4vm import CatalogPage, ProvisionRP4VMPage


class ProvisionRP4VMManager(BaseUseCase):
    class Func(object):
        PROVISION_RP4VM, PROVISION_VM = (
            'test_provision_rp4vm',
            'test_provision_vm')

    def __init__(self, name=None, method_name=Func.PROVISION_RP4VM, **kwargs):
        super(ProvisionRP4VMManager, self).__init__(
            name, method_name, **kwargs)

    def setUp(self):
        self._request_page = ProvisionRP4VMPage(self.blueprint, self.vsphere_blueprint_id)
        self.wait_loading = LoadingPopupWaiter(
            self, browser=self._browser.instance._browser)

    def tearDown(self):
        RequestManager(self).save_unsubmitted_request()

    def test_provision_rp4vm(self):
        self._start_new_service_request()
        self._provision_rp4vm()
        self._submit_request()

    def test_provision_vm(self):
        self._start_new_service_request()
        self._submit_request()

    def _start_new_service_request(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        PageNavigator(self).go_to_catalog_page()

        _catalog_page = CatalogPage()

        self.wait_loading.wait_for_popup_loading_finish()

        with _catalog_page.frm_catalog:
            _catalog_page.lnk_all_services.click()

            self.wait_loading.wait_for_popup_loading_finish()

            self.assertTrue(
                self._request_page.btn_RP4VM_blueprint_request.exists(),
                msg=_formatter(
                    step='Validate Request button of RP4VM Blueprint')
            )

            self._request_page.btn_RP4VM_blueprint_request.click()

    def _submit_request(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        with self._request_page.frm_catalog:
            self.wait_loading.wait_for_popup_loading_finish()
            self.assertTrue(self._request_page.btn_submit.exists(),
                            msg=_formatter(step='Click submit button'))
            self._request_page.btn_submit.click()

        with self._request_page.frm_catalog:
            self.assertTrue(self._request_page.lbl_success_msg.exists(),
                            msg='Failed to submit request')
            self._request_page.btn_ok.click()

    def _provision_rp4vm(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format
        with self._request_page.frm_catalog:
            self.wait_loading.wait_for_popup_loading_finish()
            with self._request_page.frm_rp4vm:
                self._request_page.txt_rp4vm_description.set(self._testMethodName)

                self._request_page.lnk_rp4vm_blueprint.click()
                self.wait_loading.wait_for_popup_loading_finish()
                time.sleep(5)   # need to wait for some drop down lists to be enabled

                self.assertTrue(self._request_page.cbo_rp4vm_policy.exists(),
                                msg=_formatter(step='Display combox rp4vm policy'))

                self._request_page.txt_rp4vm_cg.set(self.vm_info['cg'])
                self._request_page.txt_rp4vm_boot_priority.set(self.vm_info['sequence'])

                self.assertTrue(self._request_page.cbo_rp4vm_policy.exists(),
                                msg=_formatter(step='Policy Combobox'))
                self._request_page.cbo_rp4vm_policy.select(by_visible_text=self.vm_info['policy'])

                if self.vm_info['backup_service'] and self._request_page.cbo_backup_service.exists():
                    self._request_page.cbo_backup_service.select(by_visible_text=self.vm_info['backup_service'])

    def _validate_input_args(self, **kwargs):
        self.__validate_args_of_provision_rp4vm(**kwargs)

    def _finalize_output_params(self):
        # if self.deployed_vms:
        #     self._output += self.deployed_vms
        pass

    def __validate_args_of_provision_rp4vm(self, browser=None, **vm_info):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        self.assertIsNotNone(vm_info, msg=_formatter(step='Validate provision vm info'))
        self.vm_info = vm_info
        self.blueprint = vm_info['blueprint']
        self.vsphere_blueprint_id = vm_info['vsphere_blueprint_id']
        self._browser = browser
