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
from ehc_rest_utilities.session_manager import ViPRSession
from ehc_rest_utilities.vipr_rest_utilities import ViPRRestEx
from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.auc.uimap.shared import RequestsPage, CatalogPage, LoadingWindow
from ehc_e2e.auc.uimap.specific import DeleteDataStorePage


class DeleteDataStore(BaseUseCase):
    """
    del datastore
    """
    has_failures = False
    failed_to_delete_datastores = []
    successful_delete_datastores = []
    DELETE_DATASTORE_TAB_CONFIRM_SELECTION = 'Confirm'
    _formatter = 'Running on step: "Delete Datastore" - FAILED, {}'

    def test_delete_datastore(self):
        for counter, datastore in enumerate(self.datastores_to_delete):
            if not datastore.name:
                logger.debug('No datastore need to delete.')
                continue

            item = datastore.name[0]
            description = 'test_delete_datastore_{}'.format(item)
            logger.info('Start to delete datastore: {}'.format(item), False, True)
            catalog_page = CatalogPage()
            loading_window = LoadingWindow()
            delete_datastore_page = DeleteDataStorePage()

            self.assertTrue(
                catalog_page.navigate_to_catalog(self.current_browser),
                msg=self._formatter.format('switch to catalog frame failed.')
            )

            delete_datastore_page.btn_cloud_storage.click()
            catalog_page.btn_datastore_maintenance_request.click()
            loading_window.wait_loading(self.current_browser, 30)
            # delete storage failed, and find the loading window need used method wait_loading2 to wait
            loading_window.wait_loading2(self.current_browser, 30)
            try:
                self.assertTrue(
                    delete_datastore_page.txt_description.exists(),
                    self._formatter.format('description textbox does not exist.')
                )
                delete_datastore_page.txt_description.set(description)
                logger.info('Filled in description tab.', False, True)
                delete_datastore_page.btn_next.click()

                self.assertTrue(
                    delete_datastore_page.btn_select_datastore_to_delete.exists(),
                    self._formatter.format('Option "Select Datastore to delete" does not exist.')
                )
                delete_datastore_page.btn_select_datastore_to_delete.click()

                # Wenda: default item is empty in Badger. so change to click dropdownlist method.
                self.assertTrue(
                    delete_datastore_page.click_drop_down_list(
                        delete_datastore_page.lbl_active_value, 'div', item),
                    self._formatter.format(
                        'Select datastore: {} to delete from dropdownlist.'.format(item))
                )
                logger.info('Selected datastore: {} to delete.'.format(item), False, True)

                loading_window.wait_loading(self.current_browser, 30)
                self.assertTrue(
                    delete_datastore_page.btn_open_confirm_dropdownlist.exists(),
                    self._formatter.format(
                        '"Confirm" dropdownlist open button does not exist.')
                )
                delete_datastore_page.btn_open_confirm_dropdownlist.click()
                self.assertTrue(
                    delete_datastore_page.click_drop_down_list(
                        delete_datastore_page.lbl_active_value, 'div',
                        self.DELETE_DATASTORE_TAB_CONFIRM_SELECTION),
                    self._formatter.format('Select "Confirm" from dropdownlist.')
                )
                logger.info(
                    'Selected: {} from dropdownlist.'.format(
                        self.DELETE_DATASTORE_TAB_CONFIRM_SELECTION
                    )
                )
                loading_window.wait_loading(self.current_browser, 30)
                delete_datastore_page.btn_next.click()
                loading_window.wait_loading(self.current_browser, 30)

                self.assertTrue(delete_datastore_page.btn_submit.exists(),
                                msg=self._formatter.format('Submit button does not exist.'))
                delete_datastore_page.btn_submit.click()
                loading_window.wait_loading(self.current_browser, 30)

                self.assertTrue(
                    delete_datastore_page.lbl_confirmation_success.exists(),
                    msg=self._formatter.format(
                        'Label: "The request has been submitted successfully" does not exist.')
                )
                delete_datastore_page.btn_ok.click()

                # switch to request
                self.assertTrue(
                    RequestsPage().navigate_to_request(self.current_browser),
                    self._formatter.format('switch to request frame failed.')
                )
                # check the request
                request_result = RequestsPage().get_request_result(description)
                self.assertIsNotNone(
                    request_result, self._formatter.format('failed to get the request result.')
                )
                if request_result.status == 'Successful':
                    self.successful_delete_datastores.append(item)
                    logger.info("Deleting datastore {} succeeded.".format(item), False, True)

                    self.delete_datastore_in_vipr(item)

                else:
                    self.failed_to_delete_datastores.append(item)
                    logger.error(
                        "Deleting datastore {} failed, more request details: {}".format(
                            item, request_result.status_details))

            except AssertionError:
                delete_datastore_page.save_request()
                raise
            except:
                delete_datastore_page.save_request()
                self.fail(
                    self._formatter.format(
                        'unexpected error, more details: {}'.format(sys.exc_info()))
                )

    def runTest(self):
        self.test_delete_datastore()

    def _validate_context(self):
        if self.ctx_in:
            assert self.ctx_in.shared.current_browser.is_login is True, \
                self._formatter.format("can't do anything if you are not logged in")
            self.current_browser = self.ctx_in.shared.current_browser

            self.datastores_to_delete = getattr(self.ctx_in, 'added_cloud_storage', [])

    def _finalize_context(self):
        # We will log failures and succeeded deletion if there is any,
        # if there is failure, will fail the AUC.
        if len(self.successful_delete_datastores) > 0:
            logger.info(
                'Those datastores: {} were deleted successfully.'.format(
                    ', '.join(self.successful_delete_datastores))
            )
        assert len(self.failed_to_delete_datastores) == 0, \
            self._formatter.format('failed to delete datastores: ' + ', '.join(self.failed_to_delete_datastores))

    def delete_datastore_in_vipr(self, datastore_name):
        logger.info('Start to delete datastore {0} in ViPR'.format(datastore_name), False, True)
        if not hasattr(self.ctx_in, 'vipr'):
            logger.warn('ViPR section is not provided in YAML. Task ignored')
            return

        vipr_address = getattr(self.ctx_in.vipr, 'address')
        vipr_username = getattr(self.ctx_in.vipr, 'username')
        vipr_password = getattr(self.ctx_in.vipr, 'password')

        try:
            vipr_session = ViPRSession(vipr_address, vipr_username, vipr_password)
        except:
            logger.warn('Failed to create ViPR session. Task ignored. Error message = {0}'.format(sys.exc_info()))
            return
        try:
            vipr_ex = ViPRRestEx(vipr_session)
            if vipr_ex.delete_volume(datastore_name):
                logger.info('Succeeded to delete datastore in ViPR', False, True)
        except:
            logger.warn('Error occurred during communicating with ViPR. Task ignored. Error message = {0}'
                        .format(sys.exc_info()))
        finally:
            vipr_session.logout()
