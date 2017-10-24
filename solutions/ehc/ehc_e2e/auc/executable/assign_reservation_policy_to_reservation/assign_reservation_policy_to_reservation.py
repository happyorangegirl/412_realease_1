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
from ehc_e2e.auc.reusable import context_util
from ehc_e2e.auc.reusable.browser_relauncher import close_relaunch_browser_operation
from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.auc.uimap.shared.basepage import BasePage
from ehc_e2e.auc.uimap.shared.infrastructurepage import InfrastructurePage
from ehc_e2e.auc.uimap.specific.reservation_page import ReservationPage


class AssignReservationPolicyToReservation(BaseUseCase):
    '''
    # Assign RP[0] to reservation[0], RP[1] to reservation[1] when both RPs and Reservations
            # contain 2 items this is workflow scenario from RP4VM.
            # otherwise, use 1st item as reservation policy name.
    '''

    MAX_TIMES_TO_CLOSE_RELAUNCH = 3
    failure_formatter = \
        'Running on step:"Assign Reservation Policy To Reservation" FAILED, {}'.format

    def test_assign_reservation_policy_to_reservation(self, reservation_name, reservation_policy_name):
        self.infrastructure_page = InfrastructurePage()
        reservation_page = ReservationPage()
        ret_navigate_dest = self.infrastructure_page.navigate_to_dest_page(
            self.current_browser, self.infrastructure_page.btn_reservations,
            self.infrastructure_page.btn_dest_reservations)

        if ret_navigate_dest:
            logger.info('Navigated to Infrastructure->Reservations.', False, True)
        else:
            logger.warn('Navigate to Infrastructure->Reservations failed.')
            return False

        lnk_reservation = self.infrastructure_page.filter_reservation(
            self.current_browser,
            reservation_name)

        self.assertIsNotNone(
            lnk_reservation,
            msg=self.failure_formatter(
                'reservation: {} is not found.'.format(reservation_name)
            )
        )

        self.assertTrue(
            self.infrastructure_page.select_reservation_to_edit(
                self.current_browser, lnk_reservation),
            self.failure_formatter(
                'failed to go to edit page of reservation {}.'.format(reservation_name)
            )
        )

        logger.info('Try to select reservation policy: {}'.format(
            reservation_policy_name
        ))
        self.assertTrue(
            reservation_page.btn_rsrvtn_policy.exists(),
            self.failure_formatter('reservation policy dropdown open button does not exist.')
        )
        reservation_page.btn_rsrvtn_policy.click()
        logger.info('Clicked button to open reservation policy dropdown.')

        self.assertTrue(
            BasePage().click_drop_down_list(
                reservation_page.lst_rsrvtn_policy, 'li',
                reservation_policy_name, strip_text=True),
            msg=self.failure_formatter(
                'failed to select reservation policy:{}.'.format(reservation_policy_name))
        )
        logger.info('Reservation policy {} is found and set.'.format(
            reservation_policy_name
        ), False, True)

        if self.infrastructure_page.navigate_to_reservation_detail_1st_frame(self.current_browser):
            logger.info('Switched back to "Reservations" first frame.', False, True)
        else:
            logger.warn('Switch back to "Reservations" first frame failed.')
            return False

        self.assertTrue(
            reservation_page.btn_ok.exists(),
            msg=self.failure_formatter(
                'reservation edit OK button not found.')
        )
        reservation_page.btn_ok.click()
        logger.info('Clicked "OK" button.', False, True)
        BasePage().wait_for_loading_complete(1)
        logger.info('Assigned Reservation policy {0} to {1} successful.'.format(reservation_policy_name,
                                                                                reservation_name), False, True)
        logger.info(
            'Assign Reservation policy {0} to reservation {1} is successful.'
            ''.format(reservation_policy_name, reservation_name)
        )
        self.list_reservations_assigned_reservation_policy.append(reservation_name)
        BasePage().wait_for_loading_complete(3)

        self.infrastructure_page.back_to_infrastructure_default_page(
            self.current_browser)

    def runTest(self):
        for i, reservation_name in enumerate(self.reservation_names):
            reservation_policy_name = self.reservation_policy_names[i] if len(
                self.reservation_policy_names) == 2 and len(
                    self.reservation_names) == 2 else self.reservation_policy_names[0]
            logger.info('Start to assign reservation policy: {} to reservation: {}'.
                        format(reservation_policy_name, reservation_name), False, True)

            retry_times = 1
            max_times = AssignReservationPolicyToReservation.MAX_TIMES_TO_CLOSE_RELAUNCH
            while retry_times <= max_times \
                    and self.test_assign_reservation_policy_to_reservation(reservation_name, reservation_policy_name) \
                    is False:
                logger.debug('The {} time to close and relaunch browser'.format(retry_times), False)
                close_relaunch_browser_operation()
                self.current_browser = context_util.get_last_baseworkflow_instance().wf_context.shared.current_browser
                retry_times += 1

            self.assertTrue(retry_times <= max_times,
                            self.failure_formatter('after {} times close and relaunch browser'.format(max_times)))

    def _validate_context(self):
        assert hasattr(self.ctx_in, 'added_reservation'), \
            self.failure_formatter('added_reservation attribute should exist in context object.')
        assert hasattr(self.ctx_in, 'added_reservation_policy'), \
            self.failure_formatter('added_reservation_policy name should be in context object')

        self.current_browser = self.ctx_in.shared.current_browser
        self.reservation_names = []
        self.reservation_policy_names = []
        # list to record reservations whose assign reservation policy succeeded.
        self.list_reservations_assigned_reservation_policy = []
        if self.ctx_in.added_reservation:
            logger.info(
                'Using "added_reservation" from YAML file as reservation names'
            )
            self.reservation_names = self.ctx_in.added_reservation
        else:
            logger.info(
                'Using "reservation_names" from assign_reservation_policy_to_reservation'
                ' in YAML data as reservation names.')
            self.reservation_names = \
                self.ctx_in.assign_reservation_policy_to_reservation.reservation_names

        if self.ctx_in.added_reservation_policy:
            logger.info(
                'Using "added_reservation_policy" from YAML file as reservation policy names.', False, True)
            self.reservation_policy_names = self.ctx_in.added_reservation_policy

        else:
            logger.info(
                'Using "reservation_policy_name" from assign_reservation_policy_to_reservation'
                ' in YAML data as reservation policy names.', False, True)
            self.reservation_policy_names = \
                self.ctx_in.assign_reservation_policy_to_reservation.reservation_policy_names

        assert len(self.reservation_policy_names) > 0, \
            self.failure_formatter('Reservation policy names used should not be empty.')
        assert len(self.reservation_names) > 0, self.failure_formatter('Reservation names should not be empty.')

    def _finalize_context(self):
        setattr(
            self.ctx_out,
            'assigned_reservation_policy_reservations',
            self.list_reservations_assigned_reservation_policy
        )
