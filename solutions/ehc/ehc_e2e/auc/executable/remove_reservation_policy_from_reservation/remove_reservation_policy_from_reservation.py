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
from ehc_e2e.auc.uimap.shared.basepage import BasePage
from ehc_e2e.auc.uimap.shared.infrastructurepage import InfrastructurePage
from ehc_e2e.auc.uimap.specific.reservation_page import ReservationPage


class RemoveReservationPolicyFromReservation(BaseUseCase):
    failure_formatter = \
        'Running on step:"Remove Reservation Policy From Reservation" - FAILED, {}'.format

    def test_remove_reservation_policy_from_reservation(self):
        self.infrastructure_page = InfrastructurePage()
        reservation_page = ReservationPage()
        for reservation_name in self.reservation_names:
            ret_navigate_dest = self.infrastructure_page.navigate_to_dest_page(
                self.current_browser, self.infrastructure_page.btn_reservations,
                self.infrastructure_page.btn_dest_reservations)
            self.assertTrue(
                ret_navigate_dest,
                msg=self.failure_formatter('failed to navigate to reservations page.'))
            logger.info('Navigated to Infrastructure->reservations.', False, True)

            lnk_reservation = self.infrastructure_page.filter_reservation(
                self.current_browser, reservation_name)

            self.assertIsNotNone(
                lnk_reservation,
                self.failure_formatter('reservation {} is not found.'.format(reservation_name))
            )

            self.assertTrue(
                self.infrastructure_page.select_reservation_to_edit(
                    self.current_browser, lnk_reservation),
                self.failure_formatter(
                    'failed to go to edit page of reservation {}.'.format(reservation_name)
                )
            )

            logger.info(
                'Try to set reservation policy to empty for Reservation: {}'
                ''.format(reservation_name)
            )
            self.assertTrue(
                reservation_page.txt_reservation_policy.exists(),
                msg=self.failure_formatter(
                    'reservation policy edit textbox does not exist.')
            )
            self.assertTrue(
                reservation_page.btn_rsrvtn_policy.exists(),
                msg=self.failure_formatter('open reservation policy dropdownlist button does not exist.')
            )
            reservation_page.btn_rsrvtn_policy.click()
            BasePage().wait_for_loading_complete(1)
            self.assertTrue(BasePage().click_drop_down_list(
                reservation_page.lst_rsrvtn_policy, 'li', '', True),
                            self.failure_formatter(
                                'can not remove reservation policy from reservation: {}.'.format(reservation_name))
                           )

            logger.info('Reservation policy is removed for Reservation {}.'.format(
                reservation_name), False, True)

            self.infrastructure_page.navigate_to_reservation_detail_1st_frame(
                self.current_browser)
            self.assertTrue(
                reservation_page.btn_ok.exists(),
                self.failure_formatter('reservation edit OK button not found.')
            )
            reservation_page.btn_ok.click()
            BasePage().wait_for_loading_complete(1)

            logger.info(
                'Reservation policy is removed from reservation {0}.'
                ''.format(reservation_name), False, True)
            BasePage().wait_for_loading_complete(2)

    def runTest(self):
        if not self.reservation_names:
            logger.warn(
                msg='No reservation is assigned with reservation policy, no need to remove!')
            return
        self.test_remove_reservation_policy_from_reservation()

    def _validate_context(self):
        if not isinstance(getattr(self.ctx_in, 'assigned_reservation_policy_reservations', None), list):
            setattr(self.ctx_in, 'assigned_reservation_policy_reservations', [])

        self.current_browser = self.ctx_in.shared.current_browser
        self.reservation_names = self.ctx_in.assigned_reservation_policy_reservations

    def _finalize_context(self):
        if self.reservation_names:
            infrastructure_page = InfrastructurePage()
            infrastructure_page.back_to_infrastructure_default_page(
                self.current_browser)
