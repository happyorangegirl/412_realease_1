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


class selectDefaultPage(object):
    def click_drop_down_list(self, parent_element=None, tag_name=None, item_to_select=None):
        self.element_value_flag = False
        if parent_element is not None and tag_name is not None and item_to_select is not None:
            if parent_element.current:
                try:
                    all_tag_elements = parent_element.current.find_elements_by_tag_name(tag_name)
                    if len(all_tag_elements) > 0:
                        all_tag_elements[1].click()
                        self.element_value_flag = True

                    else:
                        logger.info("the target value is not exists")
                        return self.element_value_flag
                except Exception as e:
                    logger.error(e.message)
                    raise Exception(e.message)
            else:
                return self.element_value_flag

        return self.element_value_flag

    def click_default_list(self, parent_element=None, tag_name=None, item_to_select=None):
        self.element_value_flag = False
        if parent_element is not None and tag_name is not None and item_to_select is not None:
            if parent_element.current:
                try:
                    all_tag_elements = parent_element.current.find_elements_by_tag_name(tag_name)
                    if len(all_tag_elements) > 0:
                        all_tag_elements[0].click()
                        self.element_value_flag = True

                    else:
                        logger.info("the target value is not exists")
                        return self.element_value_flag
                except Exception as e:
                    logger.error(e.message)
                    raise Exception(e.message)
            else:
                return self.element_value_flag

        return self.element_value_flag
