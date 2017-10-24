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
import time
from uiacore.modeling.webui.controls import WebLink
from robot.api import logger


class WebCombo(object):
    def __init__(self, parent=None, container_xpath=None, **criteria):
        self._list = WebLink(parent, **criteria)

        if container_xpath:
            self._xpath_of_items = container_xpath
        else:
            self._xpath_of_items = '//div[@class="popupContent"]/div[@class="listBoxEx"]'

    def activate(self):
        if self._list._parent and self.exists():
            self._list._parent.execute_script(
                'arguments[0].focus();', self.object)

    def exists(self, timeout_in_secs=30):
        return self._list.exists(timeout_in_secs)

    @property
    def object(self):
        """
        Test Object in Memory (Not refreshed)
        :return: WebElement
        """
        return self._list.object

    @property
    def current(self):
        """
        Runtime object on web page within specific browser
        :return: WebElement
        """
        return self._list.current

    def select(self, index=None, by_value='', by_visible_text=''):
        if not self.exists():
            raise RuntimeError('Failed to locate the dropdown list')

        self._list.click()
        try:
            if index is not None:
                logger.info('Begin to select the {0} item'.format(index+1))
                _element = self.object.find_element_by_xpath(
                    '{}//tr[{}]/td/div'.format(
                        self._xpath_of_items, index + 1))
            elif by_value.strip():
                logger.info('Begin to select item: {}'.format(by_value.strip()))
                _element = self.object.find_element_by_xpath(
                    "{}//td/div[text()='{}']".format(
                        self._xpath_of_items, by_value.strip()))
            elif by_visible_text.strip():
                logger.info('Begin to select item: {}'.format(by_visible_text.strip()))
                _element = self.object.find_element_by_xpath(
                    "{}//td/div[text()='{}']".format(
                        self._xpath_of_items, unicode(by_visible_text.strip())))
            else:
                raise ValueError('The identifier is not specified')
        except ValueError as ve:
            raise ve
        except:
            raise RuntimeError(
                'selecting item "{}" failed for exception:{}'.format(by_visible_text, sys.exc_info())
            )
        else:
            _element.click()
            logger.info('Selected item: {}'.format(_element.text), True, False)

    def items(self):
        __selection_items = []
        if self.exists():
            try:
                self._list.click()

                __selection_items = self.object.find_elements_by_xpath(
                    '{}//td/div'.format(self._xpath_of_items))
                __selection_items = [_item.text for _item in __selection_items]

                self._list.click()
            except:
                pass

        return __selection_items

    @property
    def can_select_multiple(self):
        # arbitrarily supposed no support for selecting multiple values
        return False

class WebComboEx(object):

    picker_pattern = "dropdownlist-(\d+)-trigger-picker"
    ul_id_format = "boundlist-{id}-listEl"

    def __init__(self, parent=None, **criteria):
        self._cbo_parent = WebLink(parent, **criteria)


    @property
    def picker(self):
        xpath = './/div[contains(@id, "trigger-picker")]'
        ele = self._cbo_parent.current.find_element_by_xpath(xpath)
        if ele:
            return WebLink(element=ele)
        return None

    @property
    def ul_id(self):
        _pickerid = self.picker.current.get_attribute('id')
        match = re.search(self.picker_pattern, _pickerid)
        if match:
            _id = int(match.group(1))
            _id += 1
            _ul_id = self.ul_id_format.format(id=_id)
            return _ul_id
        return None

    @property
    def ul_data(self):
        return WebLink(id=self.ul_id)

    def exists(self, timeout_in_secs=30):
        return self._cbo_parent.exists(timeout_in_secs)

    @property
    def object(self):
        """
        Test Object in Memory (Not refreshed)
        :return: WebElement
        """
        return self._cbo_parent.object

    @property
    def current(self):
        """
        Runtime object on web page within specific browser
        :return: WebElement
        """
        return self._cbo_parent.current


    def select(self, index=None, by_visible_text=''):

        if not self.exists():
            raise RuntimeError('Failed to locate the dropdown list')

        self.picker.click()
        time.sleep(1)
        elements = self.ul_data.current.find_elements_by_tag_name('li')
        logger.debug('Elements are: {}'.format([ele.text.strip() for ele in elements if ele]))
        try:
            if index is not None:
                _element = self.ul_data.current.find_element_by_xpath(
                    './li[{}]'.format(index+1))

            elif by_visible_text.strip():
                _element = self.ul_data.current.find_element_by_xpath(
                    "./li[text()='{}']".format(unicode(by_visible_text.strip())))
            else:
                raise ValueError('The identifier is not specified')
        except ValueError as ve:
            raise ve
        except:
            raise RuntimeError(
                'selecting item "{}" failed for exception:{}, items are:{}'.format(
                    by_visible_text, sys.exc_info(), [ele.text.strip() for ele in elements if ele]
                )
            )
        else:
            _element.click()
            logger.info('Selected item: {}'.format(_element.text), True, False)

    def items(self):
        __selection_items = []
        if self.exists():

            try:
                self.picker.click()

                __selection_items = self.ul_data.find_elements_by_tag('li')
                __selection_items = [_item.text for _item in __selection_items]

                self.picker.click()
            except:
                pass

        return __selection_items

    @property
    def can_select_multiple(self):
        # arbitrarily supposed no support for selecting multiple values
        return False
