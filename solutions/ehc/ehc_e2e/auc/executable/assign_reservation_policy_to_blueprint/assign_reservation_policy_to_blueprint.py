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
from robot.api import logger
from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.auc.uimap.shared.basepage import BasePage
from ehc_e2e.auc.uimap.shared.designpage import DesignPage
from ehc_e2e.auc.reusable.browser_relauncher import close_relaunch_browser_operation
from ehc_e2e.auc.reusable import context_util


class AssignReservationPolicyToBlueprint(BaseUseCase):
    '''
    Will only pick 1st reservation policy from added_reservation_policy to assign
    to blueprints.
    blueprints: will check blueprints and then try to get its vSphere ID from blueprint_machine_pairs
    '''
    MAX_TIMES_TO_CLOSE_RELAUNCH = 3
    assign_reservation_policy_to_blueprint_succeed = False
    failure_formatter = \
        'Running on step:"Assign Reservation Policy To Blueprint"-FAILED, {}'.format

    def test_assign_reservation_policy_to_blueprint(self):
        try:
            design_page = DesignPage()
            ret_navigate_blueprints = design_page.navigate_to_sub_page(
                self.current_browser,
                design_page.btn_blueprints)
            if ret_navigate_blueprints:
                logger.info('Navigated to blueprint page.', False, True)
            else:
                logger.warn('Failed to navigate to blueprint page, try to close and relaunch '
                            'browser for a second attempt.')
                return False
            lnk_blueprint = design_page.get_blueprint_item_link(
                self.current_browser, self.blueprint_name)
            if lnk_blueprint:
                logger.info('blueprint {} is found.'.format(self.blueprint_name), False, True)
            else:
                logger.warn('blueprint {} is not found.'.format(self.blueprint_name))
                return False

            open_blueprint_to_edit = design_page.click_blueprint_item_to_edit(
                self.current_browser, lnk_blueprint)
            if open_blueprint_to_edit:
                logger.info('Switching to blueprint edit page', False, True)
            else:
                logger.warn('Failed to switch to blueprint edit page')
                return False

            open_vsphere_machine = design_page.click_vsphere_machine_item_to_edit(
                self.current_browser, self.machine_name
            )
            if open_vsphere_machine:
                logger.info('Clicked vSphere machine: {} to edit.'.format(self.machine_name), False, True)
            else:
                logger.warn('Failed to click vSphere machine: {} to edit.'.format(self.machine_name))
                return False

            _browser = self.current_browser.instance._browser.current

            self.assertTrue(
                design_page.btn_open_reservation_policy_dropdownlist.exists(),
                msg=self.failure_formatter('reservation policy dropdownlist open button does not exist.')
            )
            logger.info('Reservation Policy DropdownList open button exists.')
            BasePage().wait_for_loading_complete(3)
            # Reservation Policy DropdownList open button may be covered , send js to click
            _browser.execute_script('arguments[0].click();',
                                    design_page.btn_open_reservation_policy_dropdownlist.current)

            logger.info('Clicked Reservation Policy DropdownList open button.')
            BasePage().wait_for_loading_complete(3)
            self.assertTrue(
                design_page.click_drop_down_list(
                    design_page.lnk_reservation_policy_dropdownlist,
                    'li', self.reservation_policy_name),
                msg=self.failure_formatter(
                    'select reservation policy: {} from dropdownlist.'.format(self.reservation_policy_name))
            )
            logger.info('Reservation policy {} is found and set.'.format(
                self.reservation_policy_name), False, True)

            blueprint_edit_finish = design_page.finish_blueprint_edit(self.current_browser, self.blueprint_name)
            if blueprint_edit_finish:
                logger.info('Finished blueprint edit', False, True)
            else:
                logger.warn('Failed to finish blueprint edit')
                return False

            self.assigned_blueprints.append(self.blueprint_name)
            BasePage().wait_for_loading_complete(2)
        except:
            ex = sys.exc_info()
            logger.error('Encounter error in assign reservation policy to blueprint, detail info: {}'.format(ex))

    def runTest(self):
        retry_times = 1
        max_times = AssignReservationPolicyToBlueprint.MAX_TIMES_TO_CLOSE_RELAUNCH
        while retry_times <= max_times \
                and self.test_assign_reservation_policy_to_blueprint() is False:
            logger.debug('The {} time to close and relaunch browser'.format(retry_times), False)
            close_relaunch_browser_operation()
            self.current_browser = \
                context_util.get_last_baseworkflow_instance().wf_context.shared.current_browser

            retry_times += 1

        self.assertTrue(retry_times <= max_times,
                        self.failure_formatter('after {} times close and relaunch browser'.format(max_times)))

    def _validate_input_args(self, **kwargs):
        self.blueprint_name = self._kwargs.get('blueprint_name')
        self.machine_name = self._kwargs.get('machine_name')
        self.reservation_policy_name = self._kwargs.get('reservation_policy_name')
        self.current_browser = self._kwargs.get('current_browser')
        self.assigned_blueprints = []

    def _finalize_context(self):
        self._output.extend(self.assigned_blueprints)
        logger.info('Assigned reservation_policy: {} to blueprints: {}'.
                    format(self.reservation_policy_name, self.assigned_blueprints),
                    False, True)
