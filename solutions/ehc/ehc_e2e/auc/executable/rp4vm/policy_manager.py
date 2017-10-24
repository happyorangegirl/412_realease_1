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
from ehc_e2e.auc.uimap.shared.basepage import BasePage
from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.auc.reusable import (
    LoadingPopupWaiter, PageNavigator, RequestManager)
from ehc_e2e.auc.uimap.specific.rp4vm import CatalogPage, PolicyMaintenancePage


class PolicyManager(BaseUseCase):
    class Func(object):
        ADD_SYNC_POLICY, ADD_ASYNC_POLICY, DELETE_POLICY = (
            'test_adding_synchronous_policy',
            'test_adding_asynchronous_policy',
            'test_deleting_policy')

    def __init__(self, name=None, method_name=Func.ADD_SYNC_POLICY, **kwargs):
        super(PolicyManager, self).__init__(
            name, method_name, **kwargs)

    def setUp(self):
        self._request_page = PolicyMaintenancePage()
        self.wait_loading = LoadingPopupWaiter(
            self, browser=self._browser.instance._browser)

    def tearDown(self):
        RequestManager(self).save_unsubmitted_request()

    def test_adding_synchronous_policy(self):
        self._start_new_service_request()
        self._fill_out_request_info()
        self._add_sync_policy()
        self._submit_request()

    def test_adding_asynchronous_policy(self):
        self._start_new_service_request()
        self._fill_out_request_info()
        self._add_async_policy()
        self._submit_request()

    def test_deleting_policy(self):
        self._start_new_service_request()
        self._fill_out_request_info()
        self._delete_policy()
        self._submit_request()

    def _start_new_service_request(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        PageNavigator(self).go_to_catalog_page()

        _catalog_page = CatalogPage()

        self.wait_loading.wait_for_popup_loading_finish()

        with _catalog_page.frm_catalog:
            # _catalog_page.lnk_data_protection_services.click()
            _catalog_page.lnk_ehc_recoverpoint_for_vms.click()

            self.wait_loading.wait_for_popup_loading_finish()

            self.assertTrue(
                _catalog_page.btn_RP4VM_policy_maintenance_request.exists(),
                msg=_formatter(
                    step='Validate Request button of RP4VM Policy Maintenance')
            )
            _catalog_page.btn_RP4VM_policy_maintenance_request.click()

    def _fill_out_request_info(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        with self._request_page.frm_catalog:
            self.wait_loading.wait_for_popup_loading_finish()
            self.assertTrue(
                self._request_page.txt_description.exists(),
                msg=_formatter(step='Display Description text box')
            )

            self._request_page.txt_description.set(self.policy_info['description'])
            self._request_page.txt_reasons.set(self.policy_info['description'])
            self.wait_loading.wait_for_popup_loading_finish()
            self._request_page.btn_next.click()

            self.assertTrue(
                self._request_page.cbo_operation.exists(),
                msg=_formatter(step='Display Operation dropdown list'))

    def _submit_request(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        with self._request_page.frm_catalog:
            self.wait_loading.wait_for_popup_loading_finish()
            self.assertTrue(self._request_page.btn_submit.exists(),
                            msg=_formatter(step='Click submit button'))
            self._request_page.btn_submit.click()

        with self._request_page.frm_catalog:
            self.wait_loading.wait_for_popup_loading_finish()
            self.assertTrue(self._request_page.lbl_success_msg.exists(),
                            msg='Failed to submit request')
            self._request_page.btn_ok.click()

    def _add_sync_policy(self):
        _formatter = 'Running on step: "Add Synchronous Policy" - FAILED, {step}'.format
        with self._request_page.frm_catalog:
            self.wait_loading.wait_for_popup_loading_finish()
            self._request_page.cbo_operation.select(by_visible_text='Add Synchronous Policy')
            self.wait_loading.wait_for_popup_loading_finish()
            self.assertTrue(self._request_page.btn_next.exists(),
                            msg=_formatter(step='cannot find "Next" button after selecting Action.'))
            self._request_page.btn_next.click()

            self.assertTrue(self._request_page.txt_sync_policy_name.exists(),
                            msg=_formatter(step='cannot find input box of policy name.'))
            self._request_page.txt_sync_policy_name.set(self.policy_info['policy_name'])
            self.wait_loading.wait_for_popup_loading_finish()
            logger.debug('Set policy name: {}'.format(self.policy_info['policy_name']))
            self.assertTrue(self._request_page.txt_sync_journal_size.exists(),
                            msg=_formatter(step='cannot find input box of journal size.'))
            self._request_page.txt_sync_journal_size.set('')
            self.wait_loading.wait_for_popup_loading_finish()
            self._request_page.txt_sync_journal_size.set(self.policy_info['journal_size'])
            self.wait_loading.wait_for_popup_loading_finish()
            logger.debug('Set Journal Size: {}'.format(self.policy_info['journal_size']))
            self.assertTrue(self._request_page.btn_next.exists(),
                            msg=_formatter(step='cannot find "Next" button.'))
            self._request_page.btn_next.click()

    def _add_async_policy(self):
        _formatter = 'Running on step: "Add ASynchronous Policy" - FAILED, {step}'.format
        with self._request_page.frm_catalog:
            self.wait_loading.wait_for_popup_loading_finish()
            self._request_page.cbo_operation.select(by_visible_text='Add Asynchronous Policy')
            self.wait_loading.wait_for_popup_loading_finish()
            self.assertTrue(self._request_page.btn_next.exists(),
                            msg=_formatter(step='Cannot find "Next" button after selecting Action.'))
            self._request_page.btn_next.click()
            self.assertTrue(self._request_page.txt_async_policy_name.exists(),
                            msg=_formatter(step='cannot find input box of policy name.'))
            self._request_page.txt_async_policy_name.set(self.policy_info['policy_name'])
            self.wait_loading.wait_for_popup_loading_finish()
            logger.debug('Set policy name: {}'.format(self.policy_info['policy_name']))
            self.assertTrue(self._request_page.txt_async_journal_size.exists(),
                            msg=_formatter(step='cannot find input box of journal size.'))
            self._request_page.txt_async_journal_size.activate()
            self.wait_loading.wait_for_popup_loading_finish()
            self._request_page.txt_async_journal_size.set(self.policy_info['journal_size'])
            self.wait_loading.wait_for_popup_loading_finish()
            logger.debug('Set Journal Size: {}'.format(self.policy_info['journal_size']))

            # open dropdownlist for rp unites and then select from that dpdlst.
            # self.assertTrue(
            #     self._request_page.btn_rp_units_open.exists(),
            #     msg=_formatter(step='drop-down list open button for RPO Unit does not exist.')
            # )
            # self._request_page.btn_rp_units_open.click()
            # logger.info('clicked rp units drop downlist open button.', False, True)
            # self.assertTrue(
            #     BasePage().click_drop_down_list(
            #             self._request_page.lnk_rp_units_dropdown, tag_name='tr',
            #         item_to_select=self.policy_info['rpo_units']), msg=_formatter(
            #         step='select RPO Unit:"{}" failed.'.format(self.policy_info['rpo_units']))
            # )
            self.assertTrue(self._request_page.cbo_rp_units.exists(),
                            msg=_formatter(step='cannot find drop-down box of RPO Unit.'))
            self._request_page.cbo_rp_units.select(by_visible_text=self.policy_info['rpo_units'])


            self.wait_loading.wait_for_popup_loading_finish()
            self.assertTrue(self._request_page.txt_rp_number.exists(),
                            msg=_formatter(step='cannot find input box of RPO Unit Count.'))
            self._request_page.txt_rp_number.set(self.policy_info['rpo_number'])
            logger.debug('Set RPO Unit Count: {}'.format(self.policy_info['rpo_number']))
            self.assertTrue(self._request_page.btn_next.exists(),
                            msg=_formatter(step='cannot find "Next" button.'))
            self._request_page.btn_next.click()

    def _delete_policy(self):
        _formatter = 'Running on step: "{step}" - FAILED'.format
        with self._request_page.frm_catalog:
            self.wait_loading.wait_for_popup_loading_finish()
            self._request_page.cbo_operation.select(by_visible_text='Delete Policy')
            self.wait_loading.wait_for_popup_loading_finish()
            self.assertTrue(self._request_page.btn_next.exists(),
                            msg=_formatter(step='cannot find "Next" button.'))
            BasePage.send_tab_key(self._request_page.btn_next)
            self.wait_loading.wait_for_popup_loading_finish()
            self._request_page.btn_next.click()
            self.assertTrue(self._request_page.cbo_policy_to_delete.exists(60),
                            msg=_formatter(step='Display policy name'))

            self._request_page.cbo_policy_to_delete.select(by_visible_text=self.policy_info['policy_name'])
            self.wait_loading.wait_for_popup_loading_finish()
            self._request_page.cbo_delete_confirm.select(by_visible_text='Confirm')
            self.wait_loading.wait_for_popup_loading_finish()
            self.assertTrue(self._request_page.btn_next.exists(),
                            msg=_formatter(step='cannot find "Next" button.'))
            self._request_page.btn_next.click()

    def _validate_input_args(self, **kwargs):
        if self._testMethodName in [self.Func.ADD_ASYNC_POLICY, self.Func.ADD_SYNC_POLICY]:
            self.__validate_args_of_adding_policy(**kwargs)
        elif self._testMethodName == self.Func.DELETE_POLICY:
            self._validate_args_of_deleting_policy(**kwargs)
        else:
            raise NotImplementedError('Validate method %s '.format(**kwargs))

    def __validate_args_of_adding_policy(self, browser=None, **policy_info):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        self.assertIsNotNone(policy_info, msg=_formatter(step='Validate policy info'))
        self.policy_info = policy_info
        self._browser = browser

    def _validate_args_of_deleting_policy(self, browser=None, **policy_info):
        _formatter = 'Running on step: "{step}" - FAILED'.format

        self.assertIsNotNone(policy_info, msg=_formatter(step='Validate policy info'))
        self.policy_info = policy_info
        self._browser = browser