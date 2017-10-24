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


class EditARR(BaseUseCase):
    """
    edit Avamar Replication Relationship:
    if no arr value in YAML 'Edit Avamar Replication Relationship',
    the edit arr will get the first arr in 'added_avamar_replication_relationship'.
    if no arr added in 'added_avamar_replication_relationship' , AUC will failed.
    """
    step_failed_msg = 'Running on step: "Edit Avamar Replication Relationship"-FAILED, {}'.format
    request_result = None

    def test_edit_arr(self):

        arr_page = ARRPage()
        catalog_page = CatalogPage()
        load_window = LoadingWindow()
        logger.info('Start to edit arr: {0}'.format(self.arr), False, True)
        # switch to catalog frame

        navigate_to_catalog = catalog_page.navigate_to_catalog(self.current_browser)
        self.assertTrue(navigate_to_catalog,
                        msg=self.step_failed_msg('switch to catalog frame failed.'))
        catalog_page.wait_for_loading_complete(3)
        self.assertTrue(catalog_page.lnk_data_protection_services.exists(),
                        msg=self.step_failed_msg('cannot find Data Protection Services card in the left page.'))
        catalog_page.lnk_data_protection_services.click()
        catalog_page.wait_for_loading_complete(3)
        logger.info(msg='Start to click the Avamar Replication Relationship (ARR) Maintenance request button.')
        self.assertTrue(catalog_page.btn_arr_maintenance_request.exists(),
                        msg=self.step_failed_msg(
                            'cannot find Avamar Replication Relationship (ARR) Maintenance card in the right page.'))
        catalog_page.btn_arr_maintenance_request.click()
        load_window.wait_loading(self.current_browser)
        try:
            logger.info(msg='Start to fill items in the Request Information tab')
            self.assertTrue(arr_page.txt_description.exists(),
                            msg=self.step_failed_msg('cannot find textbox description.'))
            arr_page.txt_description.set(self.description)
            catalog_page.wait_for_loading_complete(2)
            self.assertTrue(arr_page.btn_next.exists(), msg=self.step_failed_msg('cannot find Next Button.'))
            arr_page.btn_next.click()
            load_window.wait_loading(self.current_browser)

            logger.info(msg='Start to fill items in the Action Choose tab')
            self.assertTrue(arr_page.lnk_operation_type_menu.exists(),
                            msg=self.step_failed_msg('Action DropDownList open button does not exist.'))
            arr_page.lnk_operation_type_menu.click()
            self.assertTrue(arr_page.click_drop_down_list(arr_page.lnk_select_dropdownlist, 'div', self.action),
                            msg=self.step_failed_msg(
                                'in DropDownList Action cannot find option: {}'.format(self.action)))
            load_window.wait_loading(self.current_browser, 30)
            self.assertTrue(arr_page.btn_next.exists(), msg=self.step_failed_msg('cannot find Next Button.'))
            arr_page.btn_next.click()
            load_window.wait_loading(self.current_browser, 30)

            logger.info(msg='Start to fill items in edit ARR tab')
            # wait to load frame
            arr_page.wait_for_loading_complete(wait_time=2)
            self.assertTrue(arr_page.lnk_edit_arr_menu.exists(),
                            msg=self.step_failed_msg('ARR DropDownList open button does not exist.'))
            arr_page.lnk_edit_arr_menu.click()
            self.assertTrue(arr_page.click_drop_down_list(
                arr_page.lnk_select_dropdownlist, 'div', self.arr, compare_contains=True),
                            msg=self.step_failed_msg('in DropDownList ARR cannot find option: {}'.format(self.arr)))
            load_window.wait_loading(self.current_browser, 30)

            self.assertTrue(arr_page.lnk_admin_full_menu.exists(),
                            msg=self.step_failed_msg('Admin Full DropDownList open button does not exist.'))
            arr_page.lnk_admin_full_menu.click()
            self.assertTrue(arr_page.click_drop_down_list(arr_page.lnk_select_dropdownlist, 'div', self.admin_full),
                            msg=self.step_failed_msg(
                                'in DropDownList Admin Full cannot find option:'.format(self.admin_full)))

            load_window.wait_loading(self.current_browser, 30)
            self.assertTrue(arr_page.btn_next.exists(), msg=self.step_failed_msg('cannot find Next Button.'))
            arr_page.btn_next.click()

            logger.info(msg='Start to Submit Request.')
            # wait to load frame
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

        logger.info(msg='Go into the request has been submitted successully page')
        self.assertTrue(arr_page.lbl_confirmation_success.exists(),
                        msg=self.step_failed_msg('there is no label: The request has been submitted successfully.'))
        # wait to load frame
        arr_page.wait_for_loading_complete(wait_time=2)
        self.assertTrue(arr_page.btn_ok.exists(),
                        msg=self.step_failed_msg('there is no Button OK after submitting request.'))
        arr_page.btn_ok.click()

        # switch to request
        self.assertTrue(RequestsPage().navigate_to_request(self.current_browser),
                        msg=self.step_failed_msg('switch to request frame failed.'))

        # check the request
        self.request_result = RequestsPage().get_request_result(self.description)

        self.assertIsNotNone(self.request_result,
                             msg=self.step_failed_msg('failed to get the request result.'))

    def runTest(self):
        self.test_edit_arr()

    def _validate_context(self):
        if self.ctx_in:
            self.current_browser = getattr(self.ctx_in.shared, 'current_browser', None)
            assert self.current_browser, \
                self.step_failed_msg('current_browser in yaml is None, may be there is no active browser')
            assert getattr(self.current_browser, 'is_login') is True, \
                self.step_failed_msg('please login to vRA, The flag is_login is False.')
            self.edit_arr = getattr(self.ctx_in, 'edit_avamar_replication_relationship', [])
            self.added_arrs = getattr(self.ctx_in, 'added_avamar_replication_relationship', [])

            if getattr(self.edit_arr, 'arr', None):
                self.arr = self.edit_arr.arr
            elif len(self.added_arrs) > 0:
                self.arr = self.added_arrs[0]
            else:
                self.fail('Please check whether add one arr successfully in test case: '
                          'Cloud Administrator Adds An Avamar Replication Relationship')

            self.admin_full = 'Yes' if getattr(self.edit_arr, 'admin_full', 'No') in (True, 'Yes') else 'No'
            self.description = 'edit arr ' + self.arr
            self.action = 'Edit ARR'

    def _finalize_context(self):
        if self.request_result:
            more_details = "{" + self.arr + ", " + self.request_result.status + ", " + \
                           self.request_result.status_details + "}"
            if self.request_result.status == 'Successful':
                logger.info('Edit ARR successful:{0}, for more details: {1}'.format(
                    self.arr, more_details), False, True)
            else:
                self.fail('Edit ARR failed: {0}, for more details: {1}'.format(self.arr, more_details))
