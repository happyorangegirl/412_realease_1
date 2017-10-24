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
from robot.api import logger
from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.auc.uimap.shared import MainPage, RequestsPage, LoadingWindow
from ehc_e2e.auc.uimap.specific import OperateVMPage


class GetBackupSummary(BaseUseCase):

    def get_backup_summary(self):

        main_page = MainPage()
        request_page = RequestsPage()
        loading_window = LoadingWindow()

        driver_ref = self.current_browser.instance._browser.current
        self.assertIsNotNone(driver_ref, 'Failed to get WebDriver reference')

        # request Get Backup Status task for each deployed VM
        for vm_name in self.deployed_vms_list:

            operate_vm_page = OperateVMPage(vm_name)

            # switch to item frame
            try:
                driver_ref.switch_to.frame(None)
                self.assertTrue(main_page.btn_items.exists(), 'Cannot find item button to navigate to item page')
                main_page.btn_items.click()
                iframe_elem = driver_ref.find_element_by_xpath(
                    '//iframe[contains(@onload, "' + operate_vm_page.gadget_url_str + '")]')
                driver_ref.switch_to.frame(iframe_elem)

            except AssertionError:
                raise
            except:
                ex = sys.exc_info()
                self.fail('WebDriver failed to find or switch to iframe. Error message: {0}'.format(ex))

            # click Machines button
            self.assertTrue(operate_vm_page.btn_machine.exists(), 'Machines button does not exists')
            operate_vm_page.btn_machine.click()
            loading_window.wait_loading(self.current_browser, 30)

            # go to vm details page and request Get Backup Status task
            self.assertTrue(operate_vm_page.lnk_test_vm.exists(), 'Target VM: {} does not exists'.format(vm_name))
            operate_vm_page.lnk_test_vm.click()
            loading_window.wait_loading(self.current_browser, 30)

            self.assertTrue(operate_vm_page.btn_get_backup_status.exists(), 'Cannot find Get Backup Status link')
            operate_vm_page.btn_get_backup_status.click()

            try:
                # Set description and reason
                description = self.get_backup_summary.__name__
                description += ' ' + operate_vm_page.make_timestamp()
                self.assertTrue(operate_vm_page.txt_description.exists(), 'Cannot find Description textbox')
                operate_vm_page.txt_description.set(description)

                self.assertTrue(operate_vm_page.txt_reasons.exists(), 'Cannot find Reasons textbox')
                operate_vm_page.txt_reasons.set('fill in reasons field')
                self.assertTrue(operate_vm_page.btn_next.exists(), 'Cannot find Next button')
                operate_vm_page.btn_next.click()

                # Submit and check whether succeeded
                self.assertTrue(operate_vm_page.btn_submit.exists(), 'Cannot find Submit button')
                operate_vm_page.btn_submit.click()
                self.assertTrue(operate_vm_page.btn_ok.exists(), 'Cannot find OK button after submit')
                operate_vm_page.btn_ok.click()

            except Exception as e:
                operate_vm_page.save_request()

                if isinstance(e, AssertionError):
                    logger.error('Get Backup Status failed on VM {0}, request saved'.format(vm_name))
                    raise
                else:
                    ex = sys.exc_info()
                    logger.error('Get Backup Status failed on VM {0} error: {1}, request saved'.format(vm_name, ex))

            # Check request result. Stop running on failure
            self.assertTrue(request_page.navigate_to_request(self.current_browser), 'Failed to switch to request page')
            request_result = request_page.get_request_result(description)
            self.assertIsNotNone(request_result, 'Failed to get request result')

            self.succeeded_vms = []
            self.failed_vms = []

            if request_result.status != 'Successful':
                logger.error('Failed to Get Backup Status of VM {vm}. status = {status}, '
                             'status details = {status_details}'.format(vm=vm_name, status=request_result.status,
                                                                        status_details=request_result.status_details))
                self.failed_vms.append(vm_name)
            else:
                logger.info('Succeeded to Get Backup Status of VM {}'.format(vm_name))
                self.succeeded_vms.append(vm_name)

    def runTest(self):
        self.get_backup_summary()

    def _validate_context(self):
        # I'm not sure whether it should be True of not None...I just saw others wrote True
        if not self.ctx_in:
            return

        self.current_browser = self.ctx_in.shared.current_browser
        self.assertIsNotNone(self.current_browser,
                             'current_browser instance is not found, may be there is no active browser')
        self.assertTrue(self.current_browser.is_login, 'Please login to vRA.')

        self.deployed_vms_list = self.ctx_in.deployed_vms
        self.assertIsNotNone(self.deployed_vms_list, 'key of deployed_vms in configuration file is None')
        self.assertGreater(len(self.deployed_vms_list), 0, 'there is no vm deployed')

    def _finalize_context(self):
        logger.info('Get Backup Summary: {0} VM(s) succeeded and {1} VM(s) failed'.format(
            len(self.succeeded_vms), len(self.failed_vms)))
        if len(self.failed_vms) > 0:
            self.fail('Running on step: "Get Backup Summary" - FAILED. ')
