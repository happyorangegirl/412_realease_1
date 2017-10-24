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

from robot.api import logger
from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.auc.uimap.shared.basepage import BasePage
from ehc_e2e.auc.uimap.shared.designpage import DesignPage
from ehc_e2e.auc.reusable.browser_relauncher import close_relaunch_browser_operation
from ehc_e2e.auc.reusable import context_util


class AssignStorageReservationPolicyToBlueprint(BaseUseCase):
    '''
    Will use storage reservation policy retrieved from vRO provisioned cloud storage.

    blueprints: will use blueprints from blueprint_machine_pairs, srp from added_cloud_storage.
                1st cloud_storage's srp will be assigned to 1st blueprint
                2nd cloud_storage's srp will be assigned to 2nd blueprint.
    '''
    MAX_TIMES_TO_CLOSE_RELAUNCH = 3

    failure_formatter = \
        'Running on step:"Assign Storage Reservation Policy To Blueprint"-FAILED, {}'.format

    def test_assign_storage_reservation_policy_to_blueprint(self, blueprint_name, srp):
        design_page = DesignPage()

        ret_navigate_blueprints = design_page.navigate_to_sub_page(
            self.current_browser,
            design_page.btn_blueprints)
        if ret_navigate_blueprints:
            logger.info('Navigated to blueprint page', False, True)
        else:
            logger.warn('Navigate to blueprint page failed.')
            return False

        machine_name = self.blueprint_machine_pairs.get(blueprint_name)
        self.assertIsNotNone(machine_name, msg=self.failure_formatter('vSphere ID is None.'))
        lnk_blueprint = design_page.get_blueprint_item_link(
            self.current_browser, blueprint_name)
        self.assertIsNotNone(
            lnk_blueprint,
            msg=self.failure_formatter('blueprint {} is not found.'.format(blueprint_name))
            )

        open_blueprint_to_edit = design_page.click_blueprint_item_to_edit(
            self.current_browser, lnk_blueprint)
        if open_blueprint_to_edit:
            logger.info('Clicked blueprint to open edit page.', False, True)
        else:
            logger.warn('Click blueprint to open edit page failed.')
            return False

        open_vsphere_machine = design_page.click_vsphere_machine_item_to_edit(
            self.current_browser, machine_name
        )

        if open_vsphere_machine:
            logger.info('Clicked vSphere machine: {} to edit.'.format(machine_name), False, True)
        else:
            logger.warn('Click vSphere machine: {} to edit failed..'.format(machine_name))
            return False

        self.assertTrue(
            design_page.lnk_storage_tab.exists(),
            msg=self.failure_formatter('Storage tab does not exist.')
        )
        design_page.lnk_storage_tab.click()
        BasePage().wait_for_loading_complete(1)
        self.assertTrue(
            design_page.lnk_storage_first_row.exists(),
            msg=self.failure_formatter('storage reservation policy first item does not exist.')
        )
        design_page.lnk_storage_first_row.click()
        self.assertTrue(
            design_page.btn_storage_edit.exists(),
            msg=self.failure_formatter('storage resrvation policy edit button does not exist.')
        )
        design_page.btn_storage_edit.click()
        BasePage().wait_for_loading_complete(1)
        self.assertTrue(
            design_page.btn_storage_reservation_policy_dropdownlist_open.exists(),
            msg=self.failure_formatter('storage reseration policy dropdown open button does not exist.')
        )
        design_page.btn_storage_reservation_policy_dropdownlist_open.click()
        BasePage().wait_for_loading_complete(1)
        self.assertTrue(
            BasePage().click_drop_down_list(
                design_page.lnk_storage_reservation_policy_dropdownlist,
                'li', srp),
            msg=self.failure_formatter(
                'select storage reservation policy: {} from dropdownlist.'.format(srp))
        )

        if design_page.btn_ok_in_floading_window.exists():
            design_page.btn_ok_in_floading_window.click()
            logger.info(
                'Storage reservation policy {} is found and set.'.format(
                    srp), False, True)

        self.assertTrue(design_page.finish_blueprint_edit(self.current_browser, blueprint_name),
                        'Failed to click "Finish" button.')
        logger.info('Assigned srp: {} to blueprint: {}'.format(srp, blueprint_name), False, True)
        self.assigned_blueprints.append(blueprint_name)
        BasePage().wait_for_loading_complete(2)

    def runTest(self):

        for i, blueprint_name in enumerate(self.blueprint_names):
            srps = self.added_cloud_storage_list[i].srp
            srp = srps[0] if srps else None
            if srp:
                logger.info(
                    'Retrieved srp:{} from added_cloud_storage for No. {} provisioned storage '.format(srp, i))
            else:
                self.assertIsNotNone(srps, msg=self.failure_formatter(
                    'no srp found from added_cloud_storage for cloud storage No. {}'.format(i)))
            retry_times = 1
            max_times = AssignStorageReservationPolicyToBlueprint.MAX_TIMES_TO_CLOSE_RELAUNCH
            while retry_times <= max_times \
                    and self.test_assign_storage_reservation_policy_to_blueprint(blueprint_name, srp) is False:
                logger.debug('The {} time to close and relaunch browser'.format(retry_times), False)
                close_relaunch_browser_operation()
                self.current_browser = \
                    context_util.get_last_baseworkflow_instance().wf_context.shared.current_browser

                retry_times += 1

            self.assertTrue(retry_times <= max_times,
                            self.failure_formatter('after {} times close and relaunch browser'.format(max_times))
                           )

    def _validate_context(self):
        assert self.ctx_in.blueprint_machine_pairs is not None, \
            'blueprint_machine_pairs should contain blueprint-machine pairs.'
        self.current_browser = self.ctx_in.shared.current_browser
        self.blueprint_names = []
        self.assigned_blueprints = []
        self.blueprint_machine_pairs = self.ctx_in.blueprint_machine_pairs.__dict__
        self.added_cloud_storage_list = self.ctx_in.added_cloud_storage

        logger.info(
            'Using "blueprint_names" from assign_reservation_policy_to_blueprint'
            'in YAML data as blueprint names.')
        self.blueprint_names = (self.blueprint_machine_pairs.keys() if self.blueprint_machine_pairs
                                else None)

        assert self.blueprint_names and len(self.blueprint_names) > 0, 'Blueprint names should not be empty.'
        assert self.added_cloud_storage_list and len(self.added_cloud_storage_list) > 0, \
            'there is no provisioned cloud storage.'
        for cloud_storage in self.added_cloud_storage_list:
            assert cloud_storage.name is not None, 'No datastore provisioned.'
            assert len(cloud_storage.srp) > 0, 'No Storage Reservation Policy detected, can not assign.'

    def _finalize_context(self):
        setattr(self.ctx_out, 'assigned_storage_reservation_policy_blueprints', self.assigned_blueprints)
        logger.info('assigned_storage_reservation_policy_blueprints: {}'.format(self.assigned_blueprints),)
