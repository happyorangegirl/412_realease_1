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
import re
import string
import time
from selenium.webdriver.common.keys import Keys
from robot.api import logger
from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.auc.uimap.specific import ReservationPage
from ehc_e2e.auc.uimap.shared import InfrastructurePage, LoadingWindow
from ehc_e2e.auc.reusable import context_util
from ehc_e2e.auc.reusable.browser_relauncher import close_relaunch_browser_operation


class CreateReservation(BaseUseCase):
    """This class is defined to create reservation.

    """
    MAX_TIMES_TO_CLOSE_RELAUNCH = 3
    _formatter = '"Running on step: Create Reservation" - FAILED, {step}'

    def test_create_reservation(self):
        """Create reservation UI operations.
        return:
            None
        """
        try:
            self.create_rsrvtn_page = ReservationPage()
            _browser = self.current_browser.instance._browser.current
            _navigate_to_reservations_subpage = self.infrastructure_page.navigate_to_dest_page(
                self.current_browser,
                self.infrastructure_page.btn_reservations,
                self.infrastructure_page.btn_dest_reservations
            )

            if _navigate_to_reservations_subpage:
                logger.info('Navigated to infrastructure frame and '
                            'clicked destination "Reservations" button.', False, True)
            else:
                logger.warn('Navigate to infrastructure frame and click destination "Reservations" button failed.')
                return False

            self.create_rsrvtn_page.wait_for_loading_complete(5)
            # Navigate to reservation iframe
            if self.navigate_to_iframe(self.create_rsrvtn_page.rservation_extensionid):
                logger.info('Navigated to "Reservations" first details frame.', False, True)
            else:
                logger.warn('Navigate to "Reservations" first frame failed.')
                return False

            # Create new vSphere reservation
            self.assertTrue(self.create_rsrvtn_page.btn_new_rsrvtn.exists(),
                            msg=self._formatter.format(step='Can not find new reservation button.')
                           )
            self.create_rsrvtn_page.btn_new_rsrvtn.click()
            logger.info('Clicked new reservation button', False, True)

            LoadingWindow().wait_loading_infra_page(self.current_browser, 5)
            self.assertTrue(self.create_rsrvtn_page.tbl_popup_rsrvtn_type.exists(),
                            msg=self._formatter.format(step='Can not find new reservation type list.')
                           )
            logger.info('Reservation type list exists', False, True)
            _click_result = self.create_rsrvtn_page.click_drop_down_list(
                self.create_rsrvtn_page.tbl_popup_rsrvtn_type,
                'div',
                self.reservation_type
            )
            self.assertTrue(_click_result,
                            msg=self._formatter.format(step='Can not select vSphere reservation type'))

            LoadingWindow().wait_loading_infra_page(self.current_browser, 5)
            logger.info('Start to create new vSphere virtual reservation.', False, True)
            self.create_rsrvtn_page.wait_for_loading_complete(5)
            # Navigate to reservation details iframe
            if self.navigate_to_iframe(self.create_rsrvtn_page.rservation_detaild_extensionid):
                logger.info('Navigated to "Reservations" second details frame.', False, True)
            else:
                logger.warn('Navigate to "Reservations" second details frame failed.')
                return False

            # Reservation information
            self.assertIsNotNone(self.create_rsrvtn_page.tbl_general_info.current.location_once_scrolled_into_view,
                                 msg=self._formatter.format(
                                     step='Can not scroll general information table button into view'))

            self.assertTrue(self.create_rsrvtn_page.tbl_general_info.exists(),
                            msg=self._formatter.format(step='Can not fill in general information'))
            self.create_rsrvtn_page.tbl_general_info.click()
            logger.info('Start to fill in reservation general information', False, True)

            # Reservation name
            self.assertTrue(self.create_rsrvtn_page.txt_rsrvtn_name.exists(),
                            msg=self._formatter.format(step='Can not find reservation name input'))
            self.create_rsrvtn_page.wait_for_loading_complete(5)
            self.create_rsrvtn_page.txt_rsrvtn_name.set(self.rsrvtn_name)
            logger.info('Typed in reservation name: {}'.format(self.rsrvtn_name), False, True)
            # Tenant
            self.create_rsrvtn_page.wait_for_loading_complete(5)
            self.assertTrue(self.create_rsrvtn_page.btn_tenant.exists(),
                            msg=self._formatter.format(step='Can not find tenant button.'))
            self.create_rsrvtn_page.btn_tenant.click()
            LoadingWindow().wait_loading_infra_page(self.current_browser, 5)
            if self.create_rsrvtn_page.lst_tenant.exists():
                logger.info('Find tenants list.', False, True)
            else:
                logger.warn('Can not find tenants list.')
                return False

            _click_result = self.create_rsrvtn_page.click_drop_down_list(self.create_rsrvtn_page.lst_tenant,
                                                                         'li',
                                                                         self.tenant)
            if not _click_result:
                logger.warn('Can not select tenant: {}.'.format(self.tenant))
                return False
            self.create_rsrvtn_page.wait_for_loading_complete(5)
            self.create_rsrvtn_page.tbl_general_info.click()
            logger.info('Selected tenant: {}'.format(self.tenant), False, True)
            # UI BUG WORKAROUND
            logger.debug('waiting 5 seconds')
            self.create_rsrvtn_page.wait_for_loading_complete(5)
            logger.debug('Waiting infra')
            LoadingWindow().wait_loading_infra_page(self.current_browser, 5)
            self.create_rsrvtn_page.wait_for_loading_complete(5)
            logger.info('Workround for tenant table not disappearing')

            # Business group
            self.assertTrue(self.create_rsrvtn_page.btn_bsns_grp.exists(),
                            msg=self._formatter.format(step='Can not find business group button.'))
            self.create_rsrvtn_page.btn_bsns_grp.click()
            logger.info('Clicked business group button')
            logger.debug('Waiting 5 seconds')
            LoadingWindow().wait_loading_infra_page(self.current_browser, 5)
            self.assertIsNotNone(self.create_rsrvtn_page.tbl_resources.current.location_once_scrolled_into_view,
                                 msg=self._formatter.format(step='Can not scroll resources table button into view'))
            _click_result = self.create_rsrvtn_page.click_drop_down_list(
                self.create_rsrvtn_page.lst_bsns_grp,
                'li',
                self.bsns_grp
            )
            time.sleep(5)
            self.assertTrue(_click_result, msg=self._formatter.format(step='Can not select business group.'))
            logger.info('Selected business group: {}'.format(self.bsns_grp))
            # Priority
            self.assertTrue(self.create_rsrvtn_page.dwnkey_priority.exists(),
                            msg=self._formatter.format(step='Can not find reservation priority label.'))
            logger.info('Clicking priority', False, True)
            self.create_rsrvtn_page.dwnkey_priority.click()

            self.create_rsrvtn_page.txt_priority.set(Keys.BACKSPACE)
            logger.info('Typed key back space', False, True)

            self.create_rsrvtn_page.txt_priority.set(self.rsvrtn_priority)
            logger.info('Typed reservation priority: {}'.format(self.rsvrtn_priority), False, True)

            # Go to resources table
            self.assertIsNotNone(self.create_rsrvtn_page.tbl_resources.current.location_once_scrolled_into_view,
                                 msg=self._formatter.format(step='Can not scroll resources table button into view'))
            self.assertTrue(self.create_rsrvtn_page.tbl_resources.exists(),
                            msg=self._formatter.format(step='Can not find resources table'))
            self.create_rsrvtn_page.tbl_resources.click()
            logger.info('Clicked resource tab.', False, True)
            LoadingWindow().wait_loading_infra_page(self.current_browser, 5)
            logger.info('Start to fill in resources.', False, True)

            # Computer resource
            self.assertIsNotNone(self.create_rsrvtn_page.tbl_resources.current.location_once_scrolled_into_view,
                                 msg=self._formatter.format(step='Can not scroll resources table button into view'))
            self.assertTrue(self.create_rsrvtn_page.btn_cmptr_rsrce.exists(),
                            msg=self._formatter.format(step='Can not select computer resource'))
            self.create_rsrvtn_page.btn_cmptr_rsrce.click()
            time.sleep(2)
            self.assertIsNotNone(self.create_rsrvtn_page.tbl_resources.current.location_once_scrolled_into_view,
                                 msg=self._formatter.format(step='Can not scroll resources table button into view'))
            _click_result = \
                self.create_rsrvtn_page.click_drop_down_list(
                    self.create_rsrvtn_page.lst_cmptr_rsrce,
                    'li',
                    self.computer_resource, True, True)
            time.sleep(2)
            LoadingWindow().wait_loading_infra_page(self.current_browser, 5)
            self.assertTrue(_click_result, msg=self._formatter.format(step='Can not select computer resource'))
            logger.info('Selected computer resource: {}'.format(self.computer_resource), False, True)

            # Memory
            self.assertTrue(
                self.create_rsrvtn_page.txt_memory.exists(),
                msg=self._formatter.format(step='Can not find memory input')
            )
            logger.info('Text memory input exists')
            self.create_rsrvtn_page.dwnkey_memory.click()
            time.sleep(2)
            self.create_rsrvtn_page.txt_memory.set(Keys.BACKSPACE)
            time.sleep(2)
            self.create_rsrvtn_page.txt_memory.set(self.memory)
            time.sleep(2)
            logger.info('Set memory: {}'.format(self.memory), False, True)
            # Storage size and storage priority
            self.assertTrue(self.select_specific_storage(),
                            msg=self._formatter.format(step='Can not set target storage information.'))

            # Network
            self.assertIsNotNone(self.create_rsrvtn_page.tbl_network.current.location_once_scrolled_into_view,
                                 msg=self._formatter.format(step='Can not scroll network table button into view'))
            self.assertTrue(self.create_rsrvtn_page.tbl_network.exists(),
                            msg=self._formatter.format(step='Can not find network table'))
            self.create_rsrvtn_page.tbl_network.click()
            LoadingWindow().wait_loading_infra_page(self.current_browser, 5)
            logger.info('Clicked network tab', False, True)
            # Network path
            if self.network_path != 'unknown':
                self.assertTrue(self.select_specific_network(self.network_path, self.network_profile),
                                msg=self._formatter.format(
                                    step='Can not select specific network path and network profile.'))
            self.assertIsNotNone(
                self.create_rsrvtn_page.btn_ok.current.location_once_scrolled_into_view,
                msg=self._formatter.format(step='Can not scroll to OK button of network table')
            )

            # Navigate to reservation iframe
            if self.infrastructure_page.navigate_to_reservation_detail_1st_frame(self.current_browser):
                logger.info('Switched back to "Reservations" first frame.', False, True)
            else:
                logger.warn('Switch back to "Reservations" first frame failed.')
                return False

            self.assertTrue(self.create_rsrvtn_page.btn_ok.exists(),
                            msg=self._formatter.format(step='Can not find OK button.')
                           )
            self.assertIsNotNone(
                self.create_rsrvtn_page.btn_ok.current.location_once_scrolled_into_view,
                msg=self._formatter.format(step='Can not scroll ok button into view.')
            )
            self.create_rsrvtn_page.btn_ok.click()
            LoadingWindow().wait_loading_infra_page(self.current_browser, 5)
            logger.info('Clicked ok button', False, True)
            # Reservation name should be unique when compared to other existed ones
            self.create_rsrvtn_page.wait_for_loading_complete(2)
            _browser.switch_to.default_content()
            self.create_rsrvtn_page.wait_for_loading_complete(2)
            if self.create_rsrvtn_page.lbl_cant_save_rsrvtn.exists():
                logger.info('Clicked "OK" button, but "Cancel" button still exists.', False, True)
                # Navigate back to reservation iframe and cancel creating
                # Navigate to reservation iframe
                if self.infrastructure_page.navigate_to_reservation_detail_1st_frame(self.current_browser):
                    logger.info('Switched back to  to "Reservations" first frame.', False, True)
                else:
                    logger.warn('Switch back to  to "Reservations" first frame failed.')
                    return False

                self.create_rsrvtn_page.wait_for_loading_complete(2)
                self.assertTrue(self.create_rsrvtn_page.btn_cancel.exists(),
                                msg=self._formatter.format(step='Can not find cancel button.')
                               )
                self.create_rsrvtn_page.btn_cancel.click()
                logger.info('Clicked cancel button', False, True)
                LoadingWindow().wait_loading_infra_page(self.current_browser, 5)
                logger.warn(
                    'Reservation already exists, check if the reservation is configured as expected.'
                )
                self.created_resrvation.append(self.rsrvtn_name)
            else:
                # Navigate back to reservation iframe and Check if the reservation is created successfully
                LoadingWindow().wait_loading_infra_page(self.current_browser, 5)
                if self.infrastructure_page.filter_reservation(self.current_browser, self.rsrvtn_name):
                    logger.info('Found target reservation: {}.'.format(self.rsrvtn_name), False, True)
                else:
                    logger.warn('Can not find the reservation created.')
                    return False
                self.created_resrvation.append(self.rsrvtn_name)
                logger.info('Reservation: {} is created.'.format(self.rsrvtn_name), False, True)

            self.infrastructure_page.back_to_infrastructure_default_page(self.current_browser)
        except:
            logger.error('"Create Reservation" encounters an error, more info: {}'
                         .format(sys.exc_info()[:2]))
            raise

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
                                 msg=self._formatter.format(
                                     step='Can not find iframe id{}.'.format(element_attribute_id)))
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

    def select_specific_storage(self):
        """ Find and select the target storage path and storage priority
        """
        self.assertTrue(
            self.create_rsrvtn_page.lbl_tbl_storage.exists(),
            msg=self._formatter.format(step='Can not find storage table')
        )
        logger.info('Storage list exists')
        storage_list = self.create_rsrvtn_page.lbl_tbl_storage.current.find_elements_by_xpath(
            './table')

        self.assertTrue(
            any(self.tgt_datastore.lower() in item.text.lower() for item in storage_list),
            msg=self._formatter.format(
                step='Can not find the target storage with storage path:{}.'.format(self.tgt_datastore)
            )
        )

        # for index, item in enumerate(storage_list):
        for item in storage_list:
            self.assertIsNotNone(
                item.location_once_scrolled_into_view,
                msg=self._formatter.format(step='Can not scroll storage path into view.')
            )
            if self.tgt_datastore != '' and self.tgt_datastore in item.text:
                self.create_rsrvtn_page.checkbox_storage_path = \
                    item.find_element_by_xpath(self.create_rsrvtn_page.checkbox_storage_path_xpath)
                self.assertTrue(
                    self.create_rsrvtn_page.checkbox_storage_path.is_displayed(),
                    msg=self._formatter.format(step='Can not find target storage path checkbox')
                )
                self.create_rsrvtn_page.checkbox_storage_path.click()
                self.create_rsrvtn_page.wait_for_loading_complete(3)
                self.assertTrue(self.create_rsrvtn_page.lbl_storage_edit_grid.exists(),
                                msg=self._formatter.format(step='Can not find target storage grid'))
                self.storage_edit_row = self.create_rsrvtn_page.lbl_storage_edit_grid.current.find_element_by_xpath(
                    self.create_rsrvtn_page.storage_edit_row_xpath)
                self.assertTrue(self.storage_edit_row.is_displayed(),
                                msg=self._formatter.format(step='Can not find target storage editing row.'))
                self.assertTrue(self.tgt_datastore in self.storage_edit_row.text,
                                msg=self._formatter.format(step='The storage editing row is found wrongly.'))
                logger.info('Found target storage editing row', False, True)
                # Storage size
                self.txt_storage_size = self.storage_edit_row.find_element_by_xpath(
                    self.create_rsrvtn_page.txt_edit_storage_size_xpath)
                self.assertTrue(
                    self.txt_storage_size.is_displayed(),
                    msg=self._formatter.format(step='Can not find target storage size input')
                )
                self.txt_storage_size.send_keys(Keys.BACKSPACE)
                self.txt_storage_size.send_keys(self.storage_size)
                logger.info('Set storage size: {}'.format(self.storage_size), False, True)
                # storage priority
                self.txt_storage_priority = self.storage_edit_row.find_element_by_xpath(
                    self.create_rsrvtn_page.txt_edit_storage_priority_xpath)
                self.assertTrue(
                    self.txt_storage_priority.is_displayed(),
                    msg=self._formatter.format(step='Can not find target storage priority input')
                )
                self.txt_storage_priority.send_keys(Keys.BACKSPACE)
                self.txt_storage_priority.send_keys(self.storage_priority)
                logger.info('Set storage priority: {}'.format(self.storage_priority), False, True)
                # Confirm
                self.btn_confirm_storage = \
                    self.create_rsrvtn_page.lbl_edit_storage_confirm.current.find_element_by_xpath(
                        self.create_rsrvtn_page.btn_edit_confirm_storage_xpath)
                self.assertTrue(
                    self.btn_confirm_storage.is_displayed(),
                    msg=self._formatter.format(step='Can not find target storage confirm buton')
                )
                self.btn_confirm_storage.click()
                logger.info('Confirmed storage', False, True)
                return True

        logger.error(
            'Can not find the target storage with storage path:{}.'.format(self.tgt_datastore))
        return False

    def select_specific_network(self, network_path, network_profile):
        """Select specific network path and network profile.
        """
        self.tbl_network_paths = self.current_browser.instance._browser.current.find_element_by_xpath(
            self.create_rsrvtn_page.tbl_network_paths_xpath)

        self.assertTrue(self.tbl_network_paths.is_displayed(),
                        msg=self._formatter.format(step='Can not find network paths table'))
        network_path_elements = self.tbl_network_paths.find_elements_by_xpath('./table')
        self.assertTrue(
            any(network_path.lower() in item.text.lower() for item in network_path_elements),
            msg=self._formatter.format(
                step='Can not find the given network path:{}'.format(network_path.lower())
            )
        )

        for item in network_path_elements:
        # for index, item in enumerate(network_path_elements):
            self.assertIsNotNone(
                item.location_once_scrolled_into_view,
                msg=self._formatter.format(step='Can not scroll network path into view.')
            )

            if network_path.lower() in item.text.lower():
                self.create_rsrvtn_page.checkbox_network_path = \
                    item.find_element_by_xpath(
                        self.create_rsrvtn_page.checkbox_network_path_xpath
                    )
                self.assertTrue(
                    self.create_rsrvtn_page.checkbox_network_path.is_displayed(),
                    msg=self._formatter.format(step='Can not find target network path checkbox')
                )
                logger.info('Found target network path checkbox', False, True)
                self.create_rsrvtn_page.checkbox_network_path.click()
                logger.info('Selected network path: {}'.format(network_path), False, True)
                # Network profile
                if network_profile != 'unknown':
                    logger.info('Trying to set network profile:{}'.format(network_profile))
                    self.create_rsrvtn_page.btn_network_profile = item.find_element_by_xpath(
                        self.create_rsrvtn_page.btn_network_profile_xpath
                    )
                    self.assertTrue(
                        self.create_rsrvtn_page.btn_network_profile.is_displayed(),
                        msg=self._formatter.format(step='Can not find target network profile button')
                    )
                    logger.info('Found target network profile button', False, True)

                    btn_network_profile_id = self.create_rsrvtn_page.btn_network_profile.get_attribute('id')
                    re_pattern = re.compile(r'\d+')
                    num_in_btn_profile_id = re_pattern.search(btn_network_profile_id).group(0)
                    num_in_list_profile = str(string.atoi(num_in_btn_profile_id) + 1)
                    lst_network_profile_xpath = '//*[@id="boundlist-' + num_in_list_profile + '-listEl"]'

                    self.create_rsrvtn_page.btn_network_profile.click()
                    LoadingWindow().wait_loading_infra_page(self.current_browser, 5)
                    self.create_rsrvtn_page.lst_network_profile = \
                        self.current_browser.instance._browser.current.find_element_by_xpath(
                            lst_network_profile_xpath
                        )
                    self.create_rsrvtn_page.wait_for_loading_complete(5)
                    self.assertTrue(
                        self.create_rsrvtn_page.lst_network_profile.is_displayed(),
                        msg=self._formatter.format(step='Can not find target network profile table')
                    )
                    logger.info('Found target network profile table', False, True)
                    self.assertTrue(self.create_rsrvtn_page.click_drop_down_list(
                        self.create_rsrvtn_page.lst_network_profile,
                        'li',
                        network_profile,
                        strip_text=True),
                                    msg='Can not select network profile:{}'.format(network_profile))
                    logger.info('Selected network profile: {}'.format(network_profile), False, True)
                else:
                    logger.info('Network profile is configured as "unknown", leave to vRA to set default.')

                return True

        return False

    def runTest(self):
        """To create reservation, add successfully created reservation name.

        :return: None
        """
        self.created_resrvation = []
        # Navigate to create reservations page
        self.infrastructure_page = InfrastructurePage()
        for index, item in enumerate(self.create_reservation_list):
            self.cluster_name = self.added_cloud_storage_list[index].cluster_name
            self.tgt_datastore = self.added_cloud_storage_list[index].name[0]
            self.rsrvtn_name = item.reservation_name + '-' + self.infrastructure_page.make_timestamp(
                '%y-%m-%d-%I-%M-%S')
            logger.info(
                'Transformed reservation name from:{} to:{}'.format(
                    item.reservation_name, self.rsrvtn_name), False, True)
            self.tenant = self.ctx_in.vra.tenant
            self.reservation_type = item.reservation_type
            self.bsns_grp = self.ctx_in.vra.business_group
            self.rsvrtn_priority = item.reservation_priority
            self.computer_resource = item.computer_resource
            self.memory = item.memory
            self.storage_size = item.storage_size
            self.storage_priority = item.storage_priority
            self.network_path = item.network_path
            self.network_profile = item.network_profile

            retry_times = 1
            max_times = CreateReservation.MAX_TIMES_TO_CLOSE_RELAUNCH
            while retry_times <= max_times \
                    and self.test_create_reservation() is False:
                logger.debug('The {} time to close and relaunch browser'.format(retry_times), False)
                close_relaunch_browser_operation()
                self.current_browser = context_util.get_last_baseworkflow_instance().wf_context.shared.current_browser
                self.infrastructure_page = InfrastructurePage()
                retry_times += 1

            self.assertTrue(retry_times <= max_times,
                            self._formatter.format(step='after {} times close and relaunch browser'.format(max_times)))

    def _validate_context(self):
        """Validation check for input parameters.

        :return:
        """
        if self.ctx_in:
            self.assertTrue(self.ctx_in.shared.current_browser.is_login,
                            msg='Please login to vRA.')
            self.current_browser = self.ctx_in.shared.current_browser
            self.assertIsNotNone(self.ctx_in.vra,
                                 msg='vRA information is not provided.')
            for key, value in self.ctx_in.vra.__dict__.iteritems():
                self.assertIsNotNone(value, msg='{} is not provided.'.format(key))

            self.create_reservation_list = self.ctx_in.create_reservation
            self.assertTrue(isinstance(self.create_reservation_list, list),
                            msg='Reservation customer provided info is not list type.')
            self.assertTrue(len(self.create_reservation_list) > 0,
                            msg="yaml data of create reservation is not provided."
                           )
            self.added_cloud_storage_list = self.ctx_in.added_cloud_storage
            self.assertTrue(isinstance(self.added_cloud_storage_list, list),
                            msg='Added cloud storage is not list type.')
            self.assertTrue(len(self.added_cloud_storage_list) > 0,
                            msg='Target datastore is not provided.'
                           )

            for index, item in enumerate(self.create_reservation_list):
                for key, value in item.__dict__.iteritems():
                    self.assertIsNotNone(value, msg='{} from create_reservation is not provided'.format(key))

                self.assertTrue(isinstance(self.added_cloud_storage_list[index].name, list),
                                msg='Added data store name from added_cloud_storage is not list type.')
                self.assertTrue(len(self.added_cloud_storage_list[index].name) > 0,
                                msg='Target data store from added_cloud_storage is not provided.')
                self.assertIsNotNone(self.added_cloud_storage_list[index].cluster_name,
                                     msg='cluster_name from added_cloud_storage is not provided.')

    def _finalize_context(self):
        """ Save successfully created reservation name and its policy name

        :return:
        """
        setattr(self.ctx_out, 'added_reservation', self.created_resrvation)

