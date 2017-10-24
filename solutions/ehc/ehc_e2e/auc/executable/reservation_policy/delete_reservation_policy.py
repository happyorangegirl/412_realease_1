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
from ehc_e2e.auc.uimap.specific import ReservationPolicyPage
from ehc_e2e.auc.uimap.shared import InfrastructurePage
from ehc_e2e.auc.reusable import context_util
from ehc_e2e.auc.reusable.browser_relauncher import close_relaunch_browser_operation


class DeleteReservationPolicy(BaseUseCase):
    MAX_TIMES_TO_CLOSE_RELAUNCH = 3

    def __init__(self, name=None, method_name='runTest', **kwargs):
        super(DeleteReservationPolicy, self).__init__(name, method_name, **kwargs)
        self.deleted_rsv_policy = None
        self.step_error_msg = 'Running on step: "Delete Reservation Policy" - FAILED, {step}'.format

    def test_delete_reservation_policy(self):
        self.infra_page = InfrastructurePage()
        self.del_rsv_policy_page = ReservationPolicyPage()
        logger.info('Start to delete reservation policy:{0}'.format(self.reservation_policy_name), False, True)

        if self.infra_page.navigate_to_dest_page(self.current_browser,
                                                 self.infra_page.btn_reservations,
                                                 self.infra_page.btn_dest_reservation_policies):

            logger.info('Navigated to infrastructure frame and clicked destination "Reservation Policies" button.',
                        False, True)
        else:
            logger.warn('Navigate to infrastructure frame and '
                        'click destination "Reservation Policies" button failed.')
            return False

        if self.infra_page.navigate_to_iframe(
                self.current_browser,
                attribute_name='extensionid',
                url_in_attribute=self.infra_page.infra_reservation_policy_edit_frame_extensionid
        ):
            logger.info('Navigated to "Reservation Policies" frame.', False, True)
        else:
            logger.warn('Navigate to "Reservation Policies" frame failed.')
            return False

        cell_number_checked = 0
        # Displaying 1 - 30 of 77
        self.assertIsNotNone(self.del_rsv_policy_page.label_page_number.exists(),
                             self.step_error_msg(step='can not find toolbar: Display .. of ..'))
        max_cell_number = int(self.del_rsv_policy_page.label_page_number.value.split('of')[-1])
        try:
            flag_next_page = True
            while flag_next_page:
                self.assertTrue(
                    self.del_rsv_policy_page.body_rsv_policy_table.exists(),
                    msg=self.step_error_msg(step='cannot find reservation policy list table')
                )

                self.all_tr = self.del_rsv_policy_page.body_rsv_policy_table.current. \
                    find_elements_by_class_name(self.del_rsv_policy_page.row_rsv_policy_table_class)
                if len(self.all_tr) > 0:
                    for counter, item in enumerate(self.all_tr):
                        # In reservation policy table, there exist two type data:
                        # Reservation Policy, Storage Reservation Policy,
                        # The Names of two types maybe same. So according to type and reservation policy name
                        # to check the target reservation policy
                        rsv_name_column = item.find_element_by_xpath(self.del_rsv_policy_page.column_rsv_name_xpath)
                        type_column_text = item.find_element_by_xpath(self.del_rsv_policy_page.column_type_xpath).text
                        if type_column_text == 'Reservation Policy' and rsv_name_column.text == \
                                str(self.reservation_policy_name):
                            logger.info(msg='Have find reservation policy: {0}'.format(self.reservation_policy_name))
                            rsv_name_column.click()
                            logger.info(msg='Clicked target reservation policy name column')
                            self.assertTrue(
                                self.del_rsv_policy_page.btn_delete_enabled.exists(),
                                msg=self.step_error_msg(step='there is no button: delete')
                            )
                            self.del_rsv_policy_page.btn_delete_enabled.click()
                            logger.info(msg='Clicked delete button.')
                            self.del_rsv_policy_page.wait_for_loading_complete(5)
                            flag_next_page = False
                            self.assertTrue(self.del_rsv_policy_page.btn_yes.exists(),
                                            msg=self.step_error_msg(step='there is no button: yes'))
                            self.del_rsv_policy_page.btn_yes.click()
                            logger.info(msg='Clicked OK button.')
                            self.infra_page.wait_for_loading_complete(5)
                            if self.del_rsv_policy_page.btn_confirm_cancel.exists():
                                self.fail(msg=self.step_error_msg(
                                    step='Reservation policy:{} can not be deleted'.format(
                                        self.reservation_policy_name)))
                            self.infra_page.wait_for_loading_complete(5)
                            break

                        if flag_next_page and len(self.all_tr) - 1 == counter:
                            cell_number_checked += len(self.all_tr)
                            if cell_number_checked < max_cell_number:
                                self.assertTrue(self.del_rsv_policy_page.btn_next.exists(),
                                                self.step_error_msg(step='can not find next page toolbar. '))
                                self.del_rsv_policy_page.wait_for_loading_complete(2)
                                self.assertTrue(self.del_rsv_policy_page.btn_next.exists(),
                                                msg=self.step_error_msg(step='there is no button: Next'))
                                self.del_rsv_policy_page.btn_next.click()
                                flag_next_page = True
                                self.del_rsv_policy_page.wait_for_loading_complete(5)
                            else:
                                flag_next_page = False
                                logger.error(
                                    'Reservation policy:{} does not exist'.format(self.reservation_policy_name))

            logger.info(msg='Check whether delete reservation policy successful.')
            self.infra_page.back_to_infrastructure_default_page(self.current_browser)
            self._check_delete_rsv_policy_result(self.driver, self.del_rsv_policy_page.lbl_can_not_delete_xpath)

        except AssertionError:
            raise
        except:
            self.fail(sys.exc_info()[:2])

    def runTest(self):
        if self.reservation_policy_name is None:
            logger.warn('No reservation policy need to delete.')
        else:
            retry_times = 1
            max_times = DeleteReservationPolicy.MAX_TIMES_TO_CLOSE_RELAUNCH
            while retry_times <= max_times \
                    and self.test_delete_reservation_policy() == False:
                logger.debug('The {} time to close and relaunch browser'.format(retry_times), False)
                close_relaunch_browser_operation()
                self.current_browser = \
                    context_util.get_last_baseworkflow_instance().wf_context.shared.current_browser
                self.driver = self.current_browser.instance._browser.current
                retry_times += 1

            self.assertTrue(retry_times <= max_times,
                            self.step_error_msg(step='after {} times close and relaunch browser'.format(max_times)))

    def _validate_input_args(self, **kwargs):
        self.reservation_policy_name = self._kwargs.get('delete_rsv_policy_name')
        self.current_browser = self._kwargs.get('cur_browser')
        self.driver = self.current_browser.instance._browser.current

    def _finalize_output_params(self):
        pass

    def _check_delete_rsv_policy_result(self, driver, xpath):
        try:
            driver.switch_to.default_content()
            if self.del_rsv_policy_page.element_exists(xpath, driver, 5):
                if self.del_rsv_policy_page.element_exists(self.del_rsv_policy_page.xpath_failed_delete_detail_hidden,
                                                           driver, 5):
                    logger.info('Reservation policy:' + self.reservation_policy_name + 'delete successfully.')
                else:
                    self.assertTrue(self.del_rsv_policy_page.lbl_failed_delete_detail,
                                    self.step_error_msg(
                                        step='can not find the detail info of delete reservation policy failed info.'))
                    failed_detail = self.del_rsv_policy_page.lbl_failed_delete_detail.value
                    self.assertIsNotNone(failed_detail, self.step_error_msg(
                        step='the delete reservation policy failed info get is None.'))
                    self.del_rsv_policy_page.btn_close_cannot_delete.click()
                    self.fail(self.step_error_msg(step='cannot delete reservation policy ,' + failed_detail))
        except AssertionError:
            raise
        except:
            self.fail(sys.exc_info()[:2])
