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

import sys
import re

from selenium.webdriver.common.keys import Keys
from robot.api import logger

from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.auc.uimap.shared import BasePage, CatalogPage, RequestsPage, LoadingWindow
from ehc_e2e.auc.uimap.specific import DeployVMPage, DeployVmRequestPage

from ehc_e2e.auc.reusable import context_util
from ehc_e2e.auc.reusable import close_relaunch_browser_operation


class DeployVM(BaseUseCase):
    """
        Test deploying VMs from blueprints
    """
    deployed_vms = []
    _formatter_without_dp = 'Running on step:"Deploy VM"- FAILED, {}.'
    _formatter_with_dp = 'Running on step:"Deploy VM with DP"- FAILED, {}.'
    _formatter = ''
    DEPLOYVM_DP_BACKUP_SVC_LEVEL_NAME_PATTERN = r'^deploy-.*?-\d{6}'

    def _init_page_objects(self):
        self.catalog_page = CatalogPage()
        self.base_page = BasePage()
        self.loading_window = LoadingWindow()
        self.deploy_vm_page = DeployVMPage()

    def open_deploy_vm_request(self, blueprint_name):
        self.assertTrue(
            self.catalog_page.navigate_to_catalog(self.current_browser),
            msg=self._formatter.format('switch to catalog page failed.'))

        self.assertTrue(
            self.catalog_page.txt_search.exists(),
            msg=self._formatter.format('Catalog service search button does not exist.'))
        self.catalog_page.txt_search.set(blueprint_name)
        logger.info(
            'Input: {0} in {1} search textbox'.format(
                blueprint_name, self.catalog_page.__class__.__name__))
        self.catalog_page.btn_search.click()
        logger.info(
            'Clicked search button in {} search textbox'.format(self.catalog_page.__class__.__name__))

        self.catalog_page.btn_blueprint_request = self.catalog_page.retrieve_blueprint_request_buttons(
            blueprint_name).get(blueprint_name)
        try:
            self.assertTrue(
                self.catalog_page.btn_blueprint_request.exists(), msg=self._formatter.format(
                    'request button does not exist for blueprint: {}'.format(blueprint_name)))
        except AssertionError:
            logger.info('Exit deploy vm since blueprint: {} is not found.'.format(blueprint_name), False, True)
            self.catalog_page.txt_search.set('')
            raise

        self.catalog_page.btn_blueprint_request.click()
        logger.info('Clicked request button in blueprint {}'.format(blueprint_name), False, True)

        # Benson: We have a commond loading window and a mask loading window after clicking
        # the deploy vm request from catalog page.

        self.loading_window.wait_loading(self.current_browser, timeout=60)
        self.loading_window.wait_loading_deploy_vm_page(self.current_browser, timeout=60)

    def test_deploy_vm(self):
        driver_ref = self.current_browser.instance._browser.current
        self._formatter = self._formatter_with_dp if self.with_dp else self._formatter_without_dp

        for blueprint_name in self.blueprint_names:
            self._init_page_objects()
            self.open_deploy_vm_request(blueprint_name)
            try:
                _is_switched_edit = self.deploy_vm_page.switch_to_edit_areas(
                    self.current_browser)
                if not _is_switched_edit:
                    logger.warn('Switch to deploy vm edit page failed, try to close and relaunch '
                                'browser for a second attempt.')
                    close_relaunch_browser_operation()
                    self.current_browser = \
                        context_util.get_last_baseworkflow_instance().wf_context.shared.current_browser
                    logger.info('Re-instantiating catalogpage, basepage and deployvmpage.', False, True)
                    self._init_page_objects()
                    driver_ref = self.current_browser.instance._browser.current
                    logger.info(
                        'Done re-instantiate catalogpage, basepage and deployvmpage.', False, True)
                    self.open_deploy_vm_request(blueprint_name)
                    _is_switched_edit = self.deploy_vm_page.switch_to_edit_areas(
                        self.current_browser)

                self.assertTrue(_is_switched_edit,
                                msg=self._formatter.format('switch to deploy vm edit page failed.'))

            except:
                logger.error(
                    'Encounters exception, exception details: {}'.format(
                        sys.exc_info()))
                raise

            try:
                # reason for request.
                if self.reason_for_request and self.deploy_vm_page.txt_reason_for_request.exists():
                    self.deploy_vm_page.txt_reason_for_request.set(
                        self.reason_for_request)
                    logger.info('Input: {} in description textbox'.format(
                        self.reason_for_request))

                # If set description after machines, the description textbox
                # reference will become stale.
                if self.deploy_vm_page.txt_desc.exists():
                    self.deploy_vm_page.txt_desc.set(self.description)
                    logger.info('Input: {} in description textbox'.format(
                        self.description))

                # Wenda: UI change in Badger. need to click machines button first then set the number of VMs
                self.assertTrue(
                    self.deploy_vm_page.open_vsphere_blueprint(self.blueprint_machine_pairs[blueprint_name]),
                    msg=self._formatter.format('failed to open designated vSphere blueprint')
                )

                self.assertTrue(self.deploy_vm_page.txt_instances.exists(),
                                msg=self._formatter.format('cannot find instances textbox'))
                # original clear method is not working here as expected.
                # if we don't "click" btn_num_machines_down
                # the input will start with default value 1.
                # This work around cleared the default value in machines.
                default_instances_num = int(
                    self.deploy_vm_page.txt_instances.current.get_attribute('value'))

                if self.num_of_vm != default_instances_num:
                    logger.info(
                        'num_of_vm provided in YAML is different with default value {0}. Use num_of_vm'.format(
                            default_instances_num))

                    self.assertTrue(
                        self.deploy_vm_page.txt_instances.current.get_attribute('readonly') != 'true',
                        msg=self._formatter.format(
                            'failed to deploy VMs. Cannot set number of instances, textbox is readonly')
                    )

                    self.deploy_vm_page.btn_instances_down.click()
                    self.deploy_vm_page.txt_instances.set(Keys.BACKSPACE)
                    self.deploy_vm_page.txt_instances.set(self.num_of_vm)
                    self.base_page.wait_for_loading_complete(1)

                    if self.deploy_vm_page.txt_instances.current.get_attribute('data-errorqtip'):
                        logger.error('Number of instances out of range..')
                        raise AssertionError('Failed to deploy VMs. Number of instances out of range')
                    logger.info(
                        'Set number of instances to: {}'.format(self.num_of_vm))

                else:
                    logger.info(
                        'num_of_vm provided in YAML is same with default value: {0}. No need to change..'.format(
                            default_instances_num))

                # set SRM priority
                if self.SRM_power_on_priority:
                    self.assertTrue(
                        self.deploy_vm_page.btn_srm_drop_down.exists(),
                        msg=self._formatter.format('cannot find SRM drop down list, '
                                                   'Remove SRM_power_on_priority value or field in YAML '
                                                   'if you do not need to set SRM priority'))
                    self.deploy_vm_page.btn_srm_drop_down.click()
                    self.assertTrue(
                        self.deploy_vm_page.click_drop_down_list(
                            self.deploy_vm_page.lbl_drop_down_list, 'li', str(self.SRM_power_on_priority)),
                        msg=self._formatter.format('failed to select SRM priority in the drop down list. '
                                                   'Please verify the value exists. '
                                                   'Remove SRM_power_on_priority value or field in YAML '
                                                   'if you do not need to set SRM priority'))

                # DP = True. set Backup Service Level
                if self.with_dp:
                    self.base_page.wait_for_loading_complete(5)
                    if self.browser_type == 'firefox':
                        # firefox has problem to select item of li type element in ul dropdownlist
                        # TODO: figure out a reliable solution later.
                        self.assertTrue(self.deploy_vm_page.btn_bkp_input.exists(),
                                        msg=self._formatter.format('backup service level textbox does not exist.'))
                        self.deploy_vm_page.btn_bkp_input.set(
                            self.backup_service_level)
                        logger.info(
                            'Finished setting backup service level: {}.'.format(
                                self.backup_service_level), False, True)
                    else:
                        self.assertTrue(
                            self.deploy_vm_page.btn_bkp_drop_down.exists(),
                            msg=self._formatter.format('cannot find Backup Service Level drop down list'))
                        self.deploy_vm_page.btn_bkp_drop_down.click()
                        self.assertTrue(
                            self.deploy_vm_page.click_drop_down_list(
                                self.deploy_vm_page.lbl_drop_down_list, 'li', self.backup_service_level),
                            msg=self._formatter.format(
                                'failed to select Backup Service Level in the drop down list. Please verify '
                                'if "{}" exists'.format(self.backup_service_level)))
                self.deploy_vm_page.wait_for_loading_complete(5)

                self.deploy_vm_page.switch_to_service_gadget_frame(
                    self.current_browser)
                self.assertTrue(
                    self.deploy_vm_page.btn_submit.exists(), msg=self._formatter.format('submit button does not exist'))

                self.deploy_vm_page.btn_submit.click()
                logger.info(
                    'Clicked submit button in blueprint {} request page.'.format(
                        blueprint_name))
            except AssertionError:
                logger.error('Deploy VM on blueprint {0} encounters error'
                             ', just save request.'.format(blueprint_name))
                self.deploy_vm_page.switch_to_service_gadget_frame(self.current_browser)
                self.deploy_vm_page.save_request()
                raise
            except:
                ex = sys.exc_info()
                logger.error('Deploy VM on blueprint {0} encounters error: {1}'
                             ', just save request.'.format(blueprint_name, ex))
                self.deploy_vm_page.switch_to_service_gadget_frame(
                    self.current_browser)
                self.deploy_vm_page.save_request()

                raise

            self.current_browser.instance._browser.current.implicitly_wait(10)

            if self.catalog_page.lbl_success.exists():
                self.catalog_page.btn_ok.click()
                logger.info('Clicked request successful OK button.')
            else:
                switched_edit_after_submit = self.deploy_vm_page.switch_to_edit_areas(self.current_browser)
                if switched_edit_after_submit:
                    logger.info(
                        'Trying to detect if the error label appears after submit successful label not found.',
                        False, True)
                    self.current_browser.instance._browser.current.implicitly_wait(2)
                    if self.deploy_vm_page.lbl_error_request_form.exists():
                        logger.error(
                            'Deploy vm request has some fields not set properly, submit button will not proceed.')
                    self.current_browser.instance._browser.current.implicitly_wait(30)
                from ehc_e2e.utils.snapshot import SnapShot
                SnapShot.takes_screen_shot()
                raise AssertionError(
                    self._formatter.format(
                        'submit button failed to proceed to "The request has been submitted successfully" page')
                )

            self.current_browser.instance._browser.current.implicitly_wait(30)

            try:
                # switch to request
                self.assertTrue(
                    RequestsPage().navigate_to_request(self.current_browser),
                    msg=self._formatter.format(
                        'switch to request frame failed'))
                # deploy vm request may take longer than usual
                # set the last timeout to 2h and let it wait 1 minute before the first time to get
                # request , then set the reflesh interval time to 5 minutes
                request_result = RequestsPage(self.current_browser.instance._browser.current).get_request_result(
                    self.description, timeout=7200, slp=300,
                    firstwaitduration=60)
                if not request_result:
                    logger.warn('First time getting request result failed, try to close and '
                                'relaunch browser for a second attempt.')
                    close_relaunch_browser_operation()
                    self.current_browser = \
                        context_util.get_last_baseworkflow_instance().wf_context.shared.current_browser
                    logger.info('Re-instantiating catalogpage, basepage and deployvmpage.', False, True)
                    self._init_page_objects()
                    driver_ref = self.current_browser.instance._browser.current
                    logger.info('Done re-instantiate catalogpage, basepage and deployvmpage.', False, True)
                    self.assertTrue(
                        RequestsPage().navigate_to_request(self.current_browser),
                        msg=self._formatter.format('switch to request frame failed'))

                    request_result = RequestsPage(self.current_browser.instance._browser.current).get_request_result(
                        self.description, timeout=7200, slp=300, firstwaitduration=60)
            except:
                logger.warn(
                    'First time getting request result encounters error:{}'.format(
                        sys.exc_info()))
                close_relaunch_browser_operation()
                self.current_browser = \
                    context_util.get_last_baseworkflow_instance().wf_context.shared.current_browser
                logger.info('Re-instantiating catalogpage, basepage and deployvmpage.', False, True)
                self._init_page_objects()
                driver_ref = self.current_browser.instance._browser.current
                logger.info('Done re-instantiate catalogpage, basepage and deployvmpage.', False, True)
                self.assertTrue(
                    RequestsPage().navigate_to_request(self.current_browser),
                    msg=self._formatter.format('switch to request frame failed')
                )
                request_result = RequestsPage(self.current_browser.instance._browser.current).get_request_result(
                    self.description, timeout=7200, slp=300, firstwaitduration=60)

            self.assertIsNotNone(
                request_result, msg=self._formatter.format('failed to get the request result')
            )
            logger.debug('Successful getting request result for deploy vm.')

            self.base_page.wait_for_loading_complete(3)

            request_title = driver_ref.find_element_by_xpath(
                '//td[@cellindex="0"]/div/a/b[text()="' + str(request_result.request) + '"]')

            self.assertIsNotNone(request_title, msg=self._formatter.format(
                'Request title for request id :"{}" not found.'.format(request_result.request)))
            request_title.click()
            logger.info('Clicked request title to open request details page.', False, True)
            LoadingWindow().wait_loading(current_browser=self.current_browser.instance._browser.current, timeout=30)

            deploy_vm_request_page = DeployVmRequestPage()
            self.deployed_vms = deploy_vm_request_page.get_deployed_vms()

            if len(self.deployed_vms) > 0:
                logger.info(
                    'Deploy VM succeeded, deployed VM(s): {}.'.format(
                        self.deployed_vms))
            else:
                logger.error(
                    'Deploy VM failed, no VM deployed. request status details: '
                    '{}'.format(request_result.status_details))

            self.assertTrue(len(self.deployed_vms) > 0,
                            msg=self._formatter.format('no VM deployed'))

    def runTest(self):
        self.test_deploy_vm()

    def _validate_context(self):
        assert self.ctx_in.blueprints is not None, self._formatter.format('blueprints should not be None')
        assert self.ctx_in.deploy_vm.description is not None, \
            self._formatter.format('description of blueprint should not be None')
        assert self.ctx_in.deploy_vm.number_of_vm is not None, \
            self._formatter.format('number of VMs to be deployed should not be None')
        assert int(self.ctx_in.deploy_vm.number_of_vm) > 0, \
            self._formatter.format('number of VMs to be deployed should be greater than 0')
        assert self.ctx_in.deploy_vm.with_dp is not None, \
            self._formatter.format('with_dp flag should be specified')

        # check blueprint_machine_pairs
        assert self.ctx_in.blueprint_machine_pairs is not None, \
            self._formatter.format('blueprint_machine_paris should not be None')
        self.blueprint_machine_pairs = self.ctx_in.blueprint_machine_pairs.__dict__
        for blueprint_name in self.ctx_in.blueprints:
            assert self.blueprint_machine_pairs[blueprint_name] is not None, \
                self._formatter.format('blueprint -> vSphere machine ID should not be None')
        self.browser_type = self.ctx_in.launch_browser.browserType
        self.with_dp = self.ctx_in.deploy_vm.with_dp
        self.blueprint_names = self.ctx_in.blueprints
        self.description = self.ctx_in.deploy_vm.description
        self.num_of_vm = self.ctx_in.deploy_vm.number_of_vm
        self.reason_for_request = None
        self.backup_service_level = None
        self.SRM_power_on_priority = None
        self.current_browser = self.ctx_in.shared.current_browser

        if hasattr(self.ctx_in.deploy_vm, 'SRM_power_on_priority'):
            self.SRM_power_on_priority = self.ctx_in.deploy_vm.SRM_power_on_priority

        if self.with_dp:
            if hasattr(self.ctx_in, 'added_backup_service_level'):
                self.backup_service_level = self.ctx_in.added_backup_service_level.backup_to_operate_vm
                logger.info(
                    'Use backup_service_level from added_backup_service_level '
                    'in context object.', False, True)
                assert self.backup_service_level is not None, self._formatter.format('backup service level is None')

            else:
                assert hasattr(self.ctx_in, 'added_backup_service_level') or \
                       hasattr(self.ctx_in.deploy_vm, 'backup_service_level'), \
                       self._formatter.format('no backup service level provided')
                self.backup_service_level = self.ctx_in.deploy_vm.backup_service_level

            if not re.search(DeployVM.DEPLOYVM_DP_BACKUP_SVC_LEVEL_NAME_PATTERN, self.backup_service_level):
                logger.warn(
                    'The backup service level for deployvm from context is:{}, The workflow added '
                    'bksl name should have timestamp appended.\n It is likely you are resuming '
                    'workflow but not using dump file.'.format(self.backup_service_level))

        if hasattr(self.ctx_in.deploy_vm, 'reason_for_request'):
            self.reason_for_request = self.ctx_in.deploy_vm.reason_for_request

    def _finalize_context(self):
        logger.info('Deployed VMs : {}'.format(self.deployed_vms), False, True)
        if getattr(self.ctx_in, 'deployed_vms', None):  # Chenyang
            logger.debug(
                'The "deployed_vms" from context object is:{}, type is:{}'.format(
                    self.ctx_in.deployed_vms, type(self.ctx_in.deployed_vms)))
            self.deployed_vms = self.ctx_in.deployed_vms + self.deployed_vms
        setattr(self.ctx_out, 'deployed_vms',
                self.deployed_vms)  # append if not empty
        self.assertTrue(len(self.deployed_vms) > 0, self._formatter.format('There is no VM deployed successfully.'))