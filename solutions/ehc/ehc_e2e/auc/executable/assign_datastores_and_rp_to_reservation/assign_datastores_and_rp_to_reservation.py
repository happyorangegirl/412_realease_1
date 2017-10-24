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
from selenium.webdriver.common.keys import Keys
from robot.api import logger
from ehc_e2e.auc.reusable import context_util
from ehc_e2e.auc.reusable.browser_relauncher import close_relaunch_browser_operation
from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.auc.uimap.shared.basepage import BasePage
from ehc_e2e.auc.uimap.shared import InfrastructurePage, LoadingWindow
from ehc_e2e.auc.uimap.specific.reservation_page import ReservationPage


class AssignDatastoresAndReservationPolicyToReservation(BaseUseCase):
    """
    # Assign [datasotores] to reservations.
             RP[0] to reservation[0], RP[1] to reservation[1] when both RPs and Reservations
             # contain 2 items this is workflow scenario from RP4VM.
             # otherwise, use 1st item as reservation policy name.
    """

    MAX_TIMES_TO_CLOSE_RELAUNCH = 3
    failure_formatter = \
        'Running on step: "Assign Datastores And Reservation Policy To Reservation" FAILED- {}'.format

    def test_assigns_datastores_and_reservation_policy_to_reservation(self):
        ret_navigate_dest = self.infrastructure_page.navigate_to_dest_page(
            self.current_browser, self.infrastructure_page.btn_reservations,
            self.infrastructure_page.btn_dest_reservations)

        if ret_navigate_dest:
            logger.info('Navigated to Infrastructure->Reservations.', False, True)
        else:
            logger.warn('Navigate to Infrastructure->Reservations failed.')
            return False
        # filtering reservation without tenant due to vra7.3 issue EHC-10020/ENGOPS1656
        logger.warn('Filtering reservation without tenant due to vra7.3 issue EHC-10020/ENGOPS1656.')
        lnk_reservation = self.infrastructure_page.filter_reservation(
            self.current_browser, self.reservation_name)

        self.assertIsNotNone(
            lnk_reservation,
            msg=self.failure_formatter(
                'reservation: {} is not found.'.format(self.reservation_name)
            )
        )
        self.assertTrue(
            self.infrastructure_page.select_reservation_to_edit(
                self.current_browser, lnk_reservation),
            self.failure_formatter(
                'go to edit page of reservation {}.'.format(self.reservation_name)
            )
        )
        logger.info('Try to select reservation policy: {}'.format(
            self.reservation_policy_name), False, True)
        self.assertTrue(
            self.reservation_page.btn_rsrvtn_policy.exists(),
            self.failure_formatter('reservation policy drop down open button does not exist.')
        )
        self.reservation_page.btn_rsrvtn_policy.click()
        logger.info('Clicked button to open reservation policy dropdown.')

        self.assertTrue(
            BasePage().click_drop_down_list(
                self.reservation_page.lst_rsrvtn_policy, 'li',
                self.reservation_policy_name, strip_text=True),
            msg=self.failure_formatter(
                'select reservation policy:{}.'.format(self.reservation_policy_name))
        )
        logger.info('Reservation policy {} is found and set.'.format(
            self.reservation_policy_name), False, True)
        LoadingWindow().wait_loading_infra_page(self.current_browser, 5)

        # Go to resources table and add provisioned datastores
        self.assertIsNotNone(self.reservation_page.tbl_resources.current.location_once_scrolled_into_view,
                             msg=self.failure_formatter('Can not scroll resources table button into view'))
        self.assertTrue(self.reservation_page.tbl_resources.exists(),
                        msg=self.failure_formatter('Can not find resources table'))
        self.reservation_page.tbl_resources.click()
        logger.info('Clicked resource tab.', False, True)
        LoadingWindow().wait_loading_infra_page(self.current_browser, 5)
        logger.info('Start to select datastores in resources.', False, True)

        self.assertIsNotNone(self.reservation_page.tbl_resources.current.location_once_scrolled_into_view,
                             msg=self.failure_formatter('Can not scroll resources table button into view'))
        self.select_specific_storages()

        if self.infrastructure_page.navigate_to_reservation_detail_1st_frame(self.current_browser):
            logger.info('Switched back to "Reservations" first frame.', False, True)
        else:
            logger.warn('Switch back to "Reservations" first frame failed.')
            return False
        self.assertTrue(
            self.reservation_page.btn_ok.exists(),
            msg=self.failure_formatter(
                'reservation edit OK button not found.')
        )
        self.reservation_page.btn_ok.click()
        logger.info('Clicked "OK" button.', False, True)
        BasePage().wait_for_loading_complete(10)
        self.current_browser.instance._browser.current.switch_to.default_content()
        self.assertFalse(
            self.reservation_page.lbl_reservation_save_error.exists(),
            msg=self.failure_formatter(
                'details: {}.'.format(
                    self.reservation_page.lbl_reservation_save_error.value)
            )
        )
        logger.info(
            'Assign Datastores: {0} and Reservation policy: {1} to reservation: {2} successful.'
            ''.format(self.tgt_datastores, self.reservation_policy_name, self.reservation_name), False, True
        )
        self.reservation_assigned = self.reservation_name

        self.infrastructure_page.back_to_infrastructure_default_page(
            self.current_browser)

    def select_specific_storages(self):
        """ Find and select the target storage path and storage priority
        """
        self.assertTrue(
            self.reservation_page.lbl_tbl_storage.exists(),
            msg=self.failure_formatter('Can not find storage table.')
        )
        logger.info('Storage list exists', False, True)
        storage_list = self.reservation_page.lbl_tbl_storage.current.find_elements_by_xpath(
            './table')
        for data_store in self.tgt_datastores:
            self.assertTrue(
                any(data_store.lower() in item.text.lower() for item in storage_list),
                msg=self.failure_formatter(
                    'Can not find the target storage with storage path:{}.'.format(data_store))
            )

        for i in range(len(storage_list)):

            self.assertIsNotNone(
                storage_list[i].location_once_scrolled_into_view,
                msg=self.failure_formatter('Can not scroll storage path into view.')
            )
            self.txt_storage_path = storage_list[i].find_element_by_xpath(self.reservation_page.txt_storage_path_xpath)
            self.assertTrue(
                self.txt_storage_path.is_displayed(),
                msg=self.failure_formatter('Can not find target storage path.'))
            storage_path_value = self.txt_storage_path.text
            logger.debug('Current storage is: "{}"'.format(storage_path_value))
            self.reservation_page.checkbox_storage_path = \
                storage_list[i].find_element_by_xpath(self.reservation_page.checkbox_storage_path_xpath)
            self.assertTrue(
                self.reservation_page.checkbox_storage_path.is_displayed(),
                msg=self.failure_formatter('Can not find target storage path checkbox')
            )
            checkbox_storage_path_class_attr = self.reservation_page.checkbox_storage_path.get_attribute('class')
            if storage_path_value in self.tgt_datastores:
                logger.info(
                    'Current storage: "{}" is in provided datastores: {}'.format(
                        storage_path_value, self.tgt_datastores), False, True)
                self.txt_physical = storage_list[i].find_element_by_xpath(
                    self.reservation_page.txt_physical_xpath)
                self.assertTrue(
                    self.txt_physical.is_displayed(),
                    msg=self.failure_formatter('Can not find target storage physical value.')
                )
                target_storage_physical_value = self.txt_physical.text
                logger.debug('Current value of physical is: {}'.format(target_storage_physical_value))
                if 'checked' in checkbox_storage_path_class_attr:
                    self.btn_storage_edit = storage_list[i].find_element_by_xpath(
                        self.reservation_page.btn_storage_edit_xpath)
                    self.assertTrue(
                        self.btn_storage_edit.is_displayed(),
                        msg=self.failure_formatter('Can not find target storage edit button.'))
                    self.btn_storage_edit.click()
                    logger.info(
                        'Current storage: "{}" is already selected, clicked edit button.'.format(storage_path_value),
                        False, True)
                else:
                    self.reservation_page.checkbox_storage_path.click()
                    logger.info(
                        'Current storage: "{}" is not selected, clicked checkbox.'.format(storage_path_value),
                        False, True)
                self.reservation_page.wait_for_loading_complete(3)
                # according to TAF-1610
                # set the value of 'This Reservation Reserved' = value of 'Physical'
                # set the value of 'Priority' = '1'
                self.fill_storage_info(target_storage_physical_value)
                storage_list = self.reservation_page.lbl_tbl_storage.current.find_elements_by_xpath(
                    './table')
                self.validate_edited_storage(storage_list[i], storage_path_value, target_storage_physical_value)

            elif 'checked' in checkbox_storage_path_class_attr:
                self.reservation_page.checkbox_storage_path.click()
                logger.info(
                    'Current storage: "{}" is not in provided datastores list, '
                    'clicked checkbox to unselect it.'.format(storage_path_value), False, True
                )
                self.reservation_page.wait_for_loading_complete(3)
                self.assertTrue(self.reservation_page.lbl_messagebox_toolbar.exists(),
                                msg=self.failure_formatter('Can not find message box.'))
                self.btn_messagebox_confirm = \
                    self.reservation_page.lbl_messagebox_toolbar.current.find_element_by_xpath(
                        self.reservation_page.btn_messagebox_toolbar_confirm_xpath)
                self.assertTrue(
                    self.btn_messagebox_confirm.is_displayed(),
                    self.failure_formatter('Can not find "Yes" button on message box.'))
                self.btn_messagebox_confirm.click()
                logger.warn('Cannot estimate disabled or not about the storage due to vra7.3 issue EHC10020/ENGOPS1654,'
                            ' unselected useless storage if it was selected.')
                logger.info('Clicked confirm button.', False, True)
                self.reservation_page.wait_for_loading_complete(3)
                storage_list = self.reservation_page.lbl_tbl_storage.current.find_elements_by_xpath(
                    './table')

                # Cannot estimate disabled or not about the storage due to vra7.3 issue EHC10020/ENGOPS1654.
                # self.txt_disabled = storage_list[i].find_element_by_xpath(
                #     self.reservation_page.txt_storage_disabled_xpath)
                # self.assertTrue(
                #     self.txt_disabled.is_displayed(),
                #     msg=self.failure_formatter('Can not find target storage disabled value.')
                # )
                # target_storage_disabled_value = self.txt_disabled.text
                # if target_storage_disabled_value == 'No':
                #     self.reservation_page.checkbox_storage_path.click()
                #     logger.info(
                #         'Current storage: "{}" not in provided datastores is selected with enabled situation, '
                #         'clicked checkbox to unselect.'.format(storage_path_value), False, True)
                #     self.reservation_page.wait_for_loading_complete(3)
                #     self.assertTrue(self.reservation_page.lbl_messagebox_toolbar.exists(),
                #                     msg=self.failure_formatter('Can not find message box.'))
                #     self.btn_messagebox_confirm = \
                #         self.reservation_page.lbl_messagebox_toolbar.current.find_element_by_xpath(
                #             self.reservation_page.btn_messagebox_toolbar_confirm_xpath)
                #     self.assertTrue(
                #         self.btn_messagebox_confirm.is_displayed(),
                #         self.failure_formatter('Can not find "Yes" button on message box.'))
                #     self.btn_messagebox_confirm.click()
                #     logger.info('Clicked confirm button.', False, True)
                #     self.reservation_page.wait_for_loading_complete(3)
                #     storage_list = self.reservation_page.lbl_tbl_storage.current.find_elements_by_xpath(
                #         './table')
                #
                # else:
                #     logger.info(
                #         'Current storage: {} not in provided datastores is selected but with disabled situation, '
                #         'do not any operations on it.'.format(storage_path_value), False, True)
            else:
                pass

    def validate_edited_storage(
            self, storage_row_obj, storage_path, storage_size,
            storage_priority='1', storage_selected_flag=True, storage_disabled='No'):
        logger.info('Start to validate edited storage.', False, True)
        self.storage_path = storage_row_obj.find_element_by_xpath(self.reservation_page.txt_storage_path_xpath)
        self.assertTrue(
            self.storage_path.is_displayed(),
            msg=self.failure_formatter('Can not find target storage path.'))
        edited_storage_path_value = self.storage_path.text
        self.reservation_page.checkbox_storage_path = \
            storage_row_obj.find_element_by_xpath(self.reservation_page.checkbox_storage_path_xpath)
        self.assertTrue(
            self.reservation_page.checkbox_storage_path.is_displayed(),
            msg=self.failure_formatter('Can not find target storage path checkbox')
        )
        edited_checkbox_storage_path_checked_flag = \
            'checked' in self.reservation_page.checkbox_storage_path.get_attribute('class')
        self.storage_size = storage_row_obj.find_element_by_xpath(self.reservation_page.txt_storage_size_xpath)
        self.assertTrue(
            self.storage_size.is_displayed(),
            msg=self.failure_formatter('Can not find target storage path.'))
        edited_storage_size_value = self.storage_size.text

        self.storage_priority = \
            storage_row_obj.find_element_by_xpath(self.reservation_page.txt_storage_priority_xpath)
        self.assertTrue(
            self.storage_priority.is_displayed(),
            msg=self.failure_formatter('Can not find target storage path.'))
        edited_storage_priority_value = self.storage_priority.text

        self.storage_disabled = \
            storage_row_obj.find_element_by_xpath(self.reservation_page.txt_storage_disabled_xpath)
        self.assertTrue(
            self.storage_disabled.is_displayed(),
            msg=self.failure_formatter('Can not find target storage disabled cell.'))
        edited_storage_disabled_value = self.storage_disabled.text
        if (edited_storage_path_value == storage_path) \
                and (edited_checkbox_storage_path_checked_flag == storage_selected_flag) \
                and (edited_storage_size_value == storage_size) \
                and (edited_storage_priority_value == storage_priority)\
                and (edited_storage_disabled_value == storage_disabled):
            logger.info('Storage: "{}" was edited correctly.'.format(storage_path), False, True)
        else:
            logger.error('Storage: "{}" was not edited correctly, but continue next step.'.format(storage_path))

    def navigate_to_iframe(self, element_attribute_id):
        """ Navigate to specific iframe
        """
        try:
            _browser = self.current_browser.instance._browser.current
            iframe_id = self.infrastructure_page.get_accurate_frameid(
                self.current_browser,
                element_attribute_id,
                False,
                'extensionid')
            self.assertIsNotNone(iframe_id,
                                 msg=self.failure_formatter(
                                     'Can not find iframe id{}.'.format(element_attribute_id)))
            logger.info('{} found.'.format(element_attribute_id), False, True)
            _browser.switch_to.frame(iframe_id)
            logger.info(
                'Infrastructure page navigated destination page, switched to'
                ' {}.'.format(element_attribute_id), False, True)
        except:
            logger.error(
                'Switching to reservation edit detail first frame encounters error: {}'
                ''.format(sys.exc_info()[:2])
            )
            return False

        return True

    def fill_storage_info(self, storage_size, disabled=False, storage_priority='1'):
        logger.info('Start to fill info in storage edit grid.', False, True)
        self.assertTrue(self.reservation_page.lbl_storage_edit_grid.exists(),
                        msg=self.failure_formatter('Can not find target storage grid'))
        self.storage_edit_row = self.reservation_page.lbl_storage_edit_grid.current.find_element_by_xpath(
            self.reservation_page.storage_edit_row_xpath)
        self.assertTrue(self.storage_edit_row.is_displayed(),
                        msg=self.failure_formatter('Can not find target storage editing row.'))
        logger.info('Found target storage editing row', False, True)
        # Storage size
        self.txt_storage_size = self.storage_edit_row.find_element_by_xpath(
            self.reservation_page.txt_edit_storage_size_xpath)
        self.assertTrue(
            self.txt_storage_size.is_displayed(),
            msg=self.failure_formatter('Can not find target storage size input')
        )
        # self.txt_storage_size.send_keys(Keys.BACKSPACE)
        self.txt_storage_size.clear()
        self.txt_storage_size.send_keys(storage_size)
        logger.info('Set storage size: {}'.format(storage_size), False, True)
        # storage priority
        self.txt_storage_priority = self.storage_edit_row.find_element_by_xpath(
            self.reservation_page.txt_edit_storage_priority_xpath)
        self.assertTrue(
            self.txt_storage_priority.is_displayed(),
            msg=self.failure_formatter('Can not find target storage priority input')
        )
        self.txt_storage_priority.send_keys(Keys.BACKSPACE)
        self.txt_storage_priority.send_keys(storage_priority)
        logger.info('Set storage priority: {}'.format(storage_priority), False, True)
        # storage disabled
        self.checkbox_storage_disabled = self.storage_edit_row.find_element_by_xpath(
            self.reservation_page.checkbox_edit_storage_disabled_xpath
        )
        self.assertTrue(
            self.checkbox_storage_disabled.is_displayed(),
            msg=self.failure_formatter('Can not find target storage disabled input')
        )
        cell_storage_disabled = self.storage_edit_row.find_element_by_xpath(
            self.reservation_page.cell_edit_storage_disabled_xpath
        )
        disabled_checked_flag = 'checked' in cell_storage_disabled.get_attribute('class')
        if disabled != disabled_checked_flag:
            self.checkbox_storage_disabled.click()
        logger.info('Set storage disabled: {}'.format(disabled), False, True)
        # Confirm
        self.btn_confirm_storage = self.reservation_page.lbl_edit_storage_confirm.current.find_element_by_xpath(
            self.reservation_page.btn_edit_confirm_storage_xpath)
        self.assertTrue(
            self.btn_confirm_storage.is_displayed(),
            msg=self.failure_formatter('Can not find target storage confirm buton')
        )
        self.btn_confirm_storage.click()
        self.reservation_page.wait_for_loading_complete(3)
        logger.info('Confirmed storage', False, True)

    def runTest(self):
        logger.info('Start to assign datastores: {} and reservation policy: {} to reservation: {}'.
                    format(self.tgt_datastores, self.reservation_policy_name, self.reservation_name),
                    False, True)
        retry_times = 1
        max_times = AssignDatastoresAndReservationPolicyToReservation.MAX_TIMES_TO_CLOSE_RELAUNCH
        while retry_times <= max_times \
                and self.test_assigns_datastores_and_reservation_policy_to_reservation() is False:
            logger.debug('The {} time to close and relaunch browser'.format(retry_times), False)
            close_relaunch_browser_operation()
            self.current_browser = \
                context_util.get_last_baseworkflow_instance().wf_context.shared.current_browser
            retry_times += 1
        self.assertTrue(retry_times <= max_times,
                        self.failure_formatter(
                            'after {} times close and relaunch browser'.format(max_times))
                        )

    def _validate_input_args(self, **kwargs):
        self.infrastructure_page = InfrastructurePage()
        self.reservation_page = ReservationPage()
        self.current_browser = kwargs.get('current_browser')
        self.tgt_datastores = kwargs.get('storages')
        self.tenant_name = kwargs.get('tenant_name')
        self.reservation_name = kwargs.get('reservation_name')
        self.reservation_policy_name = kwargs.get('reservation_policy')
        self.reservation_assigned = None

    def _finalize_output_params(self):
        self._output.append(self.reservation_assigned)