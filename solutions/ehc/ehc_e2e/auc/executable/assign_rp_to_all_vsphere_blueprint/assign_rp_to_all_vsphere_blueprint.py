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
from ehc_e2e.auc.uimap.extension import WebFrame
from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.auc.uimap.shared.designpage import DesignPage
from ehc_e2e.auc.uimap.shared.loadingwindow import LoadingWindow
from ehc_e2e.auc.reusable.browser_relauncher import close_relaunch_browser_operation
from ehc_e2e.auc.reusable import context_util


class AssignRPtoAllvSphereBlueprint(BaseUseCase):
    MAX_TIMES_TO_CLOSE_RELAUNCH = 3

    def assertTrue(self, expr, msg=None):
        logger.info(msg, False, True)
        super(AssignRPtoAllvSphereBlueprint, self).assertTrue(
            expr,
            'Running on step: "Assign Reservation Policy to all vSphere Blueprints" - FAILED. Failed at: ' + msg)

    def test_assign_rp_to_all_vsphere_bluprint(self):
        design_page = DesignPage()
        driver_ref = self.current_browser.instance._browser.current
        if design_page.navigate_to_sub_page(self.current_browser, design_page.btn_blueprints):
            logger.info('Navigated to blueprint page', False, True)
        else:
            logger.warn('Navigate to blueprint page failed.')
            return False
        lnk_blueprint = design_page.get_blueprint_item_link(self.current_browser, self.blueprint)
        if lnk_blueprint:
            logger.info('Found blueprint ({}) link element'.format(self.blueprint), False, True)
        else:
            logger.warn('Find blueprint ({}) link element failed.'.format(self.blueprint))
            return False
        if design_page.click_blueprint_item_to_edit(self.current_browser, lnk_blueprint):
            logger.info('Go to blueprint editing page successfully.', False, True)
        else:
            logger.warn('Go to blueprint editing page failed.')
            return False

        # find all vsphere blueprint and set reservation policy
        with WebFrame(extensionid='com.vmware.vcac.core.design.blueprints.createoredit'):
            lbl_vsphere_bp_list = driver_ref.find_elements_by_xpath(
                '//div[contains(@class, "graph-node-arrow arrow-down")]/following-sibling::span')
            logger.info('Found {} vsphere blueprint(s) in total'.format(len(lbl_vsphere_bp_list)))

            for idx, lbl_vsphere_bp in enumerate(lbl_vsphere_bp_list):
                vsphere_bp_name = lbl_vsphere_bp.text
                # blueprint found in vRA not found in YAML -> FAIL
                self.assertTrue(vsphere_bp_name in self.bp_2_rp_dict,
                                'Check vsphere blueprint {} in vRA is valid in YAML'.format(vsphere_bp_name))
                rp = self.bp_2_rp_dict[vsphere_bp_name]
                del self.bp_2_rp_dict[vsphere_bp_name]

                lbl_vsphere_bp.click()
                LoadingWindow().wait_loading_infra_page(self.current_browser, timeout=10)
                design_page.wait_for_loading_complete(3)

                # set reservation policy
                self.assertTrue(design_page.btn_open_reservation_policy_dropdownlist.exists(),
                                'Find reservation policy dropdownlist')
                design_page.btn_open_reservation_policy_dropdownlist.click()
                design_page.wait_for_loading_complete(1)
                self.assertTrue(design_page.click_drop_down_list(design_page.lnk_reservation_policy_dropdownlist,
                                                                 'li', rp),
                                'Select reservation policy {} in dropdownlist'.format(rp))

                logger.info('Reservation policy assigned to vsphere blueprint {0} of {1}'.
                            format(idx+1, len(lbl_vsphere_bp_list)), False, True)

        # blueprint found in YAML not found in vRA -> FAIL
        self.assertTrue(len(self.bp_2_rp_dict) == 0,
                        'Check all vsphere blueprints defined in YAML are found in vRA,'
                        ' and have been associated with a reservation policy.')
        # done, submit
        self.assertTrue(design_page.finish_blueprint_edit(self.current_browser, self.blueprint),
                        'Failed to click "Finish" button.')
        logger.info('Assigned reservation policy to all vsphere machines.')

    def runTest(self):
        retry_times = 1
        max_times = AssignRPtoAllvSphereBlueprint.MAX_TIMES_TO_CLOSE_RELAUNCH
        while retry_times <= max_times \
                and self.test_assign_rp_to_all_vsphere_bluprint() is False:
            logger.debug('The {} time to close and relaunch browser'.format(retry_times), False)
            close_relaunch_browser_operation()
            self.current_browser = \
                context_util.get_last_baseworkflow_instance().wf_context.shared.current_browser

            retry_times += 1

        self.assertTrue(retry_times <= max_times,
                        '"Assign Reservation Policy to all vSphere Blueprints" - FAILED, '
                        'after {} times close and relaunch browser'.format(max_times))

    def _validate_context(self):
        self.current_browser = self.ctx_in.shared.current_browser
        assert hasattr(self.ctx_in, 'deploy_multiple_vms'), 'deploy_multiple_vms does not exist in YAML'

        self.blueprint = getattr(self.ctx_in.deploy_multiple_vms, 'blueprint', None)
        assert self.blueprint and isinstance(self.blueprint, str) and not self.blueprint.isspace(),\
            'deploy_multiple_vms.blueprint should be valid and not empty in YAML'

        self.vm_settings = getattr(self.ctx_in.deploy_multiple_vms, 'vm_settings', None)
        assert self.vm_settings, 'deploy_multiple_vms.vm_settings is invalid in YAML'

        self.bp_2_rp_dict = {}
        for vm_setting in self.vm_settings:
            vsphere_id = getattr(vm_setting, 'vsphere_id', None)
            assert vsphere_id and isinstance(vsphere_id, str) and not vsphere_id.isspace(),\
                'in deploy_multiple_vms.vm_settings: vsphere_id should be valid and not empty in YAML'
            rp = getattr(vm_setting, 'reservation_policy', None)
            assert rp and isinstance(rp, str) and not rp.isspace(),\
                'in deploy_multiple_vms.vm_settings: reservation_policy should be valid and not empty in YAML'
            assert vsphere_id not in self.bp_2_rp_dict, \
                'in deploy_multiple_vms.vm_settings: duplicated vsphere_id {}'.format(vsphere_id)
            self.bp_2_rp_dict[vsphere_id] = rp
