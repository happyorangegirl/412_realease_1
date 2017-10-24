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
import re
from robot.api import logger

from ehc_e2e.auc.executable.baseusecase import BaseUseCase
from ehc_e2e.auc.uimap.shared import MainPage
from ehc_e2e.auc.uimap.shared import RequestsPage
from ehc_e2e.auc.uimap.shared.basepage import BasePage
from ehc_e2e.auc.uimap.shared.loadingwindow import LoadingWindow
from ehc_e2e.auc.uimap.specific import SetBackupServiceLevelPage


class SetBackupServiceLevel(BaseUseCase):
    _properties_check_res = ''
    _request_result_status = ''
    _epc_backup_servicelevels_prop_name = 'epc.backup.servicelevels'
    _formatter = 'Running on step: "Set Backup Service Level" - FAILED, {step}'
    SET_BACKUP_SVC_LEVEL_NAME_PATTERN = '^set-.*?-\d{6}'

    def test_set_backup_service_level(self):

        self.set_backup_service_level_page = SetBackupServiceLevelPage(self.vm_name)
        self._basepage = BasePage()
        self._loadingwindow = LoadingWindow()

        self._click_test_vm_link()
        try:
            self.assertTrue(
                self.set_backup_service_level_page.btn_set_backup_service_level.exists(),
                msg=self._formatter.format(step='can not find Set Backup Service Level button.'))
            self.set_backup_service_level_page.btn_set_backup_service_level.click()
            self._loadingwindow.wait_loading(self.current_browser, 30)
        except AssertionError:
            self.set_backup_service_level_page.cancel_or_close_request()
            logger.error('Set backup service level on vm {0} error'
                         ', just close the Items Detail page.'.format(self.vm_name))
            raise

        try:
            self.assertTrue(
                self.set_backup_service_level_page.txt_desc.exists(),
                msg=self._formatter.format(step='can not find description textbox.'))
            self.set_backup_service_level_page.txt_desc.set(self.description)
            logger.info(
                msg='Input {} in description textbox.'.format(self.description))

            self.assertTrue(
                self.set_backup_service_level_page.btn_next.exists(),
                msg=self._formatter.format(step='can not find next button.'))
            self.set_backup_service_level_page.btn_next.click()
            logger.info('Click Next button.')
            self._loadingwindow.wait_loading(self.current_browser, 30)

            self.assertTrue(
                self.set_backup_service_level_page.lnk_set_backup_service_level_menu.exists(),
                msg=self._formatter.format(step='go to select backup service level.'))

            self.set_backup_service_level_page.lnk_set_backup_service_level_menu.click()
            self.set_backup_service_level_page.wait_for_loading_complete(2)
            self.assertTrue(self.set_backup_service_level_page
                            .click_drop_down_list(self.set_backup_service_level_page
                                                  .lnk_set_backup_service_level_dropdownlist,
                                                  'div',
                                                  self.backup_service_level_name),
                            msg=self._formatter.format(step='target backup service level {name} does not exist.')
                            .format(name=self.backup_service_level_name))
            self.set_backup_service_level_page.wait_for_loading_complete(2)
            logger.info(msg='Select target backup service level {level_name}.'
                        .format(level_name=self.backup_service_level_name))
        except AssertionError:
            self.set_backup_service_level_page.save_request()
            raise
        except:
            ex = sys.exc_info()
            self.set_backup_service_level_page.save_request()
            logger.error('Set backup service level {0} on vm {1} encounters error : {2}'
                         ', just save request.'.format(self.backup_service_level_name, self.vm_name, ex))
            raise

        self._submit_request()
        self._check_request_result()

    def _click_test_vm_link(self):
        try:
            self.assertTrue(self.navigate_to_items_page(self.current_browser),
                            msg=self._formatter.format(step='switch to items page.'))
            logger.info(msg='Switch to Items page.')
            self.set_backup_service_level_page.wait_for_loading_complete(10)
            self.switch_to_target_frame(go_inner_frame=False)

            self.assertTrue(
                self.set_backup_service_level_page.btn_machine.exists(),
                msg=self._formatter.format(step='the button Machine does not exist.')
            )
            self.set_backup_service_level_page.btn_machine.click()
            logger.info('Click Machine button.')
            self.set_backup_service_level_page.wait_for_loading_complete(5)

            if not self.set_backup_service_level_page.test_vm_item.exists():
                self.set_backup_service_level_page.btn_refresh_item.click()
                self.set_backup_service_level_page.wait_for_loading_complete(10)
            self.assertTrue(
                self.set_backup_service_level_page.test_vm_item.exists(),
                msg=self._formatter.format(step='the vm {} does not exist.').format(self.vm_name)
            )
            self.set_backup_service_level_page.test_vm_item.click()
            logger.info('Click {}'.format(self.vm_name))
            self._loadingwindow.wait_loading(self.current_browser, 30)

        except AssertionError:
            logger.error('Set backup service level {0} on vm {1} error.'
                         .format(self.backup_service_level_name, self.vm_name))
            raise
        except:
            ex = sys.exc_info()[:2]
            logger.error('Set backup service level {0} on vm {1} encounters error : {2}.'
                         .format(self.backup_service_level_name, self.vm_name, ex))
            raise

    def _submit_request(self):
        try:
            self.assertTrue(
                self.set_backup_service_level_page.btn_submit.exists(),
                msg=self._formatter.format(step='can not find submit button.'))
            self.set_backup_service_level_page.btn_submit.click()
            logger.info('Click Submit button.')
            self.set_backup_service_level_page.wait_for_loading_complete(2)

            self.assertTrue(
                self.set_backup_service_level_page.lbl_confirmation_success.exists(),
                msg=self._formatter.format(step='label "The request has been submitted successfully" does not exist.'))

            self.assertTrue(
                self.set_backup_service_level_page.btn_ok.exists(),
                msg=self._formatter.format(step='can not find OK button.'))
            self.set_backup_service_level_page.btn_ok.click()
            logger.info('Click OK button.')
        except AssertionError:
            logger.error('Set backup service level {0} on vm {1} error.'
                         .format(self.backup_service_level_name, self.vm_name))
            raise
        except:
            ex = sys.exc_info()[:2]
            logger.error('Set backup service level {0} on vm {1} encounters error : {2}.'
                         .format(self.backup_service_level_name, self.vm_name, ex))
            raise

    def _check_request_result(self):
        # switch to request
        _request_page = RequestsPage()
        self.assertTrue(
            _request_page.navigate_to_request(self.current_browser),
            msg=self._formatter.format(step='switch to request page.'))

        # check the request
        logger.info(msg='Go to check request result.')
        request_result = _request_page.get_request_result(self.description)
        self.assertIsNotNone(
            request_result, self._formatter.format(step='failed to get the request result.')
        )

        self._request_result_status = request_result.status

        if self._request_result_status != 'Successful':
            assert False, 'Set backup service level {level_name} on vm {vm_name} failed, ' \
                          'the status detail is: {status_detail}.' \
                .format(level_name=self.backup_service_level_name,
                        vm_name=self.vm_name,
                        status_detail=request_result.status_details)

        else:
            logger.info('Set backup service level {0} on vm {1} successfully.'
                        .format(self.backup_service_level_name, self.vm_name))

            self._click_test_vm_link()
            try:
                self.switch_to_target_frame(go_inner_frame=True)
                logger.info("Navigate to Item Details innerFrame page.")

                self.assertTrue(self.set_backup_service_level_page.lnk_properties.exists(),
                                msg=self._formatter.format(step='navigate to properties page.'))
                self.set_backup_service_level_page.lnk_properties.click()
                logger.info("Navigate to Item Details Properties page.")
                self._properties_check_res = self.get_properties_check_res()
                if self._properties_check_res != '':
                    if self._properties_check_res == self.backup_service_level_name:
                        logger.info('{prop_name} on vm {vm_name} is {backup_service_level}.'
                                    .format(prop_name=self._epc_backup_servicelevels_prop_name, vm_name=self.vm_name,
                                            backup_service_level=self.backup_service_level_name))
                    else:
                        logger.error('{prop_name} on vm {vm_name} is not {backup_service_level}.'
                                     .format(prop_name=self._epc_backup_servicelevels_prop_name, vm_name=self.vm_name,
                                             backup_service_level=self.backup_service_level_name))
                else:
                    logger.error('{prop_name} is not listed in properties.'.format(
                        prop_name=self._epc_backup_servicelevels_prop_name))
                self.set_backup_service_level_page.wait_for_loading_complete(2)
                self.switch_to_target_frame(go_inner_frame=False)
                self.assertTrue(self.set_backup_service_level_page.btn_close.exists(),
                                msg=self._formatter.format(step='can not find cancel button.'))
                self.set_backup_service_level_page.btn_close.click()

            except:
                ex = sys.exc_info()
                self.set_backup_service_level_page.cancel_or_close_request()
                logger.error('Set backup service level {0} on vm {1} encounters error : {2}'
                             ', just close the Items Detail page.'
                             .format(self.backup_service_level_name, self.vm_name, ex))
                raise

    def get_properties_check_res(self):
        assert self.set_backup_service_level_page.lbl_properties_data.current is not None, \
            'There is no frame of properties_data.'
        container = self.set_backup_service_level_page.lbl_properties_data.current
        properties_list = container.find_elements_by_tag_name('tr')
        properties_check_res = ''
        list_length = len(properties_list)
        if list_length >= 6:
            for properties_row_index in range(5, list_length):
                properties_row = properties_list[properties_row_index]
                properties_row_selector_index = properties_row_index - 5
                selector_name_xpath = self.set_backup_service_level_page\
                                          .properties_row_xpath_str + str(properties_row_selector_index) + '"]/td[1]'
                selector_value_xpath = self.set_backup_service_level_page\
                                           .properties_row_xpath_str + str(properties_row_selector_index) + '"]/td[2]'
                if properties_row.find_element_by_xpath(selector_name_xpath).text == \
                        self._epc_backup_servicelevels_prop_name:
                    properties_check_res = properties_row.find_element_by_xpath(selector_value_xpath).text

        return properties_check_res

    def navigate_to_items_page(self, current_browser):
        _browser = current_browser.instance._browser.current
        _browser.switch_to.frame(None)

        if MainPage().btn_items.exists():
            MainPage().btn_items.click()
            self.set_backup_service_level_page.wait_for_loading_complete(3)
            return True
        else:
            return False

    def switch_to_target_frame(self, go_inner_frame=False):

        _browser = self.current_browser.instance._browser.current
        if go_inner_frame:
            target_frame_id = self._basepage.get_accurate_frameid(
                self.current_browser,
                self.set_backup_service_level_page.gadget_url_item_details_str,
                False
            )
        else:
            _browser.switch_to.default_content()
            target_frame_id = self._basepage.get_accurate_frameid(
                self.current_browser,
                self.set_backup_service_level_page.gadget_url_str)

        if target_frame_id:
            _browser.switch_to.frame(target_frame_id)
            logger.info(
                'Switch to frame {}'.format(target_frame_id))
        else:
            logger.error('Looking for target iframe failed.')

        if go_inner_frame:
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
                logger.error('Looking for innerFrame failed.')

    def runTest(self):
        self.test_set_backup_service_level()

    def _validate_input_args(self, current_browser=None, is_login=False,
                             description=None, vm_name=None, backup_service_level_name=None):
        assert current_browser is not None, 'current_browser is None, may be there is no active browser.'
        assert is_login is True, "Can't do anything if you didn't login to vRA."
        assert vm_name is not None, 'Name of VMs to set back up service level should not be None.'
        self.current_browser = current_browser
        self.vm_name = vm_name
        self.description = description
        self.backup_service_level_name = backup_service_level_name
        assert self.backup_service_level_name is not None, 'backup service level should not be none.'
        if not re.search(
                SetBackupServiceLevel.SET_BACKUP_SVC_LEVEL_NAME_PATTERN,
                self.backup_service_level_name):
            logger.warn(
                'The backup service level for setting VM from context is:{}, The workflow added '
                'bksl name should have timestamp appended.\n It is likely you are resuming workflow'
                ' but not using dump file.'.format(self.backup_service_level_name)
            )

    def _finalize_context(self):
        pass
