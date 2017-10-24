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

import time
from robot.api import logger
from uiacore.modeling.webui.controls import WebTextBox, WebButton, WebLabel, WebLink
from ehc_e2e.auc.uimap.shared.basepage import BasePage


class SiteMaintenancePage(BasePage):
    def __init__(self):
        super(SiteMaintenancePage, self).__init__()
        # request informations items
        self.lbl_new_request = WebLabel(xpath='//div[text()="New Request"]')
        self.txt_describe = WebTextBox(id='description')

        # action choice items
        self.lnk_action_to_be_performed_menu = WebLink(
            xpath='//*[@id="provider-currentAction"]/tbody/tr/td[@align="right"]')
        self.lnk_action_to_be_performed_dropdownlist = WebLink(
            xpath='//*[@class="listBoxEx"]/div/table/tbody')

        # adds site items
        self.txt_site_name = WebTextBox(
            xpath='//input[@id="provider-entityName" and @class="gwt-TextBox" and @style="width: 182px;"]')

        # edit site items
        self.lnk_edit_site_menu = WebLink(
            xpath='//*[@id="provider-entityToUpdate"]/tbody/tr/td[@align="right"]')
        self.lnk_edit_site_dropdownlist = WebLink(
            xpath='//*[@class="listBoxEx"]/div/table/tbody')
        self.txt_new_site_name = WebTextBox(xpath='//*[@id="provider-entityUpdated"]')

        # deletes site items
        self.lnk_delete_site_menu = WebLink(
            xpath='//*[@id="provider-entityToDelete"]/tbody/tr/td[@align="right"]')
        self.lnk_delete_site_dropdownlist = WebLink(
            xpath='//*[@class="listBoxEx"]/div/table/tbody')
        self.lnk_confirm_delete_site_menu = WebLink(
            xpath='//*[@id="provider-confirmation"]/tbody/tr/td[@align="right"]')
        self.lnk_confirm_delete_site_dropdownlist = WebLink(
            xpath='//*[@class="listBoxEx"]/div/table/tbody')

        # review and submit items
        self.lbl_review_action = WebLabel(id="provider-reviewAction")
        self.lbl_review_site = WebLabel(id="provider-reviewSite")
        self.lbl_review_new_site = WebLabel(id="provider-reviewSiteNew")
        self.str_default_site = '[ sitename ]'
        self.lbl_confirmation_success = WebLabel(xpath='//div[text()="The request has been submitted successfully."]')

        # buttons
        self.btn_next = WebButton(id='next')
        self.btn_submit = WebButton(id='submit')
        self.btn_ok = WebButton(id="CONFIRMATION_OK_BUTTON")
        self.btn_save = WebButton(id="save")
        self.btn_cancel = WebButton(id="cancel")
        self.txt_exist_site_error = 'Cannot add Site because it already exists'

    def wait_to_replace_default_site_in_review_action(self, expect_value, timeout=30):
        txt_review_site = self.lbl_review_site.value
        while txt_review_site == self.str_default_site and timeout > 0:
            time.sleep(3)
            timeout -= 3
            txt_review_site = self.lbl_review_site.value
        if txt_review_site != self.str_default_site:
            if txt_review_site == expect_value:
                return True
            else:
                logger.error('Site do not match with the site user added, user added: {0}, Site: {1}'.format(
                    expect_value, txt_review_site))
        else:
            logger.error('Wait replace defalut site failed, exceeded timeout!')

        return False
