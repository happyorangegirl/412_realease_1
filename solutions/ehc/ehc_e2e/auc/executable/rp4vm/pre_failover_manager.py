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

from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.auc.reusable import (
    LoadingPopupWaiter, PageNavigator, RequestManager)
from ehc_e2e.auc.uimap.specific.rp4vm import CatalogPage, PreFailoverMaintenancePage


class PreFailoverManager(BaseUseCase):
    class Func(object):
        STAGE_CGs, UNSTAGE_CGs = (
            'test_stage_cgs',
            'test_unstage_cgs')

    def __init__(self, name=None, method_name=Func.STAGE_CGs, **kwargs):
        super(PreFailoverManager, self).__init__(
            name, method_name, **kwargs)

    def setUp(self):
        self._request_page = PreFailoverMaintenancePage()
        self.wait_loading = LoadingPopupWaiter(
            self, browser=self._browser.instance._browser)

    def tearDown(self):
        RequestManager(self).save_unsubmitted_request()

    def test_stage_cgs(self):
        self._start_new_service_request()
        self._fill_out_request_info()
        self._stage_cgs()
        self._submit_request()

    def test_unstage_cgs(self):
        self._start_new_service_request()
        self._fill_out_request_info()
        self._unstage_cgs()
        self._submit_request()

    def _start_new_service_request(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        PageNavigator(self).go_to_catalog_page()

        _catalog_page = CatalogPage()

        self.wait_loading.wait_for_popup_loading_finish()

        with _catalog_page.frm_catalog:

            _catalog_page.lnk_ehc_recoverpoint_for_vms.click()

            self.wait_loading.wait_for_popup_loading_finish()

            self.assertTrue(
                _catalog_page.btn_RP4VM_policy_maintenance_request.exists(),
                msg=_formatter(
                    step='Validate Request button of RP4VM Policy Maintenance')
            )
            _catalog_page.btn_RP4VM_pre_failover_request.click()

    def _fill_out_request_info(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        with self._request_page.frm_catalog:
            self.assertTrue(
                self._request_page.txt_description.exists(),
                msg=_formatter(step='Display Description text box')
            )

            self._request_page.txt_description.set(self._testMethodName)
            self._request_page.txt_reasons.set(self._name)
            self._request_page.btn_next.click()

            self.assertTrue(
                self._request_page.cbo_operation.exists(),
                msg=_formatter(step='Display Action dropdown list'))

    def _submit_request(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        with self._request_page.frm_catalog:
            self.assertTrue(self._request_page.btn_submit.exists(),
                            msg=_formatter(step='Click submit button'))
            self._request_page.btn_submit.click()

        with self._request_page.frm_catalog:
            self.assertTrue(self._request_page.lbl_success_msg.exists(),
                            msg='Failed to submit request')
            self._request_page.btn_ok.click()

    def _stage_cgs(self):
        with self._request_page.frm_catalog:
            self._request_page.cbo_operation.select(by_visible_text='Stage Consistency Group')
            self.wait_loading.wait_for_popup_loading_finish()
            self.assertTrue(self._request_page.btn_next.exists(),
                            msg="<Next> button doesn't exist after selecting action.")
            self._request_page.btn_next.click()
            self.__select_stage_bg_and_cgs()

    def _unstage_cgs(self):
        with self._request_page.frm_catalog:
            self._request_page.cbo_operation.select(by_visible_text='Unstage Consistency Group')
            self.wait_loading.wait_for_popup_loading_finish()
            self.assertTrue(self._request_page.btn_next.exists(),
                            msg="<Next> button doesn't exist after selecting action.")
            self._request_page.btn_next.click()
            self.__select_unstage_bg_and_cgs()

    def __select_stage_bg_and_cgs(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format
        self.wait_loading.wait_for_popup_loading_finish()
        self.assertTrue(self._request_page.cbo_stage_bussiness_group.exists(),
                        msg=_formatter(step='Stage Consistency Group.'))
        self._request_page.cbo_stage_bussiness_group.select(by_visible_text=self.cg_info['bg'])
        self.wait_loading.wait_for_popup_loading_finish()
        _checkbox_list = self._request_page.get_cg_checkbox_list(self._request_page.lst_stage_cgs, self.cg_info['cgs'])
        for item in _checkbox_list:
            item.tick()
        self.wait_loading.wait_for_popup_loading_finish()
        self._request_page.cbo_stage_confirm.select('Confirm')
        self.wait_loading.wait_for_popup_loading_finish()
        self._request_page.btn_next.click()

    def __select_unstage_bg_and_cgs(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format
        self.wait_loading.wait_for_popup_loading_finish()
        self.assertTrue(self._request_page.cbo_unstage_bussiness_group.exists(),
                        msg=_formatter(step='Unstage Consistency Group.'))
        self._request_page.cbo_unstage_bussiness_group.select(by_visible_text=self.cg_info['bg'])
        self.wait_loading.wait_for_popup_loading_finish()
        _checkbox_list = self._request_page.get_cg_checkbox_list(self._request_page.lst_unstage_cgs, self.cg_info['cgs'])
        for item in _checkbox_list:
            item.tick()
        self.wait_loading.wait_for_popup_loading_finish()
        self._request_page.cbo_unstage_confirm.select('Confirm')
        self.wait_loading.wait_for_popup_loading_finish()
        self._request_page.btn_next.click()

    def _validate_input_args(self, **kwargs):
        if self._testMethodName in (self.Func.STAGE_CGs, self.Func.UNSTAGE_CGs):
            self.__validate_args_of_stage_cgs(**kwargs)
        else:
            raise NotImplementedError('Validate method %s '.format(**kwargs))

    def __validate_args_of_stage_cgs(self, browser=None, **cg_info):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        self.assertIsNotNone(cg_info, msg=_formatter(step='Validate cg info'))
        self.cg_info = cg_info
        self._browser = browser
