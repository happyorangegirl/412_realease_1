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
from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.auc.uimap.specific import ReservationPolicyPage
from ehc_e2e.auc.uimap.shared import InfrastructurePage
from ehc_e2e.auc.reusable import context_util
from ehc_e2e.auc.reusable.browser_relauncher import close_relaunch_browser_operation
from robot.api import logger


class CreateReservationPolicy(BaseUseCase):
    MAX_TIMES_TO_CLOSE_RELAUNCH = 3

    def __init__(self, name=None, method_name='runTest', **kwargs):
        super(CreateReservationPolicy, self).__init__(name, method_name, **kwargs)
        self.added_rsv_policy = None
        self.step_error_msg = 'Running on step: "Create Reservation Policy" - FAILED, {step}'.format

    def test_create_reservation_policy(self):
        self.infra_page = InfrastructurePage()
        self.rsv_policy_page = ReservationPolicyPage()
        self.new_rsv_policy_name = self.rsv_policy_name + '-' + self.infra_page.make_timestamp(
            '%y-%m-%d-%I-%M-%S')
        logger.info(
            'Transformed reservation policy name from:{} to:{}'.format(
                self.rsv_policy_name, self.new_rsv_policy_name), False, True)
        # switch to create reservation poliy frame
        if self.infra_page.navigate_to_dest_page(self.current_browser,
                                                 self.infra_page.btn_reservations,
                                                 self.infra_page.btn_dest_reservation_policies):
            logger.info('Navigated to infrastructure frame and clicked destination "Reservation Policies" button.',
                        False, True)
        else:
            logger.warn('Navigate to infrastructure frame and click destination "Reservation Policies" button failed.')
            return False

        if self.infra_page.navigate_to_iframe(self.current_browser, attribute_name='extensionid',
                                              url_in_attribute=\
                                                      self.infra_page.infra_reservation_policy_edit_frame_extensionid):
            logger.info('Navigated to "Reservation Policies" frame.', False, True)
        else:
            logger.warn('Navigate to "Reservation Policies" frame failed.')
            return False

        logger.info(msg='Start to click New Reservation Policy Button')
        self.assertTrue(self.rsv_policy_page.btn_new_rsv_policy.exists(),
                        msg=self.step_error_msg(step='there is no button: New Reservation Policy'))
        self.rsv_policy_page.btn_new_rsv_policy.click()
        self.infra_page.wait_for_loading_complete(2)
        logger.info(msg='Start to fill name and description of New Reservation Policy')
        self.assertTrue(self.rsv_policy_page.txt_create_rsv_policy_name.exists(),
                        msg=self.step_error_msg(step='there is no input textbox: name'))
        self.rsv_policy_page.txt_create_rsv_policy_name.set(self.new_rsv_policy_name)
        logger.info('Filled reservation policy name: {0}'.format(self.new_rsv_policy_name))
        self.infra_page.wait_for_loading_complete(1)
        self.assertTrue(self.rsv_policy_page.txt_create_rsv_policy_description.exists(),
                        msg=self.step_error_msg(step='there is no input textbox: Description'))
        self.rsv_policy_page.txt_create_rsv_policy_description.set(self.new_rsv_policy_description)
        self.infra_page.wait_for_loading_complete(2)
        self.assertTrue(self.rsv_policy_page.btn_img_save.exists(),
                        msg=self.step_error_msg(step='there is no button: OK'))
        self.rsv_policy_page.btn_img_save.click()

        self.infra_page.wait_for_loading_complete(3)

        logger.info(msg='Check whether create reservation policy successful.')
        self.infra_page.back_to_infrastructure_default_page(self.current_browser)

        self._check_create_rsv_policy_result(self.driver, self.rsv_policy_page.lbl_can_not_save_xpath)
        self.infra_page.wait_for_loading_complete(3)
        self.added_rsv_policy = self.new_rsv_policy_name

    def runTest(self):
        retry_times = 1
        max_times = CreateReservationPolicy.MAX_TIMES_TO_CLOSE_RELAUNCH
        while retry_times <= max_times \
                and self.test_create_reservation_policy() == False:
            logger.debug('The {} time to close and relaunch browser'.format(retry_times), False)
            close_relaunch_browser_operation()
            self.current_browser = \
                context_util.get_last_baseworkflow_instance().wf_context.shared.current_browser
            self.driver = self.current_browser.instance._browser.current
            retry_times += 1
        self.assertTrue(retry_times <= max_times,
                        self.step_error_msg(step='after {} times close and relaunch browser'.format(max_times)))

    def _validate_input_args(self, **kwargs):
        self.rsv_policy_name = self._kwargs.get('reservation_policy_name')
        self.new_rsv_policy_description = 'test_add_reservation_policy'
        self.current_browser = self._kwargs.get('cur_browser')
        self.driver = self.current_browser.instance._browser.current

    def _finalize_output_params(self):
        self._output.append(self.added_rsv_policy)

    def _check_create_rsv_policy_result(self, driver, xpath):

        try:
            driver.switch_to.default_content()
            if self.rsv_policy_page.element_exists(xpath, driver, 5):
                if self.rsv_policy_page.element_exists(self.rsv_policy_page.xpath_failed_detail_hidden, driver, 5):
                    logger.info('Reservation policy:' + self.new_rsv_policy_name + 'create successfully.')
                else:
                    failed_detail = self.rsv_policy_page.lbl_failed_detail.value
                    self.assertIsNotNone(failed_detail, 'The create reservation policy failed info get is None.')
                    detail_text = failed_detail.split(self.new_rsv_policy_name)
                    if len(detail_text) == 2 and detail_text[0].strip() == "The reservation policy name" \
                            and detail_text[1].strip() == "exists.":
                        self.added_rsv_policy = self.new_rsv_policy_name
                        self.rsv_policy_page.btn_close_cannot_create.click()
                        logger.warn('Reservation policy already exists:' + self.new_rsv_policy_name)
                    else:
                        self.fail('Cannot save reservation policy,' + failed_detail)
        except AssertionError:
            raise
        except:
            self.fail(sys.exc_info()[:2])
