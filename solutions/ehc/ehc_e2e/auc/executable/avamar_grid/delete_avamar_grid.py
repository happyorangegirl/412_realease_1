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

from robot.api import logger

from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.auc.uimap.shared import CatalogPage
from ehc_e2e.auc.uimap.shared import LoadingWindow
from ehc_e2e.auc.uimap.shared import RequestsPage
from ehc_e2e.auc.uimap.specific import DeleteAvamarGridPage


class DeleteAvamarGrid(BaseUseCase):
    """
    Delete AvamarGrid
    """
    REQUEST_SUCCESSFUL = 'Successful'
    _formatter = 'Running on step: "Delete Avamar Grid"-FAILED, {}'

    failed_to_delete_basket = []

    def test_delete_avamar_grid(self):
        self.successful_to_delete_basket = []
        loading_window = LoadingWindow()

        for added_avamar_grid_name in self.ctx_in.added_avamar_grid:
            catalog_page = CatalogPage()
            self.assertTrue(catalog_page.navigate_to_catalog(self.current_browser),
                            self._formatter.format('failed to navigate to catalog page.'))
            delete_avamar_grid_page = DeleteAvamarGridPage()
            self.assertTrue(delete_avamar_grid_page.btn_data_protection_services.exists(),
                            self._formatter.format('data protection button does not exist.'))
            delete_avamar_grid_page.btn_data_protection_services.click()
            self.assertTrue(catalog_page.btn_avamar_grid_maintenance_request.exists(),
                            self._formatter.format('avamar grid maintenance button does not exist.'))
            catalog_page.btn_avamar_grid_maintenance_request.click()
            loading_window.wait_loading(self.current_browser, 30)

            # input description.
            logger.info(msg='Start to fill items in the Request information tab.')
            self.assertTrue(delete_avamar_grid_page.txt_description.exists(),
                            self._formatter.format('description textbox does not exist.'))
            delete_avamar_grid_page.txt_description.set(self.ctx_in.delete_avamar_grid.description)
            logger.info(msg='Filled description textbox.')
            self.assertTrue(delete_avamar_grid_page.btn_next.exists(),
                            self._formatter.format('Next button does not exist.'))
            delete_avamar_grid_page.btn_next.click()
            loading_window.wait_loading(self.current_browser, 30)

            # providing operation type
            logger.info(msg='Start to fill items in the Action Choose tab')
            self.assertTrue(delete_avamar_grid_page.btn_operation_type.exists(),
                            self._formatter.format('Action DropDownList open button does not exist.'))
            delete_avamar_grid_page.btn_operation_type.click()
            self.assertTrue(delete_avamar_grid_page.click_drop_down_list(
                delete_avamar_grid_page.lbl_active_value, 'div',
                self.ctx_in.delete_avamar_grid.select_operation_type),
                            self._formatter.format('Select Action {} does not exist.'
                                                   .format(self.ctx_in.delete_avamar_grid.select_operation_type)))

            loading_window.wait_loading(self.current_browser, 30)
            self.assertTrue(delete_avamar_grid_page.btn_next.exists(),
                            self._formatter.format('Next button does not exist.'))
            delete_avamar_grid_page.btn_next.click()

            # validating and selecting delete action button
            logger.info(msg='Start to fill items in the Delete Avamar')
            self.assertTrue(delete_avamar_grid_page.btn_provider_del_avamar_grid.exists(),
                            self._formatter.format('Avamar Grid Name DropDownList open button does not exist.'))
            delete_avamar_grid_page.btn_provider_del_avamar_grid.click()
            self.assertTrue(delete_avamar_grid_page.click_drop_down_list(
                delete_avamar_grid_page.lbl_active_value, 'div', added_avamar_grid_name),
                            self._formatter.format(
                                'avamar grid name {} does not exist on drop down list.'.format(added_avamar_grid_name)))
            logger.info(msg='Selected avamar grid name from drop down list')

            # Providing the Input values
            loading_window.wait_loading(self.current_browser, 30)
            self.assertTrue(delete_avamar_grid_page.btn_provider_confirmation.exists(),
                            self._formatter.format('delete confirm DropDownList open button does not exist.'))
            delete_avamar_grid_page.btn_provider_confirmation.click()
            self.assertTrue(delete_avamar_grid_page.click_drop_down_list(delete_avamar_grid_page.lbl_active_value,
                                                                         'div',
                                                                         self.ctx_in.delete_avamar_grid.confirmation),
                            self._formatter.format('select delete confirm does not exist.'))
            loading_window.wait_loading(self.current_browser, 30)
            self.assertTrue(delete_avamar_grid_page.btn_next.exists(),
                            self._formatter.format('Next button does not exist.'))
            delete_avamar_grid_page.btn_next.click()
            loading_window.wait_loading(self.current_browser, 30)
            # Submit request.
            logger.info(msg='Start to fill items in the tab Review and Submit.')
            self.assertTrue(delete_avamar_grid_page.btn_submit.exists(),
                            self._formatter.format('submit button does not exist.'))
            delete_avamar_grid_page.btn_submit.click()
            logger.info('Clicked submit button.', False, True)
            loading_window.wait_loading(self.current_browser, 30)

            self.assertTrue(delete_avamar_grid_page.lbl_confirmation_success.exists(),
                            self._formatter.format('label: "confirm information in Review and Submit, '
                                                   'click submit button" does not exist.'))
            self.assertTrue(delete_avamar_grid_page.btn_ok.exists(),
                            self._formatter.format('OK button in confirm success does not exist.'))
            delete_avamar_grid_page.btn_ok.click()
            logger.info('Clicked ok button in confirm success page.', False, True)
            loading_window.wait_loading(self.current_browser, 30)

            # switch to request
            requests_page = RequestsPage()
            self.assertTrue(requests_page.navigate_to_request(self.current_browser),
                            self._formatter.format('switch to request frame failed.'))

            # check the request
            request_result = requests_page.get_request_result(self.ctx_in.delete_avamar_grid.description)

            self.assertIsNotNone(request_result, self._formatter.format(
                'getting request failed for deleting avamar grid: {}'.format(added_avamar_grid_name)))
            # check request result after each request completes.
            if request_result.status == self.REQUEST_SUCCESSFUL:
                logger.info("delete the avamar grid maintenance{0} has been already deleted successfully, "
                            "for more details: {1}".format(str(added_avamar_grid_name),
                                                           str(request_result.status_details)))

            else:
                logger.error("delete avamar grid {} failed.".format(added_avamar_grid_name))
                self.failed_to_delete_basket.append(added_avamar_grid_name)
                raise AssertionError(self._formatter.format(
                    ' the request status of {name} is: ' \
                    '{status}, the status detail is: {status_detail}.' \
                        .format(name=request_result.description,
                                status=request_result.status,
                                status_detail=request_result.status_details)))

    def runTest(self):
        self.test_delete_avamar_grid()

    def _validate_context(self):
        if self.ctx_in:
            self.current_browser = self.ctx_in.shared.current_browser
            assert self.current_browser is not None, \
                self._formatter.format('current_browser in yaml is None, may be there is no active browser.')
            self.assertTrue(self.current_browser.is_login,
                            msg=self._formatter.format('please login to vRA, The flag value is_login is: False.'))
            assert self.ctx_in.delete_avamar_grid.description is not None, \
                self._formatter.format('the description of delete_avamar_grid in yaml file is None.')
            assert self.ctx_in.delete_avamar_grid.select_operation_type is not None, \
                self._formatter.format('the select_operation_type of delete_avamar_grid in yaml file is None.')
            assert self.ctx_in.delete_avamar_grid.confirmation is not None, \
                self._formatter.format('the confirmation of delete_avamar_grid in yaml file is None.')
            self.len_added_avamar_grid = len(self.ctx_in.added_avamar_grid)
            self.assertTrue(self.len_added_avamar_grid > 0,
                            msg=self._formatter.format('the data item in yaml: added_avamar_grid is None.'))

    def _finalize_context(self):
        setattr(self.ctx_out, 'delete_avamar grid.failed_to_delete_avamar_grid', self.failed_to_delete_basket)
