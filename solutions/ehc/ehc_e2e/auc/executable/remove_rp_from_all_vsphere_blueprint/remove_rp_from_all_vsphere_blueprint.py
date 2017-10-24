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


class RemoveRPfromAllvSphereBlueprint(BaseUseCase):

    def assertTrue(self, expr, msg=None):
        logger.info(msg, False, True)
        super(RemoveRPfromAllvSphereBlueprint, self).\
            assertTrue(expr,
                       'Running on step: "Remove Reservation Policy from all vSphere Blueprints" - FAILED. Failed at: '
                       + msg)

    def test_remove_rp_from_all_vsphere_bluprint(self):
        design_page = DesignPage()
        driver_ref = self.current_browser.instance._browser.current

        self.assertTrue(design_page.navigate_to_design(self.current_browser), 'Navigate to design page')
        self.assertTrue(design_page.navigate_to_sub_page(self.current_browser, design_page.btn_blueprints),
                        'Navigate to blueprint page')
        lnk_blueprint = design_page.get_blueprint_item_link(self.current_browser, self.blueprint)
        self.assertTrue(lnk_blueprint is not None, 'Find blueprint name link element')
        self.assertTrue(design_page.click_blueprint_item_to_edit(self.current_browser, lnk_blueprint),
                        'Go to blueprint editing page')

        # find all vsphere machine blueprint and set reservation policy
        with WebFrame(extensionid='com.vmware.vcac.core.design.blueprints.createoredit'):
            lbl_vsphere_bp_list = driver_ref.find_elements_by_xpath('//div[@class="graph-node-footer-text"]')
            self.assertTrue(len(lbl_vsphere_bp_list) > 0, 'Check there is at least 1 vsphere machine blueprint')
            logger.info('Found {} vsphere machine blueprint(s) in total'.format(len(lbl_vsphere_bp_list)), False, True)

            for idx, lbl_vsphere_bp in enumerate(lbl_vsphere_bp_list):
                lbl_vsphere_bp.click()
                LoadingWindow().wait_loading_infra_page(self.current_browser, timeout=10)
                design_page.wait_for_loading_complete(3)

                # set reservation policy
                self.assertTrue(design_page.btn_open_reservation_policy_dropdownlist.exists(),
                                'Find reservation policy dropdownlist')
                design_page.btn_open_reservation_policy_dropdownlist.click()
                design_page.wait_for_loading_complete(1)
                self.assertTrue(
                    design_page.click_drop_down_list(design_page.lnk_reservation_policy_dropdownlist, 'li', ''),
                    'reservation policy dropdownlist to blank')

                logger.info('Reservation policy removed from vsphere machine blueprint {0} of {1}'.
                            format(idx+1, len(lbl_vsphere_bp_list)))

        # done, submit
        self.assertTrue(design_page.finish_blueprint_edit(self.current_browser, self.blueprint),
                        'Failed to click "Finish" button.')

        logger.info('Removed reservation policy from all vsphere machines.')

    def runTest(self):
        self.test_remove_rp_from_all_vsphere_bluprint()

    def _validate_context(self):
        assert self.ctx_in.deploy_multiple_vms.blueprint is not None, \
            'deploy_multiple_vms.blueprint is required in YAML file'
        self.blueprint = self.ctx_in.deploy_multiple_vms.blueprint
        self.current_browser = self.ctx_in.shared.current_browser
