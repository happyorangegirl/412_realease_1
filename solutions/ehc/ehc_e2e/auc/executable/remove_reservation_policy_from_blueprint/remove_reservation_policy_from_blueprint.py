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
from ehc_e2e.auc.uimap.shared.designpage import DesignPage
from ehc_e2e.auc.reusable import context_util
from ehc_e2e.auc.reusable.browser_relauncher import close_relaunch_browser_operation


class RemoveReservationPolicyFromBlueprint(BaseUseCase):
    MAX_TIMES_TO_CLOSE_RELAUNCH = 3
    failure_formatter = \
        'Running on step:"Remove Reservation Policy From Blueprint" - FAILED, {}'.format

    def test_remove_reservation_policy_from_blueprint(self):
        design_page = DesignPage()
        for blueprint_name in self.blueprint_names:
            design_page.navigate_to_design(self.current_browser)
            logger.info('Navigated to Design page.', False, True)
            ret_navigate_blueprints = design_page.navigate_to_sub_page(
                self.current_browser, design_page.btn_blueprints)
            if ret_navigate_blueprints:
                logger.info('Navigated to blueprint page.', False, True)
            else:
                logger.warn('Navigate to blueprint page failed.')
                return False

            machine_name = self.blueprint_machine_pairs.get(blueprint_name)
            lnk_blueprint = design_page.get_blueprint_item_link(
                self.current_browser, blueprint_name)
            if lnk_blueprint:
                logger.info('Blueprint {} is found.'.format(blueprint_name), False, True)
            else:
                logger.warn('Blueprint {} is not found.'.format(blueprint_name))
                return False

            open_blueprint_to_edit = design_page.click_blueprint_item_to_edit(
                self.current_browser, lnk_blueprint)
            if open_blueprint_to_edit:
                logger.info('Switched to blueprint edit page', False, True)
            else:
                logger.warn('Switch to blueprint edit page failed')
                return False

            open_vsphere_machine = design_page.click_vsphere_machine_item_to_edit(
                self.current_browser, machine_name)
            if open_vsphere_machine:
                logger.info('Clicked vSphere machine: {} to edit.'.format(machine_name), False, True)
            else:
                logger.warn('Click vSphere machine: {} to edit failed.'.format(machine_name))
                return False

            _browser = self.current_browser.instance._browser.current

            self.assertTrue(
                design_page.btn_open_reservation_policy_dropdownlist.exists(),
                msg=self.failure_formatter('reservation policy dropdownlist open button does not exist.')
            )
            logger.info('Reservation Policy DropdownList open button exists.')

            # Reservation Policy DropdownList open button may be covered , send js to click

            _browser.execute_script('arguments[0].click();',
                                    design_page.btn_open_reservation_policy_dropdownlist.current)
            # design_page.btn_open_reservation_policy_dropdownlist.click()
            BasePage().wait_for_loading_complete(1)
            self.assertTrue(BasePage().click_drop_down_list(
                design_page.lnk_reservation_policy_dropdownlist, 'li', ''),
                            msg=self.failure_formatter(
                                'remove reservation policy from blueprint: {}'.format(blueprint_name))
                           )
            logger.info('Reservation policy is removed from blueprint :{}.'.format(
                blueprint_name), False, True)

            finish_blueprint_edit = design_page.finish_blueprint_edit(self.current_browser,
                                                                      blueprint_name)
            if finish_blueprint_edit:
                logger.info('Clicked "Finish" button to finish blueprint edit.', False, True)
            else:
                logger.warn('Click "Finish" button failed')
                return False
            BasePage().wait_for_loading_complete(3)

    def runTest(self):
        if not self.blueprint_names:
            logger.warn(
                msg='No Blueprint in {} is assigned with reservation policy!'.format(self.origin_blueprint_names))
            return
        logger.debug(msg='blueprint_names are: {}'.format(self.blueprint_names))
        retry_times = 1
        max_times = RemoveReservationPolicyFromBlueprint.MAX_TIMES_TO_CLOSE_RELAUNCH
        while retry_times <= max_times \
                and self.test_remove_reservation_policy_from_blueprint() is False:

            logger.debug('The {} time to close and relaunch browser'.format(retry_times), False)
            close_relaunch_browser_operation()
            self.current_browser = \
                context_util.get_last_baseworkflow_instance().wf_context.shared.current_browser

            retry_times += 1

        self.assertTrue(retry_times <= max_times,
                        self.failure_formatter('after {} times close and relaunch browser'.format(max_times)))

    def _validate_context(self):
        assert self.ctx_in.blueprints is not None, \
            self.failure_formatter('blueprints in YAML should not be None.')
        assert self.ctx_in.blueprint_machine_pairs is not None, \
            self.failure_formatter('blueprint_machine_pairs should contain blueprint-machine pairs.')
        self.origin_blueprint_names = getattr(self.ctx_in, 'blueprints', [])
        self.current_browser = self.ctx_in.shared.current_browser
        if not isinstance(getattr(self.ctx_in, 'assigned_reservation_policy_blueprints', None), list):
            setattr(self.ctx_in, 'assigned_reservation_policy_blueprints', [])
        self.blueprint_names = getattr(self.ctx_in, 'assigned_reservation_policy_blueprints')
        self.blueprint_machine_pairs = self.ctx_in.blueprint_machine_pairs.__dict__

        for blueprint in self.blueprint_names:
            machine = self.blueprint_machine_pairs.get(blueprint)
            logger.debug(msg="Blueprint: {}, vSphere_machine ID:{}".format(blueprint, machine))
            assert machine is not None, self.failure_formatter(
                '"vSphere_machine ID" is not found for blueprint: {0} in "blueprint_machine_pairs"'.format(blueprint))

    def _finalize_context(self):
        pass
