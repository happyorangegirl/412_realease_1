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
from selenium.webdriver.remote.webelement import WebElement
from robot.api import logger
from uiacore.modeling.webui.controls import (WebTextBox, WebButton,
                                             WebLabel)
from ehc_e2e.auc.uimap.shared.basepage import BasePage


class RunAdminReportPage(BasePage):
    def __init__(self):
        super(RunAdminReportPage, self).__init__()
        self.data_protection_services = WebButton(xpath='//div[text()="Data Protection Services"]')
        self.txt_description = WebTextBox(id='description')
        self.txt_reasons = WebTextBox(id='reasons')
        self.btn_next = WebButton(id='next')
        self.lab_select_backup_level_name = WebLabel(xpath='//div[@title="Backup Service Level:"]')

        self.parent_element = WebLabel(xpath='//div[@class="popupContent"]/div[@class="listBoxEx"]/div/table')
        self.btn_set_backup_service_name = WebButton(xpath='//table[@id="provider-serviceLevelName"]/tbody/tr/td[1]')
        self.btn_select_pdf_page_orientation = WebButton(xpath='//table[@id="provider-pageOrientation"]/tbody/tr/td[1]')

        self.select_one_or_more_reports_to_run = WebLabel(xpath=
                                                          '//div[@id="provider-ReportNames"]/div/table/tbody')
        self.btn_select_a_time_frame = WebButton(xpath='//table[@id="provider-timeWindowName"]/tbody/tr/td[1]')
        self.btn_email_results = WebButton(xpath='//table[@id="provider-EmailResults"]/tbody/tr/td[1]')
        self.txt_email_address = WebTextBox(id='provider-EmailAddress')
        self.btn_submit = WebButton(id='submit')
        self.lab_confirmation_success = WebLabel(xpath='//div[text()="The request has been submitted successfully."]')
        self.btn_ok = WebButton(id='CONFIRMATION_OK_BUTTON')
        self.btn_cancel = WebButton(id='cancel')
        self.btn_save = WebButton(id="save")

    # select listbox according to option index
    def select_listbox(self, parent_element, tag_name):
        element_value_flag = False
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
                    return element_value_flag

                if len(all_tag_elements) > 0:
                    for element in all_tag_elements:
                        if element.location_once_scrolled_into_view:
                            element.click()
                            element_value_flag = True
                        else:
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
            logger.error(msg='Please correct parameters of select_listbox.')

        return element_value_flag
