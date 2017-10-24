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
from ehc_e2e.auc.uimap.shared import CatalogPage
from ehc_e2e.auc.uimap.shared import RequestsPage, LoadingWindow
from ehc_e2e.auc.uimap.specific import BackupServiceLevelPage


class DeleteBackupServiceLevel(BaseUseCase):
    """
    delete Backup Service Level
    Caveats:
     current implementation will just check the context.shared.backup_service_levels.for_deletion
     and iterate items within that for deletion.
    """
    failed_msg = 'Running on step: "Delete Backup Service Level"-FAILED, {}'

    def test_delete_backup_service_level(self):

        self.result = []
        loading_window = LoadingWindow()
        for item in self.backup_service_levels_to_delete:
            catalog_page = CatalogPage()
            delete_description = self.description + ' for ' + item
            self.assertTrue(
                catalog_page.navigate_to_catalog(self.current_browser),
                self.failed_msg.format('switch to catalog frame failed.')
            )

            backup_service_level_page = BackupServiceLevelPage()

            backup_service_level_page.data_protection_services.click()
            catalog_page.btn_backup_service_level_request.click()

            try:
                self.assertTrue(
                    backup_service_level_page.txt_description.exists(),
                    self.failed_msg.format('"description" textbox does not exist.')
                )
                backup_service_level_page.txt_description.set(delete_description)
                backup_service_level_page.txt_reasons.set(self.reasons)
                loading_window.wait_loading(self.current_browser, 30)
                backup_service_level_page.btn_next.click()

                self.assertTrue(
                    backup_service_level_page.btn_delete_backup_service_level.exists(),
                    self.failed_msg.format('failed to navigate to Please Select Action for Backup Service Level page')
                )

                backup_service_level_page.btn_delete_backup_service_level.click()
                self.assertTrue(backup_service_level_page.click_drop_down_list(
                    backup_service_level_page.parent_element, "div",
                    self.please_select_action_for_backup_service_level),
                    self.failed_msg.format(
                        'failed to select {} from drop down list.'.format(
                            self.please_select_action_for_backup_service_level)))
                logger.info(
                    'Selected: {} as the action.'.format(
                        self.please_select_action_for_backup_service_level), False, True
                )
                loading_window.wait_loading(self.current_browser, 30)
                backup_service_level_page.btn_next.click()

                backup_service_level_page.btn_select_backup_service_level_to_delete.click()

                # If we don't find the backup service level we intend to delete, we just log error
                # and continue for next deletion.
                try:
                    self.assertTrue(
                        backup_service_level_page.click_drop_down_list(
                            backup_service_level_page.parent_element, "div", item),
                        self.failed_msg.format(
                            'select Backup Service Level: {} from dropdownlist to delete.'.format(item)
                        )
                    )
                except AssertionError:
                    backup_service_level_page.save_request()
                    logger.warn(
                        'Backup service level:{} not found, we just continue to next deletion '
                        'if there is.'.format(item)
                    )
                    continue

                loading_window.wait_loading(self.current_browser, 30)
                logger.info(
                    'Selected Backup Service Level:{} from dropdownlist to delete.'.format(item),
                    False, True
                )
                backup_service_level_page.btn_confirm_deletion_of_backup_service_level.click()
                confirm_delete = 'Confirm'
                if self.confirm_deletion_of_backup_service_level is False:
                    confirm_delete = 'Deny'
                self.assertTrue(backup_service_level_page.click_drop_down_list(
                    backup_service_level_page.parent_element, "div", confirm_delete), '')
                loading_window.wait_loading(self.current_browser, 30)
                logger.info(
                    'Selected:{} from "Confirm delete" dropdownlist.'.format(confirm_delete), False, True
                )
                backup_service_level_page.btn_next.click()
                loading_window.wait_loading(self.current_browser, 30)
                self.assertTrue(
                    backup_service_level_page.btn_submit.exists(),
                    self.failed_msg.format('"Submit" button does not exist.'))
                backup_service_level_page.btn_submit.click()

            except AssertionError:
                backup_service_level_page.save_request()
                raise
            except:
                backup_service_level_page.save_request()
                self.fail(self.failed_msg.format(
                    ' encounters error, more error info: {}'.format(sys.exc_info())))

            self.assertTrue(
                backup_service_level_page.lab_confirmation_success.exists(),
                self.failed_msg.format(
                    'after clicking submit button, cannot find label: The request has been submitted successfully.'))
            backup_service_level_page.btn_ok.click()
            # switch to request
            self.assertTrue(
                RequestsPage().navigate_to_request(self.current_browser),
                self.failed_msg.format('switch to request frame failed.')
            )

            # check the request
            request_result = RequestsPage().get_request_result(delete_description)
            self.assertIsNotNone(request_result, self.failed_msg.format('failed to get the request result.'))
            self.result.append(request_result)

    def runTest(self):
        self.test_delete_backup_service_level()

    def _validate_context(self):
        if self.ctx_in:
            self.current_browser = self.ctx_in.shared.current_browser
            assert self.current_browser is not None, \
                self.failed_msg.format('current_browser in yaml is None, may be there is no active browser.')
            self.assertTrue(self.current_browser.is_login,
                            msg=self.failed_msg.format('please login to vRA, The flag value is_login is: False.'))

            self.assertIsNotNone(self.ctx_in.shared.backup_service_levels,
                                 self.failed_msg.format(
                                     'no backup service level to delete, make sure context.share. '
                                     'backup_service_levels is set.'))
            self.description = 'delete_backup_service_level'
            self.reasons = 'backup_service_level deletion'
            self.please_select_action_for_backup_service_level = 'Delete Backup Service Level'
            self.confirm_deletion_of_backup_service_level = 'Yes'

            self.backup_service_levels_to_delete = self.ctx_in.shared.backup_service_levels.for_deletion
            logger.info(
                'We have following backup service level to delete:{}'.format(
                    ','.join(self.backup_service_levels_to_delete)
                ), False, True)

    def _finalize_context(self):
        for res in self.result:
            if res.status == 'Failed':
                logger.error(
                    'the request status of delete backup service level:{name} is: {status}, '
                    'the status detaial is: {status_detail}'.format(
                        name=res.description, status=res.status, status_detail=res.status_details))
            else:
                logger.info(
                    'the request status of add destroy_vms:{name} request result is successful'.format(
                        name=res.description))
