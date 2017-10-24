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
from ehc_e2e.auc.reusable import LoadingPopupWaiter
from ehc_e2e.auc.reusable import PageNavigator
from ehc_e2e.auc.reusable import RequestManager
from ehc_e2e.auc.uimap.specific.rp4vm import CatalogPage, ClusterMaintenancePage


class ClusterManager(BaseUseCase):
    class Func(object):
        ONBOARD_LOCAL_CLUSTER = 'test_onboard_local_cluster'
        ONBOARD_VSAN_CLUSTER = 'test_onboard_vsan_cluster'

    def __init__(self, name=None, method_name=Func.ONBOARD_LOCAL_CLUSTER, **kwargs):
        super(ClusterManager, self).__init__(name, method_name, **kwargs)
        self._added_clusters = None

    def setUp(self):
        self.navigator = PageNavigator(self)
        self.request_page = ClusterMaintenancePage()
        self.wait_loading = LoadingPopupWaiter(
            self, browser=self._browser.instance._browser)

    def tearDown(self):
        RequestManager(self).save_unsubmitted_request()

    def test_onboard_local_cluster(self):
        self._start_new_service_request()
        self._fill_out_request_info_local()
        self._submit_request_local()

    def test_onboard_vsan_cluster(self):
        self._start_new_service_request()
        self._fill_out_request_info_vsan()
        self._submit_request_vsan()

    def _start_new_service_request(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        self.navigator.go_to_catalog_page()

        _catalog_page = CatalogPage()

        with _catalog_page.frm_catalog:
            _catalog_page.lnk_ehc_configuration.click()

            self.assertTrue(
                _catalog_page.btn_cluster_maintenance_request.exists(),
                msg=_formatter(
                    step='Validate Request button of vCenter Relationship Maintenance')
            )

            _catalog_page.btn_cluster_maintenance_request.click()

    def _fill_out_request_info_vsan(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        with self.request_page.frm_catalog:
            self.assertTrue(
                self.request_page.txt_description.exists(60),
                msg=_formatter(step='Display Description text box')
            )

            self.request_page.txt_description.set(self._description)
            self.request_page.txt_reasons.set(self._description)
            self.request_page.btn_next.click()

        with self.request_page.frm_catalog:
            self.assertTrue(
                self.request_page.cbo_operation.exists(10),
                msg=_formatter(step='Display Operation dropdown list')
            )

            self.request_page.cbo_operation.select(by_visible_text='Onboard VSAN Cluster')
            ####
            self.wait_loading.wait_for_popup_loading_finish()
            self.request_page.btn_next.click()
            self.wait_loading.wait_for_popup_loading_finish()

        with self.request_page.frm_catalog:
            self.assertTrue(
                self.request_page.cbo_hardware_island_vsan.exists(5),
                msg=_formatter(step='Display a hardware island dropdown list')
            )
            self.request_page.cbo_hardware_island_vsan.select(by_visible_text=self._vsan_cluster_hardware_island)
            self.wait_loading.wait_for_popup_loading_finish()

            self.assertTrue(
                self.request_page.cbo_unprepared_cluster_vsan.exists(5),
                msg=_formatter(step='Display an unprepared cluster dropdown list')
            )
            self.request_page.cbo_unprepared_cluster_vsan.select(by_visible_text=self._vsan_cluster_name)
            self.wait_loading.wait_for_popup_loading_finish()

            self.assertTrue(
                self.request_page.cbo_hardware_island_for_rp4vm_vsan.exists(5),
                msg=_formatter(step='Display a hardware island for rp4vm dropdown list')
            )
            self.request_page.cbo_hardware_island_for_rp4vm_vsan.select(
                by_visible_text=self._partner_vsan_cluster_hardware_island)
            self.wait_loading.wait_for_popup_loading_finish()

            self.assertTrue(
                self.request_page.cbo_partner_cluster_for_rp4vm_vsan.exists(5),
                msg=_formatter(step='Display a partner cluster for rp4vm dropdown list')
            )
            self.request_page.cbo_partner_cluster_for_rp4vm_vsan.select(by_visible_text=self._partner_vsan_cluster_name)
            self.wait_loading.wait_for_popup_loading_finish()

            self.request_page.btn_next.click()
            self.wait_loading.wait_for_popup_loading_finish()

    def _fill_out_request_info_local(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        with self.request_page.frm_catalog:
            self.assertTrue(
                self.request_page.txt_description.exists(60),
                msg=_formatter(step='Display Description text box')
            )

            self.request_page.txt_description.set(self._description)
            self.request_page.txt_reasons.set(self._description)
            self.request_page.btn_next.click()

        with self.request_page.frm_catalog:
            self.assertTrue(
                self.request_page.cbo_operation.exists(10),
                msg=_formatter(step='Display Operation dropdown list')
            )

            self.request_page.cbo_operation.select(by_visible_text='Onboard Local Cluster')
            ####
            self.wait_loading.wait_for_popup_loading_finish()
            self.request_page.btn_next.click()
            self.wait_loading.wait_for_popup_loading_finish()

        with self.request_page.frm_catalog:
            self.assertTrue(
                self.request_page.cbo_hardware_island.exists(5),
                msg=_formatter(step='Display a hardware island dropdown list')
            )
            self.request_page.cbo_hardware_island.select(by_visible_text=self._local_cluster_hardware_island)
            self.wait_loading.wait_for_popup_loading_finish()

            self.assertTrue(
                self.request_page.cbo_unprepared_cluster.exists(5),
                msg=_formatter(step='Display an unprepared cluster dropdown list')
            )
            self.request_page.cbo_unprepared_cluster.select(by_visible_text=self._local_cluster_name)
            self.wait_loading.wait_for_popup_loading_finish()

            self.assertTrue(
                self.request_page.cbo_hardware_island_for_rp4vm.exists(5),
                msg=_formatter(step='Display a hardware island for rp4vm dropdown list')
            )
            self.request_page.cbo_hardware_island_for_rp4vm.select(
                by_visible_text=self._partner_cluster_hardware_island)
            self.wait_loading.wait_for_popup_loading_finish()

            self.assertTrue(
                self.request_page.cbo_partner_cluster_for_rp4vm.exists(5),
                msg=_formatter(step='Display a partner cluster for rp4vm dropdown list')
            )
            self.request_page.cbo_partner_cluster_for_rp4vm.select(by_visible_text=self._partner_cluster_name)
            self.wait_loading.wait_for_popup_loading_finish()

            self.request_page.btn_next.click()
            self.wait_loading.wait_for_popup_loading_finish()

    def _submit_request_local(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format
        with self.request_page.frm_catalog:
            self.assertTrue(self.request_page.btn_submit.exists(),
                            msg=_formatter(step='Click submit button'))
            self.request_page.btn_submit.click()
            self.wait_loading.wait_for_popup_loading_finish()

            self.assertTrue(self.request_page.lbl_success_msg.exists(),
                            msg='Failed to submit request')
            self.assertTrue(self.request_page.btn_ok.exists(),
                            msg='Failed to submit request')
            self.request_page.btn_ok.click()
            self._added_clusters = {
                'local_cluster': self._local_cluster_name,
                'partner_cluster_name': self._partner_cluster_name
            }

    def _submit_request_vsan(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format
        with self.request_page.frm_catalog:
            self.assertTrue(self.request_page.btn_submit.exists(),
                            msg=_formatter(step='Click submit button'))
            self.request_page.btn_submit.click()
            self.wait_loading.wait_for_popup_loading_finish()

            self.assertTrue(self.request_page.lbl_success_msg.exists(),
                            msg='Failed to submit request')
            self.assertTrue(self.request_page.btn_ok.exists(),
                            msg='Failed to submit request')
            self.request_page.btn_ok.click()
            self._added_clusters = {
                'vsan_cluster': self._vsan_cluster_name,
                'partner_vsan_cluster_name': self._partner_vsan_cluster_name
            }

    def _validate_input_args(self, **kwargs):
        self._description = self._testMethodName
        self._reason = self._testMethodName

        if self._testMethodName == self.Func.ONBOARD_LOCAL_CLUSTER:
            self.__validate_args_of_onboard_local_cluster(**kwargs)
        elif self._testMethodName == self.Func.ONBOARD_VSAN_CLUSTER:
            self.__validate_args_of_onboard_vsan_cluster(**kwargs)
        else:
            raise NotImplementedError('There is no this method')

    def _finalize_output_params(self):
        if self._testMethodName == self.Func.ONBOARD_LOCAL_CLUSTER:
            if self._added_clusters:
                self._output.append(self._added_clusters)
        elif self._testMethodName == self.Func.ONBOARD_VSAN_CLUSTER:
            if self._added_clusters:
                self._output.append(self._added_clusters)
        else:
            pass

    def __validate_args_of_onboard_local_cluster(self, **kwargs):
        self._local_cluster_hardware_island = kwargs.get('local_cluster_hardware_island')
        self._local_cluster_name = kwargs.get('local_cluster_name')
        self._partner_cluster_hardware_island = kwargs.get('partner_cluster_hardware_island')
        self._partner_cluster_name = kwargs.get('partner_cluster_name')
        self._browser = kwargs.get('cur_browser')

    def __validate_args_of_onboard_vsan_cluster(self, **kwargs):
        self._vsan_cluster_hardware_island = kwargs.get('vsan_cluster_hardware_island')
        self._vsan_cluster_name = kwargs.get('vsan_cluster_name')
        self._partner_vsan_cluster_hardware_island = kwargs.get('partner_vsan_cluster_hardware_island')
        self._partner_vsan_cluster_name = kwargs.get('partner_vsan_cluster_name')
        self._browser = kwargs.get('cur_browser')
