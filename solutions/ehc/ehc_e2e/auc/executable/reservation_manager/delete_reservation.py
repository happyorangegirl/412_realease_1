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
from ehc_e2e.auc.uimap.specific import ReservationPage
from ehc_e2e.auc.uimap.shared import InfrastructurePage, LoadingWindow
from ehc_e2e.auc.reusable import context_util
from ehc_e2e.auc.reusable.browser_relauncher import close_relaunch_browser_operation


class DeleteReservation(BaseUseCase):
    """This class is defined to delete reservation.
    """
    formatter = '"Running on step: Delete Reservation" - FAILED, {step}'
    reservation_delete_result = 'NG'
    MAX_TIMES_TO_CLOSE_RELAUNCH = 3

    def test_delete_reservation(self):
        try:
            # Navigate to create reservations page
            self.infrastructure_page = InfrastructurePage()
            self.delete_reservation_page = ReservationPage()

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

            target_reservation = \
                self.infrastructure_page.filter_reservation(self.current_browser, self.reservation)
            self.delete_reservation_page.wait_for_loading_complete(5)

            if target_reservation:
                self.assertTrue(self.delete_reservation_page.lbl_res_table.exists(),
                                msg=self.formatter.format(step='can not find the target {} reservation row.'
                                                          .format(self.reservation)))
                self.delete_reservation_page.lbl_res_table.click()
                logger.info('Selected target {} reservation row.'.format(self.reservation), False, True)
                self.delete_reservation_page.wait_for_loading_complete(3)

                self.assertTrue(
                    self.delete_reservation_page.btn_delete_res.exists(),
                    msg=self.formatter.format(step='can not find the Delete button.')
                )
                self.delete_reservation_page.btn_delete_res.click()
                logger.info('Clicked Delete button.', False, True)
                LoadingWindow().wait_loading_infra_page(self.current_browser, 5)
                self.assertTrue(
                    self.delete_reservation_page.btn_delete_res_OK.exists(),
                    msg=self.formatter.format(step='can not find OK button.')
                )
                self.delete_reservation_page.btn_delete_res_OK.click()
                logger.info('Clicked OK button.', False, True)
                self.delete_reservation_page.wait_for_loading_complete(3)
                self.reservation_delete_result = 'OK'
            else:
                self.reservation_delete_result = 'Not Find'

            if self.infrastructure_page.txt_reservation_name.exists():
                self.infrastructure_page.txt_reservation_name.set('')
            self.infrastructure_page.back_to_infrastructure_default_page(self.current_browser)

        except:
            logger.error(self.formatter.format(step='"Delete Reservation" encounters an error, more info: {}'
                                               .format(sys.exc_info()[:2])))
            raise

    def runTest(self):
        retry_times = 1
        max_times = DeleteReservation.MAX_TIMES_TO_CLOSE_RELAUNCH
        while retry_times <= max_times \
                and self.test_delete_reservation() is False:
            logger.debug('The {} time to close and relaunch browser'.format(retry_times), False)
            close_relaunch_browser_operation()
            self.current_browser = context_util.get_last_baseworkflow_instance().wf_context.shared.current_browser
            retry_times += 1

        self.assertTrue(retry_times <= max_times,
                        self.formatter.format(step='after {} times close and relaunch browser'.format(max_times)))

    def _validate_input_args(self, current_browser, is_login, reservation):
        assert current_browser is not None, \
            self.formatter.format(step='current_browser is None, may be there is no active browser.')
        self.assertTrue(is_login, msg=self.formatter.format(step='please login to vRA.'))
        self.assertIsNotNone(
            reservation,
            msg=self.formatter.format(step='reservations to be deleted are not provided.')
        )
        self.current_browser = current_browser
        self.reservation = reservation

    def _finalize_context(self):
        if self.reservation_delete_result == 'OK':
            logger.info('Reservation: {} is deleted successfully.'.format(self.reservation), False, True)
        elif self.reservation_delete_result == 'NG':
            logger.error(self.formatter.format(
                step='Delete Reservation {} failed, please delete it manually.'.format(self.reservation)))
        else:
            logger.info('No reservation matches the name given.')
