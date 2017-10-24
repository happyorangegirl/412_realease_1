"""
 Copyright 2016 EMC GSE SW Automation

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

import sys

from robot.api import logger

from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.auc.uimap.shared import CatalogPage, RequestsPage, LoadingWindow
from ehc_e2e.auc.uimap.specific import BackupServiceLevelPage


class DisplayBackupServiceLevel(BaseUseCase):
    fail_msg = 'Running on step "Display backup service level"-FAILED, {}'

    def test_display_backup_service_level(self):
        self.request_result = None
        loading_window = LoadingWindow()
        request_page = RequestsPage()
        catalog_page = CatalogPage()
        display_backup_service_level_page = BackupServiceLevelPage()
        description = self.test_display_backup_service_level.__name__
        description += ' ' + display_backup_service_level_page.make_timestamp()

        # Go to Backup Service Level Maintenance page
        self.assertTrue(
            catalog_page.navigate_to_catalog(self.current_browser),
            self.fail_msg.format('failed to switch to catalog frame.'))

        self.assertTrue(
            catalog_page.lnk_data_protection_services.exists(),
            self.fail_msg.format('cannot find "Data Protection" button.'))
        catalog_page.lnk_data_protection_services.click()
        self.assertTrue(
            catalog_page.btn_backup_service_level_request.exists(),
            self.fail_msg.format('cannot find "Backup Service Level" request button.'))
        catalog_page.btn_backup_service_level_request.click()
        loading_window.wait_loading(self.current_browser, 30)

        try:
            # Set description and reason
            self.assertTrue(
                display_backup_service_level_page.txt_description.exists(),
                self.fail_msg.format('cannot find Description textbox.'))
            display_backup_service_level_page.txt_description.set(description)
            self.assertTrue(
                display_backup_service_level_page.txt_reasons.exists(),
                self.fail_msg.format('cannot find Reasons textbox.')
            )
            display_backup_service_level_page.txt_reasons.set('fill in Reasons field.')

            self.assertTrue(
                display_backup_service_level_page.btn_next.exists(), self.fail_msg.format('cannot find Next button.'))
            display_backup_service_level_page.btn_next.click()
            loading_window.wait_loading(self.current_browser, 30)

            # Select action
            self.assertTrue(
                display_backup_service_level_page.btn_select_action.exists(),
                self.fail_msg.format('cannot find button to open action drop down list.'))

            display_backup_service_level_page.btn_select_action.click()
            self.assertTrue(
                display_backup_service_level_page.click_drop_down_list(
                    display_backup_service_level_page.lbl_action_list, 'div',
                    self.ctx_in.display_backup_service_level.please_select_action_for_backup_service_level),
                self.fail_msg.format('failed to select action in drop down list.')
            )
            loading_window.wait_loading(self.current_browser, 30)

            self.assertTrue(
                display_backup_service_level_page.btn_next.exists(), self.fail_msg.format('Cannot find Next button'))
            display_backup_service_level_page.btn_next.click()

            self.assertTrue(
                display_backup_service_level_page.btn_open_additional_email_dropdown.exists(),
                self.fail_msg.format('cannot find button to open additional email dropdownlist.'))
            has_additional_email = 'Yes' if self.additional_email else 'No'
            display_backup_service_level_page.btn_open_additional_email_dropdown.click()
            self.assertTrue(
                display_backup_service_level_page.click_drop_down_list(
                    display_backup_service_level_page.lbl_action_list, 'div', has_additional_email),
                self.fail_msg.format(
                    'failed to select "{}" in "Additional Email" drop down list.'.format(has_additional_email)))
            loading_window.wait_loading(self.current_browser, 30)
            logger.info(
                'Selected {} for "Additional Email" option.'.format(has_additional_email), False, True)
            if has_additional_email == 'Yes':
                self.assertTrue(
                    display_backup_service_level_page.txt_email_address.exists(),
                    self.fail_msg.format('additional email address textbox does not exit.'))
                display_backup_service_level_page.txt_email_address.set(self.additional_email)
                logger.info('Input Email Address:{}.'.format(self.additional_email), False, True)
            self.assertTrue(
                display_backup_service_level_page.btn_next.exists(), self.fail_msg.format('cannot find Next button.')
            )
            display_backup_service_level_page.btn_next.click()

            # Submit
            self.assertTrue(
                display_backup_service_level_page.btn_submit.exists(),
                self.fail_msg.format('cannot find Submit button.')
            )
            display_backup_service_level_page.btn_submit.click()

        except AssertionError:
            display_backup_service_level_page.save_request()
            raise
        except:
            logger.error('encounters error, more error info: {}.'.format(sys.exc_info()))
            display_backup_service_level_page.save_request()
            raise

        # check whether submitted successfully
        self.assertTrue(
            display_backup_service_level_page.lbl_confirmation_success.exists(),
            self.fail_msg.format('cannot find submitted successfully page.'))
        self.assertTrue(display_backup_service_level_page.btn_ok.exists(),
                        self.fail_msg.format('cannot find OK button.'))
        display_backup_service_level_page.btn_ok.click()

        # Get request result
        self.assertTrue(
            request_page.navigate_to_request(self.current_browser),
            self.fail_msg.format('failed to switch to request frame.'))
        self.request_result = request_page.get_request_result(description)
        self.assertIsNotNone(self.request_result,
                             self.fail_msg.format('failed to get request result (object is None).'))

    def runTest(self):
        self.test_display_backup_service_level()

    def _validate_context(self):
        if not self.ctx_in:
            return

        self.current_browser = self.ctx_in.shared.current_browser
        self.assertIsNotNone(self.current_browser,
                             self.fail_msg.format(
                                 'current_browser in yaml is None, may be there is no active browser.'))
        self.assertTrue(self.current_browser.is_login,
                        self.fail_msg.format('please login to vRA, The flag value is_login is: False.'))

        self.assertIsNotNone(self.ctx_in.display_backup_service_level,
                             self.fail_msg.format('yaml data of display_backup_service_level value is None.'))
        self.assertIsNotNone(
            self.ctx_in.display_backup_service_level.please_select_action_for_backup_service_level,
            self.fail_msg.format('yaml data of please_select_action_for_backup_service_level value is None.'))
        self.additional_email = getattr(self.ctx_in.display_backup_service_level, 'additional_email', None)

    def _finalize_context(self):
        if self.request_result:
            if self.request_result.status != 'Successful':
                logger.error(
                    'Failed to display backup service level. status = {status}, status details = {status_details}'
                    ''.format(status=self.request_result.status, status_details=self.request_result.status_details)
                )
                raise AssertionError(
                    self.fail_msg.format('Request result not equal to Successful.')
                )
        else:
            logger.error(
                'Request result is None. This may be caused by unexpected exceptions in runTest()')
            raise AssertionError(
                self.fail_msg.format('Request result is None.'))
