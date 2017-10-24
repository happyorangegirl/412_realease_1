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
from ehc_e2e.auc.uimap.specific.rp4vm import CatalogPage, vCenterRelationshipMaintenancePage


class VCenterRelationshipManager(BaseUseCase):
    class Func(object):
        ADD_RELATIONSHIP, DELETE_RELATIONSHIP = (
            'test_adding_vCenter_relationship',
            'test_deleting_vCenter_relationship')

    def __init__(self, name=None, method_name=Func.ADD_RELATIONSHIP, **kwargs):
        super(VCenterRelationshipManager, self).__init__(
            name, method_name, **kwargs)
        self._related_vcenters = None

    def setUp(self):
        self._request_page = vCenterRelationshipMaintenancePage()
        self.wait_loading = LoadingPopupWaiter(
            self, browser=self._browser.instance._browser)

    def tearDown(self):
        RequestManager(self).save_unsubmitted_request()

    def test_adding_vCenter_relationship(self):
        self._start_new_service_request()
        self._fill_out_request_info()
        self._add_rp4vm_vcenter_relationship()
        self._review_input_info()
        self._submit_request()

    def test_deleting_vCenter_relationship(self):
        self._start_new_service_request()
        self._fill_out_request_info()
        self._delete_rp4vm_vcenter_relationship()
        self._review_input_info()
        self._submit_request()

    def _start_new_service_request(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        PageNavigator(self).go_to_catalog_page()
        import time
        time.sleep(2)

        _catalog_page = CatalogPage()

        with _catalog_page.frm_catalog:
            _catalog_page.lnk_ehc_configuration.click()

            self.assertTrue(
                _catalog_page.btn_vcenter_relationship_request.exists(),
                msg=_formatter(
                    step='Validate Request button of vCenter Relationship Maintenance')
            )

            _catalog_page.btn_vcenter_relationship_request.click()

    def _fill_out_request_info(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        # fulfill request information tab
        with self._request_page.frm_catalog:
            self.assertTrue(
                self._request_page.txt_description.exists(60),
                msg=_formatter(step='Display Description text box')
            )

            self._request_page.txt_description.set(self._testMethodName)
            self._request_page.txt_reasons.set(self._name)
            self._request_page.btn_next.click()

    def _add_rp4vm_vcenter_relationship(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        # select operation type
        with self._request_page.frm_catalog:
            self.assertTrue(
                self._request_page.cbo_operation.exists(60),
                msg=_formatter(step='Display Operation dropdown list')
            )

            self._request_page.cbo_operation.select(
                by_visible_text='Add RP4VM vCenter Relationship')
            self.wait_loading.wait_for_popup_loading_finish()
            self._request_page.btn_next.click()

        # fulfill protected and recovery vcenter information
        with self._request_page.frm_catalog:
            self.assertTrue(
                self._request_page.cbo_protected_vcenter.exists(60),
                msg=_formatter(step='Display protected vCenter selection')
            )
            self._request_page.cbo_protected_vcenter.select(by_visible_text=self._protected_vcenter.get('vCenter_name'))
            self.wait_loading.wait_for_popup_loading_finish()
            self._request_page.txt_prorected_vcenter_username.set(self._protected_vcenter.get('vCenter_user'))
            self._request_page.txt_prorected_vcenter_pwd.set(self._protected_vcenter.get('vCenter_pwd'))

            self._request_page.cbo_recovery_vcenter.select(by_visible_text=self._recovery_vcenter.get('vCenter_name'))
            self.wait_loading.wait_for_popup_loading_finish()
            self._request_page.txt_recovery_vcenter_username.set(self._recovery_vcenter.get('vCenter_user'))
            self._request_page.txt_recovery_vcenter_pwd.set(self._recovery_vcenter.get('vCenter_pwd'))

            self._request_page.btn_next.click()

        # fulfill NSX manager configuration info
        with self._request_page.frm_catalog:
            self.assertTrue(
                self._request_page.cbo_NSX_available.exists(60),
                msg=_formatter(step='Display NSX available selection')
            )
            if self._NSX_available:
                self._request_page.cbo_NSX_available.select(by_visible_text='Yes')
                self.wait_loading.wait_for_popup_loading_finish()
                self._request_page.txt_protect_site_NSX_mgr_url.set(self._protected_NSX_mgr.get('mgr_url'))
                self._request_page.txt_protect_site_NSX_mgr_user.set(self._protected_NSX_mgr.get('mgr_user'))
                self._request_page.txt_protect_site_NSX_mgr_pwd.set(self._protected_NSX_mgr.get('mgr_pwd'))
                self._request_page.txt_recovery_site_NSX_mgr_url.set(self._recovery_NSX_mgr.get('mgr_url'))
                self._request_page.txt_recovery_site_NSX_mgr_user.set(self._recovery_NSX_mgr.get('mgr_user'))
                self._request_page.txt_recovery_site_NSX_mgr_pwd.set(self._recovery_NSX_mgr.get('mgr_pwd'))

            else:
                self._request_page.cbo_NSX_available.select(by_visible_text='No')
                self.wait_loading.wait_for_popup_loading_finish()

            self._request_page.btn_next.click()

    def _delete_rp4vm_vcenter_relationship(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        # select operation type
        with self._request_page.frm_catalog:
            self.assertTrue(
                self._request_page.cbo_operation.exists(60),
                msg=_formatter(step='Display Operation dropdown list')
            )

            self._request_page.cbo_operation.select(
                by_visible_text='Delete vCenter Relationship')
            self.wait_loading.wait_for_popup_loading_finish()
            self._request_page.btn_next.click()

            # fulfill protected and recovery vcenter information
        with self._request_page.frm_catalog:
            self.assertTrue(
                self._request_page.cbo_protected_vcenter.exists(60),
                msg=_formatter(step='Display protected vCenter selection')
            )
            self._request_page.cbo_protected_vcenter.select(
                by_visible_text=self._protected_vcenter.get('vCenter_name'))
            self.wait_loading.wait_for_popup_loading_finish()
            self._request_page.cbo_recovery_vcenter.select(
                by_visible_text=self._recovery_vcenter.get('vCenter_name'))
            self.wait_loading.wait_for_popup_loading_finish()
            self.assertTrue(
                self._request_page.cbo_confirm_vcenter_relationship.exists(60),
                msg=_formatter(step='Confirm dropdown not exists')
            )
            self._request_page.cbo_confirm_vcenter_relationship.select(
                by_visible_text='Confirm')
            self.wait_loading.wait_for_popup_loading_finish()

            self._request_page.btn_next.click()

    def _review_input_info(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        exp_operation_type = None
        if self._testMethodName == self.Func.ADD_RELATIONSHIP:
            exp_operation_type = 'Add RP4VM vCenter Relationship'
        elif self._testMethodName == self.Func.DELETE_RELATIONSHIP:
            exp_operation_type = 'Delete vCenter Relationship'

        with self._request_page.frm_catalog:
            self.assertTrue(
                self._request_page.lbl_operation_type.exists(60),
                msg=_formatter(step='Display the selected operation in review tab')
            )
            str_operation_type = self._request_page.lbl_operation_type.value
            self.assertEqual(str_operation_type.strip(), exp_operation_type,
                             msg=_formatter(step='Validate selected operation in review tab'))
            str_protected_vcenter = self._request_page.lbl_protected_vcenter_name.value
            self.assertEqual(str_protected_vcenter.strip(),
                             self._protected_vcenter.get('vCenter_name'),
                             msg=_formatter(step='Validate the input of protected vCenter name'))
            str_recovery_vcenter = self._request_page.lbl_recovery_vcenter_name.value
            self.assertEqual(str_recovery_vcenter.strip(),
                             self._recovery_vcenter.get('vCenter_name'),
                             msg=_formatter(step='Validate the input of recovery vCenter name'))

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
            if self._testMethodName == self.Func.ADD_RELATIONSHIP:
                self._related_vcenters = {
                    'protected_vcenter': self._protected_vcenter.get('vCenter_name'),
                    'recovery_vcenter': self._recovery_vcenter.get('vCenter_name')
                }

    def _validate_input_args(self, **kwargs):
        if self._testMethodName == self.Func.ADD_RELATIONSHIP:
            self._validate_args_of_adding_relationship(**kwargs)
        elif self._testMethodName == self.Func.DELETE_RELATIONSHIP:
            self._validate_args_of_deleting_relationship(**kwargs)
        else:
            pass

    def _finalize_output_params(self):
        if self._testMethodName == self.Func.ADD_RELATIONSHIP:
            if self._related_vcenters:
                self._output.append(self._related_vcenters)
        else:
            pass

    def _validate_args_of_adding_relationship(self, protected_vcenter, recovery_vcenter, NSX_available,
                                              protected_nsx_mgr=None, recovery_nsx_mgr=None,
                                              browser=None, output=None):

        _formatter = 'Running on step: "{step}" - FAILED'.format

        def _validate_info_dict(dict_info, sorted_keys):
            self.assertTrue((dict_info and
                             isinstance(dict_info, dict) and
                             (sorted(dict_info.keys()) == sorted_keys)),
                            msg=_formatter(step='Validate vCenter info dict'))

            for value in dict_info.itervalues():
                self.assertTrue((value and (
                    isinstance(value, basestring)) and
                                 value.strip() != ''),
                                msg=_formatter(step='Validate cluster info'))

        keys = ['vCenter_name', 'vCenter_pwd', 'vCenter_user']
        _validate_info_dict(protected_vcenter, keys)
        _validate_info_dict(recovery_vcenter, keys)
        self.assertIn(NSX_available, [True, False],
                      msg=_formatter(step='Input NSX_available should be a boolean'))

        if NSX_available:
            keys = ['mgr_pwd', 'mgr_url', 'mgr_user']
            _validate_info_dict(protected_nsx_mgr, keys)
            _validate_info_dict(recovery_nsx_mgr, keys)

        self._protected_vcenter = protected_vcenter
        self._recovery_vcenter = recovery_vcenter
        self._NSX_available = NSX_available
        self._protected_NSX_mgr = protected_nsx_mgr
        self._recovery_NSX_mgr = recovery_nsx_mgr
        self._browser = browser

    def _validate_args_of_deleting_relationship(self, protected_vcenter, recovery_vcenter, browser=None):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        self.assertTrue((protected_vcenter and (
            isinstance(protected_vcenter, dict)) and
                         protected_vcenter.get('vCenter_name')),
                        msg=_formatter(step='Validate protected_vcenter_name'))
        self.assertTrue((protected_vcenter and (
            isinstance(protected_vcenter, dict)) and
                         protected_vcenter.get('vCenter_name')),
                        msg=_formatter(step='Validate recovery_vcenter_name'))

        self._protected_vcenter = protected_vcenter
        self._recovery_vcenter = recovery_vcenter
        self._browser = browser
