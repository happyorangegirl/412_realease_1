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
from ehc_e2e.auc.reusable import LoadingPopupWaiter
from ehc_e2e.auc.reusable import PageNavigator
from ehc_e2e.auc.reusable import RequestManager
from ehc_e2e.auc.uimap.specific.rp4vm import CatalogPage
from ehc_e2e.auc.uimap.specific.rp4vm import vRPAClusterMaintenancePage


class VRPAClustersManager(BaseUseCase):
    class Func(object):
        ADD_CLUSTER, DELETE_CLUSTER = (
            'test_adding_vRPA_cluster',
            'test_deleting_vRPA_cluster')

    def __init__(self, name=None, method_name=Func.ADD_CLUSTER, **kwargs):
        super(VRPAClustersManager, self).__init__(
            name, method_name, **kwargs)
        self._created_vRPA_clusters = None

    def setUp(self):
        self.navigator = PageNavigator(self)
        self._request_page = vRPAClusterMaintenancePage()
        self.wait_loading = LoadingPopupWaiter(
            self, browser=self._browser.instance._browser)

    def tearDown(self):
        RequestManager(self).save_unsubmitted_request()

    def test_adding_vRPA_cluster(self):
        self._start_new_service_request()
        self._fill_out_request_info()
        self._add_vRPA_cluster()
        self._submit_request()

    def test_deleting_vRPA_cluster(self):
        self._start_new_service_request()
        self._fill_out_request_info()
        self._delete_vRPA_cluster()
        self._submit_request()

    def _start_new_service_request(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        self.navigator.go_to_catalog_page()
        time.sleep(2)

        _catalog_page = CatalogPage()

        with _catalog_page.frm_catalog:
            self.assertTrue(
                _catalog_page.lnk_ehc_recoverpoint_for_vms.exists(),
                msg=_formatter(
                    step='Validate side bar button EHC RecoverPoint for VMs'
                ))

            _catalog_page.lnk_ehc_recoverpoint_for_vms.click()
            self.assertTrue(
                _catalog_page.btn_RP4VM_vRPA_cluster_maintenance_request.exists(),
                msg=_formatter(
                    step='Validate Request button of RP4VM vRPA Cluster Maintenance')
            )
            time.sleep(2)
            _catalog_page.btn_RP4VM_vRPA_cluster_maintenance_request.click()

    def _fill_out_request_info(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        with self._request_page.frm_catalog:
            self.assertTrue(
                self._request_page.txt_description.exists(60),
                msg=_formatter(step='Display Description text box')
            )

            self._request_page.txt_description.set(self._testMethodName)
            self._request_page.txt_reasons.set(self._name)

            self._request_page.btn_next.click()

        with self._request_page.frm_catalog:
            self.assertTrue(
                self._request_page.cbo_operation.exists(60),
                msg=_formatter(step='Display Operation dropdown list')
            )

    def _add_vRPA_cluster(self):

        with self._request_page.frm_catalog:
            self._request_page.cbo_operation.select(by_visible_text='Add vRPA Cluster Pair')
            self.wait_loading.wait_for_popup_loading_finish()
            self.assertTrue(
                self._request_page.btn_next.exists(60),
                msg="<Next> button doesn't exist after selecting <Add vRPA Cluster Pair>."
            )
            self._request_page.btn_next.click()
            self.assertTrue(
                self._request_page.txt_primary_cluster_ip.exists(60),
                msg="<Primary Cluster Manangement IP> input box doesn't exist."
            )
            self._request_page.txt_primary_cluster_ip.set(self._primary_cluster.get('management_ip'))
            self.wait_loading.wait_for_popup_loading_finish()
            self._request_page.txt_primary_cluster_admin.activate()
            self.wait_loading.wait_for_popup_loading_finish()
            self._request_page.txt_primary_cluster_admin.set(self._primary_cluster.get('admin_user'))
            self.wait_loading.wait_for_popup_loading_finish()
            self._request_page.txt_primary_cluster_password.activate()
            self.wait_loading.wait_for_popup_loading_finish()
            self._request_page.txt_primary_cluster_password.set(self._primary_cluster.get('admin_password'))
            self.wait_loading.wait_for_popup_loading_finish()
            self._request_page.txt_secondary_cluster_ip.activate()
            self.wait_loading.wait_for_popup_loading_finish()
            self._request_page.txt_secondary_cluster_ip.set(self._secondary_cluster.get('management_ip'))
            self._request_page.txt_secondary_cluster_admin.activate()
            self.wait_loading.wait_for_popup_loading_finish()
            self._request_page.txt_secondary_cluster_admin.set(self._secondary_cluster.get('admin_user'))
            self._request_page.txt_secondary_cluster_password.activate()
            self.wait_loading.wait_for_popup_loading_finish()
            self._request_page.txt_secondary_cluster_password.set(self._secondary_cluster.get('admin_password'))
            self.wait_loading.wait_for_popup_loading_finish()

            self.assertTrue(
                self._request_page.btn_next.exists(60),
                msg="<Next> button doesn't exist after filling tab <Add vRPA Cluster Pair>."
            )
            self._request_page.btn_next.click()

    def _delete_vRPA_cluster(self):
        with self._request_page.frm_catalog:
            self.wait_loading.wait_for_popup_loading_finish()
            self._request_page.cbo_operation.select(by_visible_text='Delete vRPA Cluster Pair')
            self.wait_loading.wait_for_popup_loading_finish()
            self.assertTrue(
                self._request_page.btn_next.exists(60),
                msg="<Next> button doesn't exist after selecting <Delete vRPA Cluster Pair>."
            )
            self._request_page.btn_next.click()
            self.assertTrue(
                self._request_page.cbo_primary_cluster_name.exists(60),
                msg="<Primary Cluster Name> dropdown list doesn't exist."
            )
            self._request_page.cbo_primary_cluster_name.select(by_visible_text=self._primary_cluster_name)
            self.wait_loading.wait_for_popup_loading_finish()
            self._request_page.cbo_confirm.select(by_visible_text='Confirm')
            self.wait_loading.wait_for_popup_loading_finish()
            self._request_page.btn_next.click()
            self.wait_loading.wait_for_popup_loading_finish()

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
            if self._testMethodName == self.Func.ADD_CLUSTER:
                self._created_vRPA_clusters = {
                    'primary_mgmt_ip': self._primary_cluster.get('management_ip'),
                    'secondary_mgmt_ip': self._secondary_cluster.get('management_ip')
                }

    def _validate_input_args(self, **kwargs):
        if self._testMethodName == self.Func.ADD_CLUSTER:
            self._validate_args_of_adding_vRPA_cluster(**kwargs)
        elif self._testMethodName == self.Func.DELETE_CLUSTER:
            self._validate_args_of_deleting_vRPA_cluster(**kwargs)
        else:
            pass

    def _finalize_output_params(self):
        if self._testMethodName == self.Func.ADD_CLUSTER:
            if self._created_vRPA_clusters:
                self._output.append(self._created_vRPA_clusters)
        else:
            pass

    def _validate_args_of_adding_vRPA_cluster(self, primary_cluster, secondary_cluster, browser=None, output=None):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        def __validate_vRPA_cluster_info_dict(cluster_dict):
            self.assertTrue((cluster_dict and
                             isinstance(cluster_dict, dict) and
                             sorted(cluster_dict.keys()) == ['admin_password', 'admin_user', 'management_ip']),
                            msg=_formatter(step='Validate vRPA cluster info dict'))

            for value in cluster_dict.itervalues():
                self.assertTrue((value and (
                    isinstance(value, basestring)) and value.strip() != ''),
                                msg=_formatter(step='Validate cluster info'))

        __validate_vRPA_cluster_info_dict(primary_cluster)
        __validate_vRPA_cluster_info_dict(secondary_cluster)

        self._primary_cluster = primary_cluster
        self._secondary_cluster = secondary_cluster
        self._browser = browser

    def _validate_args_of_deleting_vRPA_cluster(self, primary_clusert_name, browser=None):
        _formatter = 'Running on step: "{step}" - FAILED'.format
        self._browser = browser
        self.assertTrue((primary_clusert_name and
                         (isinstance(primary_clusert_name, basestring)) and
                         primary_clusert_name.strip() != ''),
                        msg=_formatter(step='Validate cluster info'))
        self._primary_cluster_name = primary_clusert_name
