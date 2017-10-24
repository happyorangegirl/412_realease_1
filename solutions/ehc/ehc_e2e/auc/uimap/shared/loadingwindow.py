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
import time

from robot.api import logger
from selenium.webdriver.remote.webdriver import WebDriver


class LoadingWindow(object):
    def _wait_loading_element_by_class_or_id(self, current_browser, attribute_name='class',
                                             attribute_value='', timeout=30):
        '''
        We only support find by class and find by id
        :param current_browser:
        :param attribute_name: only support 'class' or 'id'
        :param attribute_value: the value for class/ id.
        :param timeout: the timeout for the wait loading
        :return:
        '''
        _loading_window = []
        timeout = 240
        logger.debug('The maximum timeout for LoadingWindow is: {}'.format(timeout))
        _browser = current_browser if isinstance(current_browser,
                                                 WebDriver) else current_browser.instance._browser.current

        # by default, we use find_by_class_name to find element.
        webdriver_find_func = _browser.find_elements_by_id \
            if attribute_name.lower() == 'id' else _browser.find_elements_by_class_name

        try:
            _browser.implicitly_wait(1)
            logger.debug('Start to wait for loading element with {}:{}'.format(attribute_name,
                                                                               attribute_value))
            _loading_window = webdriver_find_func(attribute_value)
            while len(_loading_window) > 0 and timeout > 0:
                logger.debug('Waiting for loading completion...timeout: {}'.format(timeout))
                time.sleep(1)
                timeout -= 1
                _loading_window = webdriver_find_func(attribute_value)
            if len(_loading_window) == 0:
                logger.debug('Loading already done.', False)
            else:
                raise RuntimeError('Wait loading window exceeded timeout')
        except:
            logger.error(
                'Encountered exception when waiting for loading window. Error details: {}'.format(
                    sys.exc_info()))
            from ehc_e2e.utils.snapshot import SnapShot
            SnapShot.takes_screen_shot(file_name='Wait_for_loading_window')
            raise
        finally:
            _browser.implicitly_wait(30)

    def wait_loading(self, current_browser, timeout=30):
        self._wait_loading_element_by_class_or_id(current_browser, attribute_name='class',
                                                  attribute_value='gwt-PopupPanelGlass', timeout=timeout)

    def wait_loading_class_gwt_dialog_box(self, current_browser, timeout=30):
        self._wait_loading_element_by_class_or_id(current_browser, attribute_name='class',
                                                  attribute_value='gwt-DialogBox', timeout=timeout)

    def wait_loading_deploy_vm_page(self, current_browser, timeout=30):
        self._wait_loading_element_by_class_or_id(current_browser, 'class', 'x-mask-msg-text',
                                                  timeout)

    def wait_loading_add_fg_page(self, current_browser, timeout=30):
        self._wait_loading_element_by_class_or_id(
            current_browser, 'id', 'ctl00_ctl00_MasterContent_MainContentPlaceHolder_txtMembers_UserPicker_LPV',
            timeout)

    def wait_loading2(self, current_browser, timeout=30):
        """
        When create new request opened, there is a loading spinner image before the
        request.description/reason appear
        """
        _loading_window = []
        _browser = current_browser if isinstance(current_browser, WebDriver) \
            else current_browser.instance._browser.current
        _img_xpath = '//div[@class="dialogContentInner"]/div/img[@class="gwt-Image"]'

        try:
            _browser.implicitly_wait(1)
            _loading_window = _browser.find_elements_by_xpath(
                _img_xpath)
            while len(_loading_window) > 0 and timeout > 0:
                time.sleep(1)
                timeout -= 1
                logger.debug('Waiting for loading completion...timeout: {}'.format(timeout), False)
                _loading_window = _browser.find_elements_by_xpath(
                    _img_xpath)
            if len(_loading_window) == 0:
                logger.debug('Loading already done.', False)
            else:
                raise RuntimeError('Wait loading window exceeded timeout')
        except:
            logger.error(
                'Encountered exception when waiting for loading window. Error details: {}'.format(
                    sys.exc_info()))
            from ehc_e2e.utils.snapshot import SnapShot
            SnapShot.takes_screen_shot(file_name='Wait_for_loading_window')
            raise
        finally:
            _browser.implicitly_wait(30)

    def wait_loading_infra_page(self, current_browser,
                                timeout=30,
                                element_xpath=
                                '//div[not(contains(@style,"display: none"))]/div/div/*[text()="Loading..."]'):
        _browser = current_browser.instance._browser.current
        try:
            _browser.implicitly_wait(1)
            _loading_table_list = _browser.find_elements_by_xpath(
                element_xpath)
            while len(_loading_table_list) > 0 and timeout >= 0:
                time.sleep(2)
                timeout -= 2
                _loading_table_list = _browser.find_elements_by_xpath(
                    element_xpath)
            if len(_loading_table_list) == 0:
                logger.info('Loading already done.')
            if timeout < 0:
                raise RuntimeError('Wait loading window exceeded timeout')

            # Comments the below method, because only need to check whether exists loading element which display.
            # for _loading_table in _loading_table_list:
            #     # Only check the loading table that is showing in the page
            #     if 'display: none' not in _loading_table.get_attribute('style'):
            #         while timeout > 0 and 'display: none' not in _loading_table.get_attribute(
            #                 'style'):
            #             logger.info('Waiting for loading table completion...', False, True)
            #             time.sleep(1)
            #             timeout -= 1
            #         if 'display: none' not in _loading_table.get_attribute('style'):
            #             logger.error('Wait loading table failed, exceeded timeout!')
            #         else:
            #             logger.debug('Loading already done.', False)
        except:
            logger.error(
                'Encountered exception when waiting for loading window. Error details: {}'.format(
                    sys.exc_info()))
            raise
        finally:
            _browser.implicitly_wait(30)

    def wait_loading_catalog_request_enter(self, current_browser, timeout=240):
        '''
        We have two phases after clicking request button for a catalog item. this function is used
        for processing the two phases of loading window.
        :param current_browser:
        :param timeout:
        :return:
        '''
        self._wait_loading_element_by_class_or_id(current_browser, attribute_name='class',
                                                  attribute_value='gwt-PopupPanelGlass', timeout=timeout)

        # need to figure out a neat way for dealing with the second loading image.
        # self._wait_loading_element_by_class_or_id(current_browser, attribute_name='class',
        #     attribute_value='gwt-Image', timeout=timeout)
