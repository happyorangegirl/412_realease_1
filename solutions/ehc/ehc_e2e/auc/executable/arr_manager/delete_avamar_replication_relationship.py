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
from ehc_e2e.auc.uimap.specific import ARRPage
from ehc_e2e.auc.uimap.shared import RequestsPage
from ehc_e2e.auc.uimap.shared import LoadingWindow


class DeleteARR(BaseUseCase):
    """
    delete Avamar Replication Relationship
    """
    delete_arrs_list = []
    step_failed_msg = 'Running on step: "Delete Avamar Replication Relationship"-FAILED, {}'.format

    def test_delete_arr(self):
        if self.len_add_arrs == 0:
            logger.info(msg='The item added_arrs in yaml file is None, there are no arrs need to delete.')
        else:
            logger.info('The arr list need to delete is : {0}'.format(self.added_arrs))
            arr_page = ARRPage()
            load_window = LoadingWindow()
            for added_arr in self.added_arrs:
                delete_arr_result = {}
                timestamp = arr_page.make_timestamp()
                _description = self.description + ' ' + timestamp
                logger.info('Start to delete arr: {0}'.format(added_arr), False, True)
                # switch to catalog frame
                self.catalog_page = CatalogPage()
                navigate_to_catalog = self.catalog_page.navigate_to_catalog(self.current_browser)
                self.assertTrue(navigate_to_catalog,
                                msg=self.step_failed_msg('switch to catalog frame failed.'))
                self.catalog_page.wait_for_loading_complete(3)
                self.assertTrue(self.catalog_page.lnk_data_protection_services.exists(),
                                msg=self.step_failed_msg('cannot find Data Protection Services card in the left page.'))
                self.catalog_page.lnk_data_protection_services.click()
                self.catalog_page.wait_for_loading_complete(3)
                logger.info(msg='Start to click the Avamar Replication Relationship (ARR) Maintenance request button.')
                self.assertTrue(self.catalog_page.btn_arr_maintenance_request.exists(), msg=self.step_failed_msg(
                    'cannot find Avamar Replication Relationship (ARR) Maintenance card in the right page.'))
                self.catalog_page.btn_arr_maintenance_request.click()
                load_window.wait_loading(self.current_browser, 30)

                try:
                    logger.info(msg='Start to fill items in the Request information tab')
                    self.assertTrue(arr_page.txt_description.exists(),
                                    msg=self.step_failed_msg('cannot find textbox "description".'))
                    arr_page.txt_description.set(_description)
                    self.catalog_page.wait_for_loading_complete(2)
                    self.assertTrue(arr_page.btn_next.exists(),
                                    msg=self.step_failed_msg('there is no Next Button.'))
                    arr_page.btn_next.click()
                    load_window.wait_loading(self.current_browser, 30)

                    logger.info(msg='Start to fill items in the Action Choose tab')
                    self.assertTrue(arr_page.lnk_operation_type_menu.exists(),
                                    msg=self.step_failed_msg('action DropDownList open button does not exist.'))
                    arr_page.lnk_operation_type_menu.click()
                    self.assertTrue(
                        arr_page.click_drop_down_list(arr_page.lnk_select_dropdownlist, 'div', self.operation_type),
                        msg=self.step_failed_msg(
                            'in DropDownList Action cannot find option: {}'.format(self.operation_type)))
                    load_window.wait_loading(self.current_browser, 30)
                    self.assertTrue(arr_page.btn_next.exists(),
                                    msg=self.step_failed_msg('there is no Next Button.'))
                    arr_page.btn_next.click()
                    load_window.wait_loading(self.current_browser, 30)

                    logger.info(msg='Start to fill items in Delete ARR tab')
                    # wait to load frame
                    self.assertTrue(arr_page.lnk_delete_arr_menu.exists(),
                                    msg=self.step_failed_msg('ARR DropDownList open button does not exist.'))
                    arr_page.lnk_delete_arr_menu.click()
                    self.assertTrue(arr_page.click_drop_down_list(arr_page.lnk_select_dropdownlist, 'div', added_arr),
                                    msg=self.step_failed_msg(
                                        'in DropDownList ARR cannot find option: {}'.format(added_arr)))
                    load_window.wait_loading(self.current_browser, 30)
                    logger.info(msg='Start to confirm delete arr')
                    self.assertTrue(arr_page.lnk_delete_confirm_menu.exists(),
                                    msg=self.step_failed_msg('Confirm DropDownList open button does not exist.'))
                    arr_page.lnk_delete_confirm_menu.click()
                    self.assertTrue(arr_page.click_drop_down_list(
                        arr_page.lnk_select_dropdownlist, 'div', self.confirm),
                                    msg=self.step_failed_msg(
                                        'in DropDownList Confirm cannot find option: {}'.format(self.confirm)))

                    load_window.wait_loading(self.current_browser, 30)
                    self.assertTrue(arr_page.btn_next.exists(),
                                    msg=self.step_failed_msg('there is no Next Button.'))
                    arr_page.btn_next.click()
                    load_window.wait_loading(self.current_browser, 30)
                    self.assertTrue(arr_page.btn_submit.exists(),
                                    msg=self.step_failed_msg('there is no Button: Submit.'))
                    arr_page.btn_submit.click()
                    load_window.wait_loading(self.current_browser, 30)
                except AssertionError:
                    arr_page.save_request()
                    raise
                except:
                    arr_page.save_request()
                    self.fail(msg=self.step_failed_msg('more error info: {}'.format(sys.exc_info())))

                logger.info(msg='Start to go into the request has been submitted successully page')
                self.assertTrue(arr_page.lbl_confirmation_success.exists(),
                                msg=self.step_failed_msg(
                                    'there is not exists label: "The request has been submitted successfully" '
                                    'after clicking submit button.'))
                arr_page.wait_for_loading_complete(wait_time=2)
                self.assertTrue(arr_page.btn_ok.exists(), msg=self.step_failed_msg('there is no OK button.'))
                arr_page.btn_ok.click()
                load_window.wait_loading(self.current_browser, 30)

                # switch to request
                self.assertTrue(RequestsPage().navigate_to_request(self.current_browser),
                                msg=self.step_failed_msg('switch to request frame failed.'))

                # check the request
                request_result = RequestsPage().get_request_result(_description)
                self.assertIsNotNone(request_result,
                                     msg=self.step_failed_msg('failed to get the request result.'))
                delete_arr_result.update(arr_name=added_arr, status=request_result.status,
                                         status_details=request_result.status_details)
                self.delete_arrs_list.append(delete_arr_result)

    def runTest(self):
        self.test_delete_arr()

    def _validate_context(self):
        if self.ctx_in:
            self.current_browser = self.ctx_in.shared.current_browser
            assert self.current_browser is not None, \
                self.step_failed_msg('current_browser in yaml is None, may be there is no active browser')
            assert self.current_browser.is_login is True, \
                self.step_failed_msg('please login to vRA, The flag is_login is False.')
            self.added_arrs = getattr(self.ctx_in, 'added_avamar_replication_relationship', [])
            self.len_add_arrs = len(self.added_arrs)
            self.operation_type = 'Delete ARR'
            self.description = 'test_delete_arr'
            self.confirm = 'Confirm'

    def _finalize_context(self):
        failed_delete_arr = []
        arr_deleted = True
        for delete_arr_dict in self.delete_arrs_list:
            status = delete_arr_dict['status']
            if status == 'Successful':
                logger.info(msg='Delete ARR successful:{0}, '
                                'for more details:{1}'.format(delete_arr_dict['arr_name'], str(delete_arr_dict)))
            else:
                arr_deleted = False
                failed_delete_arr.append(delete_arr_dict['arr_name'])
                logger.error('Delete ARR failed :{0}, '
                             'for more details:{1}'.format(delete_arr_dict['arr_name'], str(delete_arr_dict)))
        self.assertTrue(arr_deleted,
                        msg=self.step_failed_msg('delete these ARR failed: {}'.format(', '.join(failed_delete_arr))))
