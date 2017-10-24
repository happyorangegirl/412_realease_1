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
from ehc_e2e.auc.uimap.specific.avamar_fail_action import AvamarFailActionPage, CatalogPage


class AvamarFailAction(BaseUseCase):
    class Func(object):
        FAILOVER_SITE, FAILBACK_SITE, FAILOVER_GRID, FAILBACK_GRID = (
            'test_failover_avamar_site',
            'test_failback_avamar_site',
            'test_failover_avamar_grid',
            'test_failback_avamar_grid')

    def __init__(self, name=None, method_name=Func.FAILOVER_SITE, **kwargs):
        super(AvamarFailAction, self).__init__(
            name, method_name, **kwargs)

    def setUp(self):
        self._request_page = AvamarFailActionPage()
        self.wait_loading = LoadingPopupWaiter(
            self, browser=self._browser.instance._browser)
        self._catalog_page = CatalogPage()

    def tearDown(self):
        RequestManager(self).save_unsubmitted_request()

    def test_failover_avamar_site(self):
        self._start_new_service_request(self._catalog_page.btn_failover_avamar_site_request, "failover avamar site")
        self._fill_out_request_info()
        self._fail_action(self._request_page.cbo_failover_site)
        self._submit_request()

    def test_failback_avamar_site(self):
        self._start_new_service_request(self._catalog_page.btn_failback_avamar_site_request, "failback avamar site")
        self._fill_out_request_info()
        self._fail_action(self._request_page.cbo_failback_site)
        self._submit_request()

    def test_failover_avamar_grid(self):
        self._start_new_service_request(self._catalog_page.btn_failover_avamar_grid_request, "failover avamar grid")
        self._fill_out_request_info()
        self._fail_action(self._request_page.cbo_avamargrid)
        self._submit_request()

    def test_failback_avamar_grid(self):
        self._start_new_service_request(self._catalog_page.btn_failback_avamar_grid_request, "failback avamar grid")
        self._fill_out_request_info()
        self._fail_action(self._request_page.cbo_avamargrid)
        self._submit_request()

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

    def _submit_request(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        with self._request_page.frm_catalog:
            # Checking for next button before submit button page and clicking it, Recent GUI has next button.
            self.assertTrue(self._request_page.btn_next.exists(),
                            msg=_formatter(step='next button not exists'))
            self.wait_loading.wait_for_popup_loading_finish()
            self._request_page.btn_next.click()
            self.wait_loading.wait_for_popup_loading_finish()
            self.assertTrue(self._request_page.btn_submit.exists(),
                            msg=_formatter(step='Click submit button'))
            self._request_page.btn_submit.click()

        with self._request_page.frm_catalog:
            self.assertTrue(self._request_page.lbl_success_msg.exists(),
                            msg='Failed to submit request')
            self._request_page.btn_ok.click()

    def _start_new_service_request(self, request_btn, request_name):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        PageNavigator(self).go_to_catalog_page()

        self.wait_loading.wait_for_popup_loading_finish()

        with self._catalog_page.frm_catalog:
            self._catalog_page.lnk_data_protection_services.click()

            self.wait_loading.wait_for_popup_loading_finish()

            self.assertTrue(
                request_btn.exists(),
                msg=_formatter(
                    step='Validate Request button of '+request_name)
            )
            request_btn.click()

    def _fail_action(self, cbo_select):
        with self._request_page.frm_catalog:
            cbo_select.select(by_visible_text=self.failaction['data'])

    def _validate_input_args(self, **kwargs):
        if self._testMethodName in (self.Func.FAILOVER_SITE, self.Func.FAILBACK_SITE, self.Func.FAILOVER_GRID,
                                    self.Func.FAILBACK_GRID):
            self.__validate_args_of_fail_action(**kwargs)
        else:
            raise NotImplementedError('Validate method %s '.format(**kwargs))

    def __validate_args_of_fail_action(self, browser=None, **failaction):
        _formatter = 'Running on step: "{step}" - FAILED'.format
        self.assertIsNotNone(failaction, msg=_formatter(step='Validate fail action data'))
        self._browser = browser
        self.failaction = failaction
