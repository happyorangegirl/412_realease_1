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
import sys
from robot.api import logger
from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.auc.reusable import LoadingPopupWaiter
from ehc_e2e.auc.reusable import PageNavigator
from ehc_e2e.auc.uimap.specific.srm import CatalogPage
from ehc_e2e.auc.uimap.specific.srm import PostFailoverUpdaterPage, DRRemediatorPage
from ehc_e2e.auc.uimap.specific.srm import PrepareSRMDPFailoverPage
from ehc_e2e.auc.uimap.shared.loadingwindow import LoadingWindow
from ehc_e2e.auc.uimap.shared.basepage import BasePage
from ehc_e2e.auc.uimap.shared.requestspage import RequestsPage
from .srm_client import SrmClient


class SRMDRMigrationManager(BaseUseCase):
    class Func(object):
        PREPARE, VALIDATE_PROTECTION, RECOVER, REPROTECT, REMEDIATE_MANAGEMENT = (
            'test_prepare_for_srm_dp_failover',
            'test_validates_protection_for_srm_dr_workloads',
            'test_srm_dr_recovery',
            'test_srm_dr_reprotect',
            'test_remediate_manages_srm_dr_protected_workloads')

    def __init__(self, name=None, method_name=Func.PREPARE, **kwargs):
        super(SRMDRMigrationManager, self).__init__(
            name, method_name, **kwargs)
        self._load_window = LoadingWindow()
        self._base_page = BasePage()
        _auc_name = ' '.join([word.capitalize() for word in name.split('_')])
        self._formatter = ('Running on: ' + _auc_name + ' - FAILED, "{step}"').format

    def setUp(self):
        if self._testMethodName in (
                SRMDRMigrationManager.Func.RECOVER,
                SRMDRMigrationManager.Func.REPROTECT):
            pass
        else:
            if hasattr(self, '_browser') and self._browser:
                self.wait_loading = LoadingPopupWaiter(
                    self, browser=self._browser.instance._browser)
            else:
                self.wait_loading = LoadingPopupWaiter(
                    self, browser=None)

    def test_prepare_for_srm_dp_failover(self):
        try:
            self._start_prepare_for_srm_dp_failover_request()
            self._fill_out_request_info()
            self._select_protected_cluster()
            self._submit_request()
        except AssertionError:
            self._handle_assert_exception()
            raise
        except:
            ex = sys.exc_info()
            self._handle_other_exception(ex)

    def test_validates_protection_for_srm_dr_workloads(self):
        try:
            self._start_validates_protection_for_srm_dr_workloads_request()
            self._fill_out_request_info()
            self._select_protected_cluster()
            self._choose_datastores_to_protect()
            self._choose_vms_to_protect()
            self._submit_request()
        except AssertionError:
            self._handle_assert_exception()
            raise
        except:
            ex = sys.exc_info()
            self._handle_other_exception(ex)

    def test_srm_dr_recovery(self):
        recovery_plan_moref, recovery_srm_info = \
            self._get_recovery_plan_morefs()

        self._start_recovery_plan_in_specified_mode(
            moref=recovery_plan_moref,
            mode='migrate',
            **recovery_srm_info)

    def test_srm_dr_reprotect(self):
        recovery_plan_moref, recovery_srm_info = \
            self._get_recovery_plan_morefs()

        self._start_recovery_plan_in_specified_mode(
            moref=recovery_plan_moref,
            mode='reprotect',
            **recovery_srm_info)

        # after success reprotect ,fill result in to _output, the output in srmworkflow will be the flag to decide
        # whether exchange protected site, data center, cluster, srm local server with recovery site , data center,
        # cluster, srm remote server.
        self._output.append('Successful')

    def test_remediate_manages_srm_dr_protected_workloads(self):
        _round = 1
        while _round <= 20:
            try:
                self._start_remediate_manages_srm_dr_protected_workloads_request()
                self._fill_out_request_info()
                self._select_recovery_cluster()
                self._submit_request()
                request_result = self._get_request_result()
                if request_result.status == 'Successful':
                    logger.info(msg='In {round} round, the request successed, status: {status}, detail info: {detail}'.
                                format(round=_round, status=request_result.status,
                                       detail=request_result.status_details))
                    break
                else:
                    logger.error(msg='In {round} round, the request result status {status}, detail info: {detail}'.
                                 format(round=_round, status=request_result.status,
                                        detail=request_result.status_details))
                    _round += 1
            except AssertionError:
                self._handle_assert_exception()
                raise
            except:
                ex = sys.exc_info()
                self._handle_other_exception(ex)
        self.assertTrue(_round <= 20, msg='The request still failed after 20 rounds trying.')

    def _start_remediate_manages_srm_dr_protected_workloads_request(self):
        _catalog_page = CatalogPage()
        PageNavigator(self).go_to_catalog_page()
        with _catalog_page.frm_catalog:
            self.assertTrue(
                _catalog_page.lnk_data_protection_services.exists(),
                msg=self._formatter(step='cannot find Data Protection Services"'))
            _catalog_page.lnk_data_protection_services.click()

            self.assertTrue(
                _catalog_page.btn_dr_post_failover_updater_request.exists(),
                msg=self._formatter(step='cannot find Request button of '
                                         '"Remediate Management of SRM DR Protected Workloads"'))

            _catalog_page.btn_dr_post_failover_updater_request.click()

    def _start_prepare_for_srm_dp_failover_request(self):
        _catalog_page = CatalogPage()
        PageNavigator(self).go_to_catalog_page()
        with _catalog_page.frm_catalog:
            self.assertTrue(
                _catalog_page.lnk_data_protection_services.exists(),
                msg=self._formatter(step='cannot find Data Protection Services"'))
            _catalog_page.lnk_data_protection_services.click()

            self.assertTrue(
                _catalog_page.btn_prepare_for_srm_dp_failover_request.exists(),
                msg=self._formatter(step='cannot find Request button of "Prepare for SRM DP Failover"'))

            _catalog_page.btn_prepare_for_srm_dp_failover_request.click()

    def _start_validates_protection_for_srm_dr_workloads_request(self):
        _catalog_page = CatalogPage()
        PageNavigator(self).go_to_catalog_page()
        with _catalog_page.frm_catalog:
            self.assertTrue(
                _catalog_page.lnk_data_protection_services.exists(),
                msg=self._formatter(step='cannot find Data Protection Services"'))
            _catalog_page.lnk_data_protection_services.click()

            self.assertTrue(
                _catalog_page.btn_dr_remediator_request.exists(),
                msg=self._formatter(step='cannot find Request button of "Validate Protection for SRM DR Workloads"'))

            _catalog_page.btn_dr_remediator_request.click()

    def _fill_out_request_info(self):
        logger.info(msg='Start to fill items in the Request information tab')
        with self._request_page.frm_catalog:
            self._load_window.wait_loading(self._browser)
            self.assertTrue(
                self._request_page.txt_description.exists(),
                msg=self._formatter(step='cannot find Description text box'))

            self._request_page.txt_description.set(self._testMethodName)
            self._request_page.txt_reasons.set(self._name)
            logger.info(msg='set description : {}'.format(self._testMethodName))
            self._request_page.btn_next.click()

        logger.info(msg='Finish fill the Request information tab.')

    def _submit_request(self):
        with self._request_page.frm_catalog:
            self.assertTrue(self._request_page.btn_submit.exists(),
                            msg=self._formatter(step='cannot find Submit button'))

            self._request_page.btn_submit.click()
            logger.info(msg='Clicked Submit button.')

        with self._request_page.frm_catalog:
            self.assertTrue(self._request_page.lbl_success_msg.exists(),
                            msg=self._formatter(step='failed to find "The request has been submitted successfully." '
                                                     'after submit request'))
            self._request_page.btn_ok.click()

    def _get_request_result(self):
        # switch to request
        self.assertTrue(
            RequestsPage().navigate_to_request(self._browser),
            msg=self._formatter(step='switch to request frame failed.'))

        req_result = RequestsPage().get_request_result(self._testMethodName, slp=60)
        self.assertIsNotNone(req_result,
                             msg=self._formatter(step='failed to get the request result.'))
        return req_result

    def _select_recovery_cluster(self):
        with self._request_page.frm_catalog:
            self._load_window.wait_loading(self._browser)
            self.assertTrue(self._request_page.cbo_recovery_cluster.exists(),
                            msg=self._formatter(step='cannot find Recovery Cluster Combobox'))

            self._request_page.cbo_recovery_cluster.select(by_visible_text=self._recovery_cluster)
            self._request_page.txt_email.set(self._email)
            self._base_page.wait_for_loading_complete(wait_time=2)
            self._request_page.btn_next.click()

    def _select_protected_cluster(self):
        logger.info(msg='Start to fill items in the Prepare Avamar for SRM DR Failover tab')
        with self._request_page.frm_catalog:
            self.assertTrue(self._request_page.cbo_protected_cluster.exists(),
                            msg=self._formatter(step='cannot find Protected Cluster Combobox'))

            self._request_page.cbo_protected_cluster.select(by_visible_text=self._protected_cluster)
            logger.info(msg='Selected Protected cluster: {}'.format(self._protected_cluster))
            self.wait_loading.wait_for_popup_loading_finish()
            self._base_page.wait_for_loading_complete(wait_time=2)
            self._request_page.btn_next.click()

        logger.info(msg='Finish fill items in the Prepare Avamar for SRM DR Failover tab')

    def _choose_datastores_to_protect(self):
        with self._request_page.frm_catalog:
            self.assertTrue(self._request_page.lst_unprotected_datastores.exists(),
                            msg=self._formatter(step='cannot find Unprotected Datastore List Box'))
            if self._datastore_list == 'select all':
                self._request_page.chk_protect_all_datastores.tick()
            else:
                # Choose datastore workflow create to protect,
                # if not find the datastore in DropDownList individual datastores to protect,
                # No datastore need to choose for this workflow, so untick protect all datastores checkbox

                self._request_page.chk_protect_all_datastores.untick()
                _checkbox_list = self._request_page.get_datastores_checkbox_list()
                for item in _checkbox_list:
                    item.tick()
                    self.wait_loading.wait_for_popup_loading_finish()
            self._base_page.wait_for_loading_complete(wait_time=2)
            self._request_page.btn_next.click()

    def _choose_vms_to_protect(self):
        with self._request_page.frm_catalog:
            self.assertTrue(self._request_page.lst_unprotected_vms.exists(),
                            msg=self._formatter(step='cannot find Unprotected Virtual Machine List Box'))
            if self._vm_list == 'select all':
                self._request_page.chk_protect_all_vms.tick()
            else:
                self._request_page.chk_protect_all_vms.untick()
                _checkbox_list = self._request_page.get_vms_checkbox_list()
                for item in _checkbox_list:
                    item.tick()
                    self.wait_loading.wait_for_popup_loading_finish()
            self._base_page.wait_for_loading_complete(wait_time=2)
            self._request_page.btn_next.click()

    def _get_recovery_plan_morefs(self):
        recovery_srm_info = self.recovery_srm_info

        with SrmClient(**recovery_srm_info) as proxy:
            plans = proxy.get_recovery_plans()
            self.assertTrue(plans, msg=self._formatter(step='there is no recovery plan or get recovery plans failed.'))

            self.assertTrue(self.recovery_plan_name in plans,
                            msg=self._formatter(step='there is no recovery plan: {0}, all the recovery plans are: {1}'.
                                                format(self.recovery_plan_name, plans)))

            recovery_plan_moref = plans[self.recovery_plan_name].get('moref')
            state = plans[self.recovery_plan_name].get('state')
            logger.info(msg='the initial state of recovery plan {0} is {1}'.format(self.recovery_plan_name, state))

            if state != 'ready':
                recovery_plan_moref = proxy.get_peer_recovery_plan(recovery_plan_moref)
                recovery_srm_info = self.protected_srm_info

        return recovery_plan_moref, recovery_srm_info

    def _start_recovery_plan_in_specified_mode(
            self, hostname, username, password, moref, mode):
        with SrmClient(hostname, username, password) as proxy:
            # self.assertEqual(
            #     proxy.get_recovery_state_of_recovery_plan(moref), 'ready',
            #     msg=_formatter(step='Validate the status of the recovery plan'))

            _msg = 'Performing "{}" action on recovery plan: "{}" ...' \
                   ' \nDirection: {} -> {}'.format(mode,
                                                   self.recovery_plan_name,
                                                   proxy.get_paired_site_name(),
                                                   proxy.get_site_name())
            logger.info(_msg, False, True)

            self.assertTrue(proxy.start(moref, mode), msg=self._formatter(step='post {} request failed.'.format(mode)))
            time.sleep(5)
            timeout_in_sec = 30*60
            _now = time.time()
            _state_of_recovery_plan = proxy.get_recovery_state_of_recovery_plan(moref)
            self.assertTrue(_state_of_recovery_plan != 'unknown',
                            msg=self._formatter(step='failed to get state of {0} result'.format(mode)))
            logger.info(msg='The state after request of {0} is {1}'.format(mode, _state_of_recovery_plan))
            while (_state_of_recovery_plan == 'running') and (
                    timeout_in_sec > (time.time() - _now)):
                if proxy.get_recovery_state_of_recovery_plan(moref) in (
                        'cancelling', 'error', 'prompting'):
                    self.fail(msg=self._formatter(step='performing Recovery action - {} was failed.'.format(mode)))

                time.sleep(60)
                _state_of_recovery_plan = proxy.get_recovery_state_of_recovery_plan(moref)
                logger.info(msg='The state after request of {0} is {1}'.format(mode, _state_of_recovery_plan))

            self.assertNotIn(
                proxy.get_recovery_state_of_recovery_plan(moref),
                ('cancelling', 'error', 'prompting'),
                msg=self._formatter(step='performing Recovery action - {} was failed.'.format(mode)))

            _latest_results = proxy.get_recovery_result(moref)
            self.assertTrue(len(_latest_results) > 0, msg='No history result get.')
            # the last result will be the first.
            _latest_result = _latest_results[0]
            #  failover have two types: failover and migrate.
            mode = 'failover' if mode == 'migrate' else mode
            self.assertEqual(
                mode, _latest_result.get('runMode'),
                msg=self._formatter(
                    step='recovery history mode: {0}, not {1}'.format(_latest_result.get('runMode'), mode)))
            self.assertEqual(
                'success', _latest_result.get('resultState'),
                msg=self._formatter(
                    step='recovery history state: {0},not {1}'.format(_latest_result.get('resultState'), 'success')))

    def _validate_input_args(self, **kwargs):
        if self._testMethodName == self.Func.PREPARE:
            self.__validate_args_of_prepare_for_srm_dp_failover(**kwargs)

            self._request_page = PrepareSRMDPFailoverPage()
        elif self._testMethodName == self.Func.REMEDIATE_MANAGEMENT:
            self.__validate_args_of_post_failover_updater(**kwargs)

            self._request_page = PostFailoverUpdaterPage()
        elif self._testMethodName == self.Func.VALIDATE_PROTECTION:
            self.__validate_args_of_dr_remediator(**kwargs)
        elif self._testMethodName in (self.Func.RECOVER, self.Func.REPROTECT):
            self.__validate_args_of_dr_recovery(**kwargs)
        else:
            raise ValueError('Unsupported test method')

    def __validate_args_of_post_failover_updater(self, browser, recovery_cluster, email_address):
        self.assertIsNotNone(
            recovery_cluster,
            msg=self._formatter(step='Recovery Cluster Name is None'))
        _email_format = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        self.assertRegexpMatches(
            email_address,
            _email_format,
            msg=self._formatter(step='Email Address do not conform the format: {0}'.format(_email_format)))

        self._recovery_cluster = recovery_cluster
        self._email = email_address
        self._browser = browser

    def __validate_args_of_dr_recovery(
            self, local_srm_hostname, username, password,
            remote_srm_hostname, remote_username, remote_password,
            recovery_plan_name
    ):
        self.assertIsNotNone(
            local_srm_hostname,
            msg=self._formatter(step='local SRM Server is None'))

        self.assertIsNotNone(
            username,
            msg=self._formatter(step='local username is None'))

        self.recovery_srm_info = {
            'hostname': local_srm_hostname,
            'username': username,
            'password': password}

        self.assertIsNotNone(
            remote_srm_hostname,
            msg=self._formatter(step='remote SRM Server is None'))

        self.assertIsNotNone(
            remote_username,
            msg=self._formatter(step='remote username is None'))

        self.protected_srm_info = {
            'hostname': remote_srm_hostname,
            'username': remote_username,
            'password': remote_password}

        self.assertIsNotNone(
            recovery_plan_name,
            msg=self._formatter(step='recovery plan is None'))

        self.recovery_plan_name = recovery_plan_name

    def __validate_args_of_dr_remediator(
            self, protected_cluster, browser, datastore_list=None, vm_list=None):
        self._browser = browser
        self.assertTrue((protected_cluster and
                         (isinstance(protected_cluster, basestring)) and
                         (protected_cluster.strip() != '')),
                        msg=self._formatter(step='please provide protected cluster name'))
        self._protected_cluster = protected_cluster

        if datastore_list:
            self.assertTrue((datastore_list and (isinstance(datastore_list, list))),
                            msg=self._formatter(step='please provide datastores list to protect'))
            self._datastore_list = datastore_list
        else:
            self._datastore_list = 'select all'

        if vm_list:
            self.assertTrue((vm_list and (isinstance(vm_list, list))),
                            msg=self._formatter(step='please provide virtual machines list to protect'))
            self._vm_list = vm_list
        else:
            self._vm_list = 'select all'

        self._request_page = DRRemediatorPage(
            datastores_to_protect=datastore_list, vms_to_protect=vm_list)

    def __validate_args_of_prepare_for_srm_dp_failover(self, browser, protected_cluster):
        self._protected_cluster = protected_cluster
        self._browser = browser

    def _handle_assert_exception(self):
        self._base_page.save_request()

    def _handle_other_exception(self, err_message):
        self._base_page.save_request()
        self.fail(msg=self._formatter(step='encounters error in {0}, details error info: {1}'.
                                      format(self._testMethodName, err_message)))
