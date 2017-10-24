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
from ehc_e2e.auc.uimap.specific import OperateVMPage
from ehc_e2e.auc.uimap.shared import RequestsPage, LoadingWindow, BasePage, MainPage
from ehc_e2e.auc.reusable import PageNavigator
from ehc_e2e.auc.reusable import context_util
from ehc_e2e.auc.reusable.browser_relauncher import close_relaunch_browser_operation


class OperateVM(BaseUseCase):
    MAX_TIMES_TO_CLOSE_RELAUNCH = 3
    _formatter = 'Running on step: "Take Basic Actions On Target VMs" - FAILED, {step}'
    _all_vms_perfect_flag = False

    def test_operations_on_vm(self):
        self.basepage = BasePage()
        self.operatevmpage = OperateVMPage(self.test_vm_name)

        try:
            self.assertTrue(self.navigate_to_items_page(self.current_browser),
                            msg=self._formatter.format(step='failed to switch to items page'))

            # basic actions sequence
            # define the operation order based on the status of the vm received just now
            basic_actions = {'Off': ['Power On', 'Reboot', 'Power Off'],
                             'On': ['Power Off', 'Power On', 'Reboot']}
            test_vm_status = ''
            _time_out = 600
            while _time_out > 0:
                self._switch_to_target_item_frame()
                self._click_vm_link()
                self.operatevmpage.wait_for_loading_complete(20)
                _time_out -= 20
                self._switch_to_target_detail_frame()
                logger.info("Navigate to Item Details innerFrame page to get the vm's status.")

                self.assertTrue(
                    self.operatevmpage.lbl_vm_status.exists(),
                    msg=self._formatter.format(step='the label Status does not exist.')
                )
                test_vm_status = self.operatevmpage.lbl_vm_status.value
                if test_vm_status == 'TurningOn' \
                        or test_vm_status == 'TurningOff' \
                        or test_vm_status == 'Rebooting':
                    logger.info(
                        'The current status of the vm {0} is : {1}. Can not take next operation.'
                            .format(self.test_vm_name, test_vm_status))
                    self._switch_to_target_item_frame()
                    self._click_cancel_button()
                else:
                    logger.info(
                        'The current status of the vm {0} is : {1}.'.format(self.test_vm_name,
                                                                            test_vm_status)
                    )
                    break

            if _time_out <= 0:
                logger.error(
                    "The vm's status is still {}, exceeded timeout !".format(test_vm_status)
                )
            else:
                self._switch_to_target_item_frame()
                request_res = True
                if len(self.user_action_list) > 0:
                    _target_action_list = self.user_action_list
                else:
                    _target_action_list = basic_actions[test_vm_status]

                for counter, action in enumerate(_target_action_list):
                    logger.info('Go to take action {0} on target vm {1}'.
                                format(action, self.test_vm_name))
                    if counter == 0 and len(self.user_action_list) > 0 and test_vm_status in action:
                        logger.info(
                            "The current status of the vm {0} is {1}, don't need to take action {2}. "
                                    .format(self.test_vm_name, test_vm_status, action)
                        )
                        self._all_vms_perfect_flag = True
                        self._click_cancel_button()
                        break
                    if counter == len(_target_action_list) - 1:
                        last_action_flag = True
                    else:
                        last_action_flag = False

                    if action == 'Power Off':
                        request_res = self.power_off_vm(action, last_action_flag)
                    elif action == 'Power On':
                        request_res = self.power_on_vm(action, last_action_flag)
                    elif action == 'Reboot':
                        request_res = self.reboot_vm(action, last_action_flag)
                    else:
                        logger.error("The vm's status must be in On|Off.")
                    logger.debug('Return request_res is: {}'.format(request_res))
                    if not request_res:
                        return request_res

        except:
            ex = sys.exc_info()
            self._switch_to_target_item_frame()
            logger.error(
                'Take basic actions on vm {0} encounters error : {1}.'.format(self.test_vm_name, ex)
            )
            self.operatevmpage.cancel_or_close_request()
            raise

    def power_off_vm(self, action, last_action_flag):
        request_res = False
        for find_power_off_time in range(0, 60):
            if self.operatevmpage.btn_poweroff.exists():
                self.operatevmpage.btn_poweroff.click()
                logger.info("Click Power Off button.")
                self.operatevmpage.wait_for_loading_complete(2)
                self._click_submit_button()
                self._click_OK_button()
                try:
                    request_res = self.get_request_result(action, self.test_vm_name)
                except:
                    request_res = False
                    logger.debug('Get request result failed.')

                if request_res:
                    self.assertTrue(self.navigate_to_items_page(self.current_browser),
                                    msg=self._formatter.format(step='failed to switch to items page'))
                    self.operatevmpage.wait_for_loading_complete(10)
                    self._switch_to_target_item_frame()
                    self.finish_tailing_work(last_action_flag, self.test_vm_name, 'Off')
                break
            else:
                self._check_button_exists(find_power_off_time, 'Power Off')
        return request_res

    def power_on_vm(self, action, last_action_flag):
        request_res = True
        for find_power_on_time in range(0, 60):
            if self.operatevmpage.btn_poweron.exists():
                self.operatevmpage.btn_poweron.click()
                logger.info("Clicked Power On button.")
                self.operatevmpage.wait_for_loading_complete(2)
                self._click_submit_button()
                self._click_OK_button()
                request_res = self.get_request_result(action, self.test_vm_name)
                if request_res:
                    self.assertTrue(self.navigate_to_items_page(self.current_browser),
                                    msg=self._formatter.format(step='failed to switch to items page'))
                    self.operatevmpage.wait_for_loading_complete(10)
                    self._switch_to_target_item_frame()
                    self.finish_tailing_work(last_action_flag, self.test_vm_name, 'On')
                break
            else:
                self._check_button_exists(find_power_on_time, 'Power On')

        return request_res

    def reboot_vm(self, action, last_action_flag):
        request_res = True

        for find_reboot_time in range(0, 60):
            if self.operatevmpage.btn_reboot.exists():
                self.operatevmpage.btn_reboot.click()
                logger.info("Clicked Reboot button.")
                self.operatevmpage.wait_for_loading_complete(2)
                self._click_submit_button()
                self._click_OK_button()
                request_res = self.get_request_result(action, self.test_vm_name)
                if request_res:
                    self.assertTrue(self.navigate_to_items_page(self.current_browser),
                                    msg=self._formatter.format(step='failed to switch to items page'))
                    self.operatevmpage.wait_for_loading_complete(10)
                    self._switch_to_target_item_frame()

                    self.finish_tailing_work(last_action_flag, self.test_vm_name, 'On')
                break
            else:
                self._check_button_exists(find_reboot_time, 'Reboot')

        return request_res

    def _click_submit_button(self):
        self.assertTrue(
            self.operatevmpage.btn_submit.exists(),
            msg=self._formatter.format(step='the submit button does not exist.')
        )
        self.operatevmpage.btn_submit.click()
        logger.info('Clicked Submit button.')
        self.operatevmpage.wait_for_loading_complete(2)

    def _click_OK_button(self):
        self.assertTrue(
            self.operatevmpage.btn_ok.exists(),
            msg=self._formatter.format(step='the OK button does not exist.')
        )
        self.operatevmpage.btn_ok.click()
        logger.info('Clicked OK button.')
        self.operatevmpage.wait_for_loading_complete(2)

    def _click_cancel_button(self):
        self.assertTrue(
            self.operatevmpage.btn_cancel.exists(),
            msg=self._formatter.format(step='the Close button does not exist.')
        )
        self.operatevmpage.btn_cancel.click()
        logger.info('Clicked Close button.')
        self.operatevmpage.wait_for_loading_complete(2)

    def _click_vm_link(self):
        self.assertTrue(
            self.operatevmpage.btn_machine.exists(),
            msg=self._formatter.format(step='the button Machine does not exist.')
        )
        self.operatevmpage.btn_machine.click()
        LoadingWindow().wait_loading(self.current_browser, 30)
        if not self.operatevmpage.lnk_test_vm.exists():
            self.operatevmpage.btn_refresh_item.click()
            self.operatevmpage.wait_for_loading_complete(10)

        self.assertTrue(
            self.operatevmpage.lnk_test_vm.exists(),
            msg=self._formatter.format(
                step='the vm {vm_name} does not exist.').format(vm_name=self.test_vm_name)
        )
        logger.info(msg='Switch to Item details page.')
        self.operatevmpage.lnk_test_vm.click()
        LoadingWindow().wait_loading(self.current_browser, 30)

    def _check_button_exists(self, check_time, button_name):
        self.operatevmpage.wait_for_loading_complete(10)
        if check_time < 59:
            logger.info("Can't find {} button.".format(button_name))
            self.wait_button_loading_complete()
        else:
            self.fail(
                msg=self._formatter.format(step='the {} button does not exist.'.format(button_name))
            )

    def wait_button_loading_complete(self):
        self._click_cancel_button()
        self._switch_to_target_item_frame()
        self._click_vm_link()

    # ensure the page contains the element of PowerOff|PowerOn|Reboot,
    # at the same time, the status of the vm is not TurningOn or TurningOFF
    # showed in the itemdetail page
    def finish_tailing_work(self, last_action_flag, test_vm_name, action):
        time_out = 600
        while time_out > 0:
            self._click_vm_link()
            self.operatevmpage.wait_for_loading_complete(30)
            time_out -= 30
            self._switch_to_target_detail_frame()
            logger.info("Navigate to item Details InnerFrame page to get the vm's status.")

            self.assertTrue(
                self.operatevmpage.lbl_vm_status.exists(),
                msg=self._formatter.format(step='the label Status does not exist.')
            )
            test_vm_status = self.operatevmpage.lbl_vm_status.value
            # after click Power On, Power Off or other operation, there may take a little time to change status to
            # turningoff or turningon and so on, so the save method to check weather opeartion successful is check the
            # status is  last status but not check whether is middle status.
            # if test_vm_status == 'TurningOn' or test_vm_status == 'TurningOff' or test_vm_status == 'Rebooting':
            if test_vm_status not in action:
                logger.info('The current status of the vm {0} is : {1}. Can not take next operation.'
                            .format(test_vm_name, test_vm_status))
                self._switch_to_target_item_frame()
                self._click_cancel_button()
                self._switch_to_target_item_frame()
            else:
                logger.info(
                    'The current status of the vm {0} is : {1}.'.format(test_vm_name, test_vm_status)
                )
                self._switch_to_target_item_frame()
                if last_action_flag:
                    self._click_cancel_button()
                break

    def _init_web_element(self, test_vm_name):
        self.basepage = BasePage()
        self.operatevmpage = OperateVMPage(test_vm_name)

    def get_request_result(self, action_name, vmname):
        navigator = PageNavigator(self)
        item_name = ' '.join([action_name, '-', vmname])
        request_page = RequestsPage()
        request_result = None

        self._click_cancel_button()
        navigator.go_to_requests_page()

        with request_page.frm_requests:
            request_result = request_page.get_request_result(
                item=item_name, fuzzymatch=True, fuzzymatchstringlist=[action_name, vmname])

        logger.info('Start to validate request result.')
        return self._validate_request_result(request_result, action_name, vmname)

    def _validate_request_result(self, request_result, action_name, vm_name):
        self.assertIsNotNone(request_result, msg='Can not get the request result')
        self.assertIsNotNone(request_result.status, msg='Request status can not be captured')
        self.assertIsNotNone(
            request_result.status_details, msg='Request status details can not be captured')
        logger.info(
            "Request status: {0}, \n request status details: {1}".format(
                request_result.status, request_result.status_details))

        if request_result.status != 'Successful':
            self._all_vms_perfect_flag = False
            logger.error("Take the action {0} on the vm {1} failed, for more details: {2}".format(
                str(action_name), str(vm_name), str(request_result.status_details)))
            return False
        else:
            self._all_vms_perfect_flag = True
            logger.info("Take the action {0} on vm {1} successfully, for more details: {2}".format(
                str(action_name), str(vm_name), str(request_result.status_details)))
            return True

    def navigate_to_items_page(self, current_browser):
        _browser = current_browser.instance._browser.current
        _browser.switch_to.frame(None)

        if MainPage().btn_items.exists():
            MainPage().btn_items.click()
            self.operatevmpage.wait_for_loading_complete(3)
            return True
        else:
            return False

    def _switch_to_target_item_frame(self):

        _browser = self.current_browser.instance._browser.current
        _browser.switch_to.default_content()
        target_frame_id = self.basepage.get_accurate_frameid(
            self.current_browser,
            self.operatevmpage.gadget_url_str)

        if target_frame_id:
            _browser.switch_to.frame(target_frame_id)
            logger.info(
                'Switch to frame {}'.format(target_frame_id))
        else:
            self.fail('Looking for target iframe failed.')

    def _switch_to_target_detail_frame(self):

        _browser = self.current_browser.instance._browser.current
        target_frame_id = self.basepage.get_accurate_frameid(
            self.current_browser,
            self.operatevmpage.gadget_url_item_details_str,
            False
        )
        if target_frame_id:
            _browser.switch_to.frame(target_frame_id)
            logger.info(
                'Switch to frame {}'.format(target_frame_id))
        else:
            self.fail('Looking for target iframe failed.')

        iframes = _browser.find_elements_by_tag_name('iframe')
        iframe_id_exist = False
        for iframe in iframes:
            iframe_id = iframe.get_attribute('id')

            if iframe_id == 'innerFrame':
                iframe_id_exist = True
                _browser.switch_to.frame(iframe_id)
                logger.info('Switch to innerFrame.')
                break
        if not iframe_id_exist:
            # used to locate the why looking for innerFrame failed
            self.fail('Looking for innerFrame failed.')

    def runTest(self):
        retry_times = 1
        max_times = OperateVM.MAX_TIMES_TO_CLOSE_RELAUNCH
        while retry_times <= max_times \
                and self.test_operations_on_vm() is False:
            logger.debug('The {} time to close and relaunch browser'.format(retry_times), False)
            from ehc_e2e.auc.executable.clean_up import CleanUp
            CleanUp().test_clean_up()
            close_relaunch_browser_operation()
            self.current_browser = \
                context_util.get_last_baseworkflow_instance().wf_context.shared.current_browser
            retry_times += 1

        self.assertTrue(retry_times <= max_times,
                        self._formatter.format(
                            step='after {} times close and relaunch browser'.format(max_times))
                        )

    def _validate_input_args(self, current_browser=None, is_login=False,
                             vm_name=None, user_action_list=None):
        assert current_browser is not None, \
            self._formatter.format(step='current_browser is None, may be there is no active browser.')
        assert is_login is True, \
            self._formatter.format(step="can't do anything if you didn't login.")
        assert vm_name is not None, \
            self._formatter.format(step='name of VMs to be deployed should not be None.')
        self.user_action_list = []
        if user_action_list is not None:
            for each_action in user_action_list:
                assert each_action in ['Power On', 'Reboot', 'Power Off'], \
                    self._formatter.format(
                        step='user action: "{}" must be Power On|Power Off|Reboot.'.format(each_action)
                    )

            assert user_action_list is not ['Power Off', 'Reboot'], \
                self._formatter.format(
                    step='informal "{}". Can not take action Reboot after Power Off.'.format(
                        user_action_list)
                                       )

            self.user_action_list = user_action_list

        self.current_browser = current_browser
        self.test_vm_name = vm_name

    def _finalize_context(self):
        assert self._all_vms_perfect_flag, \
            "Take basic actions on vm {vm_name} failed.".format(vm_name=self.test_vm_name)
