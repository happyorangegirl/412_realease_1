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
from selenium.webdriver.common.keys import Keys
import time
from robot.api import logger
import datetime
from selenium.webdriver.remote.webelement import WebElement
from uiacore.modeling.webui.controls import WebButton
import sys
import operator
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


class BasePage(object):
    def __init__(self):
        self.btn_save = WebButton(id="save")
        self.btn_cancel = WebButton(id="cancel")
        self.url_forms_gadget = 'https://com.vmware.csp.iaas.ui.vproxy//forms-gadget.xml'
        self.url_self_service_gadget = 'https://com.vmware.csp.core.cafe.catalog.' \
                                  'plugin.vproxy//selfservice/SelfServiceGadget.gadget.xml'

    @staticmethod
    def send_tab_key(tab_element):
        if tab_element:
            try:
                if isinstance(tab_element, WebElement):
                    _tag_elements = tab_element
                elif isinstance(tab_element.current, WebElement):
                    _tag_elements = tab_element.current
                else:
                    logger.error(msg='The tab_element provided is not an instance of WebElement.')
                    return

                _tag_elements.send_keys(Keys.TAB)
                logger.info(msg='Send tab key successful.', html=True, also_console=False)
            except:
                ex = sys.exc_info()[:2]
                logger.error(
                    'Error occurs when try to do tab operate, '
                    'Error: {}'.format(ex))

        else:
            logger.error(msg='Please correct parameters of send_tab_key.')

    def click_drop_down_list(self, parent_element=None, tag_name=None,
                             item_to_select=None, strip_text=False,
                             compare_contains=False, case_insensitive=True):
        element_value_flag = False
        if parent_element is not None and tag_name is not None \
                and item_to_select is not None:
            try:
                if isinstance(parent_element, WebElement):
                    all_tag_elements = parent_element.find_elements_by_tag_name(
                        tag_name)
                elif isinstance(parent_element.current, WebElement):
                    all_tag_elements = parent_element.current. \
                        find_elements_by_tag_name(tag_name)
                else:
                    return element_value_flag

                select_value = None
                op = operator.contains if compare_contains else operator.eq
                if len(all_tag_elements) > 0:
                    for element in all_tag_elements:
                        if case_insensitive:
                            if (op(element.text.strip().lower(), item_to_select.strip().lower())
                                    if strip_text else op(element.text.lower(), item_to_select.lower())):
                                select_value = element.text
                                logger.debug('Found item: {} to be selected'.format(select_value), True)
                        else:
                            if (op(element.text.strip(), item_to_select.strip())
                                    if strip_text else op(element.text, item_to_select)):
                                select_value = element.text
                                logger.debug('Found item: {} to be selected'.format(select_value), True)


                            # calling location_once_scrolled_into_view in deploy_vm
                            # "Select Backup Service Level" is throwing WebDriverException
                            # without detailed info. but the scroll is actully done,
                            # we catch exception intentionally here and continue
                            # click the element.
                        if select_value is not None:
                            scroll_result = None
                            try:
                                self.wait_for_loading_complete(1)
                                scroll_result = element.location_once_scrolled_into_view
                            except:
                                logger.warn(
                                    'Scroll item: {} into view encounters '
                                    'exception!'.format(select_value))

                            self.wait_for_loading_complete(1)
                            element.click()
                            logger.info(
                                'Selected item: {}.'.format(
                                    select_value), False, True)
                            element_value_flag = True

                            return element_value_flag

                    logger.warn('No element with name:{name} found! Items are: {items}'
                                .format(name=item_to_select,
                                        items=[el.text.strip() for el in all_tag_elements]))
                else:
                    logger.warn('No element with tag name:{name} found! Items are: {items}'
                                .format(name=tag_name,
                                        items=[el.text for el in all_tag_elements]))
                    return element_value_flag
            except:
                ex = sys.exc_info()[:2]
                logger.error(
                    'Error occurs when trying to click drop down list, '
                    'Error: {}!'.format(ex))
                raise

        return element_value_flag

    def select_drop_down_list_by_index(self, parent_element=None, tag_name=None, index_to_select=0):
        """According to option index to select drop down list,
        if you want to select the first option , set index_to_select=0"""
        element_value = None
        if parent_element is not None and tag_name is not None and index_to_select >= 0:
            try:
                if isinstance(parent_element, WebElement):
                    all_tag_elements = parent_element.find_elements_by_tag_name(
                        tag_name)
                elif isinstance(parent_element.current, WebElement):
                    all_tag_elements = parent_element.current. \
                        find_elements_by_tag_name(tag_name)
                else:
                    logger.error(msg='The parent_element provided is not an instance of WebElement.')
                    return element_value

                if len(all_tag_elements) > 0:
                    element_selected = all_tag_elements[index_to_select]
                    if element_selected.location_once_scrolled_into_view:
                        element_value = element_selected.text
                        element_selected.click()
                        logger.info('Found item: {} to be selected!'.format(element_value))
                    else:
                        logger.error('Item: {} is not visible to select!'.format(element_value))
                else:
                    logger.error("The drop down list is empty.")
                    return element_value
            except:
                ex = sys.exc_info()[:2]
                logger.error(
                    'Error occurs when trying to click drop down list, '
                    'Error: {}'.format(ex))
                raise
        else:
            logger.error(msg='Please correct parameters of select_drop_down_list_by_index.')

        return element_value

    # according to option index to select listbox,
    # if you want to select the first option , set index=0
    def select_listbox_by_index(self, parent_element, tag_name, index):
        element_value = None
        if parent_element is not None and tag_name is not None and index >= 0:
            try:
                if isinstance(parent_element, WebElement):
                    all_tag_elements = parent_element.find_elements_by_tag_name(
                        tag_name)
                elif isinstance(parent_element.current, WebElement):
                    all_tag_elements = parent_element.current. \
                        find_elements_by_tag_name(tag_name)
                else:
                    logger.error(msg='The parent_element provided is not an instance of WebElement.')
                    return element_value

                if len(all_tag_elements) > 0:
                    input_element = all_tag_elements[index].find_element_by_tag_name('input')
                    label_element = all_tag_elements[index].find_element_by_tag_name('label')
                    if input_element.location_once_scrolled_into_view:
                        element_value = label_element.text
                        input_element.click()
                        logger.info('Found item: {} to be selected!'.format(element_value), False, True)
                    else:
                        logger.error('Item: {} is not visible to select!'.format(element_value))
                        return element_value
                else:
                    logger.error("The listbox is empty.")
                    return element_value
            except:
                ex = sys.exc_info()[:2]
                logger.error(
                    'Error occurs when trying to check listbox, '
                    'Error: {}'.format(ex))
                raise
        else:
            logger.error(msg='Please correct parameters of select_listbox_by_index.')

        return element_value

    # select listbox according to option index
    def select_listbox_by_value(self, parent_element, tag_name, value):
        element_value_flag = False
        if parent_element is not None and tag_name is not None and value is not None:
            try:
                if isinstance(parent_element, WebElement):
                    all_tag_elements = parent_element.find_elements_by_tag_name(
                        tag_name)
                elif isinstance(parent_element.current, WebElement):
                    all_tag_elements = parent_element.current. \
                        find_elements_by_tag_name(tag_name)
                else:
                    logger.error(msg='The parent_element provided is not an instance of WebElement.')
                    return element_value_flag

                if len(all_tag_elements) > 0:
                    for element in all_tag_elements:
                        input_element = element.find_element_by_tag_name('input')
                        label_element = element.find_element_by_tag_name('label')
                        if label_element.text == value:
                            if input_element.location_once_scrolled_into_view:
                                input_element.click()
                                element_value_flag = True
                                logger.info('Found item: {} to be selected!'.format(value))
                            else:
                                logger.error('Item: {} is not visible to select!'.format(value))
                                return element_value_flag
                else:
                    logger.error("The listbox is empty.")
                    return element_value_flag
            except:
                ex = sys.exc_info()[:2]
                logger.error(
                    'Error occurs when trying to check listbox, '
                    'Error: {}'.format(ex))
                raise
        else:
            logger.error(msg='Please correct parameters of select_listbox_by_value.')

        return element_value_flag

    def wait_for_loading_complete(self, wait_time=10):
        time.sleep(wait_time)

    def make_timestamp(self, formatter='%y%m%d%I%M%p'):
        # make a timestamp , default formatter is '%y%m%d%I%M%p'
        # formatter like: '%m/%d/%y %I:%M %p' or '%y%m%d%I%M%p'
        now_time = time.strftime(formatter, time.localtime())
        return now_time

    def format_date(self, date, formatter='%m/%d/%y %I:%M %p'):
        # format the date, default formatter is '%m/%d/%y %I:%M %p'
        return datetime.datetime.strptime(date, formatter).date()

    def get_accurate_frameid(self, current_browser, gadget_url, from_top_document=True, attribute_name='onload'):
        """
         Find the iframe tag, whose onload attribute contains given gadget_url,
          within the page. Return the id of the iframe once found,
          None if not found.
        Args:
            current_browser: the current_browser object
            gadget_url: the url within iframe given attribute, to identify
                        which iframe the web elements you want to operate
                        reside in.
            from_top_document: indicate if this method will search iframe elemements
                                from the top of the page.
            attribute_name: specify name of the attribute this method will search for.

        Returns: the id of the iframe once found, None otherwise.

        """
        _browser = None
        try:
            _browser = current_browser if isinstance(current_browser,
                                                     WebDriver) else current_browser.instance._browser.current
            if from_top_document:
                _browser.switch_to.default_content()
            iframes = _browser.find_elements_by_tag_name('iframe')
            self.wait_for_loading_complete(5)
            for iframe in iframes:
                iframe_id = iframe.get_attribute('id')
                iframe_attribute_value = iframe.get_attribute(attribute_name)
                logger.debug('Checking iframe whose id is {0}, gadget_url is {1}, iframe_attribute_value is {2}.'.
                             format(iframe_id, gadget_url, iframe_attribute_value), True)

                if iframe_attribute_value and gadget_url in iframe_attribute_value:
                    logger.debug(
                        'IFrame with url {0} in attribute {1} is found, frameid '
                        'is {2}'.format(gadget_url, attribute_name, iframe_id), False)
                    return iframe_id

            logger.error('In {0} IFrames, IFrame with url {1} in attribute {2} is not found.'.
                         format(len(iframes), gadget_url, attribute_name), False)

        except:
            logger.error(
                'Encounter exception in get_accurate_frameid, detail info: {}'.format(sys.exc_info()))
        from ehc_e2e.utils.snapshot import SnapShot
        SnapShot.takes_screen_shot(current_driver=_browser)
        return None

    def save_request(self):
        """
            use this method to save the request when error occurs in AUC.
            This makes sure the page returns back to catalog default page,
            following AUCs can proceed afterwards.
        """
        from ehc_e2e.utils.snapshot import SnapShot
        SnapShot.takes_screen_shot()

        if self.btn_save.exists():
            # self.wait_for_loading_complete(10)
            self.btn_save.click()
            self.wait_for_loading_complete(2)
            logger.info("Clicked save button to save the request.")

    def cancel_or_close_request(self):
        """
            use this method to cancel the request or close page when error occurs in AUC.
            The locater of cancel button and close button:

                WebButton(id="cancel")
        """
        from ehc_e2e.utils.snapshot import SnapShot
        SnapShot.takes_screen_shot()

        if self.btn_cancel.exists():
            # self.wait_for_loading_complete(10)
            self.btn_cancel.click()
            self.wait_for_loading_complete(2)
            logger.info("Clicked cancel or close button.")

    def check_element_label_appear(self, element, timeout=30):
        """

        Args:
            element: the web element is going to attached to the page document.
            timeout:

        Returns:
             appear_flag: waiting result

        """
        appear_flag = False
        if element is not None and time is not None:
            try:
                if isinstance(element, WebElement):
                    pass
                elif isinstance(element.current, WebElement):
                    element = element.current
                else:
                    return appear_flag
                while timeout > 0 and not element.is_displayed():
                    time.sleep(1)
                    if element.is_displayed:
                        timeout -= 1
                        appear_flag = True
                        break
                else:
                    appear_flag = False
                    return appear_flag
            except:
                ex = sys.exc_info()[:2]
                logger.error(
                    'Error occurs when trying to check if the web element appears, '
                    'Error: {}'.format(ex))
                raise
        return appear_flag

    def check_element_label_disappear(self, element, timeout=30):
        """

        Args:
            element: the web element is going to dis-attached to the page document.
            timeout:

        Returns:
             disappear_flag: waiting result

        """
        disappear_flag = False
        if element is not None and time is not None:
            try:
                if isinstance(element, WebElement):
                    pass
                elif isinstance(element.current, WebElement):
                    element = element.current
                else:
                    return disappear_flag
                while timeout > 0 and element.is_displayed():
                    time.sleep(1)
                    if not element.is_displayed:
                        timeout -= 1
                        disappear_flag = True
                        break
                else:
                    disappear_flag = False
                    return disappear_flag
            except:
                ex = sys.exc_info()[:2]
                logger.error(
                    'Error occurs when trying to check if the web element appears, '
                    'Error: {}'.format(ex))
                raise
        return disappear_flag

    def select_drop_down_list_filter_undefined_by_index(self, parent_element=None, tag_name=None, storage_tier=None):
        element_value = None

        if parent_element is not None and tag_name is not None:
            try:
                if isinstance(parent_element, WebElement):
                    all_tag_elements = parent_element.find_elements_by_tag_name(
                        tag_name)
                elif isinstance(parent_element.current, WebElement):
                    all_tag_elements = parent_element.current. \
                        find_elements_by_tag_name(tag_name)
                else:
                    logger.error(msg='The parent_element provided is not an instance of WebElement.')
                    return element_value

                if len(all_tag_elements) > 0:
                    for i in range(len(all_tag_elements)):
                        if all_tag_elements[i].location_once_scrolled_into_view:
                            if ("DO_NOT_USE" not in all_tag_elements[i].text and 'available' in all_tag_elements[i].text
                                and 'available: 0GB' not in all_tag_elements[i].text) and (not storage_tier
                                     or storage_tier in all_tag_elements[i].text):
                                element_selected = all_tag_elements[i]
                                element_value = element_selected.text
                                element_selected.click()
                                if not storage_tier:
                                    logger.info('Storage tier is not filled,choose the first one available.')
                                logger.info('Found item: {} to be selected!'.format(element_value))
                                return element_value
                            elif "DO_NOT_USE" not in all_tag_elements[i].text and 'available: 0GB' in \
                                    all_tag_elements[i].text and storage_tier in all_tag_elements[i].text:
                                logger.error('Found item: {}, but available storage is 0.'.format(element_value))
                            elif "DO_NOT_USE" not in all_tag_elements[i].text and 'available' not in \
                                    all_tag_elements[i].text and storage_tier in all_tag_elements[i].text:
                                logger.error('Found item: {}, but it has no available info.'.format(element_value))
                        else:
                            logger.error('Item: {} is not visible to select!'.format(element_value))

                    logger.error('Select {} failed.'.format(storage_tier))
                    return element_value
                else:
                    logger.error("The drop down list is empty.")
                    return element_value
            except:
                ex = sys.exc_info()
                logger.error(
                    'Error occurs in select_drop_down_list_filter_undefined_by_index, Error: {}'.format(ex))
                raise
        else:
            logger.error(msg='Please correct parameters of select_drop_down_list_filter_undefined_by_index.')

        return element_value

    # if used element.exists() to check whether element exists, if not exists will wait 30, now write one method to
    # verify whether element exist in the timeout , the element located by xpath.
    @staticmethod
    def element_exists(element_xpath, container, timeout=30):
        driver = None
        try:
            if isinstance(container, WebElement):
                driver = container.parent
            elif isinstance(container, WebDriver):
                driver = container
            else:
                logger.error('the container parameter in method element_exists are not right.')
                return False
            driver.implicitly_wait(1)
            _elements = driver.find_elements_by_xpath(element_xpath)
            while len(_elements) > 0 and timeout > 0:
                time.sleep(1)
                timeout -= 1
                _elements = driver.find_elements_by_xpath(element_xpath)
            if len(_elements) == 0:
                return False
            if timeout <= 0:
                return True
        except:
            logger.error(
                'Encountered exception when check whether element exists. Error details: {}'.format(sys.exc_info()[:2]))
        finally:
            driver.implicitly_wait(30)
        return False

    @staticmethod
    def wait_until(browser,
                   value_of_expected_condition,
                   expected_condition=expected_conditions.frame_to_be_available_and_switch_to_it,
                   timeout=240):
        try:
            drvier_wait = WebDriverWait(browser, timeout)
            drvier_wait.until(expected_condition(value_of_expected_condition))
            return True
        except:
            logger.error('Encountered exception when call wait_until. Error details: {}'.format(sys.exc_info()))
            return False
