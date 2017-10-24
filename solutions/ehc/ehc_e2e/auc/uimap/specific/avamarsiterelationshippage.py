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

from uiacore.modeling.webui.controls import (WebTextBox, WebButton,
                                             WebLabel, WebLink)
from ehc_e2e.auc.uimap.shared.basepage import BasePage


class AvamarSiteRelationshipPage(BasePage):
    def __init__(self):
        super(AvamarSiteRelationshipPage, self).__init__()
        # request info tab
        self.lbl_description = WebLabel(
            xpath='//div[@title="Description:" and @class="gwt-HTML"]')
        self.txt_description = WebTextBox(xpath='//*[@id="description"]')
        self.lbl_reasons = WebLabel(
            xpath='//div[@title="Reasons:" and @class="gwt-HTML"]')
        self.txt_reasons = WebTextBox(xpath='//*[@id="reasons"]')
        self.btn_next = WebButton(id='next')
        # select an action tab
        self.lbl_select_action = WebLabel(
            xpath='//div[@title="Action:"]')
        self.lnk_select_action_menu_open = WebLink(
            xpath='//*[@id="provider-selectAction"]/tbody/tr/td[@align="right"]')
        self.lnk_dropdownlist = WebLink(
            xpath='//*[@class="listBoxEx"]/div/table/tbody')
        # Add ASR tab
        self.lbl_select_backup_env_type = WebLabel(
            xpath='//div[@title="Backup Type:"]')
        self.lnk_select_backup_env_type_menu_open = WebLink(
            xpath='//*[@id="provider-ASR_type_sel"]/tbody/tr/td[@align="right"]'
        )

        self.lbl_select_first_asr_site = WebLabel(
            xpath='//div[@title="Site 1:"]'
        )
        self.lnk_select_first_asr_site_menu_open = WebLink(
            xpath='//*[@id="provider-site_1"]/tbody/tr/td[@align="right"]')
        self.lnk_edit_asr_select_first_asr_site_menu_open = WebLink(
            xpath='//*[@id="provider-newSite1"]/tbody/tr/td[@align="right"]'
        )

        self.lbl_select_second_asr_site = WebLabel(
            xpath='//div[@title="Site 2:"]')
        self.lnk_select_second_asr_site_menu_open = WebLink(
            xpath='//*[@id="provider-site_2"]/tbody/tr/td[@align="right"]')
        self.lnk_edit_asr_select_second_asr_site_menu_open = WebLink(
            xpath='//*[@id="provider-newSite2"]/tbody/tr/td[@align="right"]'
        )

        self.lbl_select_third_asr_site = WebLabel(
            xpath='//div[@title="Site 3:"]')
        self.lnk_select_third_asr_site_menu_open = WebLink(
            xpath='//*[@id="provider-site_3"]/tbody/tr/td[@align="right"]')
        self.lnk_edit_asr_select_third_asr_site_menu_open = WebLink(
            xpath='//*[@id="provider-newSite3"]/tbody/tr/td[@align="right"]'
        )

        self.lbl_tab_edit_asr = WebLabel(
            xpath='//*[@id="tab-Edit-ASR"]')
        self.lnk_edit_asr_select_asr_site_menu_open = WebLink(
            xpath='//*[@id="provider-asrNameWithDetails"]/tbody/tr/td[@align="right"]'
        )

        self.btn_confirm_dropdonwlist_open = WebButton(
            xpath='//*[@id="provider-confirmDeleteASR"]/tbody/tr/td[2]'
        )

        self.lbl_confirmation_success = WebLabel(
            xpath='//div[text()="The request has been submitted successfully."]')
        self.btn_ok = WebButton(id="CONFIRMATION_OK_BUTTON")

        # Delete an ASR tab
        self.lbl_tab_delete_asr = WebLink(
            xpath='//*[@id="tab-Delete-ASR"]'
        )
        self.lbl_asr_name = WebLabel(
            xpath='//div[@class="gwt-HTML" and @title="ASR:"]'
        )
        self.lnk_select_asr_name_menu_open = WebLink(
            xpath='//*[@id="provider-asrNameWithDetails2"]/tbody/tr/td[2]/img'
        )

        self.btn_next = WebButton(xpath='//*[@id="next"]')
        self.btn_save = WebButton(xpath='//*[@id="save"]')
        self.btn_submit = WebButton(xpath='//*[@id="submit"]')
