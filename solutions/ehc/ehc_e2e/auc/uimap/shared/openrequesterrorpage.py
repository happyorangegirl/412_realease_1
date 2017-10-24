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

from uiacore.modeling.webui.controls import (WebButton, WebLabel)
from ehc_e2e.auc.uimap.shared.basepage import BasePage
from robot.api import logger

class OpenRequestErrorPage(object):
    def __init__(self):
        self.gadget_2_frame_id = '__gadget_2'
        self.inner_frame_id = 'innerFrame'
        self.lbl_request_error = WebLabel(
            xpath='//*[@id="ctl00_ctl00_MasterContent_BannerPanel"]/div/div[2]'
                  '/ul/li[@class="error"]')
        self.btn_save = WebButton(
            xpath='//*[@id="CATALOG_REQUEST_SUBMISSION_FORM"]/div/div/div[2]/'
                  'div/table/tbody/tr/td/button[@id="save"]')
        self.btn_submit = WebButton(
            xpath='//*[@id="CATALOG_REQUEST_SUBMISSION_FORM"]/div/div/div[2]/'
                  'div/table/tbody/tr/td/button[@id="submit"]')
        self.btn_cancel = WebButton(
            xpath='//*[@id="CATALOG_REQUEST_SUBMISSION_FORM"]/div/div/div[2]/'
                  'div/table/tbody/tr/td/button[@id="cancel"]')

    def try_detect_request_error(self, current_browser, request_name=''):
        _browser = current_browser.instance._browser.current
        _error_msg = ''
        #LoadingWindow().wait_loading(current_browser)
        BasePage().wait_for_loading_complete(wait_time=2)
        _browser.switch_to.default_content()

        #NOTE:
        # if its the first time enterring the request error page.
        # the error message's location is:
        # gadget_2_frame->gadget_2_frame->innerFrame
        # if it is not the first time(2, 3...) entering the request error page.
        # the error message's location is :
        # gadget_2_frame->gadget_3_frame->innerframe
        _browser.switch_to.frame(self.gadget_2_frame_id)
        _browser.switch_to.frame(self.gadget_2_frame_id)
        _browser.switch_to.frame(self.inner_frame_id)
        if self.lbl_request_error and self.lbl_request_error.exists():
            _error_msg = self.lbl_request_error.value
            # error label is in innerFrame, buttons are in gadget_2_frame
            _browser.switch_to.default_content()
            _browser.switch_to.frame(self.gadget_2_frame_id)

        if _error_msg is not '':
            logger.error('Detected request error with error message {}'
                         '.'.format(_error_msg))

            return True
        else:
            logger.info('Failed to detect request {} error.'.format(request_name))

            return False
