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

from uiacore.modeling.webui.controls import WebButton, WebLabel, WebLink


class RequestDetailsPage(object):
    def __init__(self):
        self.lbl_status = WebLabel(xpath='//div[@title="Status"]')
        self.lbl_status_content = WebLabel(id="state")
        self.lnk_status_result_xpath = '//a[@title="View Details"]'
        self.lnk_status_result = WebLink(xpath='//a[@title="View Details"]')
        self.lbl_status_result = WebLink(id="state")
        self.lbl_status_result_xpath = '//*[@id="state"]'
        self.lbl_status_details_context = WebLabel(xpath='//*[@class="gwt-DialogBox"]//*[@class="dialogContent"]')
        self.btn_ok_status_details_dialog = WebButton(xpath="//div[@class='gwt-DialogBox']//*[@id='submit']")
        self.lbl_business_group_context = WebLabel(id="subtenant")
        self.btn_ok = WebButton(xpath='//button[@id="cancel"]')
        self.xpath_btn_ok = '//button[@id="cancel"]'
